---
depth: standard
id: EVID-023
kind: evidence
last_modified_at: 2026-10-19T00:13:34.049112+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Final independent security review reviewer coworking security 20261019 01
---

# EVID-023: Final independent frozen implementation security review

## Structured Fields

evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata

reviewer_identity: reviewer/coworking-security-20261019-01
reviewer_role: security-expert
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_sha256: 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106
path_manifest: .venv/verification/audit-freeze.json; exactly 29 product paths and their SHA256 values
base: unborn master; no HEAD; EVID-021 prebuild inventory plus original 405-byte gitignore prefix
review_verdict: PASS

PASS is limited to the independently inspected offline security boundary of this exact implementation and active RFC. It is not complete product acceptance, production/live proof, activation, Guardian certification, or permission to Ship.

## Measurement

Actual physical Role B reviewer read .codex/agents/forgeplan-reviewer.toml, all canonical ground-truth PRD-001, SPEC-001, ADR-001, RFC-001 and EVID-021 via scoped ForgePlan get. Active metadata governs over historical draft prose. Read all nine application Python modules, Dockerfile, compose.yaml, pyproject.toml, blank .env.example, gitignore, relevant README/verification provenance, privacy/packaging tests and relevant transport/lifecycle/renderer tests; inspected installed aiogram and aiohttp sources. No score/reason provider, activation, runtime mutation, product write, real .env access, live Telegram/Yandex call or Docker execution. Exactly one Evidence was created with parent_id RFC-001 and automatic informs relation; only this owned Evidence is updated.

Health was read before substantial review: healthy, with advisory active/early-phase mismatches. It is not an authorization decision.

Before review all 29 file hashes matched manifest. Independently hashed UTF8 json.dumps(files,sort_keys=True,separators=(',',':')): implementation SHA above. Hashed actual canonical get.body using Python hashlib, not whole projected Markdown: exact RFC SHA above. After executed review/tests canonical get returned same ACTIVE status, exact updated_at, byte-identical body; all 29 paths again matched and map hash remained exact. No frozen path is a symlink; package whitelist currently contains exactly nine .py files.

Implementation is demonstrably NONEMPTY against declared EVID-021 baseline: 28 previously absent paths now exist with nonzero sizes; original .gitignore is now542 bytes and its first405 bytes SHA256 is 2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a, exactly the baseline prefix. Actual git symbolic-ref --short HEAD returned master; git rev-parse --verify HEAD returned128. No Git base/head/diff is invented.

## Findings

### 1. Privacy boundary challenged before formatting — PASS with bounded scope

__main__.main installs ProcessSinks before loop construction and run installs nested loop guard before settings, catalogue, session and Bot. Nested guard retains original safe sink. Logger.handle AND Handler.handle are replaced before filters/formatters, existing handlers detached, lastResort neutralized; raw stdout/stderr and their original aliases/buffer are discarded. warnings, sys exception/unraisable and asyncio loop hooks emit fixed enum events. emit_safe accepts exact enum types, opaque32hex id, integer-only bounded count0..64 and queue wait0..86400000; it serializes a fresh allowlisted record and suppresses recursive emission.

Executed test_all_process_sinks_INFO_DEBUG challenges hostile __str__/__repr__, root/library/SDK/asyncio/py.warnings records, late-added handlers, lastResort, warnings, nested causes, top-level/loop contexts and stream writes; no hostile formatting touched and only safe schema survives. Actual installed SDK connector failure and recursive sink path are also exercised. Executed startup failure before Bot, nested guard, verbosity and repeated SIGINT/SIGTERM tests passed. Source never logs raw exceptions/config/updates/routes or chat/user ids. Residual boundary is Python application diagnostics through the inspected sinks, not arbitrary native fd writes or hostile code with authority to replace guards; no physical memory zeroization/downstream history deletion claim.

### 2. SSRF, parser/coercion and markup attacks — PASS; platform acceptance remains unresolved

catalog.py has no HTTP client or fetching path. rg over all application modules found URL construction/parsing only; routes host is constant HTTPS Yandex and catalogue URL stays button data. _valid_url compares full ASCII authority against exactly yandex.ru/yandex.com optionally literal443, raw /maps boundary, controls/percent/dot/encoded slash constraints. Local validation is not a claim about remote redirect destinations or actual place identity. There is no bot catalogue-URL fetch/SSRF edge.

Independent in-memory attack command below rejected12 malicious URLs,5 coordinate coercion candidates, duplicate JSON keys/NaN/unpaired surrogate and overwrote both forged marker directions. _guard_origins runs before SDK Pydantic, removes existing marker and recomputes per-update validity; invalid numeric fields cannot become accepted coordinates through SDK coercion. Immutable per-request origin and source id feed routes/replies, no shared latest origin. Renderer performs html.escape(...,quote=True) once on catalogue text and leaves keyboard URL data intact. Executed HTML/UTF16/route parsing and isolation tests passed.

