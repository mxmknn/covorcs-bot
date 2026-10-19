---
depth: tactical
id: EVID-027
kind: evidence
last_modified_at: 2026-10-19T00:24:46.483381+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Fresh V2 independent architecture re-review — reviewer coworking architecture 20261019 02
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-027: Fresh independent V2 architecture re-review

## Structured Fields

evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata

reviewer_identity: reviewer/coworking-architecture-20261019-02
reviewer_role: architect-reviewer
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_manifest: .venv/verification/audit-freeze-v2.json
implementation_file_count: 29
implementation_sha256: 9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1
manifest_raw_sha256: b2021b436c591a9ca0b82989f6e7510268012e7b8226a97d0423a174aa80597e
base: unborn master; no HEAD/no commits; EVID-021 active prebuild inventory52 with28 absent product paths and original405-byte gitignore prefix
review_verdict: CONCERNS
scope: frozen V2 offline architecture; no activation, Guardian, Ship or complete live product acceptance
client_date: 2026-10-19

## Measurement

Fresh physical read-only Role B, distinct from generators and predecessor. Read scoped ground truth for RFC-001, ADR-001, PRD-001, SPEC-001, EVID-021 and full EVID-024; inspected all nine final package modules and relevant test/config/packaging/README/verification source. Full active planning bodies, including historical planning prose and PRD source appendix, supply normative context; current get metadata governs lifecycle. No prior PASS certifies this new freeze. EVID-022/023/025 are historical, EVID-020 is document-only Guardian evidence, and this is only one of the requested fresh specialist tracks.

Canonical get.body UTF-8 measurements, independently computed with Python hashlib on exact MCP body strings supplied through safely shell-quoted JSON argv (no projection stripping):
- RFC-001 active, 2026-10-18T21:37:59.988494+00:00,65791 bytes,e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177.
- ADR-001 active,2026-10-18T21:37:59.335862+00:00,34693 bytes,9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5.
- PRD-001 active,2026-10-18T20:51:11.875851+00:00,90673 bytes,7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d.
- SPEC-001 active,2026-10-18T20:51:12.611918+00:00,31762 bytes,624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8.
- EVID-024 draft BLOCKER,2026-10-19T00:13:51.183106+00:00,17358 bytes,b9d809796a9edb5be0a34d481e338a073f7c94d7c86ea11ea8d0bd244a1d35e4. Preserved unchanged historical refutation of V1; never relabeled PASS.

Initial and final successful manifest measurements: read each declared path, hash actual bytes and compare declaration;29 paths,zero mismatches each time. SHA256(json.dumps(files,sort_keys=True,separators=(",",":")).encode()) exactly equals new implementation digest both times. Comparing V1 declaration to V2 gives EXACTLY five changed paths: coworking_nearby/__main__.py,coworking_nearby/telegram_app.py,tests/test_privacy.py,tests/test_telegram_app.py,docs/verification.md; other24 identical and their actual bytes match. Previous architecture observations are reconsidered against actual final source and new execution, not inherited certification.

Read-only baseline commands: git symbolic-ref --short HEAD => exit0/master; git rev-parse --verify HEAD => exit128/fatal: Needed a single revision. No invented commit diff. Current .gitignore first405 bytes SHA256 2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a matches EVID-021 original. All29 manifest paths exist;28 were absent in declared prebuild inventory. EVID-021 baseline is a historical inventory, not a newly reconstructed Git revision.

forgeplan health => exit0,31 artifacts, RFC R_eff0.00 at risk,22 advisory phase mismatches, project needs attention. Suggested score was not executed. Health is not architecture proof or a gate decision.

A first attempted shell heredoc for hash inspection failed before Python execution: exit1, "can't create temp file for here document: operation not permitted". No tempfile was created; all subsequent Python commands use -c only. No sandbox bypass.

## Findings

### 1. Original EVID-024 blocker is closed for this freeze by the original probes

Both original in-memory interleavings were rerun on actual V2, preserving callback ordering: block fake Session.close with Events, register cleanup done callback that cancels caller, release close; then independently owned work gate, _defer caller, yield, register owned done callback cancelling caller, release gate. No files, real Bot/network or credentials are needed. Exact executed combined command:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import asyncio
from coworking_nearby.telegram_app import Application
from coworking_nearby.__main__ import _defer
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
    gate=asyncio.Event()
    async def work(): await gate.wait()
    owned=asyncio.create_task(work()); caller=asyncio.create_task(_defer(owned))
    await asyncio.sleep(0)
    owned.add_done_callback(lambda done: caller.cancel()); gate.set()
    result=(await asyncio.gather(caller,return_exceptions=True))[0]
    print("owned_exception",owned.exception(),"caller_outcome",type(result).__name__)
