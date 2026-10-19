---
depth: tactical
id: EVID-028
kind: evidence
last_modified_at: 2026-10-19T00:24:20.197048+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Fresh independent V2 security review reviewer coworking security 20261019 02
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-028: Fresh independent physical V2 security review

## Structured Fields

evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata

reviewer_identity: reviewer/coworking-security-20261019-02
reviewer_role: security-expert
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_sha256: 9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1
path_manifest: .venv/verification/audit-freeze-v2.json; exactly 29 product paths
prior_path_manifest: .venv/verification/audit-freeze.json
prior_implementation_sha256: 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106
base: unborn master; no HEAD; EVID-021 prebuild inventory and original gitignore prefix
review_verdict: PASS

PASS is confined to the frozen V2 offline security boundary and narrow cleanup race closure. It is not broad architecture certification, universal platform acceptance, activation or Ship authorization.

## Measurement

Fresh physical Role B review, distinct from code/planning generators. Read runtime .codex/agents/forgeplan-reviewer.toml and scoped canonical ForgePlan get inputs PRD-001, SPEC-001, ADR-001, RFC-001, EVID-021, historical security EVID-023 and architecture BLOCKER EVID-024. Actual metadata governs historical draft prose. Health inspected first: exit0, RFC at-risk and advisory phase mismatches; no score/reason/provider/gate call followed. Only one new Evidence created, parent_id RFC-001 with automatic informs; only this own Evidence body updated. All old artifacts remain untouched.

Canonical RFC get.body, safely single-quoted as argv to Python hashlib, measured 65791 UTF8 bytes and exact SHA above; whole Markdown projection and its extra EOF LF were not hashed. Post-review scoped get remains ACTIVE at exact same timestamp and byte-identical body.

Read every declared product path for independent SHA256 before and after review. Both runs: all29 match, none symlink; map hash is SHA256 UTF8 json.dumps(files,sort_keys=True,separators=(',',':')), exact V2 SHA above. Independently computed prior aggregate matches its declared SHA. Exactly five changes: coworking_nearby/__main__.py, coworking_nearby/telegram_app.py, tests/test_privacy.py, tests/test_telegram_app.py, docs/verification.md. Other24 hashes identical to prior inputs BEFORE using old attack context. Old EVID-023 PASS certifies V1 only and is not adopted as V2 certification.

Nonempty implementation independently verified: 29 product paths total376013 bytes; 28 paths were absent in EVID-021 declared prebuild inventory. Current gitignore first405 bytes hash2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a matches original inventory. git symbolic-ref --short HEAD exit0 master; git rev-parse --verify HEAD exit128, Needed a single revision. No Git revision/diff invented.

No source/test/docs/config changes, real .env read/hash/printing/interpolation/transmission, resolved Docker configuration/environment, live Telegram/Yandex/network call, Docker execution/mutation, temp file or test weakening. An initial read-only Python heredoc was rejected by zsh before execution because temp creation is prohibited; subsequent probes used shell-quoted python -c. No test failed on temporary storage in the permitted selected run.

## Findings

### 1. EVID-024 completion/caller-cancellation BLOCKER is closed for the reviewed V2 boundary

Inspected both actual catch blocks: Application.shutdown and __main__._defer now distinguish owned.cancelled() from owned.done(). Owned cancellation becomes FailStop; owned.result() retrieves a completed noncancelled task's actual failure before deferred caller cancellation; successful completion breaks and propagates CancelledError. Original RuntimeError/FailStop identity is retained, not replaced. The result retrieval is synchronous, introduces no second coordinator/close/deadline and does not format exception values. Completion/pending and already-done outcomes differ only in scheduling, not exception priority.

Executed regression matrix16 cases in selected suite: completion/already_done x success/cancel/error/failstop x both paths; all passed. Tests use barriers/callbacks, repeated caller cancellation, actual Application success cleanup, exception identity, coordinator identity, zero counters/workers and no pending tasks. Already-done cancel is injected immediately before awaiting completed owned work. Existing repeated-signal, stage-deadline, session-close error/timeout and terminal-accounting tests also passed. Source stages2/10/2/2 and fixed monotonic waiting remain unchanged by repair.

Separately executed an independent six-case in-memory probe (exact code below), repeatedly cancelling caller before gate release and again in owned done callback. Observed shutdown/defer success -> CancelledError; owned private exception -> identical PrivateError; owned cancellation -> FailStop. PrivateError.__str__/__repr__ raise if touched: neither called. No pending tasks; shutdown successful second invocation reused coordinator and did not close twice. This independently reproduces the EVID-024 interleaving with corrected outcome and challenges exception priority beyond ordinary error strings. Narrow closure does not amend historical EVID-024 or certify unrelated architecture. Noncooperative tasks/blocked event loops remain outside leak-free cooperative success.

