---
depth: standard
id: EVID-032
kind: evidence
last_modified_at: 2026-10-19T11:14:11.255794+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: NOTE-003
  relation: informs
status: draft
title: Independent Brief ADI — evidence/places-brief-adi-20261019-01
---

# EVID-032: Independent Brief ADI

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-19 |
| Target | NOTE-003 |
| Identity | evidence/places-brief-adi-20261019-01 |
| Requested depth | tactical |
| Actual metadata depth | standard; default left unchanged for separate Role D |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Measurement

Documentary planning review only. Independently read the complete NOTE-003 through scoped forgeplan_role get, read this Evidence's generated template through the same scoped tool, and computed SHA256 of the exact returned UTF-8 body using read-only Python. No source correctness, runtime delivery, demand, performance or implementation measurement is claimed. Existing EVID-031 was not used as proof or read.

Exact frozen target:
- id: NOTE-003
- status: draft
- metadata depth: deep
- updated_at: 2026-10-19T11:11:38.745005+00:00
- canonical bodySHA256: e074040bf5100840052f3ee6034c379caba639f8368daf0f2bd9aa33e3d30536
- creator pin: creator/places-brief-20261019-01, explicitly present as generator_identity in the body.

The returned timestamp and independently computed body hash exactly match the assigned freeze. Review applies only to this revision; any target change requires reassessment.

Read-only forgeplan health was inspected: existing at-risk RFC, duplicate advisories and phase mismatches were reported. Those are not a gate PASS or a mandate to alter other artifacts.

Attempted scoped forgeplan_reason on NOTE-003 with save=false. Tool returned isError=true: "MCP tool call requires approval, but approval policy is never". Its advertised schema does not expose save, and execution was refused. No successful tool reasoning, persisted tool proof or provider result exists. The ADI below is this independent reviewer's own reasoning.

## Findings

The Brief consistently distinguishes requested future behavior from executed acceptance. It changes the baseline's no-database/admin/durable-queue exclusions explicitly, preserves the read-only base catalogue and validator contract, and carries forward manual route and URL acceptance as pending. This is adequate direction for planning, not proof that the baseline can deliver the extension.

Numeric admin IDs were privately supplied and are intentionally absent here. They are not an identity blocker. User-supplied rollout evidence says two admin chats are reachable and @anastyyyyad must /start. This corrects the Brief's broader unconfirmed-reachability assumption without changing its frozen body. It is a rollout prerequisite; no Telegram call or delivery test was performed in this review.

The strongest design risk is the boundary between committed business state and notification uncertainty. "One final decision" can be transactional in local state, while uncertain external sends cannot be certified exactly once. The Brief acknowledges missing notifications and gives /pending as recovery. Later design must prove that missing notification does not strand durable pending work and that recovery never silently replays an uncertain send.

The registry introduces personal-data obligations even when search origin is excluded. Minimal columns do not settle retention, erasure across backups, authorized pagination or diagnostic leakage. These remain explicit future decisions rather than evidence of privacy correctness.

### Hypothesis H1 — do nothing

Abduction: Keep the read-only catalogue and existing search; handle suggestions outside the bot and avoid adding registry or moderation state.

Supporting evidence: This preserves the current architectural exclusions and avoids new persistence, privacy, migration and delivery risks. No demand study or volume measurement establishes that a durable workflow is economically necessary.

Deduction/falsifier: Under the owner's confirmed requirements, this offers neither the requested in-bot submission/moderation/admin journey nor automatic approved inclusion. A demonstrated withdrawal of those requirements or evidence that the existing process meets the requested outcome would favor H1; neither is supplied. Reject for requirement fit, not on invented business-benefit evidence.

### Hypothesis H2 — reduced manual queue

Abduction: Collect a shorter submission, notify moderators, and let an operator validate and edit the catalogue manually.

Supporting evidence: Smaller state machine and operational footprint could be proportionate to unknown submission volume. Human semantic checks of branch/address/coordinates/link are needed even with H3, so automation does not eliminate moderation effort.

