"""Adversarial process sinks at DEBUG and INFO, with hook restoration."""
import asyncio
import io
import json
import logging
import sys
import warnings

import pytest
from aiogram.exceptions import TelegramNetworkError
from aiogram.methods import SendMessage

from coworking_nearby import telegram_app as app


@pytest.mark.parametrize("level", [logging.DEBUG, logging.INFO])
def test_all_process_sinks_INFO_DEBUG(level, monkeypatch):
    output = io.StringIO()
    monkeypatch.setattr(sys, "stderr", output)
    monkeypatch.setattr(sys, "stdout", output)
    secrets = "FAKE_TOKEN_8xyz 55.123456789,37.987654321 https://yandex.ru/maps/?rtext=55.123456789"
    touched = []
    class Hostile:
        def __str__(self):
            touched.append("str")
            raise AssertionError("hostile formatting")
        def __repr__(self):
            touched.append("repr")
            raise AssertionError("hostile formatting")
    async def scenario():
        loop = asyncio.get_running_loop()
        handler = logging.StreamHandler(output)
        root = logging.getLogger()
        prior_level = root.level
        root.addHandler(handler)
        root.setLevel(level)
        guard = app.ProcessSinks(loop)
        guard.set_level(logging.getLevelName(level))
        try:
            for name in ("", "aiogram", "aiohttp", "asyncio", "py.warnings", "library"):
                logger = logging.getLogger(name)
                logger.addHandler(logging.StreamHandler(output))
                logger.error("%s %r %s", Hostile(), Hostile(), secrets, exc_info=True)
            logging.lastResort.handle(logging.LogRecord("x", 50, "", 1, Hostile(), (), None))
            warnings.showwarning(Hostile(), UserWarning, secrets, 1)
            warnings.warn(secrets)
            error = TelegramNetworkError(method=SendMessage(chat_id=42, text=secrets), message=secrets)
            error.__cause__ = RuntimeError(secrets)
            sys.excepthook(type(error), error, None)
            sys.unraisablehook(Hostile())
            loop.call_exception_handler({"message": secrets, "exception": error, "object": Hostile()})
            sys.stdout.write(secrets)
            sys.stderr.write(secrets)
            sys.__stderr__.write(secrets)
            sys.stderr.buffer.write(secrets.encode())
            app.emit_safe(app.Event.START, app.Stage.STARTUP, count=999)
            app.emit_safe(Hostile(), app.Stage.SEND)
            app.emit_safe(app.Event.FAIL, Hostile())
            app.emit_safe(app.Event.FAIL, app.Stage.SEND, Hostile())
            app.emit_safe(app.Event.FAIL, app.Stage.SEND, count=Hostile())
        finally:
            guard.restore()
            root.removeHandler(handler)
            root.setLevel(prior_level)
    asyncio.run(scenario())
    assert not touched
    records = [json.loads(line) for line in output.getvalue().splitlines()]
    assert records
    assert secrets not in output.getvalue()
    for record in records:
        assert set(record) == {"event", "stage", "id", "count"}
        assert record["event"] in {e.value for e in app.Event}
        assert record["stage"] in {s.value for s in app.Stage}
        assert 0 <= record["count"] <= 64


def test_startup_failure_before_Bot(monkeypatch):
    from coworking_nearby import __main__ as entry
    events = []
    class Session:
        async def close(self):
            events.append("close")
    def settings():
        events.append("settings")
        return type("Settings", (), {"catalog_path": "ignored", "bot_token": "fake", "results_limit": 3})()
    def catalog(path):
        events.append("catalog")
        return ()
    def bot(*args, **kwargs):
        events.append("bot")
        raise RuntimeError("FAKE_TOKEN_DO_NOT_FORMAT")
    monkeypatch.setattr(entry, "load_settings", settings)
    monkeypatch.setattr(entry, "load_catalog", catalog)
    monkeypatch.setattr(entry, "GuardedAiohttpSession", Session)
    monkeypatch.setattr(entry, "Bot", bot)
    assert asyncio.run(entry.run()) == 1
    assert events == ["settings", "catalog", "bot", "close"]


