"""Bounded Telegram edge. Generator: coder/coworking-20261019-01.

Queues and committed offsets belong to Scheduler, including across worker death.
No payload or exception is an observability input. Process guards are installed
by the executable, not at import time (the catalogue CLI is independent).
"""
from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass
from enum import StrEnum
import json
import logging
import re
import secrets
import sys
import warnings

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.methods import GetUpdates
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup, ReplyParameters)

from . import render
from .geo import find_nearest, validate_origin
from .models import Origin


ORIGIN_MARKER = "_coworking_invalid_origin"
PAUSE = 1.1
ATTEMPT = 10.0
SERVICE = 90.0


class DeliveryStop(Exception):
    """No response, method, description, cause or raw status retained."""


class FloodRefusal(DeliveryStop):
    def __init__(self, wait: int):
        self.wait = wait
        super().__init__()


class FailStop(Exception):
    pass


class _PostFacade:
    def __init__(self, raw):
        self._raw = raw

    def post(self, *args, **kwargs):
        kwargs["allow_redirects"] = False
        kwargs["middlewares"] = ()
        return self._raw.post(*args, **kwargs)


def _invalid_location(location):
    if not isinstance(location, dict):
        return True
    try:
        validate_origin(location.get("latitude"), location.get("longitude"))
    except ValueError:
        return True
    return False


def _guard_origins(data):
    """Localized pre-Pydantic check; repair coordinates only, never metadata."""
    if not isinstance(data, dict) or not isinstance(data.get("result"), list):
        return
    for update in data["result"]:
        if not isinstance(update, dict):
            continue
        update.pop(ORIGIN_MARKER, None)
        invalid = False
        for key in ("message", "edited_message"):
            message = update.get(key)
            if not isinstance(message, dict):
                continue
            venue = message.get("venue")
            chosen = (venue.get("location") if isinstance(venue, dict)
                      else message.get("location"))
            if key == "message" and (venue is not None or message.get("location") is not None):
                invalid = _invalid_location(chosen)
            locations = []
            if "location" in message:
                locations.append((message, "location"))
            if isinstance(venue, dict) and "location" in venue:
                locations.append((venue, "location"))
            for container, field in locations:
                location = container[field]
                # Reject malformed metadata explicitly before SDK coercion.
                if location is not None and not isinstance(location, dict):
                    raise DeliveryStop()
                if isinstance(location, dict) and _invalid_location(location):
                    location["latitude"] = 0
                    location["longitude"] = 0
        update[ORIGIN_MARKER] = invalid


class GuardedAiohttpSession(AiohttpSession):
    async def create_session(self):
        # Keep base _session as the raw owner, including after recreation.
        return _PostFacade(await super().create_session())

    def check_response(self, bot, method, status_code, content):
        if status_code >= 500 or 300 <= status_code < 400:
            raise DeliveryStop()
        try:
            data = self.json_loads(content)
        except Exception:
            raise DeliveryStop() from None
        if status_code == 429:
            parameters = data.get("parameters") if isinstance(data, dict) else None
            wait = parameters.get("retry_after") if isinstance(parameters, dict) else None
            if (isinstance(data, dict) and data.get("ok") is False
                    and type(data.get("error_code")) is int and data["error_code"] == 429
                    and type(wait) is int and wait >= 0):
                raise FloodRefusal(wait)
            raise DeliveryStop()
        if not 200 <= status_code < 300:
            raise DeliveryStop()
        if isinstance(method, GetUpdates):
            _guard_origins(data)
            content = self.json_dumps(data)
        try:
            return super().check_response(bot, method, status_code, content)
        except Exception:
            raise DeliveryStop() from None


class Kind(StrEnum):
    START = "start"
    HELP = "help"
    GROUP = "group"
    FALLBACK = "fallback"
    INVALID = "invalid"
    LOCATION = "location"


@dataclass(frozen=True, slots=True, repr=False)
class Envelope:
    chat_id: int
    source_id: int
    kind: Kind
    origin: Origin | None = None


