---
depth: standard
id: EVID-031
kind: evidence
last_modified_at: 2026-10-19T10:33:18.516209+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Narrow ingress timeout delta independent review reviewer/coworking-ingress-timeout-20261019-01
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-031: Independent first-live ingress timeout repair review

## Structured Fields

evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata

reviewer_identity: reviewer/coworking-ingress-timeout-20261019-01
reviewer_role: code-reviewer
generator_identity: coder/coworking-20261019-01
planning_creator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_sha256: dc95ecedbb842ff9ee034a2f4a3757fc0ac69f0026eb80741b7f9622684a4461
prior_implementation_sha256: 9c73a7270c617f792561dfdc9f5a2b5dbe75cc53470e5e9f5cbd431544ba87a1
manifest_path: .venv/verification/audit-freeze-ingress.json
implementation_file_count: 29
base: unborn master; EVID-021 prebuild inventory; no HEAD
review_verdict: PASS
scope: NARROW DELTA ONLY; independent offline timeout/cancellation code review, no full Ship or activation certification

## Measurement

Fresh scoped MCP forgeplan_get RFC-001 confirmed canonical metadata active and exact updated_at above. Independently SHA256-hashed the exact returned body UTF-8 with safely shell-quoted Python -c: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177, exit0. Historical draft prose does not override canonical metadata. forgeplan health exit0 reported needs attention/advisory phase mismatches; no score, reason, pipeline or gate mutation followed.

## Findings

### 1. PASS — complete pinned inventory and narrowly isolated production change

Own command PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c with json/pathlib/hashlib loaded audit-freeze-ingress.json and audit-freeze-v2.json, compared identical key sets and independently hashed every declared file. Observed count29, mismatch[], same keys True, exactly three changed paths: coworking_nearby/telegram_app.py, tests/test_telegram_app.py, docs/verification.md. SHA256 of json.dumps(files,sort_keys=True,separators=(',',':')).encode() returned dc95ecedbb842ff9ee034a2f4a3757fc0ac69f0026eb80741b7f9622684a4461. No real environment file was accessed; .env.example alone is in the declared whitelist. git rev-parse --verify HEAD returned128, consistent with unborn base, not an invented Git revision.

New source SHA256 9ab5b1a3884acfed29894aa5b3dc6de4df86b1b4abac4ff4e21ab6f9a5cdaafd; test d842b462fd8b64a7ec917b0225f3747a32e3c4368ce88829d83e4d556bac0a6b; documentation a698f4301882a73a4110fd00863445cc9257b1f94656cb3d9f3ffabc55636e62.

Own hashlib verification of .venv/verification/v2-linux/coworking_nearby/telegram_app.py and tests/test_telegram_app.py matched their V2 manifest hashes. difflib.unified_diff then showed exactly ONE production argument request_timeout=3 ->15 at telegram_app.py:441 and an appended61-line test; all prior test content remains identical. V2 staged docs/verification.md was absent, so the multi-file diff command ended1 after successfully emitting the source and test diffs; no claim of a historical documentation text diff. Current documentation was read and hashed.

### 2. PASS — timeout budget fixes demonstrated latency without changing ingress ordering or shutdown ownership

Reviewed poll and shutdown/bounded_tasks directly. Poll retains server timeout1, limit1, allowed message/edited_message, awaited feed_update, committed cursor and error backoff5. Source diff proves send10/service90/retrywait15/fullpause1.1,64global/8chat, schema/default catalogue[] and private logging unchanged. RFC does not mandate a numeric client timeout3. Local pinned aiogram dispatcher.py:215–217 explicitly computes session.timeout + polling_timeout to prevent false TimeoutError, corroborating the need for client headroom, without claiming its dispatcher is this application's ingress.

Read sanitized .venv/runtime/poll-diagnostics.json: parent observations timeout3 TelegramNetworkError/noHTTP at3.005/3.006s; timeout10 HTTP200/empty at6.181s. I did not execute live API calls, getMe, webhook queries or stop/start pollers. Those observations motivate finite15, but do not prove future network availability.

Regression test_poll_six_second_response_and_prompt_shutdown uses actual asyncio.timeout(kwargs['request_timeout']) with a six-second virtual monotonic response, not a bare constant assertion or six seconds of wall-clock network work. A real SDK Update validates source100; processing occurs after clock advance3+3, cursor101 and second poll offsets[None,101], timeout1/limit1 and no ingress errors are asserted. Shutdown cancels pending second poll at the same virtual instant, two callers and a later call retain the identical completed coordinator, pending0/workers0. This challenges the risk that a larger request budget would extend shutdown: existing cleanup independently cancels/joins ingress within2. Residual: deterministic cooperative cancellation does not prove noncooperative native/network code or all future latency below15.

### 3. PASS — own independent focused execution; prior tests were not weakened

Exact own command:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_telegram_app.py::test_poll_six_second_response_and_prompt_shutdown tests/test_telegram_app.py::test_shutdown_stage_deadlines_outer_finally tests/test_telegram_app.py::test_owned_completion_caller_cancellation_boundary tests/test_privacy.py
```
Observed exit0: 41 passed,1 warning in2.87s. Warning Unknown config option: cache_dir follows deliberately disabled cacheprovider. Includes regression, staged shutdown deadlines, completion/cancellation boundary cases and entire privacy module. Unchanged autouse conftest denies external sockets/DNS. No installation, source/test mutation, Docker or live service use.

Initial hash command via heredoc was denied because read-only sandbox cannot create a temporary file; reran using Python -c successfully. Initial RFC hash shell construction had quoting parse error; corrected with proper single-quote escaping and obtained canonical hash. These are reviewer command limitations/errors, not product defects. No historical RED is claimed from my execution. Coder target1/ingress-privacy138/host707 observations remain generator-attributable only. I did not run or certify full host/Linux suites or image builds; parent ingress-root/verification.json is not required evidence for this narrow conclusion and was not consumed.

### 4. Scope restriction — full live/product gate remains open

Uncapped organization URL versus Telegram platform acceptance remains unresolved. Manual two origins and three route modes remain unperformed here. Existing active EVID-026–029 concern the prior V2 freeze, not this new implementation digest; their status cannot certify changed bytes. Fresh scoped EVID-030 read confirms Guardian CONCERNS and unclosed full gate. This focused PASS does not replace fresh Guardian PASS, authorize Ship, activate artifacts or claim manual acceptance. Owner catalogue connection/live bot manual Telegram acceptance authorization is narrower than full Ship. No new narrow-delta blocker observed.

## Congruence Level Justification

CL3: canonical target stamp/body, all29 actual file hashes, hash-matched previous source/test snapshots, direct code/SDK contract inspection and own offline focused execution. Full-suite/container/live observations are explicitly not self-certified.

## Related Artifacts

RFC-001 informs, created atomically through parent_id. No existing artifact mutated; only this new Evidence body updated. Default depth/status remain untouched and Evidence stays draft.

## Result

NARROW DELTA ONLY PASS. Residual live/manual/platform risks and Guardian CONCERNS remain open. No activation, gate decision, secret read, real.env access, installation, source write, pipeline change or live/Docker operation.