@pytest.mark.parametrize("fault", ["config", "catalog", "session"])
def test_invalid_startup_no_Bot_polling(monkeypatch, fault):
    from coworking_nearby import __main__ as entry
    events = []
    class Settings:
        catalog_path = "PRIVATE_PATH_FAKE_TOKEN_1"
        bot_token = "PRIVATE_FAKE_TOKEN_1"
        results_limit = 3
    def settings():
        events.append("config")
        if fault == "config":
            raise RuntimeError(Settings.bot_token)
        return Settings()
    def catalog(path):
        events.append("catalog")
        if fault == "catalog":
            from coworking_nearby.catalog import CatalogError
            from coworking_nearby.models import CatalogDiagnostic
            from pathlib import Path
            raise CatalogError(CatalogDiagnostic(Path(path), "root", "$root"))
        return ()
    def session():
        events.append("session")
        raise RuntimeError(Settings.bot_token)
    def forbidden(*args, **kwargs):
        raise AssertionError("Bot must not be constructed")
    monkeypatch.setattr(entry, "load_settings", settings)
    monkeypatch.setattr(entry, "load_catalog", catalog)
    monkeypatch.setattr(entry, "GuardedAiohttpSession", session)
    monkeypatch.setattr(entry, "Bot", forbidden)
    output = io.StringIO()
    monkeypatch.setattr(sys, "stderr", output)
    assert asyncio.run(entry.run()) == 1
    assert events == {"config": ["config"], "catalog": ["config", "catalog"],
                      "session": ["config", "catalog", "session"]}[fault]
    assert "PRIVATE" not in output.getvalue()
    assert json.loads(output.getvalue())["event"] == "fail"


def test_actual_sdk_failure_and_safe_sink_recursion(monkeypatch):
    from aiogram import Bot
    from aiohttp import TCPConnector
    output = io.StringIO()
    secret = "FAKE_TOKEN_SECRET_4 55.111122223333 https://yandex.ru/maps/?rtext=55.111122223333"
    class RecursiveSink:
        def write(self, value):
            logging.getLogger("aiohttp").error(secret)
            sys.stderr.write(secret)
            app.emit_safe(app.Event.FAIL, app.Stage.PROCESS)
            return output.write(value)
        def flush(self):
            pass
    monkeypatch.setattr(sys, "stderr", RecursiveSink())
    async def scenario():
        async def rejected(*args, **kwargs):
            raise OSError(secret)
        monkeypatch.setattr(TCPConnector, "_create_connection", rejected)
        guard = app.ProcessSinks(asyncio.get_running_loop())
        session = app.GuardedAiohttpSession()
        bot = Bot("123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk", session=session)
        try:
            with pytest.raises(Exception) as failure:
                await bot.send_message(chat_id=1, text=secret)
            logging.getLogger("aiogram").error("%s", failure.value)
            sys.excepthook(type(failure.value), failure.value, failure.value.__traceback__)
            app.emit_safe(app.Event.STOP, app.Stage.SEND)
        finally:
            await session.close()
            guard.restore()
    asyncio.run(scenario())
    assert secret not in output.getvalue()
    records = [json.loads(line) for line in output.getvalue().splitlines()]
    assert [record["event"] for record in records] == ["fail", "stop"]


@pytest.mark.parametrize("close_fails", [False, True])
def test_repeated_SIGINT_SIGTERM_same_cleanup(monkeypatch, close_fails):
    import signal
    from coworking_nearby import __main__ as entry
    events = []
    class Settings:
        catalog_path = "ignored"
        bot_token = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"
        results_limit = 1
    class Session:
        async def close(self):
            events.append("close")
            # Exercise real process signal handlers during the shielded close.
            signal.raise_signal(signal.SIGINT)
            signal.raise_signal(signal.SIGTERM)
            for _ in range(10):
                await asyncio.sleep(0)
            if close_fails:
                raise RuntimeError("PRIVATE_CLOSE_FAILURE")
    class Application(app.Application):
        async def poll(self):
            events.append("poll")
            signal.raise_signal(signal.SIGTERM)
            await asyncio.Event().wait()
    monkeypatch.setattr(entry, "load_settings", lambda: Settings())
    monkeypatch.setattr(entry, "load_catalog", lambda path: ())
    monkeypatch.setattr(entry, "GuardedAiohttpSession", Session)
    monkeypatch.setattr(entry, "Application", Application)
    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}
    assert entry.main() == (1 if close_fails else 0)
    assert events == ["poll", "close"]
    assert {sig: signal.getsignal(sig) for sig in previous} == previous


def test_executable_nested_guard_retains_safe_startup_failure(monkeypatch):
    from coworking_nearby import __main__ as entry
    output = io.StringIO()
    monkeypatch.setattr(sys, "stderr", output)
    def failure():
        raise RuntimeError("DISTINCTIVE_FAKE_SECRET")
    monkeypatch.setattr(entry, "load_settings", failure)
    assert entry.main() == 1
    records = [json.loads(line) for line in output.getvalue().splitlines()]
    assert len(records) == 1
    assert records[0]["event"] == "fail" and records[0]["stage"] == "startup"
    assert "DISTINCTIVE" not in output.getvalue()