asyncio.run(check())'
```

Observed exit0:
```text
coordinator_done True coordinator_cancelled False coordinator_exception None
caller_outcome CancelledError pending 0 workers 0
owned_exception None caller_outcome CancelledError
```

V1's false FailStop outcome is absent in both original probes; cleanup succeeded and deferred caller cancellation propagates. Source examination confirms the distinction in BOTH paths: owned.cancelled() maps FailStop; owned.result() retrieves original RuntimeError/FailStop identity; successful owned completion breaks to caller CancelledError. No cleanup replacement, extra retry, deadline reset or unbounded await was introduced.

I also independently executed the16 parameterized regressions (completion/already_done x success/cancel/error/failstop x both functions). They challenge successful real Application close, repeated caller cancellation while pending, genuine owned cancellation, original exception identity and no residual tasks. All16 pass. They are stronger than only re-running the old pending-cleanup cancellation tests. No CRITICAL incident or new architecture blocker was observed.

### 2. Pure domain and snapshot boundary survive independent challenge

All six domain/config modules use stdlib with model-directed dependencies; render uses routes/models, never geo; no domain SDK/startup import. aiogram remains in telegram_app and explicit __main__ composition-root construction. Inert imports and offline catalog entrypoint are exercised by independent subprocess tests denying SDK/network/environment accesses.

Frozen values, nested button tuples and complete catalog tuple form detached immutable input/results. Catalog reads supplied path once and validates every record, including inactive/last invalid entries, before startup constructs session/Bot. Only geo filters active. No hot reload, demo fallback, catalog/Yandex fetch, address/ll extraction or invented enrichment. Reviewed strict JSON/UTF8/BOM/surrogate/duplicate members, exact13 fields, trim/codepoint lengths, numeric/null/default distinctions, normalized case-sensitive ids, Gregorian dates, rating provenance and URL raw grammar against C01–C08 and T01–T24 test source. Most catalog mutation tests require tempfiles and were inspected, not self-executed. Real[]/synthetic separation smoke did self-execute successfully.

Pure Haversine R6371000/clamp/raw-distance+id order, no rating/radius/city reorder, explicit request origin/destination and three route modes, six-digit coordinates/-0, HTML escaping once and parsed UTF16 maximum have passing independent oracles. Long organization URL remains untouched and outside text; no invented schema cap.

### 3. Admission and ownership boundaries withstand examined faults

One Application.poll loop awaits one feed_update, requests limit1, and uses scheduler committed cursor; no unordered update fanout, listener or second process. Global64/chat8 pending counts include active work. Capacity gate precedes no-await commit of queue/counters/worker/cursor. Task-creation rejection closes coroutine and rolls queue/counters back without advancing cursor. Precommit cancellation leaves admission untouched; postcommit feed-return cancellation preserves exactly one scheduler-owned envelope and cursor.

Self-run tests exercise capacity saturation64/8, creation rollback, both capacity waits, atomic observer, committed cursor after cancelled feed, cross-chat progress and source-bound response order. _retire and worker registry use task identity, preventing stale finally from removing successor. Scheduler-owned untouched queues survive ordinary worker death; active request released once, no replay of active send/confirmed prefix; exactly one successor handles FIFO, failed successor creation retains queue and sets failed. Done callback covers cancellation before worker first instruction. Notification is after accounting and cannot undo terminal release. Passing barrier/fault tests include worker_death_queued_successor_fifo, worker_death_partial_send_no_replay, supervisor_death_before_worker_first_step, worker_finally_exception and repeated_cancel_worker_finally_notification.

Residual: count bounds are not total byte/catalog-size bounds. One fetched unadmitted SDK payload is transient; head-of-line ingress blocking and crash loss remain accepted tradeoffs. No durability, exactly-once or measured load SLA follows.

### 4. Time, uncertainty and cleanup boundaries remain conditional but tested

RequestService starts fresh90s deadline at worker service, separate from admission-to-worker wait. Independent test holds queue120s, observes wait_ms120000 and first send121.1; queue time does not consume service budget. _wait_full retains one monotonic end for full1.1 pause and positive flood wait even with coarse .001 clock resolution; tests reject early1.0995 dispatch and preserve exact flood end. Full10s attempt fit checked before/after pause. Only decoded explicit rawHTTP429 with strict nonnegative integer retry_after permits one current-message retry, with request-shared15s total wait budget. Zero retained; second429, malformed429/non429 typedRetryAfter,5xx, redirect/decode/network/timeout ambiguity stops remaining delivery without replay/recursive notice.

_PostFacade disables redirects and request middleware; independent real pinned aiohttp protocol/connector wire-seam tests cover pooled/unpooled disconnect, partial write, short/UTF8/JSON responses and5xx. GET and unguarded307/308 positive controls detect actual replay at the seam. This supports transport behavior in pinned local stack rather than relying solely on fake SDK exceptions. All categories reply to source with allow_sending_without_reply=False; deletion never detaches.

One cleanup_task is shielded; bounded_tasks uses asyncio.wait and no unbounded wait_for cancellation join. Nonreset stage budgets2/10/2/2 and outer-finally close survive repeated caller cancellation, earlier errors and stubborn tasks in self-run virtual-clock tests, including full16s milestones. Cooperative terminal success/error/cancel yields zero counters/queues/workers/tasks; noncooperative expiry yields FailStop with no leak-free-success claim. Blocking event loop/arbitrary third-party cleanup is outside cooperative bound. Completion repair leaves these tests intact.

ProcessSinks suppresses raw logging/root/library/asyncio/warnings/stdout/stderr before formatting, with fixed enum/id/counter serializer and safe nested-sink restoration/verbosity. Actual pinned SDK hostile exception/cause, sink recursion, startup and signal tests pass at INFO/DEBUG. This is reference release and controlled process diagnostics, not physical memory zeroization or downstream history deletion.

### 5. CONCERN — platform and real-use acceptance are still open

Operational catalog is literally[]: syntactically valid, not useful real places. Owner-verified one-branch/name/city+house/coordinates/link/rating semantic records are absent. Actual live Telegram and manual two origins x three route modes were NOT performed. Unbounded SPEC-valid organization URL has no cap, so adapter transmission and mocked rejection containment cannot prove universal Telegram acceptance. Maximum parsed text fits, but button transport is a separate constraint. Complete AC-15/AX-05/NFR-06 acceptance remains withheld pending characterization/explicit owner resolution as applicable. No silent truncation, omitted button or new cap is proposed by reviewer.

No measured demand/load/SLA or durable queue. These concerns remain after race closure and explain CONCERNS rather than an unconditional final acceptance PASS. They do not establish a new deterministic offline architecture contradiction.

### 6. Release boundary is consistent, with provenance limits

Dockerfile pins exact Python3.12.15 base digest, public --require-hashes runtime install, explicit runtime COPYs and UID10001 with no app/catalog write bits. Compose one image-only service/noports/read-only data DIRECTORY mount/20s grace is consistent. README explicitly builds a USTAR whitelist context and forbids whole-repo docker build; COPY alone would not exclude secrets from submitted context. No .dockerignore is present; operator must use documented whitelist. Atomic same-directory candidate replacement then restart and compatible image+owner-approved catalog rollback with old poller stopped are documented; absent safe pair means remain stopped. No /about or NOTE-002 Working Moscow behavior exists in package; scope stays separate.

Static packaging subprocess tests passed. This physical reviewer did not run Docker/build/network/Compose or read actual .env. No new external compatibility research or image attestation claimed.

## Commands and observed results

Independent reviewer execution:
1. `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_telegram_app.py tests/test_privacy.py tests/test_packaging.py tests/test_render.py -k 'not accepted_long_org_url_unchanged'` => exit0,324 passed,1 deselected,1 warning in10.20s.
2. `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_catalog.py::test_real_empty_synthetic_separate` => exit0,1 passed,1 warning in0.05s.
3. `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_telegram_app.py::test_owned_completion_caller_cancellation_boundary tests/test_privacy.py::test_owned_completion_caller_cancellation_boundary` => exit0,16 passed,1 warning in2.36s. These16 are INCLUDED in324, not extra distinct coverage.
4. Original pure probes combined above => exit0, exact output above.
5. Repeated manifest/base verification command below => exit0 both successful runs, count29,zero mismatches,exact aggregate/raw digest,exact five changed paths,original gitignore prefix and unborn master outputs above.
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import json,hashlib,pathlib,subprocess
p=pathlib.Path('\''.venv/verification/audit-freeze-v2.json'\''); m=json.loads(p.read_text()); old=json.loads(pathlib.Path('\''.venv/verification/audit-freeze.json'\'').read_text()); f=m['\''files'\'']
print('\''count'\'',len(f),'\''aggregate'\'',hashlib.sha256(json.dumps(f,sort_keys=True,separators=('\'','\'','\'':'\'')).encode()).hexdigest(),'\''raw'\'',hashlib.sha256(p.read_bytes()).hexdigest())
print('\''mismatches'\'',[k for k,v in f.items() if hashlib.sha256(pathlib.Path(k).read_bytes()).hexdigest()!=v])
print('\''changed'\'', [k for k in f if f[k]!=old['\''files'\''][k]])
print('\''prefix'\'',hashlib.sha256(pathlib.Path('\''.gitignore'\'').read_bytes()[:405]).hexdigest())
for c in [['\''git'\'','\''symbolic-ref'\'','\''--short'\'','\''HEAD'\''],['\''git'\'','\''rev-parse'\'','\''--verify'\'','\''HEAD'\'']]:
 r=subprocess.run(c,capture_output=True,text=True);print(c,r.returncode,r.stdout,r.stderr)
'
```
6. Exact MCP-body hash Python code `for a in json.loads(sys.argv[1]): print(a["id"],len(a["body"].encode()),hashlib.sha256(a["body"].encode()).hexdigest())`, with actual safely quoted get bodies => exit0, pins above. Fresh scoped RFC/EVID024 reads before save: same statuses/stamps and byte-identical body strings.
7. cat/sed/rg read-only source/test/docs/role inspections => exit0; no source/config/test writes. AGENTS and loaded reviewer TOML were inspected. No need to invoke a workflow skill or extra reviewers from this assigned specialist task.

