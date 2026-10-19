---
depth: tactical
id: EVID-017
kind: evidence
last_modified_at: 2026-10-18T21:24:09.905627+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Independent repaired RFC lifecycle system review reviewer rfc system 20261019 02
---

# EVID-017: Independent repaired RFC-001 system-dev document review

## Structured Fields

evidence_type: measurement
verdict: confirmed
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/rfc-system-20261019-02
reviewer_role: system-dev
generator_identity: creator/rfc-coworking-20261018-01
maintenance_identity: maintainer/rfc-lifecycle-20261019-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:21:34.881083+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
review_verdict: PASS
review_scope: independent system-dev document design only
client_date: 2026-10-19
status: draft
depth: standard

## Measurement

Read AGENTS.md and .codex/agents/forgeplan-reviewer.toml using read-only cat, exit 0. Scoped health returned healthy with 12 advisory early-cycle active mismatches; this is not Build permission. Scoped forgeplan_get read the actual RFC body and metadata, active PRD-001 and SPEC-001, corrected draft ADR-001, EVID-014 and EVID-015. No authority was taken from a maintenance repair report or old ADI.

Exact UTF-8 forgeplan_get.body was supplied as a safely shell-quoted argv value to the read-only command python3 -c 'import sys,hashlib; print(hashlib.sha256(sys.argv[1].encode("utf-8")).hexdigest())'. RFC result, exit 0: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177. ADR result, exit 0: 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5. Neither measurement hashes a markdown projection.

Ground-truth pins: RFC-001 draft/standard updated_at=2026-10-18T21:21:34.881083+00:00; PRD-001 active/standard updated_at=2026-10-18T20:51:11.875851+00:00; SPEC-001 active/standard updated_at=2026-10-18T20:51:12.611918+00:00; ADR-001 draft/standard updated_at=2026-10-18T21:08:52.191284+00:00 with hash above. Active parent metadata overrides historical proposal/draft prose. ADR is separately gated architecture input, never Build authorization.

Read-only cat .forgeplan/codex/pipeline.json observed phase=rfc, depth=standard, dev_unlocked=false, rfc_id=null. A repository rg --files query for Python/manifest/lock/container paths returned no visible application paths (exit 1); this is an inventory observation, not test execution. No app/test runtime, dependency installation, Python3.12 compatibility or Docker proof was produced. No reason, score, source/test/config/pipeline write, activation or other-artifact update was performed.

## Findings

### 1. EVID-014 material concern 1 is repaired in the actual frozen design

The old review identified disposal of already accepted queued work on unexpected worker exit. Current TC-3 instead assigns untouched admitted FIFO envelopes to the scheduler. Unexpected worker exit terminalizes only the active request exactly once as controlled/ambiguous failure, preserves untouched queue entries and transfers ownership to exactly one supervised successor. Pop/removal/ownership decisions are no-await and registry-identity checked; stale finally cannot remove a successor. Successor creation failure retains the queue and fail-stops rather than silently losing accepted work. The distinct shutting_down condition in worker outer-finally separates ordinary replacement from shutdown-coordinator cancellation of remaining volatile admissions.

This was challenged against active-inclusive 64 global/8 per-chat bounds, another chat's progress, cancellation during send and a confirmed prefix. The repaired invariant 4, worker outer-finally pseudocode and Rollout agree: neither active ambiguous send nor confirmed prefix is replayed; successor starts the next untouched envelope. Named worker_death_queued_successor_fifo and worker_death_partial_send_no_replay require barriers, multiple queued requests, stale-finally identity checks, FIFO once-only disposition and exact counters while another chat progresses. These are substantive future observation oracles, not generic cleanup labels. Repair closes the documentary concern; task scheduling, failure injection including successor-creation fail-stop, and reference release still need implementation proof.

### 2. EVID-014 material concern 2 is repaired in the actual frozen design

Admission now commits reservation, scheduler enqueue, worker ownership and in-memory update cursor in the same no-await transaction. Task-creation failure rolls counters/FIFO/registry back to pretransaction state and leaves cursor uncommitted. Cancellation while capacity is full or before commit admits nothing and releases fetched payload. After commit the scheduler owns exactly one admission even if handler/feed_update has not returned; the next fetch uses committed cursor. This removes the previous exposed enqueue-to-offset await gap. Irrelevant/edited updates commit a skip cursor without search.

Exactly-once terminal state/counter release and ownership publication are no-await transitions, including worker-finally exception. Notifications occur after publication and cannot own or reverse accounting. The supervised outer-finally covers failure in request finally; stale-worker identity checks remain necessary. There is no claim of durable exactly-once delivery or cancellation of an already sent Telegram message.

Shutdown uses one supervisor-owned shielded coordinator, not a cleanup task recreated by each signal. Ingress join 2s, drain at most 10s, worker cancel/join 2s, session close 2s yield a 16s cooperative bound and future compose 20s grace. Per-stage monotonic deadlines do not reset on repeated cancellation. Caller cancellation is deferred then propagated after coordinator completion. Nested finally reaches session close despite earlier cleanup errors, including startup failure after session acquisition but before Bot construction. Timeout/noncooperative owned cancellation is fail-stop with fixed safe output, no indefinite follow-up join and no claim of leak-free success. This explicitly limits the bound to cooperative execution; a blocked event loop is not covered.

