---
depth: standard
id: EVID-025
kind: evidence
last_modified_at: 2026-10-19T00:15:44.200091+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Independent final offline tester review reviewer/coworking-tests-20261019-01
---

---
id: EVID-025
kind: evidence
status: draft
links:
  - target: RFC-001
    relation: informs
---

# EVID-025: Independent final offline tester review

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/coworking-tests-20261019-01
reviewer_role: tester
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_sha256: 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106
manifest_path: .venv/verification/audit-freeze.json
base: unborn master; no HEAD; EVID-021 pre-build inventory
review_verdict: PASS
review_scope: frozen offline implementation and substantive test review; conditional acceptance only, no live acceptance or Ship authorization

## Measurement

Scoped forgeplan_get RFC-001 returned active and the exact updated_at above. Independently hashed the exact returned body UTF-8 via safely shell-quoted Python hashlib: the canonical SHA256 equals the pin above. Historical draft prose does not override active metadata. Read active PRD-001 and SPEC-001 acceptance requirements and EVID-021 pre-build inventory, all nine application modules, all test files, release configuration and README/docs/verification.md. forgeplan health exited 0, healthy with advisory phase mismatches. No score/reason/activation, source/test/config edits, Git changes, Docker invocation, real .env access or live network calls.

Independently recomputed each of the manifest's exact 29 named files with hashlib.sha256(Path(path).read_bytes()). All matched. Aggregate calculation: hashlib.sha256(json.dumps(actual_files, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest(); observed 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106. Repeated after tests/probes: identical. Only .env.example is included; no real .env was opened, read, hashed or printed. git rev-parse --verify HEAD reported fatal: Needed a single revision; symbolic-ref reported master. No invented diff/commit. Current .gitignore first 405 bytes hash 2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a, equal to EVID-021's original inventory; appended ignores are part of the frozen manifest.

