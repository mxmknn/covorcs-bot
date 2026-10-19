---
depth: standard
id: EVID-024
kind: evidence
last_modified_at: 2026-10-19T00:13:51.192608+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Independent final implementation architecture audit — reviewer/coworking-architecture-20261019-01
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-024: Independent final implementation architecture audit

## Structured Fields

evidence_type: measurement
congruence_level: 3
verdict: refutes

## Review Metadata

reviewer_identity: reviewer/coworking-architecture-20261019-01
reviewer_role: architect-reviewer
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_manifest: .venv/verification/audit-freeze.json
implementation_file_count: 29
implementation_sha256: 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106
manifest_raw_sha256: 33c5a02a0e9e778dc1327a65b376726fb975d034dfd8321f46c8cbf25f8f2127
base: unborn master; no HEAD and no commits; active EVID-021 prebuild inventory
review_verdict: BLOCKER
scope: independent final frozen implementation architecture audit; no implementation, activation or gate authorization
client_date: 2026-10-19

## Measurement

Physical read-only reviewer, distinct from both generators. Read scoped ground-truth get for full active ADR-001, RFC-001, PRD-001, SPEC-001 and EVID-021; inspected package source (all nine modules), relevant behavioral tests, packaging, README and docs/verification.md. Metadata governs historical draft/planned prose in active planning bodies. ADR active updated_at 2026-10-18T21:37:59.335862+00:00; PRD active 2026-10-18T20:51:11.875851+00:00; SPEC active 2026-10-18T20:51:12.611918+00:00. No EVID-020 document-only certification is used as code proof.

forgeplan health: exit0, healthy/project looks healthy, 27 artifacts, 22 advisory phase mismatches at initial observation. Health advice does not certify this implementation.

Before and after review independently read each of the 29 manifest paths and compared hashlib.sha256(Path(path).read_bytes()).hexdigest() to its declared digest: zero mismatches. Canonical aggregate is SHA256 of json.dumps(manifest["files"],sort_keys=True,separators=(",",":")).encode(): 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106 both times, exit0. Exact canonical get.body UTF-8 was hashed with Python hashlib via safely single-quoted argv: 65791 bytes, e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177. Final scoped RFC get remained active, timestamp exactly unchanged, body string exactly equal to initial get. The known projection EOF LF is irrelevant to this canonical-body pin.

Nonempty baseline comparison: EVID-021 declares 52 prebuild entries, with 28 product paths absent and .gitignore the only existing affected product path. All 28 now exist in the independently hashed manifest; 29 product files total 362906 bytes. Current .gitignore first405 bytes SHA256 2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a matches EVID-021 original. git symbolic-ref --short HEAD => master, exit0; git rev-parse --verify HEAD => exit128. This proves a nonempty implementation relative to the declared inventory, not a Git commit/diff against an invented revision.

Independent commands:
- PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_telegram_app.py tests/test_privacy.py tests/test_packaging.py tests/test_render.py -k 'not accepted_long_org_url_unchanged'
  => exit0, 308 passed, 1 deselected, 1 warning in9.45s.
- PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_catalog.py::test_real_empty_synthetic_separate
  => exit0, 1 passed, 1 warning in0.05s.
- Both warnings: Unknown config option cache_dir, expected with cacheprovider disabled.
- Two independent pure asyncio negative probes below: each exit0, observed contract failure. They import frozen source and allocate only in-memory tasks/fake sessions; no source edits, tempfiles, Bot instance, socket/network or real credentials.
No full self-run is claimed. Tempfile-dependent catalog cases and one render case were inspected, not executed; the physical sandbox cannot create their temporary inputs. Existing network-denial fixture was preserved.

## Findings

### 1. BLOCKER — successful cleanup misclassified as fail-stop when caller cancellation meets coordinator completion

Frozen telegram_app.py:454–466 Application.shutdown catches caller CancelledError and raises FailStop whenever cleanup_task.done() is true. done() includes successful completion. This violates RFC TC-3 / Invariant6: defer caller cancellation until coordinator completion, then propagate cancellation; fail-stop corresponds to failed/expired owned cleanup. The coordinator can finish successfully before the shielded caller resumes. A repeated signal at that boundary is then reported as cleanup failure despite no failed cleanup or residual ownership. __main__.py:19–28 _defer repeats the same distinction error for startup-resource cleanup. CLI main maps FailStop to exit1, whereas normal cancellation maps exit0; actual CLI execution of this race was not performed.

Independent executable command (no file creation):
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import asyncio
from coworking_nearby.telegram_app import Application
async def check():
    closing=asyncio.Event(); release=asyncio.Event()
    class Session:
        async def close(self):
            closing.set(); await release.wait()
    application=Application(None, (), 3)
    caller=asyncio.create_task(application.shutdown(Session()))
    await closing.wait()
    application.cleanup_task.add_done_callback(lambda done: caller.cancel())
    release.set()
    result=(await asyncio.gather(caller,return_exceptions=True))[0]
    print("coordinator_done",application.cleanup_task.done(),"coordinator_cancelled",application.cleanup_task.cancelled(),"coordinator_exception",application.cleanup_task.exception())
    print("caller_outcome",type(result).__name__,"pending",application.scheduler.pending,"workers",len(application.scheduler.workers))
