---
depth: tactical
id: EVID-040
kind: evidence
last_modified_at: 2026-10-19T11:52:50.331407+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: PRD-002
  relation: informs
status: active
title: Fresh independent PRD documentary ADI — evidence/places-prd-adi-20261019-02
---

# EVID-040: Fresh independent PRD documentary ADI
Status: Draft
Created: 2026-10-19
Target: PRD-002
## Structured Fields
evidence_type: measurement
verdict: supports
congruence_level: 3
reviewer_identity: evidence/places-prd-adi-20261019-02
creator_identity: creator/places-prd-20261019-01
review_scope: documentary planning only
requested_bookkeeping_depth: tactical
actual_default_depth: standard

## Current Pin
Full current PRD-002 read through scoped forgeplan_role MCP: draft/deep; updated_at=2026-10-19T11:51:02.602042+00:00.
Canonical body SHA256 independently calculated from returned UTF-8 body:
e667b6aa3609de6478226d736dbf406d1edeab654ac6b232c21df5fc6601702e.
Matches requested frozen pin. Hash implementation checked against SHA256("abc"). No historical byte comparison was performed; the claim that only one sentence changed is not independently certified.
Active NOTE-003 read in full: deep, updated_at=2026-10-19T11:35:41.915321+00:00.
Active PRD-001 read; relevant baseline is standard, updated_at=2026-10-18T20:51:11.875851+00:00.

## Measurement
Fresh independent Role B read of target and parent, plus baseline ranking, privacy, scope and manual route acceptance clauses. No earlier Evidence findings reused. Own scoped forgeplan_reason attempted for PRD-002 with save=false; actual result: "MCP tool call requires approval, but approval policy is never", isError=true. No ADI tool output obtained, no workaround. The hypotheses below are this reviewer's independent reasoning.
Evidence template was read before replacement. Only one new Evidence created, parent_id PRD-002; automatic informs relation reported. No source/runtime inspection or implementation verification performed.

### Hypothesis
H1 — do nothing. Retain external proposals and existing read-only search.
Evidence: PRD-002 Problem/J1–J3 and NOTE-003 intake explicitly require in-bot submission, moderation and administrator user visibility; H1 supplies none.
Falsifier: owner withdraws those requirements or demonstrates an accepted existing equivalent. Neither appears in the documents read.
Deduction: reject for requirement mismatch; minimal new storage is its advantage, not evidence of suitability.

### Hypothesis
H2 — manual queue. Collect proposals, let an operator edit the base catalog.
Evidence: NOTE-003 B04/B05 and PRD-002 FR-003/005/007, AC4–7 require durable acceptance, atomic final decision and automatic approved search after restart. Manual transfer does not guarantee these properties and conflicts with read-only base publication.
Falsifier: owner explicitly accepts manual publication and reduced recovery guarantees. Current parent instead requires automatic durable workflow.
Deduction: reject for agreed scope; fewer transactional states would reduce operational complexity.

### Hypothesis
H3 — durable selected workflow. Persist drafts/submissions/registry, commit any-one moderation and approved overlay, and retain bounded delivery intents.
Evidence: PRD-002 J1–J4, FR-001–009 and AC1–18 connect each actor to observable outcomes; commit boundaries, numeric/private authorization, capacity-before-acceptance, uncertain no-replay and recovery reads implement the parent's documentary commitments.
Falsifier: future concurrency/crash tests produce duplicate/partial decisions, lost committed publication, unauthorized reads, saved search origins or uncertain automatic resend; backup/restore failure also defeats the proposed guarantee. No such tests have run here.
Deduction: select H3 as a requirements direction, conditional on later SPEC/ADR/RFC and independent proof.

## Findings
1. Ranking consistency is supported directly: PRD-001 algorithm and AC-06 require exact distance before rounding, exact ties id ascending. PRD-002 publication policy now says distance ascending/id ascending. Snapshot base/approval order describes assembly, not an alternate ranking tie rule.
2. Parent fidelity is supported: ten user fields plus three system fields, any-one final moderation, read-only base plus approved overlay, private numeric authorization and minimal registry remain explicit. PRD names narrow legacy exceptions rather than silently claiming all baseline privacy/storage prohibitions survive unchanged.
3. Documentary limitation: Progress still says metadata defaults standard and Role D must set deep, while actual target metadata is already deep. Treat as stale procedural prose; current MCP metadata and frozen pin are authoritative. No target edit made.
4. Material implementation decisions remain open: transaction/schema/crash durability, scheduler integration, callback/chunk bounds and compatible migration/restore require downstream artifacts and proof. RPO/RTO and admission numbers are acceptance targets, not measurements.
5. NOTE-003 attributes getChat checks to the main orchestrator. These establish reported identity/reachability only. Delivery of the new workflow to all three moderators remains unproven. PRD-001 manual checks of two origins and all three route modes remain open; PRD-002 AC16 preserves that boundary.

## Result
Documentary verdict: supports selected H3 for this exact PRD revision, with the stale Progress note and explicit limitations above. Three alternatives independently evaluated; zero implementation, delivery or live acceptance claims established.

## Interpretation
The draft is sufficient to carry the selected product direction into separate documentary gate review. This is neither Guardian certification, full Deep PASS nor authorization to build or activate. Demand, usability, load, storage budget and runtime behavior are unproven.
Trade-offs: durable state adds privacy, migration and backup burden; any-one approval concentrates catalog-quality responsibility; forbidding uncertain replay may lose notifications; /pending and /suggest restore discoverability rather than guarantee delivery. Bounds reject new admission rather than silently discard accepted work.

## Congruence Level Justification
CL3 refers only to direct same-context documentary inspection of the exact target and its active parent/baseline. It does not imply runtime congruence or implementation proof.

## Related Artifacts
EVID-040 informs PRD-002 through creation parent_id. NOTE-003 and PRD-001 are read-only contextual sources. SPEC-001 is referenced by the target; its full validator contract was not independently certified here. EVID-038 and EVID-039 remain unchanged.

## Maintenance Attribution
Target creator remains creator/places-prd-20261019-01. Existing target maintenance is explicitly attributed in its body to maintainer/places-prd-consistency-20261019-01; this reviewer does not assume that authorship. This Evidence's writing and any corrections are attributable solely to evidence/places-prd-adi-20261019-02.
Requested Tactical bookkeeping cannot be set by scoped new/update schema; actual Evidence default Standard is retained for Role D. Evidence remains draft; no activation or target mutation.



