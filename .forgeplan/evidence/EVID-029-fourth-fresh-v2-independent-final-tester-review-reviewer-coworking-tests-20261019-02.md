---
depth: tactical
id: EVID-029
kind: evidence
last_modified_at: 2026-10-19T00:28:51.914344+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Fourth fresh V2 independent final tester review reviewer coworking tests 20261019 02
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-029: Fourth fresh V2 independent final tester review

## Structured Fields

evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata

reviewer_identity: reviewer/coworking-tests-20261019-02
reviewer_role: tester
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_sha256: 9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1
manifest_path: .venv/verification/audit-freeze-v2.json
implementation_file_count: 29
base: unborn master; no HEAD; EVID-021 prebuild inventory; original .gitignore 405-byte prefix
review_verdict: PASS
scope: conditional offline implementation/test review only; no Guardian or Ship certification

## Measurement

Assigned physical Role B reviewer, distinct from implementation and planning generators. Read canonical scoped forgeplan_get RFC-001/PRD-001/SPEC-001/EVID-021/EVID-024/EVID-025/EVID-026. RFC metadata is active at the exact stamp above; historical draft/planned body prose does not override metadata. Exact returned RFC body UTF-8 hashed using safely single-quoted argv to PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode()).hexdigest())' returned the pinned e1ba834e... hash, exit0. Compared normative TC-1–4 and PRD/SPEC acceptance with source and named tests, rather than accepting old reviewer conclusions. Read full __main__ and telegram_app implementations including both repaired branches, coordinator, bounded joins, send state machine, scheduler and sinks; reviewed domain/loader/render/config and substantive test oracles.

forgeplan health exited0: 34 artifacts, RFC at-risk R_eff0 and advisory duplicates/phase mismatches. Health advice is not gate certification; no score/activation/deprecation was invoked. Physical .codex/agents/forgeplan-reviewer.toml matches the assigned developer role.

Each of exactly29 named manifest files was independently read and SHA256 checked: zero mismatches. Aggregate is hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest(), observed 9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1. Mapping keys/digests are ASCII so this is also canonical UTF-8 JSON with ensure_ascii=False. Old .venv/verification/audit-freeze.json describes 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106, stale implementation context. Exactly five changed paths: coworking_nearby/__main__.py, coworking_nearby/telegram_app.py, tests/test_privacy.py, tests/test_telegram_app.py, docs/verification.md; 24 unchanged. Git symbolic-ref --short HEAD returned master exit0; git rev-parse --verify HEAD returned exit128, fatal: Needed a single revision. No invented commit/diff. Current .gitignore first405 bytes SHA256 2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a matches original EVID-021 inventory.

## Independently executed commands and observed results