@dataclass(frozen=True, slots=True, repr=False)
class _Admission:
    envelope: Envelope
    admitted_at: float


def envelope_from_update(update):
    message = update.message
    if message is None:
        return None
    kind, origin = Kind.FALLBACK, None
    if message.chat.type != "private":
        kind = Kind.GROUP
    elif getattr(update, ORIGIN_MARKER, False) is True:
        kind = Kind.INVALID
    elif message.venue is not None or message.location is not None:
        location = message.venue.location if message.venue is not None else message.location
        try:
            origin = validate_origin(location.latitude, location.longitude)
            kind = Kind.LOCATION
        except ValueError:
            kind = Kind.INVALID
    elif message.text:
        words = message.text.split(maxsplit=1)
        command = words[0].split("@", 1)[0] if words else ""
        if command == "/start":
            kind = Kind.START
        elif command == "/help":
            kind = Kind.HELP
    return Envelope(message.chat.id, message.message_id, kind, origin)


def _keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(
        text=render.LOCATION_BUTTON_TEXT, request_location=True)]], resize_keyboard=True)


async def _wait_full(delay):
    """Keep a fixed monotonic end when asyncio dispatches a timer early."""
    loop = asyncio.get_running_loop()
    end = loop.time() + delay
    while (remaining := end - loop.time()) > 0:
        await asyncio.sleep(remaining)


class RequestService:
    def __init__(self, bot, snapshot, limit):
        self.bot, self.snapshot, self.limit = bot, snapshot, limit

    def messages(self, envelope):
        texts = {Kind.START: render.start_text(self.limit), Kind.HELP: render.HELP_TEXT,
                 Kind.GROUP: render.GROUP_TEXT, Kind.FALLBACK: render.FALLBACK_TEXT,
                 Kind.INVALID: render.INVALID_ORIGIN_TEXT}
        if envelope.kind != Kind.LOCATION:
            yield texts[envelope.kind], None if envelope.kind == Kind.GROUP else _keyboard()
            return
        results = find_nearest(envelope.origin, self.snapshot, self.limit)
        if not results:
            yield render.EMPTY_TEXT, _keyboard()
            return
        yield render.INTRO_TEXT, None
        for position, result in enumerate(results, 1):
            card = render.render_card(result, position, envelope.origin)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=button.text, url=button.url) for button in row
            ] for row in card.button_rows])
            yield card.text, keyboard

    async def __call__(self, envelope):
        loop = asyncio.get_running_loop()
        deadline = loop.time() + SERVICE
        waits = 0
        messages = self.messages(envelope)
        try:
            async with asyncio.timeout_at(deadline):
                for text, keyboard in messages:
                    retried = False
                    while True:
                        if deadline - loop.time() < PAUSE + ATTEMPT:
                            return
                        await _wait_full(PAUSE)
                        if deadline - loop.time() < ATTEMPT:
                            return
                        try:
                            async with asyncio.timeout(ATTEMPT):
                                await self.bot.send_message(
                                    chat_id=envelope.chat_id, text=text, parse_mode="HTML",
                                    reply_markup=keyboard, reply_parameters=ReplyParameters(
                                        message_id=envelope.source_id, allow_sending_without_reply=False),
                                    request_timeout=10)
                            break
                        except FloodRefusal as refusal:
                            wait = refusal.wait
                            if (retried or wait > 15 - waits
                                    or deadline - loop.time() < wait + PAUSE + ATTEMPT):
                                return
                            await _wait_full(wait)
                            waits += wait
                            retried = True
                        except Exception:
                            emit_safe(Event.STOP, Stage.SEND)
                            return
        except TimeoutError:
            emit_safe(Event.STOP, Stage.SEND)
        finally:
            messages.close()
            envelope = text = keyboard = messages = None


