---
depth: tactical
id: EVID-026
kind: evidence
last_modified_at: 2026-10-19T00:24:00.229176+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Independent v2 frozen code audit reviewer/coworking-code-20261019-02
---

---
links:
  - target: RFC-001
    relation: informs
---

# Independent v2 frozen implementation code audit

## Structured Fields
evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata
reviewer_identity: reviewer/coworking-code-20261019-02
reviewer_role: code-reviewer
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
review_verdict: PASS
implementation_sha256: 9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1
manifest_path: .venv/verification/audit-freeze-v2.json
manifest_raw_sha256: b2021b436c591a9ca0b82989f6e7510268012e7b8226a97d0423a174aa80597e
reviewed_files: all 29 manifest paths hashed; all nine application modules inspected, relevant tests/configuration/deployment/documentation inspected
base: unborn master; no HEAD; EVID-021 prebuild 52-entry inventory, 28 absent product paths and original 405-byte .gitignore
scope: independent physically read-only offline code audit of NEW v2; no implementer certification, Guardian decision, activation or live acceptance

## Measurement
Ground truth scoped forgeplan_get read RFC-001, PRD-001, SPEC-001, EVID-022, EVID-024, EVID-025 and EVID-021. Earlier PASS reviews are historical, and EVID-024 is a real contrary result. This review independently challenges v2; no old PASS certifies changed code. forgeplan health exited0, project needs attention: RFC R_eff0 and22 advisory phase mismatches. Its suggested score was not run.

Canonical returned bodies were passed in safely single-quoted JSON argv to PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c with hashlib.sha256(body.encode()). Observed:
- RFC active / exact timestamp above / e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177.
- PRD active / 2026-10-18T20:51:11.875851+00:00 / 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d.
- SPEC active / 2026-10-18T20:51:12.611918+00:00 / 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8.
Active metadata governs historical draft prose. Known extra LF in RFC projection is not part of canonical body.

