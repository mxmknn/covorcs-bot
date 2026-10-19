"""Offline EDGE behavior and fault oracles (generator checks, not certification)."""
import asyncio
import json

import pytest
from aiogram import Bot
from aiogram.methods import GetUpdates, SendMessage

from coworking_nearby import telegram_app as app


TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"


def raw_update(uid=100, chat=1, **fields):
    return {"update_id": uid, "message": {"message_id": uid, "date": 0,
            "chat": {"id": chat, "type": "private"}, **fields}}


def test_sdk_guard_raw_status_edges():
    session = app.GuardedAiohttpSession()
    bot = Bot(TOKEN, session=session)
    method = SendMessage(chat_id=1, text="test")
    for wait in (0, 1, 15):
        with pytest.raises(app.FloodRefusal) as caught:
            session.check_response(bot, method, 429, json.dumps({"ok": False,
                "error_code": 429, "parameters": {"retry_after": wait}}))
        assert caught.value.wait == wait
    for status, body in [(500, {"ok": False, "parameters": {"retry_after": 1}}),
                         (429, {"ok": True}), (429, {"ok": False, "error_code": 429,
                            "parameters": {"retry_after": True}})]:
        with pytest.raises(app.DeliveryStop):
            session.check_response(bot, method, status, json.dumps(body))


@pytest.mark.parametrize("bad", [True, "55.1", None, 91, float("inf"), 10**400])
def test_raw_origin_before_sdk(bad):
    session = app.GuardedAiohttpSession()
    bot = Bot(TOKEN, session=session)
    result = session.check_response(bot, GetUpdates(), 200, json.dumps({"ok": True,
        "result": [raw_update(location={"latitude": bad, "longitude": 37})]})).result
    envelope = app.envelope_from_update(result[0])
    assert envelope.kind == app.Kind.INVALID
    assert envelope.origin is None


def test_venue_preferred_and_unselected_malformed_sanitized():
    session = app.GuardedAiohttpSession()
    bot = Bot(TOKEN, session=session)
    update = raw_update(location={"latitude": True, "longitude": 0},
        venue={"title": "test", "address": "test", "location": {"latitude": 55, "longitude": 37}})
    update[app.ORIGIN_MARKER] = True
    actual = session.check_response(bot, GetUpdates(), 200,
        json.dumps({"ok": True, "result": [update]})).result[0]
    envelope = app.envelope_from_update(actual)
    assert envelope.kind == app.Kind.LOCATION
    assert envelope.origin.latitude == 55


def test_worker_death_queued_successor_fifo():
    async def scenario():
        entered = asyncio.Queue()
        barriers = {i: asyncio.Event() for i in range(100, 104)}
        async def service(envelope):
            await entered.put(envelope.source_id)
            await barriers[envelope.source_id].wait()
        scheduler = app.Scheduler(service)
        for uid, chat in [(100, 1), (101, 1), (102, 1), (103, 2)]:
            await scheduler.admit(app.Envelope(chat, uid, app.Kind.START), uid)
        assert (scheduler.pending, scheduler.counts, scheduler.cursor) == (4, {1: 3, 2: 1}, 104)
        assert {await entered.get(), await entered.get()} == {100, 103}
        old = scheduler.workers[1]
        old.cancel()
        await asyncio.gather(old, return_exceptions=True)
        assert await entered.get() == 101
        assert scheduler.workers[1] is not old
        assert (scheduler.pending, scheduler.counts, scheduler.cursor) == (3, {1: 2, 2: 1}, 104)
        barriers[103].set()
        await scheduler.wait_chat(2)
        assert (scheduler.pending, scheduler.counts) == (2, {1: 2})
        barriers[101].set()
        assert await entered.get() == 102
        assert (scheduler.pending, scheduler.counts) == (1, {1: 1})
        barriers[102].set()
        await scheduler.drain()
        assert scheduler.pending == 0
        assert not scheduler.workers and not scheduler.queues
    asyncio.run(scenario())


class ManualClock:
    """One loop.time basis, explicit advancement; sleeping tasks never advance it."""
    def __init__(self, loop):
        self.now = 0.0
        self.loop = loop
        self.original = loop.time
        self.original_resolution = loop._clock_resolution
        # Virtual time has nanosecond precision independent of host clock.
        # Docker reports 1ms; asyncio otherwise dispatches timers 1ms early.
        loop._clock_resolution = 1e-9
        loop.time = lambda: self.now

    async def pump(self, turns=30):
        for _ in range(turns):
            await asyncio.sleep(0)

    async def advance(self, delta):
        self.now += delta
        await self.pump()

    def restore(self):
        self.loop.time = self.original
        self.loop._clock_resolution = self.original_resolution


def test_finite_delivery_faults(synthetic_record):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        class Sender:
            def __init__(self, outcomes):
                self.outcomes = iter(outcomes)
                self.attempts = []
            async def send_message(self, **kwargs):
                self.attempts.append((clock.now, kwargs))
                outcome = next(self.outcomes, None)
                if outcome is not None:
                    raise outcome
        try:
            for outcomes, count in [([app.FloodRefusal(0), None, None], 3),
                                     ([app.FloodRefusal(0), app.FloodRefusal(0)], 2),
                                     ([RuntimeError("ambiguous")], 1),
                                     ([app.FloodRefusal(16)], 1)]:
                sender = Sender(outcomes)
                service = app.RequestService(sender, (synthetic_record,), 1)
                task = asyncio.create_task(service(app.Envelope(1, 77, app.Kind.LOCATION,
                    app.validate_origin(0, 0))))
                await clock.pump()
                assert not sender.attempts
                for _ in range(5):
                    await clock.advance(1.1)
                assert task.done()
                await task
                assert len(sender.attempts) == count
                for (_, kwargs) in sender.attempts:
                    assert kwargs["reply_parameters"].message_id == 77
                    assert kwargs["reply_parameters"].allow_sending_without_reply is False
                    assert kwargs["request_timeout"] == 10
                assert all(b[0] - a[0] >= 1.1 - 1e-9
                           for a, b in zip(sender.attempts, sender.attempts[1:]))
        finally:
            clock.restore()
    asyncio.run(scenario())