Deduction/falsifier: This shifts final inclusion and recovery to an operator, cannot meet the confirmed automatic inclusion requirement as stated, and a notification-only queue can lose discoverability after an uncertain send. A durable pending list could improve H2, but adding full fields, atomic decisions and automated overlay progressively restores H3's complexity. H2 becomes viable if the owner explicitly accepts manual inclusion, reduced fields and revised recovery obligations. That scope reduction is not authorized. Reject for current scope while retaining it as a legitimate lower-cost alternative.

### Hypothesis H3 — durable selected workflow

Abduction: Keep SQLite-backed drafts, submissions, minimal registry, approved overlay and explicit notification intents; allow any one authorized moderator to commit the final decision.

Supporting evidence: This aligns with the owner's confirmed SQLite, any-one decision and automatic inclusion choices. The Brief specifies restart survival, exclusion of pending/rejected records, private numeric authorization on every privileged action, an unchanged base JSON and future crash/concurrency oracles. These are coherent requirements, not executed results.

Deduction/falsifiers: Crash/concurrent decisions yielding partial state or multiple effects, an approved record missing after restart, unauthorized reads/writes, state mixing between search and wizard, or replay of uncertain delivery would refute a proposed implementation. Planning selection must be revisited if later bounded scheduling, retention or recovery design cannot meet the preserved constraints. No implementation evidence currently rules out these failure modes.

Induction: Select H3 for continued Brief-level planning because it uniquely meets the confirmed scope among these alternatives. Demand, cost, usability and implementation feasibility remain unmeasured; selection is conditional on later explicit contracts and independent proof.

## Result

Three distinct hypotheses independently challenged; all three include supporting evidence and falsifiers. One exact target revision checked; timestamp and SHA256 match. One reason attempt refused; zero successful tool-generated reasoning results. One Evidence created with parent_id NOTE-003 and automatic informs relation. No implementation acceptance scenarios were executed.

Verdict: supports the selected durable workflow as a documentary Brief direction, with the open obligations below. This is not activation approval, Guardian certification, full Deep coverage or delivery certification.

## Interpretation

Future PRD must resolve retention/deletion, abuse/admission limits, role scope, wizard resume/cancel and notice UX. SPEC must resolve state schema/versioning, identity namespace and merge behavior, interaction/timestamp semantics, field/page/payload bounds and shared validator interface. ADR/RFC must resolve transaction/outbox/overlay boundaries, event-loop-safe DB access, crash durability, bounded callbacks and recipients, uncertain-send recovery, migration compatibility, backups/restore, rollback and RPO/RTO.

These belong to subsequent planning stages; deferring concrete algorithms is appropriate at Brief abstraction. They must be resolved before build readiness and verified later. The old pending manual-route and URL findings remain open and are not discharged by B12 or this review.

Trade-offs: SQLite fits the chosen single-process direction but adds locking, disk and migration failure modes. Any-one moderation lowers coordination cost but grants each moderator decisive authority. No automatic replay of uncertain sends sacrifices notification completeness; /pending provides discoverability only if operators use it. Registry visibility aids operations while adding data-retention and access-control work. H3 costs more than H1/H2, and absent usage evidence prevents a benefit/cost claim.

## Congruence Level Justification

congruence_level 3 describes review of the exact same frozen planning document and confirmed owner constraints. It does not describe same-environment runtime testing. The independently checked revision and separate evidence identity establish documentary attribution; they do not turn the creator's baseline assertions into independently verified code facts. External links quoted in the target were not re-browsed and are not treated as verified external proof.

## Limits and status

This Evidence remains draft. Requested tactical depth is recorded here; the create tool defaulted actual metadata to standard and exposes no depth parameter. Metadata was left unchanged for Role D. No scores, activation, Guardian decision or full S10-S13 coverage assertion was made. No source/tests/pipeline/Git/private files were changed or inspected; no admin numeric IDs, tokens, network, Docker or Telegram were accessed. No other artifact was mutated. The tool-created informs link is the only target association.

## Related Artifacts

NOTE-003 is the target of the informs relation automatically created by parent_id at creation. No additional link mutation was performed.

Independent identity: evidence/places-brief-adi-20261019-01
Target creator: creator/places-brief-20261019-01

