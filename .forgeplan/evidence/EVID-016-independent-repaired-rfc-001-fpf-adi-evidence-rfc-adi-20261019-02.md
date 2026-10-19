---
depth: tactical
id: EVID-016
kind: evidence
last_modified_at: 2026-10-18T21:24:36.277942+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Independent repaired RFC-001 FPF ADI — evidence/rfc-adi-20261019-02
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-016: Independent repaired RFC-001 FPF ADI

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: evidence/rfc-adi-20261019-02
reviewer_role: evidence-gatherer
generator_identity: creator/rfc-coworking-20261018-01
maintenance_identity: maintainer/rfc-lifecycle-20261019-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:21:34.881083+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
review_verdict: PASS
client_date: 2026-10-19
scope: independent document-design ADI only

PASS is limited to the frozen document design and its explicit future proof obligations. It is not runtime, source-test, dependency-installation, Guardian or Build proof. No implementation exists; Build remains locked. This Evidence remains draft for the orchestrator.

## Measurement

Read repository AGENTS.md and assigned .codex/agents/forgeplan-evidence-gatherer.toml. Scoped health returned healthy with 12 advisory early-phase active mismatches; its generic implementation suggestion does not grant Build permission. Only role-scoped MCP created this one Evidence with parent_id=RFC-001 and its automatic informs relation. No source, tests, config, pipeline, target fixes, score or activation.

Read scoped get bodies for RFC-001, active PRD-001 and SPEC-001, corrected draft ADR-001, EVID-014 and EVID-015. Metadata active status prevails over historical proposal/draft prose in parents. EVID-014 is a source of challenges, not current-revision certification. EVID-015 reviewed the old RFC updated_at=2026-10-18T21:13:48.273934+00:00 and missed material concerns; its PASS is not adopted as proof.

Exact returned body strings were JSON-encoded, safely shell-quoted into read-only python3 -c, decoded, and hashed using hashlib.sha256(v.encode("utf-8")).hexdigest(). No projection file, envelope, newline normalization or frontmatter removal was used. Command exited 0:

| Input | Metadata status/depth | updated_at | Exact UTF-8 get.body SHA256 |
|---|---|---|---|
| RFC-001 | draft/standard | 2026-10-18T21:21:34.881083+00:00 | e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177 |
| PRD-001 | active/standard | 2026-10-18T20:51:11.875851+00:00 | 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d |
| SPEC-001 | active/standard | 2026-10-18T20:51:12.611918+00:00 | 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8 |
| ADR-001 | draft/standard | 2026-10-18T21:08:52.191284+00:00 | 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5 |

ADR is separately gated architecture input, not an active dependency or Build authorization.

## Tool reasoning attempt

Actually attempted role-scoped forgeplan_reason(id=RFC-001, save=false) exactly once. The observed error message was:
MCP tool call requires approval, but approval policy is never

This was a failed call. No completed tool analysis was obtained. No provider diagnosis, bypass or substitute tool output is inferred. The independent model ADI below is my own reasoning, separate from unperformed tool reasoning.

## Independent FPF ADI

### Hypothesis H1 — the repaired modular snapshot application fits the approved full scope

Prediction: one poller with immutable catalogue, pure domain/rendering and per-chat workers can express all accepted behavior without retained history or external enrichment.

Evidence: FR-01/02/05 have exact dynamic start text, request_location, manual-before-start, venue, initial live location only, group direction and help. FR-03/06 preserve active-only Haversine/raw-distance/id ordering and min(limit,count), including ties, zero/remote origins and no radius/rating ordering. FR-04/07 bind immutable origins and source replies, preserve old URLs and generate three explicit origin-first lat/lon modes. FR-08 preserves catalogue source/date/fallbacks without invented facts. AC-01–18, AX-01–12 and NFR-01–06 have owned future checks, with URL acceptance expressly unresolved.