@pytest.mark.parametrize("level, expected", [
    ("DEBUG", ["queue", "start", "warning", "stop", "fail"]),
    ("INFO", ["start", "warning", "stop", "fail"]),
    ("WARNING", ["warning", "stop", "fail"]),
    ("ERROR", ["fail"]), ("CRITICAL", []), ("FATAL", []),
    ("WARN", ["warning", "stop", "fail"]),
    ("NOTSET", ["queue", "start", "warning", "stop", "fail"])])
def test_safe_verbosity_threshold_and_nested_restoration(monkeypatch, level, expected):
    output = io.StringIO()
    monkeypatch.setattr(sys, "stderr", output)
    outer = app.ProcessSinks()
    try:
        outer.set_level("ERROR")
        inner = app.ProcessSinks()
        try:
            inner.set_level(level)
            for event in (app.Event.QUEUE, app.Event.START, app.Event.WARNING, app.Event.STOP, app.Event.FAIL):
                app.emit_safe(event, app.Stage.PROCESS, wait_ms=10**100)
            logging.getLogger().critical("SECRET %s", object())
        finally:
            inner.restore()
        app.emit_safe(app.Event.START, app.Stage.STARTUP)
        app.emit_safe(app.Event.FAIL, app.Stage.PROCESS)
    finally:
        outer.restore()
    records = [json.loads(line) for line in output.getvalue().splitlines()]
    assert [r["event"] for r in records] == expected + ["fail"]
    for record in records:
        if record["event"] == "queue":
            assert record["wait_ms"] == 86400000


@pytest.mark.parametrize("close_fails", [False, True])
def test_run_defers_caller_cancellation_until_acquired_session_closed(monkeypatch, close_fails):
    from coworking_nearby import __main__ as entry
    from coworking_nearby.config import Settings
    async def scenario():
        acquired, closing, release = asyncio.Event(), asyncio.Event(), asyncio.Event()
        closed = []
        class Session:
            async def close(self):
                closing.set()
                await release.wait()
                closed.append(True)
                if close_fails:
                    raise RuntimeError("PRIVATE")
        class Application(app.Application):
            async def poll(self):
                acquired.set()
                await asyncio.Event().wait()
        monkeypatch.setattr(entry, "load_settings", lambda: Settings("123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"))
        monkeypatch.setattr(entry, "load_catalog", lambda path: ())
        monkeypatch.setattr(entry, "GuardedAiohttpSession", Session)
        monkeypatch.setattr(entry, "Application", Application)
        task = asyncio.create_task(entry.run())
        await acquired.wait()
        task.cancel()
        await closing.wait()
        assert not task.done() and not closed
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        release.set()
        with pytest.raises(app.FailStop if close_fails else asyncio.CancelledError):
            await task
        assert closed == [True]
    asyncio.run(scenario())


@pytest.mark.parametrize("timing", ["completion", "already_done"])
@pytest.mark.parametrize("outcome", ["success", "cancel", "error", "failstop"])
def test_owned_completion_caller_cancellation_boundary(timing, outcome):
    async def scenario():
        entered, gate = asyncio.Event(), asyncio.Event()
        failure = app.FailStop() if outcome == "failstop" else RuntimeError("owned failure")
        async def work():
            entered.set()
            await gate.wait()
            if outcome == "cancel":
                raise asyncio.CancelledError()
            if outcome != "success":
                raise failure
        from coworking_nearby.__main__ import _defer
        owned = asyncio.create_task(work())
        caller = asyncio.create_task(_defer(owned))
        await entered.wait()
        invoke = lambda: _defer(owned)
        if timing == "completion":
            # Registered after shield's callback: cancel before caller resumes.
            owned.add_done_callback(lambda done: caller.cancel())
            caller.cancel()
            await asyncio.sleep(0)
            caller.cancel()
            await asyncio.sleep(0)
            assert not owned.done() and not owned.cancelled()
            gate.set()
        else:
            gate.set()
            await asyncio.gather(caller, return_exceptions=True)
            assert owned.done()
            async def already_done():
                asyncio.current_task().cancel()
                return await invoke()
            caller = asyncio.create_task(already_done())
        result = (await asyncio.gather(caller, return_exceptions=True))[0]
        if outcome == "success":
            assert isinstance(result, asyncio.CancelledError)
            assert not owned.cancelled() and owned.exception() is None
        elif outcome == "cancel":
            assert isinstance(result, app.FailStop)
            assert owned.cancelled()
        else:
            assert result is failure
            assert owned.exception() is failure
        assert not [task for task in asyncio.all_tasks()
                    if task is not asyncio.current_task() and not task.done()]
    asyncio.run(scenario())