Inspected exact test function names with rg before execution. Self-executed, process completed exit 0:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_render.py tests/test_telegram_app.py tests/test_privacy.py tests/test_packaging.py -k 'not long_org_url'
```

Observed 308 passed, 1 deselected, 1 warning in 9.78s. The actual excluded name is tests/test_render.py::test_accepted_long_org_url_unchanged. The shorter selector matches this exact name; the suggested long_organisation_url spelling would not. Expected warning: Unknown config option cache_dir because cacheprovider was deliberately disabled. No test weakening, bytecode, cache or temporary file creation. Autouse offline socket/DNS guard remains present. Read-only sandbox prevents tmp_path file creation even under /tmp: the 381-case catalogue file suite was reviewed statically, not self-executed. The excluded renderer case is also tmp_path-dependent.

Additional self-executed inline PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c probe, exit 0: 20 independent public load_catalog probes, with unittest.mock.patch.object(Path, "read_bytes", return_value=synthetic_bytes) solely replacing input bytes in memory. Checked empty/default acceptance; duplicate members; BOM/invalid UTF-8/surrogate/root rejection; bool coordinate and 10**400 range rejection; invalid inactive entry; Gregorian leap-century and Unicode-date rejection; yandex cross-field dependency; encoded dot URL and nonliteral443 rejection; unknown field; trimmed duplicate id; valid-first/invalid-last atomic rejection; astral Unicode/valid leap date; 20,000-character organisation URL retained exactly through loader and render_card. Observed "20 independent in-memory public-loader probes passed; no file writes or network". This does not substitute for filesystem/CLI catalogue suite execution.

## Result

Independent executed subset and additional probes passed. No blocking code/test defect found in this frozen offline scope. Supplied root records, explicitly not self-executed by this tester:

- .venv/verification/root-test-audit.json: host full suite 690 passed in 10.56s exit0; Linux ARM64 full suite 690 passed, 1 expected cache warning in 12.81s exit0.
- .venv/verification/root-runtime-audit.json: final dev package/tests hashes match freeze; runtime image sha256:93a6a3263aa5f568ced199483ad74f1f6a9e74ddc7634e258a675e67dc7ee87c; dev image sha256:8a76c52f2adb01bd9cbf26d6c9b3e73f55714406ba6b6bb934aef8a65e204479.
- Root runtime observation: exactly 11 whitelist files (nine package .py, requirements.lock, real catalogue), UID10001, Python3.12.15/aarch64, no .env. Both real[] and synthetic catalogue commands exit0 with empty output; blank token exit1 with one fixed safe fail/startup JSON record; offline synthetic-token SIGTERM exit0 in 0.5648504170021624s with safe start/stop only.

Root supplied results provide full filesystem/Linux/runtime coverage beyond this sandbox; they are attributed observations, not commands this tester ran. Implementer timings in docs differ and are separately attributed historical/final generator runs. No CI or live-service result exists in this review.

## Findings

### 1. Timing and refusal challenges pass behavioral checks, including the repaired coarse-clock lower bound

Challenged _wait_full against asyncio's early timer dispatch with loop resolution .001: test_coarse_clock_strict_lower_bound_waits actually ran both no-flood and positive2-second flood variants, asserting no send at1.0995, retained monotonic end1.1/3.1/4.2 and sends exactly at1.1 and4.2. Production repeats remaining sleep until its fixed end, without epsilon or timer-deadline reset. Test ManualClock normally uses fine virtual resolution but this regression explicitly restores the coarse condition. Thus the repair is challenged rather than hidden by the clock fixture.

Finite delivery tests check full10-second attempt availability after pause, late refusal/service90 cutoff, no partial retry wait, shared wait<=15, one retry of current message, second429 stop, and no confirmed-prefix replay. Queue wait120s is measured independently and does not consume service90. Only raw HTTP429 with decoded ok=false/error_code429/integer nonnegative retry_after is retryable; zero survives SDK truthiness, positive waits finish fully. Malformed429, non429 typed RetryAfter, redirect/5xx/decode/disconnect/partial-response ambiguity stop remaining cards. These executed tests support TC-3 rather than an exactly-once delivery claim.

### 2. Admission and worker lifecycle tests challenge races and ownership

Executed barrier tests cover full capacity64/8, precommit cancellation admitting nothing, task-creation rollback closing its rejected coroutine, postcommit cancellation preserving cursor, death before worker first instruction, identity-checked successor, stale cleanup, per-chat FIFO and cross-chat progress. test_worker_death_partial_send_no_replay confirms the ambiguous active request is not restarted and untouched queued requests continue once. Cooperative terminal success/error/cancel tests assert zero pending/counts/queues/workers and committed cursor; fault seams exercise finalizer/notification/successor failures.

Production commit/cursor/accounting is no-await; release occurs once before injectable finalizer; stale worker identity cannot retire its successor. Shutdown is separately intentional queue disposal. Executed repeated cancellation tests preserve one coordinator and original2/10/2/2 stage limits, close after earlier failure, 16s combined milestones, fail-stop rather than unbounded cancellation join. These are cooperative/event-loop bounds; noncooperative tasks are deliberately released by the test only after bounded fail-stop observation. Physical RAM erasure or hard real-time termination is not established.

### 3. Transport and privacy proof reaches real SDK paths, with an explicit fake wire boundary

RecordingTransport replaces TCPConnector connection creation below the actual aiohttp connector/pool/writer/parser and aiogram. Executed fresh/pooled disconnect, partial request, short response, malformed UTF8/JSON,5xx and redirects assert wire attempt counts and no transitive replay; unguarded GET-disconnect and307/308 POST redirect positive controls demonstrate that the harness can observe replay. Facade recreation and decoded real SDK Message results are checked; hostile aiohttp middleware is disabled for sends. This is substantive offline negative-path integration, not a live Telegram result.

Executed hostile formatter/str/repr, nested SDK exceptions, warnings/lastResort/loop hooks, stdout/stderr/buffer, recursive sink, startup/close and INFO/DEBUG tests show no hostile formatting and only fixed safe JSON paths. Queue timing is bounded and carries no chat/source/coordinates/URL/token. Source review confirms process boundary precedes config/Bot and controlled nested restoration. These Python sink tests do not prove arbitrary native code cannot write raw OS file descriptors.

### 4. Schema, pure selection and rendering preserve acceptance with bounded offline claims

Reviewed SPEC C01–C08/T01–T24 against loader and parameterized tests: closed13 fields, exact trim/codepoint limits, default/null distinctions, strict JSON duplicate/nonfinite/Unicode rejection, huge integer checks before conversion, atomic inactive/last failure, Gregorian ASCII dates, strict authority/path/percent rules and rating provenance. All file-suite results remain supplied root observations; own20 probes independently challenged central negative paths without altering production logic.

Executed independent metre oracles/permutation/tie cases check Haversine raw sorting and active-only filtering, no radius/rating influence; parsed two origins x three modes checks endpoint and latitude/longitude order, precision and negative zero. Executed HTMLParser-visible card tests verify escaped data once, exact Russian source/date/fallback/button layout and worst-case UTF16 bound<=2556<4096. Static packaging assertions alone mirror declared release requirements and cannot prove an image build; supplied root runtime inspection supplies that separate layer.

### 5. Chronology is honest; residual product acceptance is explicitly incomplete

docs/verification.md distinguishes supplied prior668 baseline, observed11failed/3passed RED, subsequent GREEN stages, initial Linux failures, historical688 images and final690 repair builds. It explicitly declines individual historical acceptance RED reconstruction. Coarse-clock repair reports real2failed RED and intermediate assertion/float advancement corrections; no fabricated historical RED or independent certification is inferred from generator prose.

Real data/coworkings.json remains [] as expected; no owner-approved branch/address/coordinate/link/rating semantics are certified. Manual two origins x all three modes, useful live Telegram delivery and universal acceptance of arbitrary unbounded SPEC-valid organisation URLs remain UNPERFORMED. Executed long-URL fake400 case proves conservative containment and unchanged serialization, not platform acceptance. The tmp_path renderer case exclusion is a local platform-limit residual; own memory probe helps retained-URL logic, supplied full690 covers its filesystem execution. Complete AC-15/AX-05/NFR-06 acceptance remains withheld; never silently cap/truncate/omit URLs. NOTE-002 /about is separate draft and intentionally unimplemented, not a missing implemented-RFC feature. Load/demand/SLA and arbitrary noncooperative dependency behavior remain unmeasured.

## Interpretation

PASS applies to the pinned offline implementation/tests with the explicit residuals above. Independent execution supports the implementation's essential behavior and root-supplied full suite/runtime proof complements sandbox limits. This is not live acceptance, a Guardian decision, activation, or Ship authorization. No critical defect discovered. Exactly one new draft Evidence was created via scoped new(parent_id=RFC-001), establishing informs; only this EVID body was updated.

## Congruence Level Justification

CL3: exact current active RFC body/revision and the exact29-file frozen implementation, directly inspected and independently exercised on its local Python environment. Platform/live/runtime claims retain separate attribution and limits rather than being generalized from mocks.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | informs |
| PRD-001 | read acceptance requirements |
| SPEC-001 | read normative C01–C08/T01–T24 |
| EVID-021 | read pre-build inventory |