Each pytest warning is Unknown config option: cache_dir, expected with cacheprovider disabled. Network-denial fixture remains unchanged. No full reviewer self-run claimed; tempfile-dependent catalog cases and one long-URL render case were inspected. No weakened IO tests, real environment configuration, recursive venv scan, score/reason/activation or source mutation.

## Supplied provenance — NOT reviewer self-execution

Coder docs/user supply actual V2 RED6failed10passed2.53s and GREEN16passed2.01s; I did not witness historical RED. Controls already green and historical criterion-by-criterion TDD RED not universally established; no fabricated chronology. Coder full host706passed10.23s, Linux ARM64706passed12.84s are implementer observations.

Read durable .venv/verification/root-test-audit-v2.json and root-runtime-audit-v2.json as attributable ROOT observations only, both pin new implementation digest. Root reports independent host706passed11.19s exit0; Linux706passed13.39s exit0 with expected cache warning, original probes fixed and freeze unchanged. Runtime root record reports UID10001, Python3.12.15/GCC12.2.0/aarch64,11 /app runtime files,env_absent=true,dev source/test hashes match, real[] and synthetic CLI exit0 empty output, blank token exit1 one safe fail/startup record, offline SIGTERM exit0/0.6398876250023022s with safe start/stop only. Its11 runtime file hashes agree with relevant V2 manifest entries by inspection. compose_local_tag_now_verified_v2=true is ROOT provenance, not reviewer daemon inspection.

