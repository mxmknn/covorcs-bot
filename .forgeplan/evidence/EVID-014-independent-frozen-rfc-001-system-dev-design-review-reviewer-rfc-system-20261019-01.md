---
depth: standard
id: EVID-014
kind: evidence
last_modified_at: 2026-10-18T21:17:51.389649+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Independent frozen RFC-001 system-dev design review — reviewer/rfc-system-20261019-01
---

# EVID-014: Independent frozen RFC-001 system-dev design review

## Structured Fields

evidence_type: measurement
verdict: inconclusive
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/rfc-system-20261019-01
reviewer_role: system-dev
generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:13:48.273934+00:00
reviewed_artifact_body_sha256: 42a5e7542164d77030b087c9e2f5ed6ba86de9759d3ca0309e153b341790d034
review_verdict: CONCERNS
client_date: 2026-10-19
review_scope: fresh independent design-only system-dev review; no implementation or runtime certification
status: draft

## Measurement

Fresh scoped forgeplan_get RFC-001 returned draft/standard and the exact frozen updated_at above. Read-only command python3 -c 'import sys,hashlib; print(hashlib.sha256(sys.argv[1].encode("utf-8")).hexdigest())' with the EXACT get.body as a shell-quoted argv value returned 42a5e7542164d77030b087c9e2f5ed6ba86de9759d3ca0309e153b341790d034, exit 0. This hashes the complete returned body including its embedded frontmatter, never a markdown projection.

Ground truth scoped gets: PRD-001 active updated_at 2026-10-18T20:51:11.875851+00:00; SPEC-001 active updated_at 2026-10-18T20:51:12.611918+00:00; ADR-001 draft updated_at 2026-10-18T21:08:52.191284+00:00. Same read-only exact-body SHA256 command for ADR returned 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5, exit 0. Metadata governs over historical body draft prose in active parents. Draft ADR is architecture input only; its activation remains independently gated.

Read AGENTS.md by cat (exit 0). Scoped health returned healthy with 12 advisory early-phase active mismatches; no routing, reason, score, lifecycle action or Build authorization inferred. No repository source/tests/pipeline written, packages installed, application tests executed, or subordinate certification delegated.

Primary-source calls actually observed:
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/client/session/base.py : check_response validates decoded response, accepts successful status+ok, then inspects truthy retry_after before HTTP error status classes. Thus typed RetryAfter alone is insufficient; zero retry_after does not trigger that branch.
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/client/session/aiohttp.py : make_request calls session.post once in this SDK layer, reads text, then calls check_response; network exception message can include underlying exception text. close awaits client close then 0.25s SSL settling. This does not prove all future aiohttp transitive behavior.
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/dispatcher/dispatcher.py : awaited feed_update is available; it logs update/bot identifiers in finally; unknown update path can warn with serialized update. RFC's process-wide raw-sink suppression is necessary, including warnings and INFO, not only DEBUG.
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/exceptions.py inspected; exception objects are sensitive, not safe log fields.
- https://pypi.org/pypi/aiogram/3.31.0/json : Python >=3.10,<3.15 and pydantic >=2.4.1,<2.14; other runtime dependencies include aiohttp, aiofiles, certifi, magic-filter, typing-extensions.
- https://pypi.org/pypi/pydantic/2.13.5/json : Python >=3.9; exact pydantic-core==2.46.5, plus annotated-types/typing-extensions/typing-inspection.
- https://pypi.org/pypi/pydantic-core/2.46.5/json and https://pypi.org/pypi/pytest/9.1.1/json retrieved; pytest Python >=3.10. Direct proposed versions are metadata-compatible with 3.12, not an installed graph proof.
- https://raw.githubusercontent.com/docker-library/official-images/master/library/python lists 3.12.15-slim-bookworm with amd64 and arm64v8 among architectures. Registry manifest URL named in RFC returned Internal Error through web; exact digest was NOT independently authenticated.
- https://core.telegram.org/bots/api#getupdates and #sendmessage/#inlinekeyboardbutton inspected; sendMessage limit is after entity parsing. No universal organisation URL acceptance inferred.
A read-only urllib metadata command failed DNS resolution (exit 1); web primary-source calls above supplied metadata instead. No installation fallback attempted.