Substantive residual: normative schema allows arbitrarily long valid organization URLs. Independently accepted100000 trailing data characters; adapter boundary test verifies unchanged10000-character URL and containment of a fabricated HTTP400, NOT real platform acceptance. The temp-backed long-URL loader/render test could not set up in this sandbox. Complete AC-15/AX-05/NFR-06 universal delivery acceptance is withheld. Do not cap, truncate or omit a schema-valid organization button to hide this conflict. Owner catalogue and live two origins x three modes remain outstanding; actual data is [].

### 3. Real installed transport challenged below SDK — PASS; no exactly-once guarantee

Installed Python3.12.15, aiogram3.31.0, aiohttp3.14.5. Read aiogram AiohttpSession.make_request: each API request is POST, response text read then check_response. aiohttp client.py permits persistent retry only for IDEMPOTENT_METHODS (GET,HEAD,OPTIONS,TRACE,PUT,DELETE), excluding POST; middleware can replay unless overridden, and307/308 normally preserve POST/body.

Guarded session facade forces allow_redirects=False and middlewares=() per POST; raw base _session remains owner for closing/recreation. Executed positive controls show unguarded307/308 cause two POSTs with same body and GET disconnect retries; guarded API sends issue one POST on307/308. Real connector/pool/writer/parser seam replaces only connection creation, retaining actual installed SDK/aiohttp machinery. Executed pooled/unpooled disconnect, partial/short response, UTF8/JSON decode and5xx faults show no POST replay. Zero429 and deliberately replaying session middleware test confirms only two explicit service attempts and zero middleware calls.

check_response rejects3xx/5xx before SDK; only raw429 with decoded ok exactlyFalse, integer error_code429 and nonnegative integer retry_after creates FloodRefusal (including0). Wrong/malformed429 and non429 typed exceptions do not authorize retries. RequestService permits one additional current-message attempt, shared full wait budget15, full1.1s pause and10s attempt fitting90s service, no confirmed prefix replay or recursive error notice. _wait_full loops to fixed monotonic end, including early timer dispatch; coarse-clock regression passed. Cancellation propagates through finally. Residual: ambiguous acceptance is intentionally stopped and may leave partial delivery; no exactly-once/restart replay promise.

### 4. Ownership, cancellation and fail-stop challenged — PASS for cooperative model

Source inspection confirms Scheduler owns FIFO/admission/cursor, atomic no-await commit/rollback/release and identity-checked successor retirement. No user envelope is stored after cooperative terminal cleanup. Application uses one shielded coordinator; repeated cancellation cannot restart stage deadlines. Ingress2 + drain10 + workers2 + close2 seconds, outer-finally session close and failed owned joins produce FailStop. Executed worker-before-first-step death, task creation rollback, commit/cancel barriers, partial-send no replay, notification faults, repeated cancellation, stage deadlines and terminal counters tests passed. Startup Bot failure closes acquired session. No universal cancellation guarantee for a blocked event loop/noncooperative library; fail-stop is not leak-free success.

### 5. Supply-chain/deployment review — PASS for static frozen inputs, image provenance unverified here

Independent parser found18 runtime and25 development pinned entries, each with SHA256 hashes; installed versions match all applicable entries (Windows-only colorama excluded). Docker base is pinned by SHA256, pip uses public index and --require-hashes, Dockerfile COPY permits only runtime lock, nine package .py and real empty catalogue; USER10001:10001. Runtime Dockerfile never installs dev lock/tests or copies .env. README streams a USTAR whitelist of Dockerfile, runtime lock, package .py and catalogue rather than repository context; inspected frozen package paths are regular files. Compose declares one image-only bot service, no ports, readonly data directory and20s grace; no automatic extra poller/replica. Five executed packaging/child-process tests passed, including independent CLI without SDK/network and blank-token executable controlled failure. This establishes source/build recipe properties, not actual image contents or registry authenticity.

Parent provenance ONLY: host full suite690 passed10.56s; coder Linux690 passed12.94s; root Linux rerun pending at assignment. Supplied runtime image sha256:93a6a3263aa5f568ced199483ad74f1f6a9e74ddc7634e258a675e67dc7ee87c and dev image sha256:8a76c52f2adb01bd9cbf26d6c9b3e73f55714406ba6b6bb934aef8a65e204479 were NOT built, run or authenticated by this reviewer. Hash locks do not establish vulnerability-freedom; no network advisory/registry audit was performed. No claim that development tools already present in upstream Python base are absent.

## Commands and observed results

All commands run in /Users/mxmknn/Documents/ChatGPT/tg-bot-org. No commands read real .env or resolved environment. Initial heredoc inspection was denied by shell before execution (temporary file prohibited); subsequent Python used -c with shell-quoted literal code.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_privacy.py tests/test_telegram_app.py tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_render.py
```

Actual exit1:303 passed,1 warning,1 setup error in7.27s. Only error tests/test_render.py::test_accepted_long_org_url_unchanged: tmp_path fixture FileNotFoundError "No usable temporary directory found". Sandbox denies temp writes, including /tmp; not a source defect and not reported as test PASS. Warning unknown cache_dir is caused by disabled cacheprovider. Tests were awaited to completion; no weakening/skipping/modification.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_packaging.py
```