V2 runtime image sha256:b909f443edde64355c0e76c0aafa65251a4ac4a90001207b9a721b6b911e200a; dev sha256:bdb4dbad98d580edb3e03a5327e2e0c6b6c97447a9e8fc1be746a31611665e78. Local tags are mutable conveniences; hashes identify supplied images. Prior690/PASS/images do not certify V2. Root/coder data do not replace this reviewer's self-executed evidence or live acceptance.

## Result

CONCERNS. Original architecture blocker closed on actual V2 by both unchanged negative probes and16 outcome regressions;325 distinct permitted pytest cases pass. No new architecture blocker observed. Full product/live acceptance and platform URL delivery remain unresolved. Canonical RFC pin and29-file freeze unchanged at final checks; EVID-024 remains unchanged historical BLOCKER.

## Interpretation

Structured verdict supports the selected offline architecture and observed narrow repair; review_verdict CONCERNS preserves unresolved acceptance limitations. This is independent specialist evidence informing RFC-001, not a Guardian gate or authorization to Ship. Exactly ONE scoped new(kind=evidence,parent_id=RFC-001) created this draft and informs edge. Only EVID-027 updated. No target/depth/status/source/test/config/index mutation, activation or implementation. Main orchestrator must synthesize fresh independent tracks and lawful gates separately.

## Congruence Level Justification

CL3: same frozen workspace/package and pinned local runtime, actual deterministic asyncio interleavings and offline behavioral execution. Docker/root/coder/live facts are explicitly attributed or unperformed.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | informs |

## Validation Observations

Initial own-ID scoped validation passed all MUST with zero errors and one SHOULD body-links-drift, listing incidental normative/baseline/historical table references. This owned revision leaves only the actual RFC informs relation in the table; normative/baseline/history references remain in substantive prose. No other links or artifacts are mutated. Final validation and readback follow; no activation is performed.