The named future oracles admission_cancel_capacity_full, admission_commit_feed_return_cursor, admission_worker_creation_rollback, repeated_cancel_worker_finally_notification, worker_finally_exception, session_close_exception_timeout, startup_failure_before_Bot, shutdown_stage_deadlines_outer_finally and cooperative_cleanup_terminal_counters_offsets require barriers/FakeClock, cursor/counter/identity assertions and bounded error paths. The pre/post-feed-return oracle tests ownership rather than assuming successful await return means commit. The stage oracle requires close after earlier error and original deadlines under repeated signals. Completed cooperative cleanup requires zero retained envelopes/orphan owned tasks; fail-stop is expressly excluded from that success claim. These repair the missing design/fault-acceptance contracts; none has been executed.

### 3. Finite delivery policy survives the repair; SDK behavior demands the specified guard

Every outbound category remains source-bound with allow_sending_without_reply=False. One current message can have only one additional retry on confirmed explicit raw HTTP429 refusal; second429 stops. Retry flag resets for each current message, while total full retry_after wait is shared across the request and capped at 15s. Queue wait is excluded from the 90s service clock; every attempt requires full 1.1s pause and 10s attempt allowance, including retry and next request. Insufficient budget/deadline stops rather than shortening waits. Ambiguous timeout/network/decode/5xx and non429 typed RetryAfter stop remaining delivery; no recursive notices or whole-result replay.

Independently opened pinned primary code:
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/client/session/base.py : check_response tests truthy retry_after before HTTP status error branches. Zero bypasses that SDK branch. A typed exception cannot establish raw429.
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/client/session/aiohttp.py : make_request calls post, reads response, then check_response; network errors can carry underlying exception text. Close includes an awaited session close and 0.25s settling.
- https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/exceptions.py : error objects are unsuitable for retained safe event fields.

RFC's pre-check raw-status guard and sdk_guard_raw_status_edges expressly cover zero, malformed429, ok=true429, mismatched refusal payload, 5xx with retry_after and non429 typedRetryAfter. finite_delivery_faults checks attempts/cursor/full waits/budgets and healthy-chat progress. transitive_transport_no_replay requires instrumentation below SDK with the future complete pinned transport graph; one visible SDK post is not proof of no lower-layer replay. No external library installation or fabricated transport test was used.

### 4. Privacy, parent fit and architecture remain documentary obligations

Pinned primary dispatcher source https://raw.githubusercontent.com/aiogram/aiogram/v3.31.0/aiogram/dispatcher/dispatcher.py confirms feed_update logs update/bot identifiers in finally and unknown-update warnings serialize an update. The RFC's boundary therefore must suppress raw records before formatting at INFO as well as DEBUG. Its fixed-schema allowlist, controlled root/library/warnings/loop/top-level/stdout/stderr sinks before Bot, startup_failure_before_Bot and all_process_sinks_INFO_DEBUG are necessary, not optional redaction improvements. Future captures must exercise actual pinned SDK warning/error paths and startup/shutdown failures, including nested exceptions and session-close failure. Physical memory zeroization is not established by dropping references.

Cross-check with active parents found no new relaxation of FR01-08, AC01-18, AX01-12 or C01-C08/T01-T24: immutable full validated snapshot, active-only selection, raw distance/id ties, precise route endpoints, exact UI/source/date/fallback/escaping and shared token-free offline/startup validator persist. SPEC normalization proposals are treated as adopted rules. Strict inactive/last-entry atomic failure and owner semantic responsibility remain distinct. Flat models/config/catalog/geo/routes/render/telegram_app/composition ownership aligns with corrected ADR; domain stays framework-neutral, render does not import geo, and bot never fetches Yandex.

Text-size arithmetic is a design bound, not actual platform acceptance. Unrestricted valid organisation URLs remain an explicit unresolved platform conflict; no hidden cap, button omission or universal acceptance promise is introduced. Real full transitive hashes/install on Python3.12.15, container digest/platform verification and owner live inputs remain pending. Host3.14/noDocker cannot prove target success.

## Result

PASS for document design on the exact frozen RFC revision only. Both material EVID-014 concerns were independently rechecked against repaired text and meaningful future fault oracles. EVID-015 reviewed the older revision and missed these concerns; it supplies no current proof. This Evidence is neither independent ADI nor Guardian proof, runtime/source test PASS, dependency-install success, complete activation gate or Build authorization. RFC and ADR remain draft and separately gated; Build remains locked.

## Interpretation

Applicable S10-S13 were considered through alternatives/tradeoffs, active requirement fidelity, explicit contracts/fault oracles and frozen independent role provenance. This specialist assessment does not certify 100% applicable activation coverage, active independent Evidence or fresh Guardian PASS. Those remain orchestrator obligations.

## Congruence Level Justification

CL3: direct project-specific ground-truth artifact inspection and exact-body measurement by an assigned reviewer identity distinct from generator and maintainer. The measured subject is design text, not application behavior.

## Residual Risk

No implementation exists to prove exception-safe no-await transitions, repeated cancellation deferral, supervised successor behavior, bounded cooperative cleanup or all-process privacy. Volatile crash/shutdown loss and ingress head-of-line blocking remain explicit; envelope counts do not bound catalogue/payload bytes or Telegram retention. Dependency/transitive replay behavior, target runtime/container compatibility, unrestricted URL acceptance, owner catalogue semantics and manual two-origin/three-mode checks require future independent observation. A target or normative-input revision change invalidates this freeze-specific conclusion.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | EVID-017 informs RFC-001; exact reviewed timestamp/hash above |

## Validation Observations

Own-Evidence structural validation, graph and outer projection YAML informs inspection, final Evidence body hash/status/depth and frozen input unchanged checks are performed after this save and reported in handoff. A body-links-drift warning alone does not justify deleting a correct informs edge.