### 2. Process privacy remains enforced before formatting in V2

Reinspected actual main/run and ProcessSinks source. main installs guards before loop construction, run before config/catalog/session/Bot. Nested guard preserves safe sink. Logger.handle and Handler.handle suppress raw records before filters/formatters; lastResort, warnings, sys/unraisable/loop hooks and stdout/stderr aliases/buffer are guarded. Safe events require exact Event/Stage enum,32hex random id and integer bounded count0..64; queue wait capped86400000. Recursive sink emission is suppressed.

Executed INFO/DEBUG hostile str/repr tests, root/library/SDK/asyncio/warnings sinks, late handlers, nested exception causes, startup before Bot, actual installed SDK connector failure, sink recursion, nested guard and repeated SIGINT/SIGTERM cases. No hostile formatter touched and raw synthetic token/location/URL absent from captured output. Repaired owned exception propagation reaches fixed safe startup/cleanup/process events in executable; exception objects are never supplied to serializer. CLI catalogue diagnostics deliberately retain required escaped path/field/id context separately. Residual scope excludes native direct file-descriptor writes or hostile code replacing guards, physical RAM zeroization and Telegram/browser history deletion.

### 3. Parser, markup and no-fetch boundaries revalidated against unchanged sources

Reinspected catalog/config/geo/routes/render and adapter marker handling. Exact int/float origin checks reject bool/string/null/nonfinite/oversized integers. _guard_origins removes attacker marker and recomputes validity before SDK Pydantic; venue precedence and malformed metadata are explicitly handled. Request envelope preserves source/origin locally. HTML catalogue strings use escape(...,quote=True) once; keyboard URLs remain data. Catalog authority is exact ASCII HTTPS yandex.ru/yandex.com with optional literal443; raw path, controls, percent and dot constraints prevent arbitrary button authorities. No catalogue URL fetching exists; routes builds constant-host URLs, so no bot-to-Yandex SSRF edge.

Fresh independent in-memory attack run exit0:12 malicious URLs rejected;5 coercion inputs rejected;both forged marker directions overwritten;duplicate JSON keys/NaN/surrogate rejected. Predicate accepts100000-character URL data tail, confirming no invented schema cap. Executed parser/SDK marker, HTML, UTF16, parsed two-origin three-mode routes, isolation and source-bound response tests passed.

Residual: syntactically accepted URL does not certify destination semantics or remote redirects. Arbitrary valid organization URL lengths remain an external Telegram delivery limitation; mock400 containment and unchanged adapter URL are not universal platform acceptance. The explicitly deselected temp-backed long-URL render test was not executed. Complete AC15/AX05/NFR06 acceptance remains withheld.

### 4. Actual installed SDK/aiohttp replay boundaries pass renewed execution

Inspected installed aiogram3.31.0 AiohttpSession.make_request/close and aiohttp3.14.5 ClientSession._request. SDK performs POST; aiohttp persistent retry requires IDEMPOTENT_METHODS, excluding POST. Redirect307/308 otherwise preserve POST/body. Per-request middleware overrides session middleware. V2 _PostFacade still forces allow_redirects=False and middlewares=(), preserving raw session owner for close/recreation.

Executed actual SDK/aiohttp wire-seam tests replacing only connector creation, retaining real pool/protocol/writer/parser: unguarded307/308 positive controls replay twice, guarded API emits one POST; GET disconnect positive control retries; pooled/unpooled disconnect/partial/short/UTF8/JSON/5xx faults do not replay POST. Replaying middleware is bypassed. check_response rejects3xx/5xx before SDK classification; only decoded raw429 with ok exactlyFalse, integer error_code429 and integer nonnegative retry_after authorizes FloodRefusal. Malformed/typed/non429 ambiguity cannot authorize retries.

Executed zero429, second429 stop, full wait1.1, attempt10/service90 fit, shared wait budget15, confirmed-prefix no replay, coarse-clock lower-bound, source ReplyParameters and deleted-source rejection/isolation cases passed. Only one additional current-message attempt is allowed; ambiguous failures terminate remaining delivery, preserving possible partial delivery rather than claiming exactly-once. Session recreation/owned cleanup tests passed. This is installed offline transport proof, not live delivery proof.

### 5. Frozen deployment inputs preserve least exposure; external observations attributed

