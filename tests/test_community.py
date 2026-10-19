"""Community workflow persistence and privilege boundaries without Telegram I/O."""
import asyncio
from dataclasses import dataclass
from types import SimpleNamespace

from coworking_nearby.community import CommunityService
from coworking_nearby.telegram_app import Kind


class FakeBot:
    def __init__(self):
        self.sent = []
        self.answers = []

    async def send_message(self, **kwargs):
        self.sent.append(kwargs)
        return SimpleNamespace(message_id=len(self.sent))

    async def answer_callback_query(self, **kwargs):
        self.answers.append(kwargs)
        return True


def envelope(actor=101, text='', **extra):
    values = dict(actor_id=actor, chat_id=actor, source_id=1, kind=Kind.FALLBACK,
                  origin=None, display_name='A <user>', username='sample', text=text,
                  callback_data=None, callback_id=None, private=True, human=True)
    values.update(extra)
    return SimpleNamespace(**values)


def test_durable_wizard_submission_and_atomic_authorized_approval(tmp_path):
    async def exercise():
        bot = FakeBot()
        state = tmp_path / 'state' / 'community.sqlite3'
        service = CommunityService(bot, (), 3, (201, 202, 203), state)
        await service(envelope(text='/suggest'))
        for value in ('Тестовое место', 'Москва, улица 1', '55.7', '37.6'):
            await service(envelope(text=value))
        service.close()
        service = CommunityService(bot, (), 3, (201, 202, 203), state)
        assert service.db.execute('SELECT step FROM drafts').fetchone() == (4,)
        for _ in range(6):
            await service(envelope(text='/skip'))
        await service(envelope(text='/submit'))
        submission, status = service.db.execute('SELECT id,status FROM submissions').fetchone()
        assert status == 'pending'
        assert service._approved() == ()
        notifications = [message for message in bot.sent if message.get('reply_markup')]
        assert {message['chat_id'] for message in notifications} == {201, 202, 203}
        assert all('reply_parameters' not in message for message in notifications)
        source = service.db.execute('SELECT source FROM moderation_messages WHERE recipient=201').fetchone()[0]
        data = f'place:a:{submission}'
        await service(envelope(actor=101, callback_data=data, callback_id='forged', source_id=source))
        assert service._approved() == ()
        await service(envelope(actor=201, callback_data=data, callback_id='valid', source_id=source))
        assert len(service._approved()) == 1
        assert service._approved()[0].active
        assert service.db.execute('SELECT status FROM submissions').fetchone() == ('approved',)
        await service(envelope(actor=201, callback_data=data, callback_id='replay', source_id=source))
        assert len(service._approved()) == 1
        service.close()
        restored = CommunityService(bot, (), 3, (201, 202, 203), state)
        assert len(restored._approved()) == 1
        restored.close()
    asyncio.run(exercise())


def test_registry_is_minimal_and_users_requires_numeric_admin(tmp_path):
    async def exercise():
        bot = FakeBot()
        service = CommunityService(bot, (), 3, (201,), tmp_path / 'state' / 'db')
        await service(envelope(text='/myid'))
        assert service.db.execute('SELECT actor,name,username FROM users').fetchone() == (101, 'A <user>', 'sample')
        assert [row[1] for row in service.db.execute('PRAGMA table_info(users)')] == ['actor', 'name', 'username', 'first_seen', 'last_seen']
        await service(envelope(text='/users', username='admin'))
        assert 'только администраторам' in bot.sent[-1]['text']
        await service(envelope(actor=201, text='/users'))
        assert any('A &lt;user&gt;' in message['text'] for message in bot.sent)
        assert service.db.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 2
        service.close()
    asyncio.run(exercise())


def test_invalid_coordinates_do_not_advance_draft(tmp_path):
    async def exercise():
        service = CommunityService(FakeBot(), (), 3, (201,), tmp_path / 'state' / 'db')
        for value in ('/suggest', 'Place', 'Address', 'nan', '91'):
            await service(envelope(text=value))
        assert service.db.execute('SELECT step FROM drafts').fetchone() == (2,)
        await service(envelope(text='/cancel'))
        assert service.db.execute('SELECT COUNT(*) FROM drafts').fetchone() == (0,)
        service.close()
    asyncio.run(exercise())