class Scheduler:
    def __init__(self, service, *, global_limit=64, chat_limit=8):
        self.service = service
        self.global_limit, self.chat_limit = global_limit, chat_limit
        self.queues = {}
        self.workers = {}
        self.counts = {}
        self.pending = 0
        self.cursor = None
        self.changed = asyncio.Event()
        self.stopping = False
        self.failed = asyncio.Event()

    def _notify(self):
        self.changed.set()

    def _publish(self):
        try:
            self._notify()
        except BaseException:
            # Notification cannot own accounting or prevent supervision.
            self.failed.set()
            self.changed.set()

    def _spawn(self, chat):
        coroutine = self._worker(chat)
        try:
            task = asyncio.create_task(coroutine)
        except BaseException:
            coroutine.close()
            raise
        self.workers[chat] = task
        task.add_done_callback(lambda done: self._worker_done(chat, done))
        return task

    def _retire(self, chat, owner):
        if self.workers.get(chat) is not owner:
            return
        self.workers.pop(chat)
        if self.queues.get(chat) and not self.stopping:
            try:
                self._spawn(chat)
            except BaseException:
                self.failed.set()
        elif not self.queues.get(chat):
            self.queues.pop(chat, None)

    def _worker_done(self, chat, task):
        # Also supervises cancellation before the coroutine's first instruction.
        if not task.cancelled():
            task.exception()
        self._retire(chat, task)
        self._publish()

    async def admit(self, envelope, update_id):
        try:
            while (self.pending >= self.global_limit
                   or self.counts.get(envelope.chat_id, 0) >= self.chat_limit):
                if self.failed.is_set() or self.stopping:
                    raise FailStop()
                self.changed.clear()
                await self.changed.wait()
            # Observe already requested cancellation before the no-await commit.
            if asyncio.current_task().cancelling():
                raise asyncio.CancelledError()
            if self.failed.is_set() or self.stopping:
                raise FailStop()
            self._commit(envelope, update_id)
        finally:
            envelope = None

    def _commit(self, envelope, update_id):
        chat = envelope.chat_id
        queue = self.queues.setdefault(chat, deque())
        queue.append(_Admission(envelope, asyncio.get_running_loop().time()))
        self.pending += 1
        self.counts[chat] = self.counts.get(chat, 0) + 1
        try:
            if chat not in self.workers:
                self._spawn(chat)
        except BaseException:
            queue.pop()
            self._release(chat)
            if not queue:
                self.queues.pop(chat, None)
            raise
        self.cursor = update_id + 1

    def _release(self, chat):
        self.pending -= 1
        remaining = self.counts[chat] - 1
        if remaining:
            self.counts[chat] = remaining
        else:
            del self.counts[chat]

    def _request_finally(self):
        """Post-accounting fault seam; no state ownership."""
        self._publish()

    async def _worker(self, chat):
        owner = asyncio.current_task()
        active = None
        try:
            while self.workers.get(chat) is owner and self.queues.get(chat):
                admission = self.queues[chat].popleft()
                active = admission.envelope
                wait_ms = int(max(0, asyncio.get_running_loop().time() - admission.admitted_at) * 1000)
                admission = None
                try:
                    emit_safe(Event.QUEUE, Stage.WORKER, wait_ms=wait_ms)
                    await self.service(active)
                except Exception:
                    emit_safe(Event.STOP, Stage.WORKER)
                finally:
                    # Clear ownership before any injectable finalizer.
                    active = None
                    self._release(chat)
                    self._request_finally()
        finally:
            # Covers unexpected failures outside request-finally as well.
            if active is not None:
                active = None
                self._release(chat)
            self._retire(chat, owner)
            self._publish()

    async def wait_chat(self, chat):
        while chat in self.workers:
            self.changed.clear()
            await self.changed.wait()

    async def drain(self):
        while self.pending:
            if self.failed.is_set():
                raise FailStop()
            self.changed.clear()
            await self.changed.wait()

    def discard_queued(self):
        for chat, queue in tuple(self.queues.items()):
            while queue:
                queue.popleft()
                self._release(chat)
            if chat not in self.workers:
                self.queues.pop(chat, None)
        self._publish()


