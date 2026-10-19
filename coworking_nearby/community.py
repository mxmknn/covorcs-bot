"""Durable place suggestions and numeric-ID administration.

User-approved fast implementation; independent release certification is separate.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import html
import json
import math
import os
from pathlib import Path
import sqlite3
import time
import uuid

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .catalog import CatalogError, _record

_FIELDS = (
    ('name', 'Название', False), ('address', 'Адрес', False),
    ('latitude', 'Широта (числом от -90 до 90)', False),
    ('longitude', 'Долгота (числом от -180 до 180)', False),
    ('yandex_maps_url', 'Ссылка на Яндекс Карты (https://yandex.ru/maps/…)', True),
    ('short_review', 'Краткий отзыв (до 200 символов)', True),
    ('description', 'Описание (до 500 символов)', True),
    ('rating_text', 'Рейтинг (до 50 символов)', True),
    ('rating_source', 'Источник рейтинга: catalog или yandex', True),
    ('rating_checked_at', 'Дата проверки рейтинга: ГГГГ-ММ-ДД', True),
)
_LIMITS = {'name': 150, 'address': 250, 'short_review': 200,
           'description': 500, 'rating_text': 50, 'yandex_maps_url': 2048,
           'rating_source': 16, 'rating_checked_at': 10}


class CommunityService:
    def __init__(self, bot, base_snapshot, limit, admin_ids: tuple[int, ...], state_path: Path):
        self.bot, self.base, self.limit = bot, tuple(base_snapshot), limit
        self.admins = frozenset(value for value in admin_ids if type(value) is int)
        self.path = Path(state_path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.path.parent, 0o700)
        self.db = sqlite3.connect(self.path, timeout=0.1)
        os.chmod(self.path, 0o600)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                actor INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT,
                first_seen REAL NOT NULL, last_seen REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS drafts (
                actor INTEGER PRIMARY KEY, step INTEGER NOT NULL, fields TEXT NOT NULL,
                changed REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY, actor INTEGER, payload TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending','approved','rejected')),
                created REAL NOT NULL, decided REAL);
            CREATE TABLE IF NOT EXISTS approved (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, ordinal INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS deliveries (
                id INTEGER PRIMARY KEY, submission TEXT NOT NULL, recipient INTEGER NOT NULL,
                purpose TEXT NOT NULL, status TEXT NOT NULL, source INTEGER,
                UNIQUE(submission,recipient,purpose));
            CREATE TABLE IF NOT EXISTS moderation_messages (
                submission TEXT NOT NULL, recipient INTEGER NOT NULL, source INTEGER NOT NULL,
                PRIMARY KEY(submission,recipient,source));
        ''')
        with self.db:
            self.db.execute("UPDATE deliveries SET status='uncertain' WHERE status='sending'")
            now = time.time()
            self.db.execute('DELETE FROM drafts WHERE changed < ?', (now - 7*86400,))
            self.db.execute('DELETE FROM users WHERE last_seen < ?', (now - 90*86400,))
            self.db.execute("DELETE FROM submissions WHERE status='rejected' AND decided < ?", (now - 30*86400,))
        self._approved()  # Fail closed on corrupt persistent catalogue state.

    def close(self):
        self.db.close()

    def _approved(self):
        seen = {record.id: index for index, record in enumerate(self.base)}
        result = []
        for index, (payload,) in enumerate(self.db.execute('SELECT payload FROM approved ORDER BY ordinal,id'), len(self.base)):
            result.append(_record(json.loads(payload), self.path, index, seen))
        return tuple(result)

    async def _send(self, chat, text, markup=None):
        message = None
        try:
            # Escape after splitting: every HTML expansion remains below Telegram's limit.
            chunks = [text[i:i+700] for i in range(0, len(text), 700)] or [' ']
            for index, chunk in enumerate(chunks):
                async with asyncio.timeout(10):
                    message = await self.bot.send_message(
                        chat_id=chat, text=html.escape(chunk, quote=False), parse_mode='HTML',
                        reply_markup=markup if index == len(chunks)-1 else None,
                        request_timeout=10)
            return message
        except Exception:
            return None

    def _buttons(self, submission):
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='✅ Одобрить', callback_data=f'place:a:{submission}'),
            InlineKeyboardButton(text='❌ Отклонить', callback_data=f'place:r:{submission}')]])

    def _preview(self, values):
        return '\n'.join(f'{i}. {label}: {values.get(field, "—")}'
                         for i, (field, label, _) in enumerate(_FIELDS, 1))

    async def _prompt(self, chat, step, values):
        if step == len(_FIELDS):
            await self._send(chat, 'Проверьте заявку:\n' + self._preview(values) +
                             '\n\nОтправить: /submit\nИзменить последнее поле: /back\nОтменить: /cancel')
        else:
            _, label, optional = _FIELDS[step]
            await self._send(chat, f'{step+1}/10. {label}' +
                             ('\nМожно пропустить: /skip или -' if optional else '') +
                             '\nНазад: /back · Отмена: /cancel')

    def _validate(self, values, record_id=None):
        entry = dict(values, id=record_id or 'community-' + uuid.uuid4().hex, active=False)
        return _record(entry, self.path, 0, {record.id: i for i, record in enumerate(self.base)})

    async def _notify(self, submission, recipient, purpose, text, markup=None):
        with self.db:
            inserted = self.db.execute(
                "INSERT OR IGNORE INTO deliveries(submission,recipient,purpose,status) VALUES(?,?,?,'sending')",
                (submission, recipient, purpose)).rowcount
        if not inserted:
            return
        message = await self._send(recipient, text, markup)
        source = getattr(message, 'message_id', None)
        with self.db:
            self.db.execute('UPDATE deliveries SET status=?,source=? WHERE submission=? AND recipient=? AND purpose=?',
                            ('sent' if message is not None else 'uncertain', source, submission, recipient, purpose))
            if markup is not None and type(source) is int:
                self.db.execute('INSERT OR IGNORE INTO moderation_messages VALUES(?,?,?)',
                                (submission, recipient, source))

    async def _callback(self, envelope, actor):
        data = envelope.callback_data or ''
        if getattr(envelope, 'callback_id', None):
            try:
                async with asyncio.timeout(10):
                    await self.bot.answer_callback_query(callback_query_id=envelope.callback_id,
                                                         request_timeout=10)
            except Exception:
                pass
        if actor not in self.admins or envelope.chat_id != actor or not envelope.private:
            return
        pieces = data.split(':')
        if len(pieces) != 3 or pieces[0] != 'place' or pieces[1] not in ('a', 'r'):
            return
        _, action, submission = pieces
        binding = self.db.execute('SELECT 1 FROM moderation_messages WHERE submission=? AND recipient=? AND source=?',
                                  (submission, actor, envelope.source_id)).fetchone()
        if not binding:
            await self._send(actor, 'Эта кнопка недействительна. Откройте /pending.')
            return
        row = self.db.execute('SELECT actor,payload,status FROM submissions WHERE id=?', (submission,)).fetchone()
        if row is None or row[2] != 'pending':
            await self._send(actor, 'Заявка уже рассмотрена.')
            return
        applicant, payload, _ = row
        status = 'approved' if action == 'a' else 'rejected'
        values = json.loads(payload)
        if action == 'a':
            values.update(active=True, updated_at=datetime.now(timezone.utc).date().isoformat())
            _record(values, self.path, 0, {record.id: i for i, record in enumerate(self.base + self._approved())})
        with self.db:
            changed = self.db.execute("UPDATE submissions SET status=?,decided=? WHERE id=? AND status='pending'",
                                      (status, time.time(), submission)).rowcount
            if changed and action == 'a':
                self.db.execute('INSERT INTO approved VALUES(?,?,?)',
                                (submission, json.dumps(values, ensure_ascii=False),
                                 self.db.execute('SELECT COUNT(*) FROM approved').fetchone()[0]))
        if changed:
            await self._send(actor, 'Место опубликовано и доступно в поиске.' if action == 'a' else 'Заявка отклонена.')
            if applicant is not None:
                await self._notify(submission, applicant, 'decision',
                                   'Ваша заявка одобрена: место появилось в поиске.' if action == 'a' else 'Ваша заявка отклонена модератором.')

    async def __call__(self, envelope):
        from .telegram_app import Kind, RequestService
        actor = getattr(envelope, 'actor_id', None)
        private = getattr(envelope, 'private', True)
        human = getattr(envelope, 'human', True)
        if type(actor) is not int or not private or not human or envelope.chat_id != actor:
            if getattr(envelope, 'callback_id', None) is not None or getattr(envelope, 'callback_data', None) is not None:
                await self._callback(envelope, None)
                return
            await RequestService(self.bot, self.base + self._approved(), self.limit)(envelope)
            return
        now = time.time()
        row = self.db.execute('SELECT 1 FROM users WHERE actor=?', (actor,)).fetchone()
        if row is None:
            if self.db.execute('SELECT COUNT(*) FROM users').fetchone()[0] >= 10000:
                await self._send(actor, 'Приём новых заявок временно недоступен. Поиск работает.')
                await RequestService(self.bot, self.base + self._approved(), self.limit)(envelope)
                return
            notice = await self._send(actor, 'Для работы заявок бот хранит ваш Telegram ID, имя, username и время активности. '
                                      'Администраторы видят список пользователей. Геопозиция поиска не сохраняется.')
            if notice is None:
                return
        name = str(getattr(envelope, 'display_name', '') or '')[:128]
        username = getattr(envelope, 'username', None)
        username = str(username)[:32] if username else None
        with self.db:
            self.db.execute('INSERT INTO users VALUES(?,?,?,?,?) ON CONFLICT(actor) DO UPDATE SET name=excluded.name,username=excluded.username,last_seen=MAX(users.last_seen,excluded.last_seen)',
                            (actor, name, username, now, now))
            self.db.execute('DELETE FROM drafts WHERE actor=? AND changed < ?', (actor, now - 7*86400))
        if getattr(envelope, 'callback_id', None) is not None or getattr(envelope, 'callback_data', None) is not None:
            await self._callback(envelope, actor)
            return
        text = (getattr(envelope, 'text', None) or '').strip()
        command = text.split(maxsplit=1)[0].split('@', 1)[0] if text else ''
        if command == '/myid':
            await self._send(actor, f'Ваш Telegram ID: {actor}')
            return
        if command in ('/users', '/pending'):
            if actor not in self.admins:
                await self._send(actor, 'Команда доступна только администраторам.')
                return
            try:
                page = max(1, min(100000, int(text.split()[1]))) if len(text.split()) > 1 else 1
            except ValueError:
                page = 1
            if command == '/users':
                total = self.db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
                rows = self.db.execute('SELECT actor,name,username,first_seen,last_seen FROM users ORDER BY last_seen DESC,actor LIMIT 10 OFFSET ?', ((page-1)*10,)).fetchall()
                lines = [f'Пользователи: {total}. Страница {page}']
                for uid, label, handle, first, last in rows:
                    lines.append(f'{uid} · {label} · @{handle or "—"}\nПервый вход: {datetime.fromtimestamp(first, timezone.utc).isoformat(timespec="seconds")}\nПоследний: {datetime.fromtimestamp(last, timezone.utc).isoformat(timespec="seconds")}')
                lines.append(f'Следующая: /users {page+1}')
                await self._send(actor, '\n\n'.join(lines))
            else:
                rows = self.db.execute("SELECT id,payload FROM submissions WHERE status='pending' ORDER BY created,id LIMIT 10 OFFSET ?", ((page-1)*10,)).fetchall()
                if not rows:
                    await self._send(actor, 'Ожидающих заявок нет.')
                for submission, payload in rows:
                    message = await self._send(actor, 'Заявка:\n' + self._preview(json.loads(payload)), self._buttons(submission))
                    source = getattr(message, 'message_id', None)
                    if type(source) is int:
                        with self.db:
                            self.db.execute('INSERT OR IGNORE INTO moderation_messages VALUES(?,?,?)', (submission, actor, source))
                if rows:
                    await self._send(actor, f'Следующая страница: /pending {page+1}')
            return
        if envelope.kind in (Kind.LOCATION, Kind.INVALID, Kind.START, Kind.HELP) or text == 'Поиск':
            await RequestService(self.bot, self.base + self._approved(), self.limit)(envelope)
            return
        draft = self.db.execute('SELECT step,fields FROM drafts WHERE actor=?', (actor,)).fetchone()
        if command == '/suggest' or text in ('Предложить место', '➕ Предложить место'):
            if draft is None:
                pending = self.db.execute("SELECT status FROM submissions WHERE actor=? ORDER BY created DESC LIMIT 1", (actor,)).fetchone()
                if pending:
                    await self._send(actor, 'Последняя заявка: ' + {'pending': 'ожидает проверки', 'approved': 'одобрена', 'rejected': 'отклонена'}[pending[0]])
                    if pending[0] == 'pending':
                        return
                if self.db.execute('SELECT COUNT(*) FROM drafts').fetchone()[0] >= 10000:
                    await self._send(actor, 'Приём заявок временно недоступен.')
                    return
                with self.db:
                    self.db.execute('INSERT INTO drafts VALUES(?,?,?,?)', (actor, 0, '{}', now))
                draft = (0, '{}')
            await self._prompt(actor, draft[0], json.loads(draft[1]))
            return
        if command == '/cancel':
            with self.db:
                self.db.execute('DELETE FROM drafts WHERE actor=?', (actor,))
            await self._send(actor, 'Заявка отменена. Для новой: /suggest')
            return
        if draft is None:
            await RequestService(self.bot, self.base + self._approved(), self.limit)(envelope)
            return
        step, raw = draft
        values = json.loads(raw)
        if command == '/back':
            step = max(0, step - 1)
        elif step == len(_FIELDS):
            if command != '/submit' and text != 'Отправить заявку':
                await self._prompt(actor, step, values)
                return
            try:
                record = self._validate(values)
            except CatalogError as error:
                field = error.diagnostic.field
                step = next((i for i, (key, _, _) in enumerate(_FIELDS) if key == field), 0)
                await self._send(actor, f'Проверьте поле {field}.')
            else:
                with self.db:
                    count = self.db.execute('SELECT COUNT(*) FROM submissions WHERE actor=? AND created>?', (actor, now-86400)).fetchone()[0]
                    pending = self.db.execute("SELECT COUNT(*) FROM submissions WHERE status='pending'").fetchone()[0]
                    own = self.db.execute("SELECT 1 FROM submissions WHERE actor=? AND status='pending'", (actor,)).fetchone()
                    if count >= 3 or pending >= 1000 or own:
                        await self._send(actor, 'Лимит заявок достигнут. Дождитесь проверки или попробуйте позже.')
                        return
                    payload = json.dumps(record.to_mapping(), ensure_ascii=False)
                    self.db.execute('INSERT INTO submissions VALUES(?,?,?,?,?,NULL)', (record.id, actor, payload, 'pending', now))
                    self.db.execute('DELETE FROM drafts WHERE actor=?', (actor,))
                await self._send(actor, 'Заявка отправлена на проверку. Статус: /suggest')
                for admin in sorted(self.admins):
                    await self._notify(record.id, admin, 'moderation', 'Новое место:\n' + self._preview(values), self._buttons(record.id))
                return
        else:
            field, _, optional = _FIELDS[step]
            skip = command == '/skip' or text == '-'
            if (skip and not optional) or not text:
                await self._send(actor, 'Это обязательное поле.')
                return
            value = None if skip else text
            if field in ('latitude', 'longitude'):
                try:
                    value = float(text.replace(',', '.'))
                    bound = 90 if field == 'latitude' else 180
                    if not math.isfinite(value) or not -bound <= value <= bound:
                        raise ValueError()
                except ValueError:
                    await self._send(actor, 'Нужно конечное число в указанном диапазоне.')
                    return
            elif value is not None and (len(value) > _LIMITS.get(field, 2048) or any(0xD800 <= ord(c) <= 0xDFFF for c in value)):
                await self._send(actor, 'Значение слишком длинное или содержит недопустимые символы.')
                return
            if field == 'rating_source':
                value = 'catalog' if skip else value.lower()
                if value not in ('catalog', 'yandex'):
                    await self._send(actor, 'Укажите catalog или yandex.')
                    return
            if value is None:
                values.pop(field, None)
            else:
                values[field] = value
            step += 1
            if step == len(_FIELDS):
                try:
                    self._validate(values)
                except CatalogError as error:
                    field = error.diagnostic.field
                    step = next((i for i, (key, _, _) in enumerate(_FIELDS) if key == field), 0)
                    await self._send(actor, f'Проверьте поле {field}; заявка пока не отправлена.')
        with self.db:
            self.db.execute('UPDATE drafts SET step=?,fields=?,changed=? WHERE actor=?',
                            (step, json.dumps(values, ensure_ascii=False), now, actor))
        await self._prompt(actor, step, values)