Actual exit0:5 passed,1 same warning in2.21s. Total this reviewer physically observed308 passing tests plus one environment-blocked setup. No claim of executing full690 or temp-backed catalogue suite.

Independent attack/lock inspection exact command:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import sys,json,re,hashlib,pathlib,importlib.metadata as md
from coworking_nearby.catalog import _valid_url,_record,CatalogError,_pairs,_constant,_check_unicode
from coworking_nearby.telegram_app import _guard_origins,ORIGIN_MARKER
bad=["https://yandex.ru@evil.invalid/maps","https://evil.invalid@yandex.ru/maps","https://yandex.ru.evil.invalid/maps","https://yandex.ru./maps","https://yandex.ru:0443/maps","https://yandex.ru/maps/%2e%2e/x","https://yandex.ru/maps/a%2fb","https://yandex.ru/maps/?q=%0aX","https://yandex.ru/maps/\\evil","https://yandex.ru/maps/?q=%5c","https://yandex.ru/maps/?q=%GG","https://yandex.ru/maps/\u2000x"]
assert all(not _valid_url(u) for u in bad)
long="https://yandex.ru/maps/?x="+"a"*100000
assert _valid_url(long)
for val in [True,"0",None,1e309,10**400]:
 try:_record(dict(id="synthetic",name="x",address="x",latitude=val,longitude=0),pathlib.Path("synthetic"),0,{})
 except CatalogError:pass
 else:raise AssertionError("coercion")
for coord,forged,expected in [(True,False,True),(55,True,False)]:
 u={"message":{"location":{"latitude":coord,"longitude":37}},ORIGIN_MARKER:forged};_guard_origins({"result":[u]});assert u[ORIGIN_MARKER] is expected
for payload in ['\''[{"id":"a","id":"b"}]'\'','\''[NaN]'\'','\''["\\ud800"]'\'']:
 try:root=json.loads(payload,object_pairs_hook=_pairs,parse_constant=_constant);_check_unicode(root)
 except ValueError:pass
 else:raise AssertionError("JSON ambiguity")
for file in ["requirements.lock","requirements-dev.lock"]:
 s=pathlib.Path(file).read_text();blocks=re.split(r"\n(?=[a-zA-Z0-9_-]+==)",s)
 pins=[]
 for b in blocks:
  match=re.search(r"^([a-zA-Z0-9_-]+)==([^ \\\n;]+)",b,re.M)
  if match:
   assert re.search(r"--hash=sha256:[0-9a-f]{64}",b)
   n,v=match.groups();pins.append((n,v))
   if n!="colorama":assert md.version(n)==v,(n,v,md.version(n))
 print(file,"hashed pinned entries",len(pins),"installed match excluding Windows-only colorama")
print("independent attacks: 12 URL rejects; 100000-byte URL retained; 5 coordinate coercions rejected; both forged marker directions overwritten; duplicate/NaN/surrogate rejected")
print("python",sys.version.split()[0],"aiogram",md.version("aiogram"),"aiohttp",md.version("aiohttp"))
'
```

Actual exit0:12 URL rejects;100000-character data tail accepted unchanged by URL predicate;5 coordinate coercions rejected; both forged markers overwritten; duplicate/NaN/surrogate rejected.18 runtime/25 dev hashed pinned entries, applicable installed versions match. Python3.12.15/aiogram3.31.0/aiohttp3.14.5.

Freeze verification performed before/after with this computation (actual results29 paths/no mismatches and exact implementation SHA):
```python
m=json.loads(pathlib.Path(".venv/verification/audit-freeze.json").read_text())
f=m["files"]
bad=[p for p,h in f.items() if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h]
hashlib.sha256(json.dumps(f,sort_keys=True,separators=(",",":")).encode()).hexdigest()
```
Canonical RFC SHA measured with hashlib.sha256(canonical_get_body.encode()).hexdigest(); post-review canonical body equality also checked directly.

## Result

PASS for scoped frozen offline security review, no critical/blocking security issue observed. Nonempty implementation frozen unchanged; active RFC still unchanged at exact stamp/body hash. Only owned EVID-023 draft created/updated, informs RFC-001. No live production proof, owner semantic acceptance or universal URL-delivery certification. NOTE-002 future Moscow/about remains separate; /about is not implemented and is outside this review.

## Interpretation

Main orchestrator must retain residual platform/live/container-proof limits and perform its own gate/activation workflow. This reviewer does not activate, score, reason for generator, change target/status, or certify uninspected production behavior.

## Congruence Level Justification

CL3 same-workspace exact canonical target, exact frozen source hash map, installed SDK source and independent offline execution by distinct physical security reviewer; no extrapolation to live external systems.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | EVID-023 informs RFC-001 |

