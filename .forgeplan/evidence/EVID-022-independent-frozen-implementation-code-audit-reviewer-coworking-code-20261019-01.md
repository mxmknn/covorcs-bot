---
depth: standard
id: EVID-022
kind: evidence
last_modified_at: 2026-10-19T00:11:52.654116+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Independent frozen implementation code audit reviewer coworking code 20261019 01
---

# Independent final implementation audit — RFC-001

## Structured Fields
evidence_type: measurement
congruence_level: 3
verdict: supports

## Review Metadata
reviewer_identity: reviewer/coworking-code-20261019-01
reviewer_role: code-reviewer
generator_identity: coder/coworking-20261019-01
planning_generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:37:59.988494+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
implementation_sha256: 87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106
reviewed_manifest: .venv/verification/audit-freeze.json
manifest_sha256: 33c5a02a0e9e778dc1327a65b376726fb975d034dfd8321f46c8cbf25f8f2127
base: unborn master; EVID-021 prebuild inventory; no HEAD
review_verdict: PASS

## Measurement
Independent physically read-only Role B review of the frozen implementation, not implementer certification, Guardian gate, activation or Ship approval. Scoped forgeplan_get supplied RFC-001, PRD-001, SPEC-001 and EVID-021 ground truth. Health was healthy with 22 advisory early-phase mismatches; those are not runtime proof. Metadata active governs over historical draft text. NOTE-002 editorial content and /about remain a separate unimplemented draft.

All 29 nonempty files in the manifest were independently read and SHA256 checked. Aggregate is SHA256 of UTF-8 json.dumps(actual_file_hash_map, sort_keys=True, separators=(',', ':')), with no trailing newline. This reproduces the exact implementation pin. Reviewed files:
.env.example; .gitignore; Dockerfile; README.md; compose.yaml; coworking_nearby/__init__.py; coworking_nearby/__main__.py; coworking_nearby/catalog.py; coworking_nearby/config.py; coworking_nearby/geo.py; coworking_nearby/models.py; coworking_nearby/render.py; coworking_nearby/routes.py; coworking_nearby/telegram_app.py; data/coworkings.json; docs/verification.md; examples/coworkings.synthetic.json; pyproject.toml; requirements-dev.lock; requirements.lock; tests/conftest.py; tests/test_catalog.py; tests/test_config.py; tests/test_geo.py; tests/test_packaging.py; tests/test_privacy.py; tests/test_render.py; tests/test_routes.py; tests/test_telegram_app.py.

git symbolic-ref --short HEAD returned master; git rev-parse --verify HEAD exited128, fatal: Needed a single revision. No Git diff from HEAD exists and no baseline was fabricated. EVID-021 identifies 28 formerly absent product paths and original .gitignore; first405 bytes still hash to 2f0e6cd89d3dfd3966d93cc5ff29ebb5c1378da44c761526949aed1362778e7a. Working data/coworkings.json is exactly b'[]', with synthetic examples separate.

## Findings
1. PASS — Strict shared catalogue acceptance challenged against SPEC C01–C08 and RFC TC-1. Startup and standalone both call load_catalog; exact dataclass field allowlist covers all13 fields, strict types exclude booleans as numbers, inactive/last invalid records fail atomically, duplicate JSON members and unpaired surrogates are rejected before schema acceptance. Explicit trim/codepoint limits, case-sensitive normalized ID uniqueness, Gregorian ASCII dates, URL authority/path/percent rules and conditional Yandex provenance match the contract. Independently executed18 in-memory cases patched Path.read_bytes only: invalid types/ranges/dates/authority/dot segments/encoded slash/duplicate keys/surrogates/BOM/duplicate IDs/invalid inactive record rejected; valid leap day and a30000-character URL accepted. No files written. Syntax does not establish owner factual branch/address/link correspondence.

2. PASS — Selection/routes/rendering challenged with source and independent expected-value tests: raw Haversine metres (R6371000 and clamp), raw distance then Unicode ID sorting before limit, active filtering without radius/rating/city, explicit latitude-longitude origin-first route pairs, pd/mt/auto modes, six decimals and normalized negative zero. Russian card order, rating source/date, absence fallbacks, half-up display at999/1000 and all five catalogue text fields escaped exactly once agree with RFC. Tests parse queries and visible HTML rather than only comparing production helpers. Owner live browser acceptance remains unperformed.

3. PASS — Lifecycle challenged beyond happy-path counts. Scheduler no-await commit combines active-inclusive64/8 capacity, queue, worker registration and cursor, rolls back task-creation failure, and checks cancellation before commit. Scheduler owns untouched FIFO; worker identity guards both retirement paths including pre-first-step cancellation and stale callbacks. Active release precedes fault seams. Tests exercise full capacity, postcommit feed cancellation with next offset, successor faults, partial-send cancellation and no prefix replay, concurrent two-origin isolation, cooperative empty terminal state. There is no durable replay or exactly-once guarantee; process restart loses volatile work as specified.

