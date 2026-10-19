"""Executable composition; bounded exit does not use asyncio.run cancel-all."""
import asyncio
import signal

from aiogram import Bot

from .catalog import load_catalog
from .config import load_settings
from .telegram_app import (Application, Event, FailStop, GuardedAiohttpSession,
                           ProcessSinks, Stage, bounded_tasks, emit_safe)


async def _close(session):
    task = asyncio.create_task(session.close())
    if not await bounded_tasks((task,), 2):
        raise FailStop()


async def _defer(task):
    cancelled = False
    while True:
        try:
            await asyncio.shield(task)
            break
        except asyncio.CancelledError:
            cancelled = True
            if task.done():
                if task.cancelled():
                    raise FailStop() from None
                # Retrieve the owned outcome before propagating caller cancellation.
                task.result()
                break
    if cancelled:
        raise asyncio.CancelledError()


async def run():
    guard = ProcessSinks(asyncio.get_running_loop())
    session = application = None
    result = 0
    cancelled = False
    cleanup_failed = False
    try:
        settings = load_settings()
        guard.set_level(getattr(settings, "log_level", "INFO"))
        snapshot = load_catalog(settings.catalog_path)
        session = GuardedAiohttpSession()
        bot = Bot(settings.bot_token, session=session)
        application = Application(bot, snapshot, settings.results_limit)
        application.ingress = asyncio.create_task(application.poll())
        emit_safe(Event.START, Stage.STARTUP)
        await asyncio.shield(application.ingress)
    except asyncio.CancelledError:
        cancelled = True
    except Exception:
        emit_safe(Event.FAIL, Stage.STARTUP)
        result = 1
    finally:
        try:
            if application is not None:
                await application.shutdown(session)
            elif session is not None:
                await _defer(asyncio.create_task(_close(session)))
        except asyncio.CancelledError:
            cancelled = True
        except BaseException:
            emit_safe(Event.FAIL, Stage.CLEANUP)
            cleanup_failed = True
        finally:
            guard.restore()
    if cleanup_failed:
        raise FailStop() from None
    if cancelled:
        raise asyncio.CancelledError()
    return result


def main():
    # Install before even loop construction: startup/runner diagnostics are guarded.
    guard = ProcessSinks()
    loop = None
    previous_signals = {}
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(lambda *_: emit_safe(Event.FAIL, Stage.PROCESS))
        task = loop.create_task(run())
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_signals[signum] = signal.getsignal(signum)
            loop.add_signal_handler(signum, task.cancel)
        return loop.run_until_complete(task)
    except asyncio.CancelledError:
        return 0
    except BaseException:
        emit_safe(Event.FAIL, Stage.PROCESS)
        return 1
    finally:
        if loop is not None:
            for signum, handler in previous_signals.items():
                loop.remove_signal_handler(signum)
                signal.signal(signum, handler)
            # Fail-stop: do not run an implicit unbounded cancellation join.
            loop.close()
            asyncio.set_event_loop(None)
        guard.restore()


if __name__ == "__main__":
    raise SystemExit(main())