Reinspected pinned Dockerfile, compose, README whitelist and packaging tests. Python3.12.15 base pinned SHA256; runtime pip --require-hashes public index; COPY only runtime lock, nine current regular .py files and real[] catalogue; USER10001:10001 with app/data write bits removed. README streams USTAR whitelist, avoiding whole-repo context. Static recipe does not itself ensure secret exclusion if an operator uses a different context. Runtime recipe installs no dev lock/tests or .env. Compose one image-only service/no ports/read-only data bind/20s grace; operator must maintain exclusive poller deployment.

Fresh lock scan:18 runtime/25 development hashed exact pins, installed versions match applicable entries excluding Windows-only colorama. Five packaging subprocess/static tests passed, including no SDK/network CLI and blank-token pre-network safe failure. No network advisory/registry audit or vulnerability-freedom claim. No container was run/built/inspected by this reviewer.

Supplied coder provenance only: RED6failed10passed; GREEN16passed; full host706/10.23s and Linux706/12.84s. Read existing root-test-audit-v2.json and root-runtime-audit-v2.json as supplied root observations: host706/11.19s, Linux706/13.39s, original two race probes corrected; runtime UID10001, source hash map match, whitelist/no.env, validator smokes, blank-token safe failure and offline SIGTERM exit0/0.639887625s. Their implementation SHA matches this freeze; these are not my executed tests/container proof. Supplied runtime image sha256:b909f443edde64355c0e76c0aafa65251a4ac4a90001207b9a721b6b911e200a and dev sha256:bdb4dbad98d580edb3e03a5327e2e0c6b6c97447a9e8fc1be746a31611665e78 were not authenticated here.

Actual catalogue remains[]. Owner semantic validation and live two origins x three modes are UNPERFORMED. No new /about handler; NOTE-002 remains separate future draft. Demand/load/SLA and owner data are outside this security PASS.

## Commands and observed results