class RecordingTransport(asyncio.Transport):
    """Wire seam below the real connector/pool/request/writer/parser stack."""
    def __init__(self, protocol, wire):
        self.protocol, self.wire = protocol, wire
        self.buffered = bytearray()
        self.closing = False
        self.partial_recorded = False

    def get_extra_info(self, name, default=None):
        return default

    def is_closing(self):
        return self.closing

    def get_write_buffer_size(self):
        return 0

    def pause_reading(self):
        pass

    def resume_reading(self):
        pass

    def close(self):
        if not self.closing:
            self.closing = True
            asyncio.get_running_loop().call_soon(self.protocol.connection_lost, None)

    def abort(self):
        self.close()

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def write(self, data):
        self.buffered.extend(data)
        if b"\r\n\r\n" not in self.buffered:
            return
        header, body = bytes(self.buffered).split(b"\r\n\r\n", 1)
        lines = header.split(b"\r\n")
        headers = dict(line.lower().split(b":", 1) for line in lines[1:])
        length = int(headers.get(b"content-length", b"0").strip())
        mode = self.wire.responses[0] if self.wire.responses else None
        if mode == "partial" and not self.partial_recorded:
            self.partial_recorded = True
            self.wire.responses.popleft()
            self.wire.requests.append((lines[0], headers, body[:max(0, length // 2)], False, self))
            self.close()
            return
        if len(body) < length:
            return
        self.wire.requests.append((lines[0], headers, body[:length], True, self))
        self.buffered = bytearray(body[length:])
        response = self.wire.responses.popleft()
        if response == "disconnect":
            self.close()
        elif response == "timeout":
            pass
        elif response == "short":
            loop = asyncio.get_running_loop()
            loop.call_soon(self.protocol.data_received,
                           b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\n{}")
            loop.call_soon(self.close)
        else:
            asyncio.get_running_loop().call_soon(self.protocol.data_received, response)


class Wire:
    def __init__(self, responses):
        from collections import deque
        self.responses = deque(responses)
        self.requests = []
        self.created = []

    def install(self, monkeypatch):
        from aiohttp import TCPConnector
        from aiohttp.client_proto import ResponseHandler
        async def create(connector, req, traces, timeout):
            protocol = ResponseHandler(asyncio.get_running_loop())
            transport = RecordingTransport(protocol, self)
            self.created.append(transport)
            protocol.connection_made(transport)
            return protocol
        monkeypatch.setattr(TCPConnector, "_create_connection", create)


def http_response(body=b'{"ok":true,"result":{"message_id":1,"date":0,"chat":{"id":1,"type":"private"}}}',
                  status=200, headers=b""):
    return (f"HTTP/1.1 {status} Test\r\nContent-Length: {len(body)}\r\n".encode()
            + headers + b"\r\n" + body)


@pytest.mark.parametrize("status", [307, 308])
def test_transitive_transport_redirect_guard(monkeypatch, status):
    from aiohttp import ClientSession
    async def scenario():
        redirect = http_response(b"{}", status, b"Location: /redirected\r\n")
        wire = Wire([redirect, http_response()])
        wire.install(monkeypatch)
        async with ClientSession() as raw:
            async with raw.post("http://offline.invalid/send", data=b"same-body") as response:
                assert response.status == 200
                await response.read()
        assert len(wire.requests) == 2
        assert [r[0].split()[0] for r in wire.requests] == [b"POST", b"POST"]
        assert wire.requests[0][2] == wire.requests[1][2] == b"same-body"
        wire = Wire([redirect, http_response()])
        wire.install(monkeypatch)
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        try:
            with pytest.raises(app.DeliveryStop):
                await bot.send_message(chat_id=1, text="test")
            assert len(wire.requests) == 1
            assert wire.requests[0][0].split()[0] == b"POST"
            assert session._session is not None
        finally:
            await session.close()
    asyncio.run(scenario())


@pytest.mark.parametrize("mode", ["disconnect", "partial", "short", "utf8", "json", "5xx"])
@pytest.mark.parametrize("pooled", [False, True])
def test_transitive_transport_no_replay(monkeypatch, mode, pooled):
    async def scenario():
        bodies = {"utf8": http_response(b"\xff"), "json": http_response(b"{"),
                  "5xx": http_response(b'{"ok":false,"error_code":500,"parameters":{"retry_after":1}}', 500)}
        fault = bodies.get(mode, mode)
        wire = Wire(([http_response()] if pooled else []) + [fault, http_response()])
        wire.install(monkeypatch)
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        try:
            if pooled:
                result = await bot.send_message(chat_id=1, text="warm pool")
                assert result.message_id == 1
            with pytest.raises(Exception):
                await bot.send_message(chat_id=1, text="fault")
            assert len(wire.requests) == 1 + int(pooled)
            if pooled:
                assert wire.requests[0][4] is wire.requests[1][4]
            assert all(r[0].split()[0] == b"POST" for r in wire.requests)
        finally:
            await session.close()
    asyncio.run(scenario())


def test_transport_GET_disconnect_positive_control(monkeypatch):
    from aiohttp import ClientSession
    async def scenario():
        wire = Wire(["disconnect", http_response(b"ok")])
        wire.install(monkeypatch)
        async with ClientSession() as raw:
            async with raw.get("http://offline.invalid/control") as response:
                assert await response.text() == "ok"
        assert len(wire.requests) == 2
        assert all(r[0].split()[0] == b"GET" for r in wire.requests)
    asyncio.run(scenario())


def test_supervisor_death_before_worker_first_step():
    async def scenario():
        calls = []
        async def service(envelope):
            calls.append(envelope.source_id)
        scheduler = app.Scheduler(service)
        await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        scheduler.workers[1].cancel()  # coroutine has not entered its try/finally
        for _ in range(20):
            await asyncio.sleep(0)
        assert calls == [100]
        assert scheduler.pending == 0 and not scheduler.workers
    asyncio.run(scenario())


def test_admission_worker_creation_rollback(monkeypatch):
    async def scenario():
        calls = []
        async def service(envelope):
            calls.append(envelope.source_id)
        scheduler = app.Scheduler(service)
        original = asyncio.create_task
        captured = []
        def reject(coroutine):
            captured.append(coroutine)
            raise RuntimeError("task creation rejected")
        monkeypatch.setattr(asyncio, "create_task", reject)
        with pytest.raises(RuntimeError):
            await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        assert (scheduler.pending, scheduler.counts, scheduler.cursor) == (0, {}, None)
        assert not scheduler.queues and not scheduler.workers
        assert captured[0].cr_frame is None
        monkeypatch.setattr(asyncio, "create_task", original)
        await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        await scheduler.drain()
        assert calls == [100] and scheduler.cursor == 101
    asyncio.run(scenario())


@pytest.mark.parametrize("global_full", [False, True])
def test_admission_cancel_capacity_full(global_full):
    async def scenario():
        gate = asyncio.Event()
        async def service(envelope):
            await gate.wait()
        scheduler = app.Scheduler(service, global_limit=1 if global_full else 64, chat_limit=1)
        await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        chat = 2 if global_full else 1
        blocked = asyncio.create_task(scheduler.admit(app.Envelope(chat, 101, app.Kind.START), 101))
        await asyncio.sleep(0)
        blocked.cancel()
        await asyncio.gather(blocked, return_exceptions=True)
        assert (scheduler.pending, scheduler.counts, scheduler.cursor) == (1, {1: 1}, 101)
        gate.set()
        await scheduler.drain()
    asyncio.run(scenario())


def test_admission_commit_feed_return_cursor():
    from aiogram.types import Update
    async def scenario():
        bot = Bot(TOKEN)
        application = app.Application(bot, (), 3)
        entered, finish, postcommit = asyncio.Event(), asyncio.Event(), asyncio.Event()
        async def service(envelope):
            entered.set()
            await finish.wait()
        application.scheduler.service = service
        original = application.scheduler.admit
        async def admit(envelope, uid):
            await original(envelope, uid)
            postcommit.set()
            await asyncio.Event().wait()
        application.scheduler.admit = admit
        update = Update.model_validate(raw_update(text="/start"))
        task = asyncio.create_task(application.dispatcher.feed_update(bot, update))
        await postcommit.wait()
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        assert (application.scheduler.pending, application.scheduler.cursor) == (1, 101)
        await entered.wait()
        finish.set()
        await application.scheduler.drain()
        await bot.session.close()
    asyncio.run(scenario())


@pytest.mark.parametrize("fault", ["request_finally", "notification", "successor"])
def test_worker_finally_exception(monkeypatch, fault):
    async def scenario():
        entered = asyncio.Queue()
        gate = asyncio.Event()
        async def service(envelope):
            entered.put_nowait(envelope.source_id)
            await gate.wait()
        scheduler = app.Scheduler(service)
        await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        await scheduler.admit(app.Envelope(1, 101, app.Kind.START), 101)
        assert await entered.get() == 100
        def reject(*args):
            raise RuntimeError("injected finalizer fault")
        if fault == "request_finally":
            monkeypatch.setattr(scheduler, "_request_finally", reject)
        elif fault == "notification":
            monkeypatch.setattr(scheduler, "_notify", reject)
        else:
            rejected_coroutines = []
            def reject_task(coroutine):
                rejected_coroutines.append(coroutine)
                raise RuntimeError("successor task creation failure")
            monkeypatch.setattr(asyncio, "create_task", reject_task)
        old = scheduler.workers[1]
        old.cancel()
        await asyncio.gather(old, return_exceptions=True)
        assert scheduler.pending == 1 and scheduler.counts == {1: 1}
        if fault == "successor":
            assert scheduler.failed.is_set()
            assert len(scheduler.queues[1]) == 1
            assert not scheduler.workers
            assert len(rejected_coroutines) == 1 and rejected_coroutines[0].cr_frame is None
            scheduler.stopping = True
            scheduler.discard_queued()
        else:
            assert await entered.get() == 101
            successor = scheduler.workers[1]
            old.cancel()
            assert scheduler.workers[1] is successor
            gate.set()
            await asyncio.gather(successor, return_exceptions=True)
        assert scheduler.pending == 0 and not scheduler.counts and not scheduler.workers
    asyncio.run(scenario())


def test_manual_before_start_live_venue_help_group_edited():
    async def scenario():
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        other_bot = Bot("987654321:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk")
        application = app.Application(other_bot, (), 3)
        envelopes = []
        async def service(envelope):
            envelopes.append(envelope)
        application.scheduler.service = service
        variants = [raw_update(100, location={"latitude": 55, "longitude": 37, "live_period": 60}),
                    raw_update(101, text="/start"), raw_update(102, text="/help"),
                    raw_update(103, text="ordinary"), raw_update(104, location={"latitude": "55", "longitude": 37}),
                    raw_update(105, venue={"title": "x", "address": "x",
                        "location": {"latitude": -10, "longitude": -20}},
                        location={"latitude": False, "longitude": 0})]
        group = raw_update(106, location={"latitude": 55, "longitude": 37})
        group["message"]["chat"]["type"] = "group"
        variants.append(group)
        edited = raw_update(107, location={"latitude": 56, "longitude": 38})
        edited["edited_message"] = edited.pop("message")
        variants.append(edited)
        for raw in variants:
            update = session.check_response(bot, GetUpdates(), 200,
                json.dumps({"ok": True, "result": [raw]})).result[0]
            await application.dispatcher.feed_update(other_bot, update)
        await application.scheduler.drain()
        assert [e.kind for e in envelopes] == [app.Kind.LOCATION, app.Kind.START, app.Kind.HELP,
            app.Kind.FALLBACK, app.Kind.INVALID, app.Kind.LOCATION, app.Kind.GROUP]
        assert envelopes[4].origin is None
        assert envelopes[5].origin.latitude == -10
        assert application.scheduler.cursor == 108
        assert len(application.dispatcher.update.handlers) == 1
        await session.close()
        await other_bot.session.close()
    asyncio.run(scenario())


def test_worker_death_partial_send_no_replay(synthetic_record):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        attempts, confirmed = [], []
        blocked = asyncio.Event()
        finish_b = asyncio.Event()
        class Sender:
            async def send_message(self, **kwargs):
                source = kwargs["reply_parameters"].message_id
                attempts.append((source, kwargs["text"]))
                if source == 100 and sum(s == 100 for s, _ in attempts) == 3:
                    blocked.set()
                    await asyncio.Event().wait()
                if source == 103 and sum(s == 103 for s, _ in attempts) == 3:
                    await finish_b.wait()
                confirmed.append((source, kwargs["text"]))
        # Use the public value type; no domain edits are part of EDGE.
        from dataclasses import replace
        records = (synthetic_record, replace(synthetic_record, id="synthetic-002", latitude=1))
        scheduler = app.Scheduler(app.RequestService(Sender(), records, 2))
        try:
            for uid, chat in [(100, 1), (101, 1), (102, 1), (103, 2)]:
                await scheduler.admit(app.Envelope(chat, uid, app.Kind.LOCATION,
                    app.validate_origin(0, 0)), uid)
            await clock.pump()
            for _ in range(3):
                await clock.advance(1.1)
            assert blocked.is_set()
            assert sum(s == 100 for s, _ in confirmed) == 2
            assert (scheduler.pending, scheduler.counts, scheduler.cursor) == (4, {1: 3, 2: 1}, 104)
            old = scheduler.workers[1]
            old.cancel()
            await clock.pump()
            assert (scheduler.pending, scheduler.counts, scheduler.cursor) == (3, {1: 2, 2: 1}, 104)
            assert scheduler.cursor == 104 and scheduler.workers[1] is not old
            successor = scheduler.workers[1]
            old.cancel()
            assert scheduler.workers[1] is successor
            finish_b.set()
            await clock.pump()
            assert (scheduler.pending, scheduler.counts) == (2, {1: 2})
            for _ in range(3):
                await clock.advance(1.1)
            assert (scheduler.pending, scheduler.counts) == (1, {1: 1})
            for _ in range(3):
                await clock.advance(1.1)
            await scheduler.drain()
            assert sum(s == 100 for s, _ in attempts) == 3
            assert [s for s, _ in attempts if s in (101, 102)] == [101] * 3 + [102] * 3
            assert scheduler.pending == 0
        finally:
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("stage", ["ingress", "drain", "worker", "close"])
def test_shutdown_stage_deadlines_outer_finally(stage):
    async def scenario():
        loop = asyncio.get_running_loop()
        clock = ManualClock(loop)
        gate = asyncio.Event()
        milestones = []
        application = app.Application(Bot(TOKEN), (), 3)
        async def stubborn(label):
            milestones.append((label, clock.now))
            while not gate.is_set():
                try:
                    await gate.wait()
                except asyncio.CancelledError:
                    pass
        class Session:
            async def close(self):
                milestones.append(("close", clock.now))
                if stage == "close":
                    await stubborn("close-wait")
        async def service(envelope):
            await stubborn("service")
        application.scheduler.service = service
        if stage in ("drain", "worker"):
            await application.scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        if stage == "ingress":
            application.ingress = asyncio.create_task(stubborn("ingress"))
        await clock.pump()
        cleanup = asyncio.create_task(application.shutdown(Session()))
        try:
            await clock.pump()
            # Repeated caller cancellations must leave a single coordinator.
            coordinator = application.cleanup_task
            cleanup.cancel()
            await clock.pump()
            cleanup.cancel()
            await clock.pump()
            assert application.cleanup_task is coordinator and not coordinator.cancelled()
            if stage == "ingress":
                await clock.advance(2 - .001)
                assert not any(label == "close" for label, _ in milestones)
                await clock.advance(.001)
                assert ("close", 2.0) in milestones
            elif stage in ("drain", "worker"):
                await clock.advance(10 - .001)
                assert not any(label == "close" for label, _ in milestones)
                await clock.advance(.001)
                assert not any(label == "close" for label, _ in milestones)
                await clock.advance(2)
                assert ("close", 12.0) in milestones
            else:
                await clock.advance(2 - .001)
                assert not coordinator.done()
                await clock.advance(.001)
            await clock.pump()
            assert coordinator.done()
            assert isinstance(coordinator.exception(), app.FailStop)
            assert cleanup.done()
            await asyncio.gather(cleanup, return_exceptions=True)
        finally:
            # Noncooperative barriers are our test's resources, released AFTER
            # bounded fail-stop observation. No zero-leak claim while blocked.
            gate.set()
            await clock.pump()
            for task in tuple(asyncio.all_tasks()):
                if task is not asyncio.current_task() and not task.done():
                    task.cancel()
            await clock.pump()
            clock.restore()
            await application.bot.session.close()
    asyncio.run(scenario())


def test_shutdown_full_16_second_milestones():
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        gate = asyncio.Event()
        application = app.Application(Bot(TOKEN), (), 3)
        stages = []
        async def stubborn():
            while not gate.is_set():
                try:
                    await gate.wait()
                except asyncio.CancelledError:
                    pass
        async def service(envelope):
            await stubborn()
        class Session:
            async def close(self):
                stages.append(("close", clock.now))
                await stubborn()
        application.scheduler.service = service
        await application.scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        application.ingress = asyncio.create_task(stubborn())
        await clock.pump()
        cleanup = asyncio.create_task(application.shutdown(Session()))
        try:
            await clock.pump()
            for delta, milestone in [(1.999, 1.999), (.001, 2), (9.999, 11.999),
                                     (.001, 12), (1.999, 13.999), (.001, 14),
                                     (1.999, 15.999), (.001, 16)]:
                await clock.advance(delta)
                assert clock.now == pytest.approx(milestone)
                if milestone < 14:
                    assert not stages
                else:
                    assert stages[0][0] == "close"
                    assert stages[0][1] == pytest.approx(14)
                if milestone < 16:
                    assert not cleanup.done()
                cleanup.cancel()
                await clock.pump()
            assert cleanup.done()
            assert isinstance((await asyncio.gather(cleanup, return_exceptions=True))[0], app.FailStop)
        finally:
            gate.set()
            await clock.pump()
            assert application.scheduler.pending == 0
            clock.restore()
            await application.bot.session.close()
    asyncio.run(scenario())


def test_ordered_ingress_barrier_fifo_cleanup_race():
    async def scenario():
        gate = asyncio.Event()
        entered = []
        async def service(envelope):
            entered.append(envelope.source_id)
            await gate.wait()
        scheduler = app.Scheduler(service)
        uid = 100
        for chat in range(8):
            for _ in range(8):
                await scheduler.admit(app.Envelope(chat, uid, app.Kind.START), uid)
                uid += 1
        assert scheduler.pending == 64 and scheduler.counts == dict.fromkeys(range(8), 8)
        assert scheduler.cursor == 164
        blocked = asyncio.create_task(scheduler.admit(app.Envelope(9, 164, app.Kind.START), 164))
        for _ in range(10):
            await asyncio.sleep(0)
        assert not blocked.done() and scheduler.cursor == 164
        assert len(entered) == 8  # cross-chat service is concurrent
        gate.set()
        await blocked
        await scheduler.drain()
        assert scheduler.pending == 0 and scheduler.cursor == 165
        assert not scheduler.queues and not scheduler.workers
        # Admission immediately after idle retirement cannot be removed by old finally.
        await scheduler.admit(app.Envelope(0, 165, app.Kind.HELP), 165)
        await scheduler.drain()
        assert entered[-1] == 165 and scheduler.pending == 0
    asyncio.run(scenario())


def test_poll_uses_committed_cursor_after_feed_return_cancel():
    from aiogram.types import Update
    async def scenario():
        bot = Bot(TOKEN)
        application = app.Application(bot, (), 3)
        offsets, envelope_ids = [], []
        gate = asyncio.Event()
        async def get_updates(**kwargs):
            offsets.append(kwargs)
            if len(offsets) == 1:
                return [Update.model_validate(raw_update(text="/start"))]
            gate.set()
            await asyncio.Event().wait()
        bot.get_updates = get_updates
        async def service(envelope):
            envelope_ids.append(envelope.source_id)
        application.scheduler.service = service
        original = application.dispatcher.feed_update
        async def feed(*args):
            await original(*args)
            raise asyncio.CancelledError()
        application.dispatcher.feed_update = feed
        first = asyncio.create_task(application.poll())
        await asyncio.gather(first, return_exceptions=True)
        application.dispatcher.feed_update = original
        second = asyncio.create_task(application.poll())
        await gate.wait()
        second.cancel()
        await asyncio.gather(second, return_exceptions=True)
        await application.scheduler.drain()
        assert envelope_ids == [100]
        assert [k["offset"] for k in offsets] == [None, 101]
        assert all(k["limit"] == 1 and k["allowed_updates"] == ["message", "edited_message", "callback_query"] for k in offsets)
        await bot.session.close()
    asyncio.run(scenario())


@pytest.mark.parametrize("kind", list(app.Kind))
def test_every_outbound_source_bound(kind, synthetic_record):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        attempts = []
        class Sender:
            async def send_message(self, **kwargs):
                attempts.append(kwargs)
        try:
            service = app.RequestService(Sender(), (synthetic_record,), 1)
            task = asyncio.create_task(service(app.Envelope(1, 99, kind,
                app.validate_origin(0, 0) if kind == app.Kind.LOCATION else None)))
            await clock.pump()
            await clock.advance(1.1)
            await clock.advance(1.1)
            await task
            assert attempts
            assert all(k["reply_parameters"].message_id == 99 and
                       k["reply_parameters"].allow_sending_without_reply is False for k in attempts)
            if kind in (app.Kind.START, app.Kind.HELP, app.Kind.FALLBACK, app.Kind.INVALID):
                assert attempts[0]["reply_markup"].keyboard[0][0].request_location is True
        finally:
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("fault", ["disconnect", "partial", "short", "utf8", "json", "5xx", "timeout"])
def test_real_transport_fault_stops_next_card(monkeypatch, synthetic_record, fault):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        bodies = {"utf8": http_response(b"\xff"), "json": http_response(b"{"),
                  "5xx": http_response(b'{"ok":false,"parameters":{"retry_after":1}}', 500)}
        wire = Wire([http_response(), bodies.get(fault, fault), http_response()])
        wire.install(monkeypatch)
        from dataclasses import replace
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        service = app.RequestService(bot, (synthetic_record, replace(synthetic_record, id="s2")), 2)
        try:
            task = asyncio.create_task(service(app.Envelope(1, 100, app.Kind.LOCATION,
                app.validate_origin(0, 0))))
            await clock.pump()
            await clock.advance(1.1)
            assert len(wire.requests) == 1
            await clock.advance(1.1)
            assert len(wire.requests) == 2
            if fault == "timeout":
                await clock.advance(9.999)
                assert not task.done()
                await clock.advance(.001)
            await clock.pump()
            assert task.done()
            await task
            assert len(wire.requests) == 2
            close = asyncio.create_task(session.close())
            await clock.pump()
            await clock.advance(.25)
            await close
        finally:
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("wait", [0, 5, 15, 16])
def test_full_retry_wait_budget_and_confirmed_prefix(wait, synthetic_record):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        attempts = []
        class Sender:
            async def send_message(self, **kwargs):
                attempts.append((clock.now, kwargs["text"]))
                if len(attempts) == 2:
                    raise app.FloodRefusal(wait)
        try:
            task = asyncio.create_task(app.RequestService(Sender(), (synthetic_record,), 1)(
                app.Envelope(1, 99, app.Kind.LOCATION, app.validate_origin(0, 0))))
            await clock.pump()
            await clock.advance(1.1)
            await clock.advance(1.1)
            assert len(attempts) == 2
            if wait <= 15:
                await clock.advance(wait)
                assert len(attempts) == 2
                await clock.advance(1.099)
                assert len(attempts) == 2
                await clock.advance((attempts[1][0] + wait + app.PAUSE) - clock.now)
                assert len(attempts) == 3
                assert attempts[1][1] == attempts[2][1]
                assert attempts[0][1] != attempts[1][1]
            else:
                assert task.done()
            await task
        finally:
            clock.restore()
    asyncio.run(scenario())


def test_retry_budget_shared_across_current_messages(synthetic_record):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        attempts = []
        class Sender:
            async def send_message(self, **kwargs):
                attempts.append(clock.now)
                if len(attempts) in (1, 3):
                    raise app.FloodRefusal(10)
        try:
            task = asyncio.create_task(app.RequestService(Sender(), (synthetic_record,), 1)(
                app.Envelope(1, 99, app.Kind.LOCATION, app.validate_origin(0, 0))))
            await clock.pump()
            await clock.advance(1.1)
            await clock.advance(10)
            await clock.advance(1.1)
            await clock.advance(1.1)
            assert task.done() and len(attempts) == 3
            await task
        finally:
            clock.restore()
    asyncio.run(scenario())


def test_deadline_refuses_partial_retry_wait_and_rechecks_pause():
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        attempts = []
        class Sender:
            async def send_message(self, **kwargs):
                attempts.append(clock.now)
                # Force a late explicit refusal without spending real wall time.
                clock.now = 80
                raise app.FloodRefusal(0)
        try:
            task = asyncio.create_task(app.RequestService(Sender(), (), 1)(
                app.Envelope(1, 99, app.Kind.START)))
            await clock.pump()
            await clock.advance(1.1)
            assert task.done() and len(attempts) == 1
            await task
            attempts.clear()
            task = asyncio.create_task(app.RequestService(Sender(), (), 1)(
                app.Envelope(1, 99, app.Kind.START)))
            await clock.pump()
            await clock.advance(81)
            assert task.done() and not attempts  # pause overslept; full 10s no longer fit
            await task
        finally:
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("error_kind", ["typed429", "403", "deleted", "invalid_url", "decode", "network"])
def test_sender_rejections_stop_and_healthy_chat_continues(error_kind, synthetic_record):
    from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramNetworkError, TelegramRetryAfter
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        method = SendMessage(chat_id=1, text="never log this")
        errors = {"typed429": TelegramRetryAfter(method=method, message="typed outside guard", retry_after=0),
                  "403": TelegramForbiddenError(method=method, message="forbidden"),
                  "deleted": TelegramBadRequest(method=method, message="reply message not found"),
                  "invalid_url": TelegramBadRequest(method=method, message="invalid URL"),
                  "decode": UnicodeDecodeError("utf8", b"\xff", 0, 1, "invalid"),
                  "network": TelegramNetworkError(method=method, message="ambiguous")}
        calls = []
        class Sender:
            async def send_message(self, **kwargs):
                calls.append(kwargs["chat_id"])
                if kwargs["chat_id"] == 1:
                    raise errors[error_kind]
        scheduler = app.Scheduler(app.RequestService(Sender(), (synthetic_record,), 1))
        try:
            for chat in (1, 2):
                await scheduler.admit(app.Envelope(chat, 100 + chat, app.Kind.LOCATION,
                    app.validate_origin(0, 0)), 100 + chat)
            await clock.pump()
            await clock.advance(1.1)
            await clock.advance(1.1)
            await scheduler.drain()
            assert calls.count(1) == 1 and calls.count(2) == 2
            assert scheduler.pending == 0
        finally:
            clock.restore()
    asyncio.run(scenario())


def test_session_recreation_facade_and_real_sdk_result(monkeypatch):
    async def scenario():
        wire = Wire([http_response(), http_response()])
        wire.install(monkeypatch)
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        first = await bot.send_message(chat_id=1, text="first")
        raw = session._session
        await session.close()
        second = await bot.send_message(chat_id=1, text="second")
        assert first.message_id == second.message_id == 1
        assert raw is not session._session and raw.closed
        assert len(wire.requests) == 2
        assert session._session.__class__.__name__ == "ClientSession"
        await session.close()
    asyncio.run(scenario())


@pytest.mark.parametrize("mode", ["exception", "cooperative_timeout"])
def test_session_close_exception_timeout(mode):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        application = app.Application(Bot(TOKEN), (), 3)
        calls = []
        class Session:
            async def close(self):
                calls.append(clock.now)
                if mode == "exception":
                    raise RuntimeError("private close error")
                await asyncio.Event().wait()
        try:
            task = asyncio.create_task(application.shutdown(Session()))
            await clock.pump()
            if mode == "cooperative_timeout":
                task.cancel()
                await clock.pump()
                await clock.advance(1.999)
                assert not task.done()
                task.cancel()
                await clock.pump()
                await clock.advance(.001)
            await clock.pump()
            result = (await asyncio.gather(task, return_exceptions=True))[0]
            assert isinstance(result, app.FailStop)
            assert calls == [0]
            assert not [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
        finally:
            clock.restore()
            await application.bot.session.close()
    asyncio.run(scenario())


def test_repeated_cancel_worker_finally_notification():
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        application = app.Application(Bot(TOKEN), (), 1)
        gate = asyncio.Event()
        events = []
        async def service(envelope):
            await gate.wait()
        class Session:
            async def close(self):
                events.append("close")
        application.scheduler.service = service
        await application.scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        await clock.pump()
        caller = asyncio.create_task(application.shutdown(Session()))
        try:
            await clock.pump()
            coordinator = application.cleanup_task
            for _ in range(3):
                caller.cancel()
                await clock.pump()
            await clock.advance(10)
            await clock.pump()
            assert application.cleanup_task is coordinator
            assert application.scheduler.pending == 0
            assert events == ["close"]
            result = (await asyncio.gather(caller, return_exceptions=True))[0]
            assert isinstance(result, asyncio.CancelledError)
            assert not application.scheduler.workers and not application.scheduler.queues
        finally:
            gate.set()
            clock.restore()
            await application.bot.session.close()
    asyncio.run(scenario())


def test_precommit_cancel_and_atomic_observation():
    async def scenario():
        gate = asyncio.Event()
        observed = []
        async def service(envelope):
            await gate.wait()
        scheduler = app.Scheduler(service)
        before = asyncio.Event()
        proceed = asyncio.Event()
        async def admission():
            before.set()
            await proceed.wait()
            await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        caller = asyncio.create_task(admission())
        await before.wait()
        caller.cancel()
        await asyncio.gather(caller, return_exceptions=True)
        assert (scheduler.pending, scheduler.cursor, scheduler.counts) == (0, None, {})
        def observer():
            observed.append((scheduler.pending, scheduler.cursor, dict(scheduler.counts),
                             len(scheduler.queues[1]), 1 in scheduler.workers))
        asyncio.get_running_loop().call_soon(observer)
        await scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        assert not observed
        await asyncio.sleep(0)
        assert observed == [(1, 101, {1: 1}, 1, True)]
        gate.set()
        await scheduler.drain()
    asyncio.run(scenario())


@pytest.mark.parametrize("body", [
    {"ok": True, "error_code": 429, "parameters": {"retry_after": 0}},
    {"ok": False, "error_code": "429", "parameters": {"retry_after": 0}},
    {"ok": False, "error_code": 429, "parameters": {"retry_after": -1}},
    {"ok": False, "error_code": 429, "parameters": {"retry_after": 1.0}},
    {"ok": False, "error_code": 429, "parameters": {"retry_after": "0"}},
    {"ok": False, "error_code": 429}, [], None])
def test_sdk_guard_malformed_429_never_retry(body):
    session = app.GuardedAiohttpSession()
    bot = Bot(TOKEN, session=session)
    with pytest.raises(app.DeliveryStop) as failure:
        session.check_response(bot, SendMessage(chat_id=1, text="x"), 429, json.dumps(body))
    assert type(failure.value) is app.DeliveryStop


def test_real_http_429_zero_and_middleware_replay_disabled(monkeypatch):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        flood = http_response(b'{"ok":false,"error_code":429,"parameters":{"retry_after":0}}', 429)
        wire = Wire([flood, http_response()])
        wire.install(monkeypatch)
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        facade = await session.create_session()
        middleware_calls = []
        async def hostile_retry_middleware(request, handler):
            middleware_calls.append(1)
            await handler(request)
            return await handler(request)
        session._session._middlewares = (hostile_retry_middleware,)
        try:
            task = asyncio.create_task(app.RequestService(bot, (), 1)(app.Envelope(1, 99, app.Kind.START)))
            await clock.pump()
            await clock.advance(1.1)
            assert len(wire.requests) == 1
            await clock.advance(1.1)
            await task
            assert len(wire.requests) == 2
            assert wire.requests[0][2] == wire.requests[1][2]
            assert not middleware_calls
            assert not asyncio.iscoroutinefunction(facade.post)
            close = asyncio.create_task(session.close())
            await clock.pump()
            await clock.advance(.25)
            await close
        finally:
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("text", [" ", "\n\t", "", "/other", "hello"])
def test_ordinary_private_input_always_fallback(text):
    from aiogram.types import Update
    envelope = app.envelope_from_update(Update.model_validate(raw_update(text=text)))
    assert envelope.kind == app.Kind.FALLBACK


def test_two_origins_fifo_crosschat(synthetic_record):
    from dataclasses import replace
    from urllib.parse import parse_qs, urlsplit
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        sends = []
        class Sender:
            async def send_message(self, **kwargs):
                sends.append((kwargs["chat_id"], kwargs["reply_parameters"].message_id,
                              kwargs["text"], kwargs["reply_markup"]))
        scheduler = app.Scheduler(app.RequestService(Sender(), (synthetic_record,
            replace(synthetic_record, id="s2", name="OTHER", latitude=50, longitude=30)), 1))
        try:
            for uid, chat, lat, lon in [(100, 1, 0, 0), (101, 1, 50, 30), (102, 2, -1, -2)]:
                await scheduler.admit(app.Envelope(chat, uid, app.Kind.LOCATION,
                    app.validate_origin(lat, lon)), uid)
            await clock.pump()
            for _ in range(4):
                await clock.advance(1.1)
            await scheduler.drain()
            assert [s[1] for s in sends if s[0] == 1] == [100, 100, 101, 101]
            cards = {uid: (text, markup) for _, uid, text, markup in sends if markup is not None}
            assert "SYNTHETIC" in cards[100][0] and "OTHER" in cards[101][0]
            for uid, origin in [(100, "0,0"), (101, "50,30"), (102, "-1,-2")]:
                keyboard = cards[uid][1]
                for row in keyboard.inline_keyboard:
                    for button in row:
                        route = parse_qs(urlsplit(button.url).query)["rtext"][0]
                        assert route.split("~")[0] == origin
            assert scheduler.pending == 0 and scheduler.cursor == 103
        finally:
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("count", [0, 1, 2])
def test_empty_one_two_inactive(count, synthetic_record):
    from dataclasses import replace
    snapshot = tuple(replace(synthetic_record, id=f"s{i}") for i in range(count))
    snapshot += (replace(synthetic_record, id="inactive", active=False),)
    service = app.RequestService(None, snapshot, 3)
    messages = list(service.messages(app.Envelope(1, 100, app.Kind.LOCATION,
        app.validate_origin(0, 0))))
    assert len(messages) == (count + 1 if count else 1)
    assert messages[0][0] == (app.render.INTRO_TEXT if count else app.render.EMPTY_TEXT)


@pytest.mark.parametrize("terminal", ["success", "error", "cancel"])
def test_cooperative_cleanup_terminal_counters_offsets(terminal):
    async def scenario():
        initial = asyncio.all_tasks()
        application = app.Application(Bot(TOKEN), (), 3)
        entered = asyncio.Event()
        async def service(envelope):
            entered.set()
            if terminal == "error":
                raise RuntimeError("contained")
            if terminal == "cancel":
                await asyncio.Event().wait()
        class Session:
            async def close(self):
                pass
        application.scheduler.service = service
        await application.scheduler.admit(app.Envelope(1, 100, app.Kind.START), 100)
        await entered.wait()
        if terminal == "cancel":
            worker = application.scheduler.workers[1]
            worker.cancel()
            await asyncio.gather(worker, return_exceptions=True)
        else:
            await application.scheduler.drain()
        await application.shutdown(Session())
        await asyncio.sleep(0)
        assert not application.scheduler.queues and not application.scheduler.workers
        assert application.scheduler.pending == 0 and application.scheduler.counts == {}
        assert application.scheduler.cursor == 101
        assert not [t for t in asyncio.all_tasks() - initial if not t.done()]
        await application.bot.session.close()
    asyncio.run(scenario())


def test_url_acceptance_boundary(monkeypatch, synthetic_record):
    from dataclasses import replace
    from urllib.parse import parse_qs
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        url = "https://yandex.ru/maps/?data=" + "a" * 10000
        wire = Wire([http_response(), http_response(b'{"ok":false,"description":"invalid URL"}', 400)])
        wire.install(monkeypatch)
        session = app.GuardedAiohttpSession()
        bot = Bot(TOKEN, session=session)
        try:
            task = asyncio.create_task(app.RequestService(bot,
                (replace(synthetic_record, yandex_maps_url=url),), 1)(
                    app.Envelope(1, 100, app.Kind.LOCATION, app.validate_origin(0, 0))))
            await clock.pump()
            await clock.advance(1.1)
            await clock.advance(1.1)
            await task
            assert len(wire.requests) == 2
            encoded = parse_qs(wire.requests[1][2].decode())
            markup = json.loads(encoded["reply_markup"][0])
            assert markup["inline_keyboard"][-1][0]["url"] == url
            # A fabricated refusal establishes controlled containment only;
            # no live platform universal-URL acceptance is asserted.
            close = asyncio.create_task(session.close())
            await clock.pump()
            await clock.advance(.25)
            await close
        finally:
            clock.restore()
    asyncio.run(scenario())


def test_shutdown_earlier_stage_exception_still_closes():
    async def scenario():
        application = app.Application(Bot(TOKEN), (), 1)
        calls = []
        async def rejected_drain():
            calls.append("drain")
            raise RuntimeError("private stage failure")
        class Session:
            async def close(self):
                calls.append("close")
        application.scheduler.drain = rejected_drain
        with pytest.raises(app.FailStop):
            await application.shutdown(Session())
        assert calls == ["drain", "close"]
        await application.bot.session.close()
    asyncio.run(scenario())


@pytest.mark.parametrize("variant", ["chosen", "nonselected", "venue"])
def test_raw_location_array_metadata_stops(variant):
    session = app.GuardedAiohttpSession()
    bot = Bot(TOKEN, session=session)
    fields = {"location": []}
    if variant != "chosen":
        fields["venue"] = {"title": "test", "address": "test", "location":
            [] if variant == "venue" else {"latitude": 55, "longitude": 37}}
    with pytest.raises(app.DeliveryStop):
        session.check_response(bot, GetUpdates(), 200,
            json.dumps({"ok": True, "result": [raw_update(**fields)]}))


def test_queue_wait_measured_separately_from_service_deadline(monkeypatch):
    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        events, sends = [], []
        barrier = asyncio.Event()
        class Sender:
            async def send_message(self, **kwargs):
                sends.append(clock.now)
                await asyncio.Event().wait()
        service = app.RequestService(Sender(), (), 3)
        async def work(envelope):
            if envelope.source_id == 1:
                await barrier.wait()
            else:
                await service(envelope)
        monkeypatch.setattr(app, "emit_safe", lambda *args, **kw: events.append((args, kw)))
        scheduler = app.Scheduler(work)
        try:
            await scheduler.admit(app.Envelope(1, 1, app.Kind.START), 1)
            await scheduler.admit(app.Envelope(1, 2, app.Kind.START), 2)
            await clock.pump()
            await clock.advance(120)
            barrier.set()
            await clock.pump()
            measurements = [kw["wait_ms"] for args, kw in events if args[0] == app.Event.QUEUE]
            assert measurements == [0, 120000]
            assert scheduler.pending == 1  # queue delay did not consume service budget
            await clock.advance(1.1)
            assert sends == [pytest.approx(121.1)]
            await clock.advance(10)
            assert scheduler.pending == 0
            assert not scheduler.queues and not scheduler.workers
        finally:
            for task in tuple(scheduler.workers.values()):
                task.cancel()
            await clock.pump()
            clock.restore()
    asyncio.run(scenario())


@pytest.mark.parametrize("flood", [False, True])
def test_coarse_clock_strict_lower_bound_waits(monkeypatch, flood):
    async def scenario():
        loop = asyncio.get_running_loop()
        clock = ManualClock(loop)
        loop._clock_resolution = .001
        sleeps, attempts = [], []
        original_sleep = asyncio.sleep

        async def recorded_sleep(delay):
            if delay > 0:
                sleeps.append((loop.time(), delay, loop.time() + delay))
            await original_sleep(delay)

        monkeypatch.setattr(app.asyncio, "sleep", recorded_sleep)

        class Sender:
            async def send_message(self, **kwargs):
                attempts.append(loop.time())
                if flood and len(attempts) == 1:
                    raise app.FloodRefusal(2)

        task = asyncio.create_task(app.RequestService(Sender(), (), 1)(
            app.Envelope(1, 77, app.Kind.START)))
        try:
            await clock.pump()
            if not flood:
                await clock.advance(1.0995)
                assert attempts == []
                assert sleeps[0] == (0, 1.1, 1.1)
                assert len(sleeps) >= 2
                assert all(s == (1.0995, 1.1 - 1.0995, 1.1) for s in sleeps[1:])
                await clock.advance(1.1 - clock.now)
                assert task.done()
                await task
                assert attempts == [1.1]
            else:
                await clock.advance(1.1)
                assert attempts == [1.1]
                assert sleeps[-1] == (1.1, 2, 3.1)
                await clock.advance(1.9995)
                assert attempts == [1.1]
                # Early callback must retain the original flood deadline.
                assert sleeps[-1] == (clock.now, 3.1 - clock.now, 3.1)
                await clock.advance(3.1 - clock.now)
                assert sleeps[-1] == (3.1, 1.1, 4.2)
                await clock.advance(1.0995)
                assert attempts == [1.1]
                assert sleeps[-1] == (clock.now, 4.2 - clock.now, 4.2)
                await clock.advance(4.2 - clock.now)
                assert task.done()
                await task
                assert attempts == [1.1, 4.2]
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            clock.restore()
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
        application = app.Application(None, (), 3)
        class Session:
            async def close(self):
                entered.set()
                await gate.wait()
        if outcome == "success":
            caller = asyncio.create_task(application.shutdown(Session()))
            await entered.wait()
            owned = application.cleanup_task
        else:
            owned = asyncio.create_task(work())
            application.cleanup_task = owned
            caller = asyncio.create_task(application.shutdown(None))
            await entered.wait()
        invoke = lambda: application.shutdown(None)
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
        assert application.cleanup_task is owned
        assert application.scheduler.pending == 0
        assert not application.scheduler.workers
        assert not [task for task in asyncio.all_tasks()
                    if task is not asyncio.current_task() and not task.done()]
    asyncio.run(scenario())


def test_poll_six_second_response_and_prompt_shutdown(monkeypatch):
    from aiogram.types import Update

    async def scenario():
        clock = ManualClock(asyncio.get_running_loop())
        bot = Bot(TOKEN)
        application = app.Application(bot, (), 3)
        calls, processed, events, cancelled = [], [], [], []
        monkeypatch.setattr(app, "emit_safe", lambda *args, **kwargs: events.append(args) if args[0] != app.Event.QUEUE else None)

        async def get_updates(**kwargs):
            calls.append((clock.now, kwargs))
            try:
                async with asyncio.timeout(kwargs["request_timeout"]):
                    await asyncio.sleep(6)
                    return [Update.model_validate(raw_update(text="/start"))]
            except asyncio.CancelledError:
                cancelled.append(clock.now)
                raise

        async def service(envelope):
            processed.append(envelope.source_id)

        bot.get_updates = get_updates
        application.scheduler.service = service
        application.ingress = asyncio.create_task(application.poll())
        try:
            await clock.pump()
            await clock.advance(3)
            await clock.advance(3)
            assert processed == [100], (events, calls)
            assert events == []
            assert application.scheduler.cursor == 101
            assert len(calls) == 2
            assert [call[1]["offset"] for call in calls] == [None, 101]
            assert all(k["timeout"] == 1 and k["limit"] == 1 for _, k in calls)
            # Second ordered request is still waiting for its six-second response.
            started = clock.now
            first = asyncio.create_task(application.shutdown(bot.session))
            second = asyncio.create_task(application.shutdown(bot.session))
            await clock.pump()
            coordinator = application.cleanup_task
            assert first.done() and second.done()
            await first
            await second
            await application.shutdown(bot.session)
            assert application.cleanup_task is coordinator
            assert coordinator.done() and application.ingress.cancelled()
            assert cancelled == [started]
            assert clock.now - started < 2
            assert application.scheduler.pending == 0
            assert not application.scheduler.workers
        finally:
            application.ingress.cancel()
            await asyncio.gather(application.ingress, return_exceptions=True)
            await application.shutdown(bot.session)
            clock.restore()

    asyncio.run(scenario())



def test_callback_envelope_uses_actor_and_accessible_private_context():
    from aiogram.types import Update
    payload = {"update_id": 777, "callback_query": {"id": "synthetic-callback", "chat_instance": "test",
        "from": {"id": 9000000001, "is_bot": False, "first_name": "Synthetic", "username": "sample"},
        "message": {"message_id": 55, "date": 1, "chat": {"id": 9000000001, "type": "private"}},
        "data": "place:a:synthetic"}}
    envelope = app.envelope_from_update(Update.model_validate(payload))
    assert envelope.actor_id == 9000000001 and envelope.chat_id == 9000000001
    assert envelope.source_id == 55 and envelope.private and envelope.human
    assert envelope.callback_data == "place:a:synthetic"
    assert envelope.callback_id == "synthetic-callback" and envelope.username == "sample"
    payload["callback_query"]["message"]["chat"] = {"id": -100, "type": "group", "title": "Synthetic"}
    assert not app.envelope_from_update(Update.model_validate(payload)).private
    del payload["callback_query"]["message"]
    payload["callback_query"]["inline_message_id"] = "synthetic-inline"
    assert not app.envelope_from_update(Update.model_validate(payload)).private


def test_message_envelope_retains_only_new_human_identity():
    from aiogram.types import Update
    payload = raw_update(text="/users", **{"from": {"id": 1, "is_bot": False, "first_name": "Test"}})
    envelope = app.envelope_from_update(Update.model_validate(payload))
    assert envelope.actor_id == 1 and envelope.text == "/users" and envelope.human
    assert envelope.callback_id is None
    edited = Update.model_validate({"update_id": 101, "edited_message": payload["message"]})
    assert app.envelope_from_update(edited) is None