Proposed pins reviewed: Python 3.12.15; aiogram==3.31.0; pydantic==2.13.5; pydantic-core==2.46.5; pytest==9.1.1; python:3.12.15-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258. A future COMPLETE runtime/dev transitive lock with exact hashes, platform wheels, resolver identity and --require-hashes install in real isolated 3.12.15 remains implementation acceptance. Host 3.14 and unavailable Docker cannot establish target success.

## Findings

1. MATERIAL CONCERN — accepted queued work is discarded on an unexpected worker exit. TC-3 ordered ingress says unexpected worker exit finally "drains/releases its admitted queued envelopes via controlled cancellation"; Invariant 4 simultaneously promises bounded backpressure without silent drops. These are already admitted, potentially offset-acknowledged requests, and normal operation's per-request exception containment does not cover this explicitly separate worker-exit path. Unlike documented process crash or operator shutdown, a worker failure can discard up to seven waiting envelopes while the process continues, with no terminal per-envelope outcome specified. This weakens AX-06/07 and the stated accepted-work guarantee. Remediation requested: distinguish intentional shutdown cancellation from unexpected worker termination; define supervised continuation/ownership transfer of untouched FIFO envelopes, or explicitly resolve the changed accepted-work contract. Never replay a partially sent active request. Add a fault oracle killing a worker with multiple queued requests while another chat progresses, asserting each untouched accepted envelope's ordered disposition, counters and replacement-worker ownership. Current generic release_success_error_cancel/cleanup-race names do not establish this outcome.

2. MATERIAL CONCERN — cancellation acceptance lacks explicit transaction-boundary and repeated-cancellation oracles. TC-3 requires enqueue+counter+worker creation atomically, then offset advance; shutdown cancels ingress, drains 10s, cancels/awaits workers, closes <=2s. The fault plan names shutdown_finite and release checks but does not explicitly cover cancellation after enqueue before feed_update returns/offset update, worker creation failure after counter increment, a second shutdown signal during worker finally/counter notification, or cancellation/exception during session.close and its follow-up await. Those cases can break accounting, retain contexts, skip close, or leave awaits outside claimed finite lifecycle bounds. Remediation requested: specify ownership/commit outcome at each admission boundary and outer finally guaranteeing close despite cleanup error; add deterministic barrier-based repeated cancellation, ingress cancellation while full, worker-finally failure and close-timeout/error oracles. Assert exact offset, no duplicate admission, zero orphan tasks/references and stated shutdown timing stages. This is a design/test-contract concern, not a claim that absent implementation failed.

3. CHALLENGED / SUPPORTED design boundaries — direct limit=1 polling, active-inclusive 64 global/8 per chat admission before next offset, one enqueue-only awaited handler, no-await FIFO worker ownership and explicit cross-chat head-of-line overload form a coherent bounded envelope design. No local batch/fanout or overload rejection is needed. Queue delay excluded from 90s service deadline is explicit; no latency SLA claimed. Every outbound category binds source ReplyParameters and rejects deleted-source fallback. Full 1.1s pause and 10s attempt fit, full retry_after <=15s/request and deadline admission, one additional retry per current message only on confirmed raw HTTP429, stop on second429, non429 typedRetryAfter, 5xx, network/timeout/decode ambiguity, and no confirmed cursor replay are conservative. Real pinned pre-check guard tests must include retry_after=0 (SDK truthiness), 429 malformed/ok or mismatched payload, 5xx with retry_after, and status-preserving rejection. Pinning must include the transport graph; SDK-level one post is not proof of all transitive transport replay behavior.