Working directory /Users/mxmknn/Documents/ChatGPT/tg-bot-org. Tests/processes awaited to completion.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_privacy.py tests/test_telegram_app.py tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_render.py tests/test_packaging.py --deselect=tests/test_render.py::test_accepted_long_org_url_unchanged
```

Actual exit0:324 passed,1 deselected,1 warning in9.56s. Warning Unknown config option cache_dir follows disabled cacheprovider. Existing socket-denial autouse fixture unchanged. Full706 is supplied provenance only.

Independent probes below used exact shell single-quoted Python code with embedded apostrophes escaped; command prefix PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c. All exit0:

```python
import asyncio
from coworking_nearby.telegram_app import Application,FailStop
from coworking_nearby.__main__ import _defer
async def check():
 for path in ('shutdown','defer'):
  for outcome in ('success','error','cancel'):
   gate=asyncio.Event();entered=asyncio.Event();closes=[]
   class PrivateError(Exception):
    def __str__(self): raise AssertionError('private formatting')
    def __repr__(self): raise AssertionError('private formatting')
   failure=PrivateError()
   async def work():
    entered.set();await gate.wait()
    if outcome=='error':raise failure
    if outcome=='cancel':raise asyncio.CancelledError()
   class Session:
    async def close(self):closes.append(1);await work()
   a=Application(None,(),3)
   if path=='shutdown' and outcome=='success':
    caller=asyncio.create_task(a.shutdown(Session()))
    await entered.wait();owned=a.cleanup_task
   else:
    owned=asyncio.create_task(work())
    if path=='shutdown':a.cleanup_task=owned
    caller=asyncio.create_task(a.shutdown(None) if path=='shutdown' else _defer(owned))
    await entered.wait()
   caller.cancel();await asyncio.sleep(0);caller.cancel();await asyncio.sleep(0)
   owned.add_done_callback(lambda _,c=caller:c.cancel())
   gate.set();result=(await asyncio.gather(caller,return_exceptions=True))[0]
   assert (isinstance(result,asyncio.CancelledError) if outcome=='success' else result is failure if outcome=='error' else isinstance(result,FailStop))
   if path=='shutdown':
    assert a.cleanup_task is owned and a.scheduler.pending==0 and not a.scheduler.workers
    if outcome=='success':
     await a.shutdown(Session());assert len(closes)==1
   assert not [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
   print(path,outcome,type(result).__name__,'priority/no-format/no-leak PASS')
asyncio.run(check())

```

Observed six PASS lines: shutdown/defer success CancelledError, error PrivateError, cancel FailStop; no formatting/no leak.

```python
import json,pathlib,re,importlib.metadata as md
from coworking_nearby.catalog import _valid_url,_record,CatalogError,_pairs,_constant,_check_unicode
from coworking_nearby.telegram_app import _guard_origins,ORIGIN_MARKER
bad=['https://yandex.ru@evil.invalid/maps','https://evil.invalid@yandex.ru/maps','https://yandex.ru.evil.invalid/maps','https://yandex.ru./maps','https://yandex.ru:0443/maps','https://yandex.ru/maps/%2e%2e/x','https://yandex.ru/maps/a%2fb','https://yandex.ru/maps/?q=%0aX','https://yandex.ru/maps/\\evil','https://yandex.ru/maps/?q=%5c','https://yandex.ru/maps/?q=%GG','https://yandex.ru/maps/\u2000x']
assert all(not _valid_url(u) for u in bad)
assert _valid_url('https://yandex.ru/maps/?x='+'a'*100000)
for val in [True,'0',None,1e309,10**400]:
 try:_record(dict(id='synthetic',name='x',address='x',latitude=val,longitude=0),pathlib.Path('synthetic'),0,{})
 except CatalogError:pass
 else:raise AssertionError('coercion')
for coord,forged,expected in [(True,False,True),(55,True,False)]:
 u={'message':{'location':{'latitude':coord,'longitude':37}},ORIGIN_MARKER:forged};_guard_origins({'result':[u]});assert u[ORIGIN_MARKER] is expected
for payload in ['[{"id":"a","id":"b"}]','[NaN]','["\\ud800"]']:
 try:root=json.loads(payload,object_pairs_hook=_pairs,parse_constant=_constant);_check_unicode(root)
 except ValueError:pass
 else:raise AssertionError('JSON ambiguity')
for file in ['requirements.lock','requirements-dev.lock']:
 s=pathlib.Path(file).read_text();pins=[]
 for b in re.split(r'\n(?=[a-zA-Z0-9_-]+==)',s):
  m=re.search(r'^([a-zA-Z0-9_-]+)==([^ \\\n;]+)',b,re.M)
  if m:
   assert re.search(r'--hash=sha256:[0-9a-f]{64}',b)
   n,v=m.groups();pins.append(n)
   if n!='colorama':assert md.version(n)==v
 print(file,len(pins),'hashed pins/installed match')
print('12 URL rejects; 100000-tail accepted; 5 coercions rejected; 2 forged markers overwritten; duplicate/NaN/surrogate rejected')

```

Observed18/25 hashed pins installed match;12 URL rejects;100000-tail accepted;5 coercions rejected;2 markers overwritten;duplicate/NaN/surrogate rejected.

Pre/post freeze command prefix same, exact code:

```python
import json,hashlib,pathlib,subprocess
v=json.loads(pathlib.Path('.venv/verification/audit-freeze-v2.json').read_text());p=json.loads(pathlib.Path('.venv/verification/audit-freeze.json').read_text())
for m in (v,p):print('aggregate',hashlib.sha256(json.dumps(m['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest())
for n,h in v['files'].items():
 assert n!='.env'
 assert hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest()==h,n
 assert not pathlib.Path(n).is_symlink()
print('matched',len(v['files']),'changed',[n for n in v['files'] if v['files'][n]!=p['files'][n]])
print('prefix',hashlib.sha256(pathlib.Path('.gitignore').read_bytes()[:405]).hexdigest(),'bytes',sum(pathlib.Path(n).stat().st_size for n in v['files']))
for a in [['git','symbolic-ref','--short','HEAD'],['git','rev-parse','--verify','HEAD']]:
 r=subprocess.run(a,capture_output=True,text=True);print(a,r.returncode,r.stdout,r.stderr)

```

Observed both times29 matched,5 declared changed,24 unchanged, aggregate exact, git master/unborn. Post-review canonical scoped get body is byte-identical to initial; its initial actual-body hashlib measurement is65791 bytes/exact RFC SHA.

## Result

PASS for this exact V2 scoped security review. EVID-024 cleanup race independently closed at reviewed boundary; no critical/blocking security defect observed.324 selected tests and independent probes physically executed. All29 frozen paths and canonical RFC unchanged after review.

## Interpretation

No historical PASS carried forward as current proof, no old BLOCKER silently ignored. Residual live/platform/owner risks remain. Exactly one new draft Evidence informs RFC-001; no activation, target/status mutation, score/provider reasoning, source fix or gate decision.

## Congruence Level Justification

CL3: actual same-workspace frozen V2 source, canonical artifact, installed local SDK and independent read-only offline execution. No extrapolation to external/live or container execution by this reviewer.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | informs |
| PRD-001 / SPEC-001 / ADR-001 | read-only normative context |
| EVID-021 | declared prebuild baseline |
| EVID-023 / EVID-024 | historical V1 security/architecture challenges |