C01–C08 and T01–T24 preserve strict UTF-8/JSON, full-file rejection including inactive/last defects, 13 closed fields, exact trim/code-point/default/null distinctions, finite numbers without bool coercion, case-sensitive normalized ids, optional-field validation, Gregorian dates, conditional Yandex provenance and exact no-fetch/no-length-cap URL policy. CLI and startup share validation; CLI deliberately retains C03 context while bot logs do not. C05 owner semantics remain distinct from syntax. Future handover includes empty real data, separate synthetic input, Russian instructions, locks, packaging and truthful verification.

Falsifier sought: dropped requirement, new URL cap, schema relaxation, shared last origin, renderer-to-geo dependency, Yandex network dependency or draft ADR unlock. No such contradiction found in these contracts. Actual counterexamples in future behavior would invalidate support; named test mappings alone do not prove behavior.

Disposition: selected for documentary requirements fit, subject to H2 repair analysis and H4 residuals.

### Hypothesis H2 — repair still loses untouched accepted work or leaves admission/cancellation ambiguous

Prediction: unexpected worker exit drains acknowledged queue entries, or cancellation between enqueue and feed return permits duplicate admission, leaked counters or unbounded close.

Evidence against the old defects: TC-3 now makes untouched FIFO envelopes scheduler-owned. Ordinary death terminalizes only the active request, forbids active/prefix replay, preserves queued envelopes and transfers ownership to exactly one identity-checked supervised successor. Stale finally cannot remove that successor. Successor-creation failure retains queue and fail-stops; it is explicitly not successful continuation or durable recovery. Intentional shutdown alone may cancel remaining admitted work after drain.

Admission now commits reservation, queue, worker ownership and cursor in one no-await transaction. Creation failure restores pretransaction counters/queue/registry/cursor; precommit cancellation admits nothing. Postcommit feed-return cancellation cannot revoke admission; the next fetch uses committed cursor. State publication/release and successor ownership do not depend on cancellable notification. A supervised outer finally covers request-finally exceptions.

Cleanup now has one shielded coordinator, deferred repeated caller cancellation, original monotonic stage deadlines of 2+10+2+2 seconds, startup acquisition inside resource scope, outer-finally close despite earlier errors, and no unbounded follow-up join. The 16s total applies to cooperative cleanup, not blocked loops or arbitrary third-party cancellation; fail-stop is not leak-free success.

Actual repair verification is textual, cross-checking TC-3, Invariants 4/6, pseudocode, rollout and future fault matrix. Named falsifiers directly address the old concerns: admission_cancel_capacity_full; admission_commit_feed_return_cursor; admission_worker_creation_rollback; worker_death_queued_successor_fifo; worker_death_partial_send_no_replay; repeated_cancel_worker_finally_notification; worker_finally_exception; session_close_exception_timeout; startup_failure_before_Bot; shutdown_stage_deadlines_outer_finally; cooperative_cleanup_terminal_counters_offsets. They demand exact offsets/counters, FIFO disposition, no duplicate successor/replay, other-chat progress and bounded close. These are design oracles, never executed observations.

Residual challenge: no-await atomicity needs careful actual implementation, including task creation behavior and idempotent release under injected finally failures. Shielding alone does not establish task ownership or finite joins. A future implementation that only adds shield() or drains queues on ordinary death fails this contract.

Disposition: EVID-014 findings 1 and 2 are repaired at document-contract level. No remaining material contradiction found in those repaired clauses; runtime closure remains unproved.

### Hypothesis H3 — scope reduction or a globally sequential service is the better compliant design

Prediction: smaller responses or one global worker removes lifecycle complexity while retaining approved behavior.

Evidence against: dropping descriptions, provenance or buttons violates FR-03/07/08 and AX-05. A single global service worker would let one request's retry waits obstruct every already-admitted chat, conflicting with cross-chat overlap/isolation expectations and the barrier oracle. Per-chat serialization is required; global serialization is unnecessary. The selected design already accepts head-of-line blocking at ordered ingress when a chat/global bound is full, while admitted other chats continue. That disclosed overload trade-off is distinct from serializing all service.

Falsifier: an approved scope change removing required card fields or concurrent-chat behavior could support reduction; none exists. No latency/load SLA is inferred from concurrency.

Disposition: rejected for current full requirements. Simpler internals cannot justify omitted behavior.

### Hypothesis H4 — durable queues, distribution or enrichment are required, or the current design already proves delivery