class Application:
    def __init__(self, bot, snapshot, limit):
        self.bot = bot
        self.scheduler = Scheduler(RequestService(bot, snapshot, limit))
        # No FSM storage, user context or per-update background fanout.
        self.dispatcher = Dispatcher(disable_fsm=True)
        self.dispatcher.update.handlers.clear()
        self.dispatcher.update.register(self._enqueue)
        self.ingress = None
        self.cleanup_task = None

    async def _enqueue(self, update):
        envelope = envelope_from_update(update)
        uid = update.update_id
        update = None
        try:
            if envelope is None:
                self.scheduler.cursor = uid + 1
            else:
                await self.scheduler.admit(envelope, uid)
        finally:
            envelope = None

    async def poll(self):
        while not self.scheduler.stopping:
            if self.scheduler.failed.is_set():
                raise FailStop()
            updates = update = None
            try:
                updates = await self.bot.get_updates(offset=self.scheduler.cursor, limit=1,
                    allowed_updates=["message", "edited_message"], timeout=1, request_timeout=15)
                if len(updates) > 1:
                    raise FailStop()
                for update in updates:
                    await self.dispatcher.feed_update(self.bot, update)
            except FailStop:
                raise
            except Exception:
                emit_safe(Event.STOP, Stage.INGRESS)
                await asyncio.sleep(5)
            finally:
                updates = update = None

    async def shutdown(self, session):
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._cleanup(session))
        cancelled = False
        while True:
            try:
                await asyncio.shield(self.cleanup_task)
                break
            except asyncio.CancelledError:
                cancelled = True
                if self.cleanup_task.done():
                    if self.cleanup_task.cancelled():
                        raise FailStop() from None
                    # Retrieve the owned outcome before propagating caller cancellation.
                    self.cleanup_task.result()
                    break
        if cancelled:
            raise asyncio.CancelledError()

    async def _cleanup(self, session):
        failed = False
        self.scheduler.stopping = True
        try:
            if self.ingress is not None:
                self.ingress.cancel()
                failed |= not await bounded_tasks((self.ingress,), 2)
            try:
                drain = asyncio.create_task(self.scheduler.drain())
                if not await bounded_tasks((drain,), 10):
                    # Expiry is normal progression to worker cancellation;
                    # an already completed drain failure is not success.
                    if drain.done():
                        failed = True
                    else:
                        drain.cancel()
            except BaseException:
                failed = True
        except BaseException:
            failed = True
        finally:
            try:
                workers = tuple(self.scheduler.workers.values())
                for worker in workers:
                    worker.cancel()
                failed |= not await bounded_tasks(workers, 2)
                self.scheduler.discard_queued()
            except BaseException:
                failed = True
            finally:
                if session is not None:
                    try:
                        close = asyncio.create_task(session.close())
                        failed |= not await bounded_tasks((close,), 2)
                    except BaseException:
                        failed = True
        if failed or self.scheduler.pending:
            emit_safe(Event.FAIL, Stage.CLEANUP)
            raise FailStop()


async def bounded_tasks(tasks, seconds):
    """No wait_for cancellation join: timeout never starts an unbounded await."""
    if not tasks:
        return True
    done, pending = await asyncio.wait(tasks, timeout=seconds)
    for task in pending:
        task.cancel()
    okay = not pending
    for task in done:
        if not task.cancelled() and task.exception() is not None:
            okay = False
    return okay


class Event(StrEnum):
    QUEUE = "queue"
    START = "start"
    STOP = "stop"
    FAIL = "fail"
    WARNING = "warning"


class Stage(StrEnum):
    STARTUP = "startup"
    INGRESS = "ingress"
    WORKER = "worker"
    SEND = "send"
    CLEANUP = "cleanup"
    PROCESS = "process"


_safe_sink = None
_emitting = False
_safe_level = logging.INFO
_EVENT_LEVELS = {Event.QUEUE: logging.DEBUG, Event.START: logging.INFO,
                 Event.WARNING: logging.WARNING, Event.STOP: logging.WARNING, Event.FAIL: logging.ERROR}