Inspected exact names using rg before running:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_render.py tests/test_telegram_app.py tests/test_privacy.py tests/test_packaging.py -k 'not accepted_long_org_url_unchanged'
```

Actual completed exit0: **324 passed, 1 deselected, 1 warning in 9.51s**. Warning is Unknown config option cache_dir, expected with cacheprovider disabled. The exact excluded tmp_path case is tests/test_render.py::test_accepted_long_org_url_unchanged. No tmp_path cases were executed; the 381 catalogue cases, including filesystem mutations/subprocess fixtures, are static/supplied-root coverage, not my full self-run. Autouse socket/DNS denial remains unchanged. No pytest cache or bytecode writes requested.

Standalone smoke (each subprocess inherited PYTHONDONTWRITEBYTECODE=1):

```sh
.venv/bin/python -B -m coworking_nearby.catalog data/coworkings.json
.venv/bin/python -B -m coworking_nearby.catalog examples/coworkings.synthetic.json
```

Both exit0, stdout='' and stderr=''. Real catalogue remains []. Independent inline scripts below ran with PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c '<literal script>', no persistent scripts/config/tempfiles:
- Original two EVID-024 race probes: exit0; shutdown successful coordinator, close once, pending0/workers0, caller CancelledError; _defer successful owned task, caller CancelledError.
- Separate16-outcome probe: exit0, completion/alreadydone × success/cancel/error/failstop × shutdown/defer. All16 assertions passed. Success -> caller CancelledError; owned cancel -> FailStop; error -> exact LookupError instance; failstop -> exact FailStop instance. Owned work called once, no leftover cooperative tasks.
- Public loader20 input probes: exit0, all passed; Path.read_bytes alone replaced with synthetic input, production logic untouched. Empty/default, BOM/UTF8/duplicate/surrogate/root, bool/huge integer, inactive invalid Gregorian date, Unicode date, yandex rating dependency, encoded dot URL/nonliteral443, unknown field/source null, trimmed duplicate id, valid-first invalid-last atomic failure, valid astral/leap date, and 20,000-character URL preserved through loader/render.

Two initial shell here-document launches failed before Python execution: zsh could not create its implicit temporary file (exit1). They were rerun successfully using literal safely single-quoted -c arguments. No filesystem workaround/temp file was used. These shell-launch failures are not product/test failures.

## Findings

### 1. EVID-024 BLOCKER is closed for this V2 freeze; EVID-025 PASS never disproved it

Original implementation conflated task.done() with failed cleanup in both Application.shutdown and _defer. Fresh source now distinguishes task.cancelled() -> FailStop, otherwise retrieves task.result() (preserving owned exception identity/priority), and on success exits the loop then propagates remembered caller CancelledError. The unchanged await/shield path still propagates owned ordinary errors directly. No restart or deadline reset was introduced.

I independently repeated both original callback-interleaving probes, without replacing cleanup logic: successful closed cleanup now produces caller CancelledError, not FailStop. Actual Application.shutdown session close ran once, coordinator succeeded, pending0/workers0. My16-branch script additionally challenged repeated caller cancellation while pending, done-callback cancellation and pre-cancelled caller on already-done owned outcomes. It uses a different LookupError identity oracle and independently counts owned executions. The shutdown branch-injection cases deliberately isolate outcome precedence; they do not replace actual coordinator/session proof from the original probe and executed deadline tests.

Both files' test_owned_completion_caller_cancellation_boundary provide16 repository cases. They verify task identity, zero remaining tasks, deferred cancellation and exact failure identity. Success in shutdown uses actual session cleanup. Error/cancel/failstop cases seed the owned coordinator seam; meaningful for branch semantics, insufficient alone for full cleanup integration. Combined with original real cleanup probe and test_run_defers_caller_cancellation_until_acquired_session_closed, this closes the reported legal interleaving.

EVID-025 was read and remains untouched. Its PASS refers to the old 87421... freeze and omitted the completed-owned boundary; pending-only repeated-cancellation tests did not refute EVID-024. EVID-026 fresh code PASS was read as corroboration, not substituted for this tester's measurements.

### 2. Timing/admission/lifecycle checks are behavioral, with bounded cooperative scope

Executed test_coarse_clock_strict_lower_bound_waits explicitly forces resolution .001 after ManualClock setup: no send at1.0995, fixed pause end1.1, full positive429 wait end3.1 and second attempt4.2. Source _wait_full holds one monotonic end and sleeps remaining time, so early timer dispatch does not shorten waits. Sleep-start/duration introspection partly mirrors the mechanism, but actual observed send/no-send timestamps are independent contract oracles. Queue120s test observes wait_ms120000 and first send121.1, retaining service90 from worker start; attempt10 remains separate. Full attempt-fit before/after pause, no partial retry wait, shared15 budget, at most one extra current-message429 retry and no confirmed-prefix replay are exercised.

Executed barrier tests challenge global64/chat8 active-inclusive accounting, no-await reservation/enqueue/worker/cursor publication, capacity cancellation, task-creation rollback, postcommit feed cancellation, pre-first-step worker death, queued successor FIFO, stale identity and finalizer/notification/successor faults. Observed source/reply order and queue/cursor/counter values give stronger oracles than checking calls to private helpers. Death during partially sent active request does not replay that active request or confirmed prefix; untouched queued work proceeds once. Volatile crash loss/head-of-line blocking are accepted, not durable delivery proof.

test_shutdown_stage_deadlines_outer_finally and test_shutdown_full_16_second_milestones actually ran: nonreset2/10/2/2 (16 total), repeated cancellations, session close after earlier failures and explicit FailStop for noncooperative owned work. test_repeated_cancel_worker_finally_notification and terminal counters tests ran with coordinator identity and zero counts/queues/workers on cooperative completion. Tests release their synthetic stubborn resources only after fail-stop observations; no leak-free or hard-real-time claim for blocked loops/arbitrary noncooperative dependencies is made.

### 3. SDK transport and privacy use substantial negative-path oracles

Executed real pinned SDK/aiohttp fresh and pooled connection cases, partial request, disconnect, short response, invalid UTF8/JSON,5xx and redirects use RecordingTransport below connector/pool/writer/parser. Wire attempt counts prove no observed replay; pooled case checks transport reuse. GET-disconnect and unguarded307/308 POST redirect positive controls prove the fake wire can detect actual replay behavior. Session recreation/Message decoding and hostile middleware disabling are exercised. Source raw status guard requires decoded HTTP429, ok=false, integer error_code429, nonnegative integer retry_after, including zero. Typed non429 RetryAfter/ambiguous failures stop. This is offline integration with synthetic transport, not live Telegram acceptance.

INFO/DEBUG hostile __str__/__repr__, nested real SDK exceptions, warnings, lastResort, loop/top-level hooks, stdout/stderr/buffer and recursive sink cases executed. Assertions require no hostile formatting and only fixed safe records. Process guards precede configuration/session/Bot in executable; arbitrary raw exceptions/payloads never enter safe JSON. Queue wait is bounded and excludes chat/source/coordinates/URL/token. No universal native-OS-file-descriptor privacy or physical RAM zeroization claim follows.

### 4. Domain/schema/render checks align with active PRD/SPEC/RFC; some tests need separate proof

Strict13-field loader validates all entries, including inactive/last, before returning immutable tuple; exact trim/codepoints/default/null/type, ASCII Gregorian dates, nested Unicode/duplicate JSON, huge integers before float conversion, rating dependencies and strict URL grammar were reviewed. Own20 public-loader probes challenge acceptance with external synthetic bytes; they do not claim filesystem errors/atomic replacement tests ran here. Catalogue failure helper's CLI diagnostic string equals production format_diagnostic, an implementation-mirroring formatting check; separately asserted class/field/id/index and SPEC examples provide the substantive oracle.

Executed geo tests use independently fixed metre/order examples, permutations, ties/raw-near-ties, active filtering and no-radius remote examples. All six two-origin×three-mode route cases decode query components and explicitly challenge latitude/longitude swapping. Executed HTMLParser-visible card assertions verify once-only escaping, exact source/date/fallback/UI order, unchanged origin inputs and worst-case <=2556 UTF16 units below4096. Exact constant tests verify normative Russian wording but by themselves do not prove handler integration; adapter tests supply it. Long organisation URL unchanged by the public loader/render passed my in-memory probe.

Packaging tests assert literal declared build/COPY/UID/Compose policy and are partly implementation-shaped: they cannot prove built-image contents. Root-supplied V2 image/file inspection below is a distinct observed layer. Count-bounded queues are not byte/catalogue-size bounds; no unsolicited byte/URL limit is inferred.

### 5. Historical RED and live/product residuals are retained honestly

New repair documentation reports actual16-case RED6failed/10passed followed by targetedGREEN16passed; these are generator observations, not my historical execution. Earlier documented11failed/3passed and coarse-clock2failed RED are separate repairs. No fabricated individual historical acceptance RED is claimed; current passing tests do not reconstruct chronology.

Owner real catalogue remains []; owner branch/city+house/coordinates/link/rating semantics unaccepted. Manual two origins×three modes opening routes/start/end/mode and live Telegram delivery are unperformed. Unrestricted valid organisation URL platform acceptance remains unresolved: fake400 containment and preserved serialization do not prove arbitrary-length acceptance. No cap/truncate/omission or universal delivery claim. Complete AC-15/AX-05/NFR-06 live/platform acceptance is withheld. NOTE-002 /about remains draft, separate and unimplemented. No CI/live service results, load/demand/SLA proof or Guardian/Ship decision.

## Supplied root observations — not self-executed by this tester

Read .venv/verification/root-test-audit-v2.json and root-runtime-audit-v2.json NOW; both pin this exact9c73... implementation. Carrying their substantive results here makes ignored JSON files nonexclusive proof:
- Root independent full host: **706 passed in11.19s exit0**.
- Root independent Linux ARM64: **706 passed,1 expected cache_dir warning in13.39s exit0**.
- Root independently reran both original EVID-024 probes: successful owned completion -> caller CancelledError, no FailStop, counters0; freeze unchanged.
- Every final dev-image package/test hash matches; dev/test image sha256:bdb4dbad98d580edb3e03a5327e2e0c6b6c97447a9e8fc1be746a31611665e78.
- Runtime sha256:b909f443edde64355c0e76c0aafa65251a4ac4a90001207b9a721b6b911e200a; local tag root-retagged and verifiedV2.
- Runtime UID10001, Python3.12.15 GCC12.2.0, aarch64. Exactly11 whitelist files: nine package modules, requirements.lock, data/coworkings.json. All listed hashes match this freeze; no .env.
- Root runtime real and synthetic catalogue CLI each exit0, stdout/stderr empty.
- Blanktoken exit1, stdout empty; stderr exactly one safe JSON fail/startup record with opaque id213d9b842dbb7d53084c91ff4cef1091 and count0.
- Offline fake-token SIGTERM exit0, stop_seconds0.6398876250023022 (about0.63989s), safe start/startup and stop/ingress records only, count0.
- No actual .env read/hash/print/use or live Telegram/Yandex calls reported.

The root JSON records **do not contain exact command strings**. I preserve this provenance gap rather than inventing root commands. docs/verification.md records generator commands such as PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q and docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev coworking-nearby:test, and real/synthetic catalogue commands; those strings are generator documentation, not an attestation that root used identical invocation. Root supplied current outcomes/image identities above are explicitly root attribution. Historical688/690 counts/images and old audit-freeze are not V2 proof. My exact executed command and inline bodies are recorded here separately.

## Reproducible independent inline probes

Each following literal body was passed via safely single-quoted argv to PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c; no file created.

### Original EVID-024 probes

```python
import asyncio
from coworking_nearby.telegram_app import Application
from coworking_nearby.__main__ import _defer
async def check():
 closing=asyncio.Event(); release=asyncio.Event(); closes=[]
 class Session:
  async def close(self):
   closes.append(1); closing.set(); await release.wait()
 application=Application(None,(),3)
 caller=asyncio.create_task(application.shutdown(Session()))
 await closing.wait()
 application.cleanup_task.add_done_callback(lambda done: caller.cancel())
 release.set()
 result=(await asyncio.gather(caller,return_exceptions=True))[0]
 assert isinstance(result,asyncio.CancelledError)
 assert application.cleanup_task.exception() is None and closes==[1]
 assert application.scheduler.pending==0 and not application.scheduler.workers
 print('original shutdown probe: CancelledError, successful coordinator, close once, pending0 workers0')
 gate=asyncio.Event()
 async def work(): await gate.wait()
 owned=asyncio.create_task(work()); caller=asyncio.create_task(_defer(owned))
 await asyncio.sleep(0)
 owned.add_done_callback(lambda done:caller.cancel()); gate.set()
 result=(await asyncio.gather(caller,return_exceptions=True))[0]
 assert isinstance(result,asyncio.CancelledError) and owned.exception() is None
 print('original defer probe: CancelledError, successful owned task')