Prediction: accepted behavior requires durable restart recovery or live external data; alternatively exact pins and future checks suffice for complete acceptance now.

Evidence against: approved scope uses owner snapshot and generated browser links; no durable/restart guarantee, DB, Redis, geocoder, live ratings or route-time ranking is required. These additions introduce retained state, migrations, credentials and new external contracts. Crash loss and intentional shutdown cancellation are disclosed. They must not be confused with ordinary worker death, which now preserves untouched work.

Evidence supporting residual uncertainty: unrestricted SPEC-valid organisation URLs may exceed actual Telegram acceptance. Visible-text arithmetic does not bound keyboard transport or prove HTML/platform behavior. The RFC preserves noURLcap and withholds complete AC-15/AX-05/NFR-06 claims. Representative tests cannot prove all arbitrary lengths; owner conflict resolution cannot silently narrow active SPEC. Exact runtime pins, supplied provenance and one SDK post call do not prove full transitive compatibility, image digest authenticity or transport no-replay. New sdk_guard_raw_status_edges and transitive_transport_no_replay correctly require raw-status/zero-wait/5xx/malformed-response and below-SDK checks.

Falsifiers: an approved durability requirement would reopen architecture; an undisclosed URL truncation/omission/cap or universal delivery claim would invalidate this review. No such narrowing/completion claim found. No external registry, SDK or live-platform verification was performed in this review.

Disposition: reject added infrastructure as necessary for this scope; retain platform/runtime uncertainty as unresolved acceptance risk.

## Selected hypothesis and trade-offs

Select H1 with H2's documentary repair supported. Reject H3 and H4's infrastructure necessity. This induction establishes a coherent future plan, not measured usefulness or executable correctness.

Single release unit and pure modules reduce coordination and support offline verification, costing snapshot restart, whole-file startup rejection and volatile crash loss. Global64/per-chat8 active-inclusive limits plus one fetched update bound envelope counts, not bytes, catalogue size, queue residence or Telegram retention. Ordered backpressure can block ingress behind one chat. Successor supervision and atomic cursor/accounting add real implementation complexity but preserve the accepted-work distinction without persistence. Conservative ambiguous-stop reduces duplicate risk at the cost of partial delivery. Fixed all-process sinks reduce leak paths but sacrifice debugging detail and require adversarial testing before Bot construction and during shutdown. No physical memory zeroization or Telegram-history deletion is claimed.

## Findings

1. EVID-014's two material defects are substantively addressed in normative text, pseudocode, invariants and specific future fault oracles, rather than only relabelled. No current material design concern found requiring target edits in this role.
2. Full product/schema fit is document-level support with explicit incomplete URL/platform acceptance. This PASS must never be used as complete release acceptance or proof of delivery for arbitrary allowed URLs.
3. Raw-status guard, non429 typed RetryAfter rejection, zero retry_after, malformed 429 and 5xx ambiguity are future pinned-SDK obligations. Transport no-replay and process-wide privacy require real independent observations. No dependencies installed or source tests run.
4. S10: independent four-hypothesis ADI and truthful failed tool attempt. S11: requirements/alternatives/trade-offs challenged. S12: C01–08/T01–24 and admission/lifecycle fault contracts checked. S13: frozen get.body hashes, one attributable Evidence with informs, own validation and frozen-input readback. This is not a Guardian gate or a claim that all activation prerequisites are satisfied.

## Result

review_verdict: PASS

Document-design only for the exact RFC revision pinned above. Residual risks: unrestricted organisation-URL delivery; no-await admission/successor/accounting implementation; cooperative cancellation and actual fail-stop handling; SDK/transitive transport behavior; all-process safe sinks; full Python3.12.15 locks/install/image verification; unmeasured load/demand; owner semantic data/token and later live checks. ADR remains separately gated; Build remains locked. Any changed input revision requires refreshed review.

## Interpretation

Only EVID-016 may be updated by this reviewer. Keep it draft; the main orchestrator handles activation separately. Deterministic validation and graph/YAML relation checks are structural evidence only. Correct informs links must be retained even if body-links-drift is reported.