4. PASS — Retry and timing boundary challenged at raw transport and service layers. Only decoded raw HTTP429 with ok=false, integer error_code429 and nonnegative integer retry_after produces FloodRefusal;5xx/redirects/non429 SDK exceptions stop. Guarded POST disables redirects and middleware replay. Wire tests below the actual connector demonstrate one POST on disconnect/partial body/short response/decode/5xx, including pooled connections, plus GET retry positive control. Service retries only current message once, shares15s waits, enforces90s service and10s attempt budgets, always binds source reply with no unthreaded fallback. _wait_full retains one monotonic end for both1.1s pauses and positive flood waits; coarse1ms callback tests explicitly prove no send at1.0995 and no early positive retry completion. Virtual-time coverage establishes algorithmic lower bounds, not hard realtime under a blocked event loop.

5. PASS — Privacy and bounded shutdown challenged with actual process hooks and cancellation barriers. ProcessSinks installs before configuration, SDK/session construction and polling, drops raw Logger/Handler records before formatting, guards warnings/loop/top-level/unraisable/stdout/stderr and uses fixed safe schema. Hostile str/repr and nested secret-bearing exceptions remain unformatted. Single shielded cleanup coordinator uses2/10/2/2 stages, outer-finally close, deferred repeated cancellation and bounded fail-stop; tests exercise16s milestones and earlier-stage faults. This does not guarantee physical RAM zeroization, deletion of Telegram/browser history, or cooperative cleanup of arbitrary noncooperative code. No universal low-level OS/native output containment is claimed.

6. Residual acceptance boundaries — Arbitrary SPEC-valid organization URLs can exceed actual Telegram platform acceptance; no approved URL length cap exists, and implementation preserves them. Fabricated platform refusal demonstrates conservative containment only. Owner real catalogue and live two origins times all three route modes remain unperformed. Historical per-criterion RED chronology for some earlier tests is unavailable; I do not infer it from current GREEN. These known limitations do not reveal a new frozen offline implementation defect and do not authorize full live acceptance.

## Commands and observed results
Actual independent command:
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q --capture=sys -p no:cacheprovider tests/test_config.py tests/test_geo.py tests/test_routes.py tests/test_render.py tests/test_telegram_app.py tests/test_privacy.py
Result:303 passed,1 setup error,1 warning in7.28s, exit1. test_render.py::test_accepted_long_org_url_unchanged needs tmp_path; physical sandbox has no writable temporary directory. This is a verification environment limitation, not a passed test or product failure.

Actual follow-up, identical command plus -k 'not test_accepted_long_org_url_unchanged':
303 passed,1 deselected,1 warning in7.39s, exit0. Warning: unknown cache_dir because cacheprovider disabled. No tests were edited or weakened. Catalogue tmp_path suite not executed here; test bodies were examined critically and18 independent in-memory cases passed via python -c/unittest.mock.patch.object(Path,'read_bytes',return_value=raw). Read-only Python hashlib/Path checks and git commands above exited successfully except expected unborn HEAD128.

External observations supplied by root: final frozen macOS full suite690 passed in10.56s. Coder reports Linux ARM64690 passed in12.94s, runtime image sha256:93a6a3263aa5f568ced199483ad74f1f6a9e74ddc7634e258a675e67dc7ee87c and dev image sha256:8a76c52f2adb01bd9cbf26d6c9b3e73f55714406ba6b6bb934aef8a65e204479. These are not my executions or independent container certification. Root Linux rerun was pending at assignment; no result is invented.

## Result and interpretation
PASS for the exact frozen offline implementation audit within the stated evidence limits. No newly identified blocker. Full live acceptance and activation remain separate decisions. Exactly one new draft Evidence created with parent_id RFC-001 and automatic informs link. Only this owned EVID was updated; no source/tests/roles/planning artifact, depth, activation, score, or pipeline mutation. Real .env and container environment/config never read; no live Telegram/Yandex/network use.

## Congruence Level Justification
CL3: exact local frozen files, scoped canonical target and same-workspace actual execution by an independently assigned code-reviewer. External full-suite/container observations remain explicitly attributed.

## Related Artifacts
EVID-022 informs RFC-001.

## Final pin verification
Canonical UTF-8 body SHA256: RFC-001 e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177; PRD-001 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d; SPEC-001 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8. Historical extra final LF in RFC projection is not a canonical-body change. Final handoff rechecks canonical bodies/stamps and all29 file hashes/aggregate; Evidence exact-body hash is measured after readback and emitted separately to avoid a self-referential hash.