def emit_safe(event, stage, request_id=None, count=0, *, wait_ms=0):
    global _emitting
    if type(event) is not Event or type(stage) is not Stage or _safe_sink is None or _emitting:
        return
    if _EVENT_LEVELS[event] < _safe_level:
        return
    if request_id is None:
        request_id = secrets.token_hex(16)
    if type(request_id) is not str or re.fullmatch(r"[0-9a-f]{32}", request_id) is None:
        return
    count = min(64, max(0, count)) if type(count) is int else 0
    _emitting = True
    try:
        record = {"event": event.value, "stage": stage.value, "id": request_id, "count": count}
        if event is Event.QUEUE:
            record["wait_ms"] = min(86400000, max(0, wait_ms)) if type(wait_ms) is int else 0
        _safe_sink.write(json.dumps(record) + "\n")
        _safe_sink.flush()
    except BaseException:
        pass
    finally:
        _emitting = False


class _Discard:
    encoding = "utf-8"
    errors = "ignore"
    def write(self, value):
        return len(value) if type(value) is str else 0
    def flush(self):
        pass
    def isatty(self):
        return False
    @property
    def buffer(self):
        return self


class ProcessSinks:
    """Reversible process boundary for the executable and isolated tests.

    Suppress at Logger.handle AND Handler.handle, before filters/formatters.
    The serializer writes directly to its captured sink; raw logging has no
    path to this sink, even through existing or subsequently added handlers.
    """
    def __init__(self, loop=None):
        global _safe_sink
        self.old_level = _safe_level
        self.loop = loop
        self.streams = sys.stdout, sys.stderr, sys.__stdout__, sys.__stderr__
        self.hooks = sys.excepthook, sys.unraisablehook, warnings.showwarning
        self.logging_hooks = logging.Logger.handle, logging.Handler.handle, logging.lastResort
        self.capture_hook = logging._warnings_showwarning
        self.old_sink = _safe_sink
        # Nested executable/async guards share the original retained sink,
        # never replace it with the outer guard's discard wrapper.
        _safe_sink = (self.old_sink if isinstance(sys.stderr, _Discard)
                      and self.old_sink is not None else sys.stderr)
        self.handlers = {}
        for logger in [logging.root, *logging.Logger.manager.loggerDict.values()]:
            if isinstance(logger, logging.Logger):
                self.handlers[logger] = logger.handlers[:], logger.propagate
                logger.handlers = []
                logger.propagate = False
        logging.Logger.handle = lambda *_args, **_kwargs: None
        logging.Handler.handle = lambda *_args, **_kwargs: None
        logging.lastResort = logging.NullHandler()
        logging.captureWarnings(True)
        warnings.showwarning = lambda *_args, **_kwargs: emit_safe(Event.WARNING, Stage.PROCESS)
        sys.excepthook = lambda *_args: emit_safe(Event.FAIL, Stage.PROCESS)
        sys.unraisablehook = lambda *_args: emit_safe(Event.FAIL, Stage.PROCESS)
        sys.stdout = sys.stderr = sys.__stdout__ = sys.__stderr__ = _Discard()
        if loop is not None:
            self.loop_hook = loop.get_exception_handler()
            loop.set_exception_handler(lambda *_args: emit_safe(Event.FAIL, Stage.PROCESS))

    def set_level(self, level):
        global _safe_level
        if type(level) is str and level in {"CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"}:
            _safe_level = logging.getLevelNamesMapping()[level]

    def restore(self):
        global _safe_sink, _safe_level
        _safe_level = self.old_level
        if self.loop is not None:
            self.loop.set_exception_handler(self.loop_hook)
        sys.stdout, sys.stderr, sys.__stdout__, sys.__stderr__ = self.streams
        sys.excepthook, sys.unraisablehook, warnings.showwarning = self.hooks
        logging.Logger.handle, logging.Handler.handle, logging.lastResort = self.logging_hooks
        logging._warnings_showwarning = self.capture_hook
        for logger, (handlers, propagate) in self.handlers.items():
            logger.handlers, logger.propagate = handlers, propagate
        for logger in logging.Logger.manager.loggerDict.values():
            if isinstance(logger, logging.Logger) and logger not in self.handlers:
                logger.handlers = []
                logger.propagate = True
        _safe_sink = self.old_sink