asyncio.run(check())'
```

Observed exit0:
```text
coordinator_done True coordinator_cancelled False coordinator_exception None
caller_outcome FailStop pending 0 workers 0
```

Second independently executed probe:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import asyncio
from coworking_nearby.__main__ import _defer
async def check():
    gate=asyncio.Event()
    async def work(): await gate.wait()
    owned=asyncio.create_task(work()); caller=asyncio.create_task(_defer(owned))
    await asyncio.sleep(0)
    owned.add_done_callback(lambda done: caller.cancel()); gate.set()
    result=(await asyncio.gather(caller,return_exceptions=True))[0]
    print("owned_exception",owned.exception(),"caller_outcome",type(result).__name__)
asyncio.run(check())'
```

Observed exit0: owned_exception None caller_outcome FailStop.
The callbacks inject cancellation only, never cancel/mutate the coordinator or production source. This is a deterministic interleaving of successful owned completion and caller cancellation. Existing test_repeated_cancel_worker_finally_notification, shutdown_full_16_second_milestones and privacy test_run_defers_caller_cancellation_until_acquired_session_closed pass but cancel while cleanup is pending; they do not challenge the successful-done boundary. No data corruption, leak or CRITICAL security incident was observed. Nonetheless exact final implementation lifecycle compliance is falsified, so this frozen implementation cannot receive architecture PASS. No fix was implemented.

### 2. Domain direction and immutable snapshot remain faithful to active design

models/config/catalog/geo/routes/render have stdlib-only boundaries. Domain never imports SDK or startup; render imports models/routes, not geo. SDK use lives at Telegram edge plus explicit composition-root Bot construction (__main__), consistent with RFC startup ownership; it does not penetrate domain. Frozen dataclasses and tuple snapshot retain validated inactive records, with geo alone filtering active. Coworking.to_mapping creates a detached mapping and omits absent nullable keys. catalog reads a supplied path once, rejects whole input before tuple return, and has no environment/network enrichment or demo fallback. run validates settings and entire catalog before session/Bot/polling. CLI shares load_catalog and remains token/SDK/network independent.

Challenged unknown/duplicate JSON keys, BOM/surrogates, finite exact numeric types, full inactive/last-entry rejection, exact trim/codepoint lengths, null/default distinctions, Gregorian dates, rating provenance and raw URL grammar against C01–C08 and test_catalog T01–T24 source. Independent config/domain/import and packaging subprocess tests passed; real[] and synthetic loader smoke passed. Most catalog mutation cases remain inspected rather than self-run. No invented owner-semantic acceptance follows.

Pure Haversine raw-distance/id ranking, no radius/rating reorder, parsed two-origin three-mode endpoints, negative-zero/precision, escaping once and maximum visible UTF16 text have behavioral oracles rather than only file counts. Independent selected suite passed these. Organisation URL is preserved without added schema cap.

### 3. Admission, retention and worker succession withstand examined ownership faults

Application.poll awaits one feed_update, uses get_updates(limit=1) and committed scheduler.cursor, with no per-update service fanout; irrelevant/edited updates only advance cursor. Scheduler default global64/chat8 counts include popped active requests. Capacity waits precede no-await _commit; reservation, queue, worker registry and cursor are published without await. _spawn closes rejected coroutine; creation failure removes appended envelope/releases counters and leaves cursor unchanged.

Identity checks in _retire and _worker avoid stale-owner removal. Scheduler queues survive ordinary worker death, active request is released once before injectable finalizer, exactly one successor is created, and done callback covers pre-first-step cancellation. Successor failure retains FIFO and sets failed rather than silently discarding. No active send/prefix replay is introduced by successor start. Independent passing tests include admission_worker_creation_rollback, admission_cancel_capacity_full, admission_commit_feed_return_cursor, poll_uses_committed_cursor_after_feed_return_cancel, precommit_cancel_and_atomic_observation, worker_death_queued_successor_fifo, supervisor_death_before_worker_first_step, worker_finally_exception, worker_death_partial_send_no_replay and ordered_ingress_barrier_fifo_cleanup_race. These assert counters/cursor/identity/observed service order at barriers, including global64 saturation and other-chat progress.

Residual: count bounds are not byte/catalog-size bounds; one fetched unadmitted SDK payload remains transient. Head-of-line ingress blocking and volatile crash loss are explicitly accepted. No durability/exactly-once or load SLA is inferred.

### 4. Timing, send uncertainty and bounded shutdown mostly hold, but do not erase finding1