asyncio.run(check())

```

### Independent16 branch outcomes

```python
import asyncio
from coworking_nearby.telegram_app import Application,FailStop
from coworking_nearby.__main__ import _defer
async def one(path,done,outcome):
 gate=asyncio.Event(); started=asyncio.Event(); calls=[]
 error=FailStop() if outcome=='failstop' else LookupError('synthetic-owned')
 async def owned_work():
  calls.append(1); started.set(); await gate.wait()
  if outcome=='cancel': raise asyncio.CancelledError()
  if outcome!='success': raise error
 application=Application(None,(),3)
 if path=='shutdown':
  application._cleanup=lambda session: owned_work()
  async def invoke(): return await application.shutdown(None)
  caller=asyncio.create_task(invoke()); await started.wait(); owned=application.cleanup_task
 else:
  owned=asyncio.create_task(owned_work())
  async def invoke(): return await _defer(owned)
  caller=asyncio.create_task(invoke()); await started.wait()
 if done:
  gate.set(); await asyncio.gather(caller,return_exceptions=True)
  async def pre_cancelled():
   asyncio.current_task().cancel()
   await invoke()
  caller=asyncio.create_task(pre_cancelled())
 else:
  caller.cancel(); await asyncio.sleep(0); caller.cancel(); await asyncio.sleep(0)
  assert not owned.done()
  owned.add_done_callback(lambda _:caller.cancel()); gate.set()
 result=(await asyncio.gather(caller,return_exceptions=True))[0]
 if outcome=='success': assert isinstance(result,asyncio.CancelledError) and owned.exception() is None
 elif outcome=='cancel': assert isinstance(result,FailStop) and owned.cancelled()
 else: assert result is error and owned.exception() is error
 assert calls==[1]
 if path=='shutdown': assert application.cleanup_task is owned
 assert not [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
 print(path,'alreadydone' if done else 'completion',outcome,type(result).__name__,'once')
async def main():
 for path in ['shutdown','defer']:
  for done in [False,True]:
   for outcome in ['success','cancel','error','failstop']: await one(path,done,outcome)
asyncio.run(main())

```

### Independent20 public-loader probes

```python
import json
from pathlib import Path
from unittest.mock import patch
from coworking_nearby.catalog import load_catalog,CatalogError
from coworking_nearby.render import render_card
from coworking_nearby.models import Origin,SearchResult
base=dict(id=' a ',name='😀',address='Synthetic',latitude=0,longitude=0)
cases=[(b'[]',True),(json.dumps([base]).encode(),True),(b'\xef\xbb\xbf[]',False),(b'\xff',False),(b'[{"id":"a","id":"b"}]',False),(b'["\\ud800"]',False),(b'{}',False)]
for change in [dict(latitude=True),dict(longitude=10**400),dict(active=False,updated_at='1900-02-29'),dict(updated_at='２０２６-01-01'),dict(rating_source='yandex',rating_text='4'),dict(yandex_maps_url='https://yandex.ru/maps/%2e%2e/x'),dict(yandex_maps_url='https://yandex.ru:0443/maps'),dict(unknown=1),dict(rating_source=None)]:
 cases.append((json.dumps([base|change]).encode(),False))
cases += [(json.dumps([base,base|dict(id='a')]).encode(),False),(json.dumps([base,base|dict(id='b',active=False,description=2)]).encode(),False),(json.dumps([base|dict(updated_at='2000-02-29',name='😀'*150)]).encode(),True)]
for raw,valid in cases:
 with patch.object(Path,'read_bytes',return_value=raw) as read:
  try: result=load_catalog('synthetic-memory.json')
  except CatalogError: assert not valid
  else: assert valid
  assert read.call_count==1
url='https://yandex.ru/maps/org/synthetic?q='+'x'*20000
with patch.object(Path,'read_bytes',return_value=json.dumps([base|dict(yandex_maps_url=url)]).encode()):
 record,=load_catalog('synthetic-memory.json')
assert record.id=='a' and record.yandex_maps_url==url
assert render_card(SearchResult(record,0),1,Origin(0,0)).button_rows[-1][0].url==url
print(len(cases)+1,'independent public loader probes passed; URL preserved; read_bytes only input replacement')

```

## Result

PASS for conditional offline scope at the pinned V2 freeze. Independently executed324 pytest cases, both original race probes,16 additional outcome probes,20 public-loader probes and two real/synthetic offline CLI smokes all completed successfully. EVID-024 race is no longer present under the original deterministic reproduction. Prior EVID-025 unchanged and stale-freeze scoped. Supplied root706 host/Linux/runtime results complement restricted filesystem coverage; no self-executed full706 claim. Remaining live/owner/platform and root exact-invocation provenance limitations above are not concealed.

## Interpretation

Exactly one new scoped new(kind=evidence,parent_id=RFC-001) created EVID-029 and its informs edge. Only this owned Evidence may be updated; remains draft. No source/test/config/target/old Evidence mutation, real secrets access, Docker invocation, live network, scoring, creator reasoning, activation or pipeline unlock. This is tester measurement, not Guardian/Ship authorization.

## Congruence Level Justification

CL3: exact canonical active artifact revision and actual frozen29-file implementation in the same workspace, exercised with pinned local Python and deterministic independent memory probes. Image/Linux/full filesystem observations retain root attribution; platform live acceptance remains unperformed.

## Related Artifacts

RFC-001: informs; PRD-001/SPEC-001: active normative requirements; EVID-021: prebuild inventory; EVID-024: real old blocker; EVID-025: old tester PASS, untouched; EVID-026: fresh code corroboration.

## Final verification observations

Own scoped validate passed=true, error_count=0, warning_count=0. Canonical readback EVID-029 was draft and body byte-for-byte equal to submitted body. End scoped gets confirmed RFC-001 still active at2026-10-18T21:37:59.988494+00:00 with byte-identical canonical body, and EVID-025 still draft at2026-10-19T00:15:44.182127+00:00 with byte-identical body; neither was modified. End all29 per-file hashes still match, aggregate9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1, same exact five changes versus old freeze and24 unchanged; original405-byte .gitignore prefix unchanged. Both real/synthetic CLI smokes repeated exit0 with empty output. Every launched test/probe process has completed. Final owned update adds only these observations, followed by own validation/readback and canonical-body SHA256 handoff; no activation.