Actual Path.read_bytes/hashlib checks before and after execution found29/29 matching file hashes. Aggregate was independently calculated from actual file digests using SHA256(json.dumps(actual,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()), equal to implementation pin above. Raw manifest hash above also unchanged. Exactly five paths differ from prior audit-freeze.json: coworking_nearby/__main__.py, coworking_nearby/telegram_app.py, tests/test_privacy.py, tests/test_telegram_app.py, docs/verification.md; other24 equal. git symbolic-ref --short HEAD => master/exit0; git rev-parse --verify HEAD => fatal Needed a single revision/exit128. No invented commit/diff. .gitignore first405 bytes SHA2562f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a equals EVID-021 original; all formerly absent28 paths are now in the29-file implementation.

Verified actual test names with rg. Self-executed exact permitted command, waited for completion:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_render.py tests/test_telegram_app.py tests/test_privacy.py -k 'not test_accepted_long_org_url_unchanged'
```
Exit0:319 passed,1 deselected,1 warning in9.00s. Expected warning Unknown config option cache_dir follows disabled cacheprovider. Exclusion names actual tmp_path-dependent test_render.py::test_accepted_long_org_url_unchanged. No weakening/edits; autouse DNS/socket guard retained. Full file/CLI catalogue suite and packaging suite were not self-executed. An initial Python here-document command was denied by zsh because physical sandbox cannot create even shell temporary files; rerun used python -c successfully. No tempfile workaround or writes occurred.

## Findings

### 1. Prior cancellation BLOCKER is resolved at this v2 freeze
Inspected Application.shutdown and __main__._defer: each shields the same owned task, remembers caller cancellation, and on owned completion distinguishes owned.cancelled() from successful or exceptional completion. Genuine owned cancellation raises FailStop. Otherwise result() preserves original exception object/priority; successful result breaks and deferred caller CancelledError propagates. Neither method replaces coordinator, restarts cleanup nor resets stage deadlines. Normal owned error propagates directly through shield; normal owned success returns normally. An already-completed owned future can bypass a suspension, but task cancellation remains observable to its caller; executed already-done controls challenge this.

Reexecuted BOTH ORIGINAL python -c commands verbatim from EVID-024's shell blocks against actual v2 source, exit0 each:
- Application probe: coordinator_done True, coordinator_cancelled False, coordinator_exception None; caller_outcome CancelledError pending0 workers0.
- _defer probe: owned_exception None caller_outcome CancelledError.
Thus the precise historical FailStop counterexample no longer reproduces, without altering the artifact or inputs.

Additional independently authored PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c matrix (in-memory asyncio only), exit0: "16 independent outcome/timing/path probes PASS; no pending tasks". Crossed shutdown/defer x success/owned cancel/RuntimeError/FailStop x completion race/already-done. Completion callback cancels caller after shield callback registration; caller also cancelled twice while owned work remains gated. For already-done, gate releases first, then a new self-cancelled caller invokes the same owned task. Asserted CancelledError on success, FailStop only on owned cancellation, original exception identity on error/failstop, same cleanup_task identity, zero scheduler pending/workers, and no residual cooperative tasks. Real Application success used actual session-close cleanup. This independently supplements the16 new behavioral pytest cases, which ran in the319-case selection. No RED was self-executed on old source; coder RED6fail/10pass then GREEN16pass is supplied chronology only.

The executed test_owned_completion_caller_cancellation_boundary in each corresponding test file covers all eight cases, checks original error identity and already-done/race outcomes. This is substantive regression coverage, not an old PASS repin. No cancellation-related blocker remains found in examined cooperative paths.

### 2. Fixed shutdown ownership, deadline and process-exit contracts survive the narrow change
Source still creates one cleanup_task without intervening await. _cleanup stops/joins ingress2s, drains10s, cancels/joins workers2s and always attempts close2s through nested outer finally. bounded_tasks uses asyncio.wait, cancels pending without unbounded follow-up join. Caller shielding prevents repeated signals from resetting stage clocks. Executed shutdown_stage_deadlines_outer_finally, shutdown_full_16_second_milestones, repeated_cancel_worker_finally_notification, session_close_exception_timeout, shutdown_earlier_stage_exception_still_closes and terminal counters cases challenge earlier failures, stubborn owned tasks and close failure/timeout. Inspected milestone assertions: close begins14, final FailStop16 under repeated caller cancellation; test-owned stubborn resources release only after bounded failure observation.

Composition run still guards acquisition, closes session even before Application construction fails, restores sinks, gives cleanup failure priority over deferred caller cancellation. main catches normal cancellation as exit0 and failure as exit1, restores signals and closes loop without asyncio.run cancel-all. Executed repeated_SIGINT_SIGTERM_same_cleanup checks real signal callbacks and one close with both close outcomes, plus run acquired-session cancellation and bootstrap failures. These are cooperative event-loop bounds; blocked loops/arbitrary noncooperative dependencies are outside16s success claims. No leaked-task success is claimed for fail-stop.

### 3. Unchanged domain/schema aspects were independently inspected and challenged
Only unchanged aspects are carried forward, after current inspection: frozen13-field Coworking/tuple snapshot and detached omission mapping; shared stdlib-only loader/CLI; startup validates whole catalogue before Bot. Closed field set comes from dataclass fields; exact trim set and codepoint lengths; required/default/null distinctions; duplicate JSON members, BOM, invalid UTF8, surrogates, nonfinite/huge numbers; all inactive/last records validate atomically. Dates use ASCII grammar plus Gregorian date.fromisoformat. Rating provenance dependencies preserve stored date and no invented rating. URL grammar inspects raw components before urlsplit, exact ASCII authority with only literal443, path/maps boundary, percent syntax/control/backslash rejection, decoded single dot segments and encoded path slash; accepted URLs remain unchanged with no cap or fetch.

Independent python -c/unittest.mock.patch.object(Path,"read_bytes",return_value=synthetic_bytes) public-loader probes ran exit0: "21 in-memory loader/render probes PASS". Covered defaults/empty, bool/huge coordinates, null active/source, invalid century/Unicode dates, nonliteral443, encoded dot/slash, missing yandex provenance, unknown field, trimmed duplicate id, valid-first/invalid-inactive-last atomic rejection, valid leap/astral text, BOM/UTF8/duplicate JSON/surrogate rejection and20,000-character organisation URL retained through actual loader and render_card. Only input bytes replaced in memory; no production patch/write. This does not stand in for full filesystem CLI coverage.

Current geo independently inspected: finite exact origin types/bounds, Haversine R6371000/clamp, active-only raw distance/id Unicode sorting before limit, no radius/rating reorder. Current route builder serializes explicit origin then destination lat/lon, six-place rounding/negative zero and pd/mt/auto. Executed domain tests use independent distance/tie/permutation oracles and parsed two-origin/three-mode links. Current render keeps exact Russian order/source/fallback/button rows, raw1000 threshold/half-up display and html.escape once. Escaping/maxUTF16 tests passed. No owner data semantics inferred from syntactic acceptance.

### 4. Unchanged admission/delivery/privacy remain supported by fresh execution
Current Scheduler no-await commit publishes active-inclusive64/8 counters, queue, worker owner and cursor atomically; failed creation closes rejected coroutine and rolls back. Precommit cancelling check admits nothing. Identity-checked retirement and done callback cover stale cleanup and death before first instruction; active release precedes injectable finalizer; successor handles untouched FIFO without replaying active send. Executed capacity, rollback, cursor/postcommit-cancel, successor, finalizer/notification-fault, ordered-ingress and partial-send tests assert state at barriers and other-chat progress. Count bounds are not byte bounds, durable queue or load SLA; one fetched unadmitted update is transient. Poll limit1 awaits feed_update and uses committed cursor.

RequestService retains separate90s service deadline (queue wait excluded), full10s attempt availability, full1.1s preattempt and shared15s full flood waits, one current-message retry, confirmed-prefix no replay and source-bound reply. _wait_full keeps a fixed monotonic end and repeats remainder on early timer dispatch. Executed coarse_clock_strict_lower_bound_waits checks Linux-like.001 resolution, no send at1.0995 and positive flood end before retry. Raw HTTP429 confirmed ok=false/error_code429/nonnegative exact integer only is retryable, including zero. Non429 SDK RetryAfter, malformed refusal, redirects,5xx,decode/disconnect/partial-write ambiguity stop. _PostFacade disables redirects/middleware send replay. Fresh selected tests exercise actual pinned SDK/aiohttp connector/parser seams with positive controls demonstrating harness can detect replay; not a live delivery guarantee.

Current ProcessSinks guards raw logger/handler/warnings/loop/bootstrap/stdout/stderr before formatting, only fixed enums/random id/bounded numeric fields enter safe serializer. Executed INFO/DEBUG hostile str/repr/nested SDK exceptions, recursion/nested guards and startup/close cases passed. Reference cleanup is not RAM zeroization or deletion of external Telegram/browser history; Python sink checks do not prove native file-descriptor suppression.

### 5. Release and residual acceptance remain explicit
Inspected unchanged Dockerfile/compose and lock declarations: pinned3.12.15 base, hash-required dependencies, UID10001, closed runtime COPY set, nonwritable catalogue, one image-only service/no ports, read-only data bind and20s grace. README whitelist context is security-relevant; COPY alone does not exclude secrets from a whole-repo build context. No Docker command or container environment/config inspection was performed by this reviewer.

data/coworkings.json independently read exactly []; synthetic examples separate. NOTE-002 editorial/about remains separate DRAFT/unimplemented and is not a missing RFC implementation feature. Owner real branch/address/city+house/coordinates/link/rating acceptance and manual live two origins x three modes remain UNPERFORMED. SPEC-valid arbitrary-length organisation URL can exceed Telegram acceptance: preserved serialization/conservative refusal is not universal platform acceptance. Complete live AC-15/AX-05/NFR-06 acceptance, usefulness, load/SLA, historical per-criterion RED, CI and Ship are not certified.

## Supplied provenance, distinctly not self-executed
Coder docs/verification.md and assignment report RED6fail/10pass, GREEN16pass; final host706pass10.23s, Linux706pass12.84s. Historical690 runs/images are superseded for changed paths, not erased.
Completed root records became available during review and were read, not executed by this reviewer:
- .venv/verification/root-test-audit-v2.json SHA256 acf4e9de1c66d7d7ac8f46cb6a4ec68bb216fa08fbc4040ca76eb2d4ba42746a: host706pass11.19s/exit0; Linux706pass13.39s/exit0 with expected cache warning; both original EVID024 probes CancelledError and zero counters; freeze unchanged.
- .venv/verification/root-runtime-audit-v2.json SHA256237ca1abb603e26e2e0de5145f0c6108bd6b5b70efebba3800f47dedfd45011f: runtime UID10001/Python3.12.15/aarch64, exact11 runtime files and matching hashes/no.env; dev source/tests match; real/synthetic validator exit0, blank token safe failure exit1, offline synthetic-token SIGTERM exit0 in0.639887625s with safe start/stop only.
- Runtime image sha256:b909f443edde64355c0e76c0aafa65251a4ac4a90001207b9a721b6b911e200a; dev image sha256:bdb4dbad98d580edb3e03a5327e2e0c6b6c97447a9e8fc1be746a31611665e78.
These complementary filesystem/Linux/runtime observations are attributable root-supplied evidence, not self-executed image attestation.

## Result and Interpretation
PASS for this exact v2 offline implementation code audit with stated residual risks. Prior EVID-024 cancellation BLOCKER is explicitly resolved by source inspection, fresh behavioral suite and original/adversarial reruns. Earlier PASS evidence never certifies the changed freeze. Final scoped RFC read remained active with exact timestamp and byte-identical canonical body; final29-file digest and raw manifest remained unchanged.

Exactly ONE new evidence EVID-026 was created via scoped MCP parent_id RFC-001, automatic informs. Only its body is updated, at default depth and DRAFT. No source/tests/roles/planning artifacts/old EVID edits, activation/score/pipeline or Git mutation, installs, live network or actual .env read/hash/print/search occurred. Distinct maintainer handles metadata and named user approval; this reviewer requests no bypass.

## Congruence Level Justification
CL3: exact local frozen implementation and active ground-truth contract, independently inspected and exercised in its actual Python environment. Supplied full-suite/runtime results retain separate attribution and live/owner acceptance remains withheld.

## Reproduction of additional outcome matrix
Self-executed as PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c with this literal body (proper shell quoting; no file creation):
```python
import asyncio
from coworking_nearby.telegram_app import Application,FailStop
from coworking_nearby.__main__ import _defer
async def check():
    count=0
    for path in ("shutdown","defer"):
      for outcome in ("success","cancel","error","failstop"):
       for timing in ("race","done"):
        gate=asyncio.Event()
        failure=RuntimeError("synthetic") if outcome=="error" else FailStop()
        async def work():
            await gate.wait()
            if outcome=="cancel": raise asyncio.CancelledError()
            if outcome!="success": raise failure
        app=Application(None,(),3)
        if path=="shutdown" and outcome=="success":
            class Session:
                async def close(self): await gate.wait()
            caller=asyncio.create_task(app.shutdown(Session()))
            while app.cleanup_task is None: await asyncio.sleep(0)
            owned=app.cleanup_task
        else:
            owned=asyncio.create_task(work())
            if path=="shutdown": app.cleanup_task=owned
            caller=asyncio.create_task(app.shutdown(None) if path=="shutdown" else _defer(owned))
        await asyncio.sleep(0)
        if timing=="race":
            owned.add_done_callback(lambda _,c=caller:c.cancel())
            caller.cancel(); await asyncio.sleep(0)
            caller.cancel(); await asyncio.sleep(0)
            assert not owned.done()
            gate.set()
        else:
            gate.set(); await asyncio.gather(caller,return_exceptions=True)
            async def invoke():
                asyncio.current_task().cancel()
                return await (app.shutdown(None) if path=="shutdown" else _defer(owned))
            caller=asyncio.create_task(invoke())
        result=(await asyncio.gather(caller,return_exceptions=True))[0]
        if outcome=="success": assert isinstance(result,asyncio.CancelledError) and owned.exception() is None
        elif outcome=="cancel": assert isinstance(result,FailStop) and owned.cancelled()
        else: assert result is failure and owned.exception() is failure
        if path=="shutdown": assert app.cleanup_task is owned and app.scheduler.pending==0 and not app.scheduler.workers
        count+=1
    assert not [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
    print(count,"independent outcome/timing/path probes PASS; no pending tasks")
asyncio.run(check())
```