_Admission timestamp measures queue wait; RequestService starts fresh service90 deadline at invocation. Independent queue_wait_measured_separately_from_service_deadline holds queued work120s and observes send121.1; queue time does not consume service budget. _wait_full captures fixed loop.time end and repeats remaining sleeps, preserving full1.1 pause and full flood waits even with coarse-clock early timer dispatch. Independent coarse_clock_strict_lower_bound_waits exercises resolution.001 and rejects sends at1.0995 / early positive flood completion. Full attempt10 availability is checked before/after pause; retry waits share15 budget; only one extra current-message attempt; source-bound ReplyParameters disallows detached replies.

Raw status guard precedes SDK classification, handles valid429 zero, refuses malformed/non429/5xx ambiguity. _PostFacade disables redirects and request middleware replay. Tests instrument real pinned aiohttp connector/protocol/wire seams with pooled/unpooled disconnect, partial write, decode,5xx and redirects; GET/unguarded redirect positive controls demonstrate the seam can detect replay. Independently passed, rather than trusting only fake typed exceptions.

One shielded cleanup_task, asyncio.wait bounded joins and outer finally session.close give examined nonreset stages2/10/2/2; no wait_for/unbounded posttimeout cancellation join or asyncio.run cancel-all in executable. Independent fake-clock 16-second milestones, repeated signals, earlier-stage failure, close exception/timeout and terminal counters tests pass. Noncooperative owned tasks produce FailStop; tests release their own barriers only after observing that result. Arbitrarily blocked loops are outside cooperative bounds. Finding1 is an additional untested legal boundary, not disproved by those passes.

ProcessSinks suppresses raw root/library/asyncio/warnings/stdout/stderr before formatting and captures safe enum-only events. Independent hostile-formatting, nested guards, actual SDK exception and signal/bootstrap tests passed at INFO/DEBUG. Reference release is not physical RAM zeroization or deletion of Telegram/browser history.

### 5. Deployment boundary and honest limitations are preserved

Dockerfile pins Python3.12.15 base digest, installs hash-locked runtime via public PyPI, COPYs only runtime lock/nine package .py/catalog, chmods app/data without write bits and uses UID10001. Compose has one image-only bot service, no ports/build, readonly data directory bind, local env_file and20s grace. README supplies actual USTAR whitelist build (explicitly excludes whole-repo context), exclusive blank-env creation, shared offline validation, atomic same-directory candidate replacement then restart, and compatible image/catalog pair rollback with old poller stopped. No .dockerignore exists; security of submitted context relies on the documented whitelist command, not COPY alone. Static packaging tests passed; this reviewer did not build/inspect a runtime image or resolve live Compose environment.

Both lockfiles contain exact transitive pins/hashes, with dev additions separate. Resolver/install/runtime portability results remain coder provenance, not this reviewer's execution. Source adapter handles only start/help and fallback/location/group; no /about or Working Moscow implementation appeared in the nine modules. NOTE-002 remains separate scope; real catalog remains[] and synthetic data separate.

Residual product acceptance: owner has not supplied verified real branch/city+house/coordinates/link/rating records; manual live Telegram two origins x all three route modes has NOT occurred. Arbitrarily long organisation URL is allowed by frozen schema and can fail platform delivery; mocked rejection containment is not universal acceptance. Full AC-15/AX-05/NFR-06 acceptance, useful live launch, load/SLA and historical criterion-by-criterion TDD RED are not certified.

## Supplied Provenance — not independently executed

Orchestrator supplied frozen macOS suite690 passed10.56s; final coder Linux ARM64 suite690 passed12.94s; root Linux rerun underway, with no completed result supplied to this reviewer. docs/verification.md labels its own final host690/10.95s and container690/12.94s observations as coder results, with earlier results historical. These timestamps are distinct observations, not this reviewer's full run.
Supplied runtime image sha256:93a6a3263aa5f568ced199483ad74f1f6a9e74ddc7634e258a675e67dc7ee87c; dev image sha256:8a76c52f2adb01bd9cbf26d6c9b3e73f55714406ba6b6bb934aef8a65e204479. No independent image attestation claimed.

## Result

BLOCKER for final architecture compliance of the frozen implementation: deterministic cancellation/completion race contradicts RFC TC-3/Invariant6. Independent selected pytest309 passed across two commands; two negative probes exit0 and expose the missing boundary. Pre/post29-file freeze and canonical RFC pin unchanged.

## Interpretation

This Evidence informs RFC-001, and refutes complete implementation conformance at this freeze; it does not refute the selected single-process architecture itself. No activation/Ship authorization or amendment to approved requirements is made. A separate implementer and fresh independent review are required for any changed freeze; this reviewer remains read-only.

## Congruence Level Justification

CL3: actual frozen package in the target workspace, actual pinned local Python environment, deterministic in-memory asyncio interleavings and offline tests. Same-context code measurement; image/live/owner facts remain attributed or unperformed.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | informs |
| ADR-001 / PRD-001 / SPEC-001 | read-only normative context |
| EVID-021 | active prebuild inventory baseline |

Exactly one scoped new(kind=evidence,parent_id=RFC-001) created EVID-024 and its informs edge. Only this new Evidence body is updated. It remains draft; no depth changes, target mutations, source/config/test writes, wrapper log work, activation, score, live network, real .env access or Git mutation.