4. CHALLENGED / SUPPORTED privacy and contract alignment — AC01-18 and AX01-12 each map to owned modules and named future checks; all C01-C08 and T01-T24 retain strict acceptance, normalization, whole-file/inactive failure, optional/source/date and URL constraints. No newly detected product/schema relaxation. C01/C02 shared CLI/startup; C03 context only in deliberate standalone channel; C04/C05 closed immutable schema/owner semantics; C06 exact URL syntax preserved without fetch/cap; C07/C08 date/source dependencies. All T01-24 have specific future cases, including atomic last/inactive failures and CLI equivalence. AC01/02/12 and AX01-05 UI, AC03-09/13 and AX10/11 pure geo/routes, AC10/11/14/15 and AX09/12 schema/render, AC16-18 and AX06-08 FIFO/fault/privacy were cross-checked against active parent wording. No test execution inferred from mapping.
ADR interfaces match the flat models/config/catalog/geo/routes/render/telegram_app/composition layout, stdlib token-free CLI, immutable snapshot, render not importing geo, no external Yandex request, one process and no history. None of this makes draft ADR active.
Privacy boundary includes raw library/root/asyncio/warnings, loop/top-level handlers and stdout/stderr before Bot; DEBUG is not an exception. Adversarial retained-sink schema tests must exercise actual pinned SDK warning/error paths and startup/shutdown exceptions, including failures before successful Bot construction. Reference cleanup is not zeroization. Text-size arithmetic is conservatively below 4096 after entity parsing; unrestricted organisation URLs remain an explicitly unresolved platform boundary, not permission to cap/omit valid fields.

## Result

CONCERNS: two material design/fault-acceptance gaps above require closure before an unqualified system-dev PASS. No code/runtime/delivery PASS is claimed. Exactly one new Evidence, EVID-014, informs RFC-001 via parent_id creation. Only this Evidence body may be updated; keep draft. No self-creator certification, activation or gate decision.

## Interpretation

S10-S13 remain applicable: alternatives/reason-attempt transparency (S10), requirements/tradeoffs (S11), normative contracts and future tests (S12), exact freeze and independent role evidence (S13) were challenged here. This specialized review is not independent ADI, complete multi-role coverage or Guardian PASS. Creator's blocked reason attempt is not independent reasoning evidence. Future activation and Build readiness remain separate orchestrator obligations.

## Congruence Level Justification

CL3: direct exact-revision document inspection in the same project, independent assigned reviewer identity distinct from generator. Measurement is document/hash/source inspection only, not executed application behavior.

## Residual Risk

Even after requested closure: cooperative cancellation and all process output interception need actual runtime fault proof; volatile crash/shutdown interruption is not durable delivery; bounded ingress counts envelopes, not catalogue bytes or external Telegram retention; overload can stall later chats. Full dependency graph/3.12 install, exact container digest, arbitrary valid URL platform behavior, owner semantic catalogue correctness and manual two-origin/three-mode acceptance remain unproven. No absent project tests run.

## Related Artifacts

| Artifact | Relation / revision |
|---|---|
| RFC-001 | EVID-014 informs RFC-001; exact frozen timestamp/hash above |
| PRD-001 | read-only active normative input; 2026-10-18T20:51:11.875851+00:00 |
| SPEC-001 | read-only active normative input; 2026-10-18T20:51:12.611918+00:00 |
| ADR-001 | read-only draft architecture proposal; 2026-10-18T21:08:52.191284+00:00 |

## Validation Observations

Observed scoped validate EVID-014: passed=true, 0 errors, 1 SHOULD body-links-drift warning (read-only normative inputs in Related Artifacts are not additional Evidence links). Scoped graph confirms EVID-014 -->|informs| RFC-001. Fresh post-creation RFC get still returns draft/standard, updated_at 2026-10-18T21:13:48.273934+00:00; exact get.body hash command still returns 42a5e7542164d77030b087c9e2f5ed6ba86de9759d3ca0309e153b341790d034, exit 0. Scoped get does not expose outer projection YAML and no scoped projection-read tool is available; YAML informs inspection remains unperformed under the explicit scoped-only artifact-access restriction. Graph relation is verified, not substituted for a claimed YAML observation. Final Evidence get/hash and validation are recorded in handoff.

