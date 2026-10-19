---
depth: standard
id: EVID-039
kind: evidence
last_modified_at: 2026-10-19T11:48:01.342353+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: PRD-002
  relation: informs
status: draft
title: Independent product PRD review reviewer/places-prd-20261019-01
---

# EVID-039: Independent product requirements review of PRD-002

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-19 |
| Valid Until | Frozen revision only; re-review on target mutation |
| Target | PRD-002 |
| Requested depth | tactical |
| Actual metadata depth | standard; separate Role D responsibility |

## Structured Fields

evidence_type: measurement
verdict: partially_supports
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/places-prd-20261019-01
reviewer_role: artifact-reviewer
generator_identity: creator/places-prd-20261019-01
reviewed_artifact_id: PRD-002
reviewed_artifact_updated_at: 2026-10-19T11:45:23.839091+00:00
reviewed_artifact_canonical_body_sha256: 8459daa65970e83588b42f3eb7791729ad61ebada9bea8916a64ee22a4daee09
review_verdict: CONCERNS
maintenance_identity: maintainer/places-prd-consistency-20261019-01

## Measurement

Independent physical read-only product artifact review. Complete PRD-002 body read from forgeplan_get; authoritative metadata deep/draft and exact timestamp match the requested pin. Canonical UTF-8 body SHA256 computed with read-only python3 -c using hashlib.sha256 on the exact MCP body; observed hash matches the requested pin. Read active NOTE-003 constraints and relevant active PRD-001 / SPEC-001 baseline clauses through MCP. Metadata status overrides historical draft prose inside baseline bodies.

Health inspected: needs_attention/advisories and pre-existing duplicate/at-risk reports are project context, not this review's gate decision. No unrelated artifacts changed. New Evidence created with parent_id PRD-002 and automatic informs relation; only this new Evidence body updated. No reason, score, activation, source/tests/helpers, Git, pipeline, private config/IDs, Docker, Telegram or network operations. No code certification or test execution.

## Result

Frozen target matches both timestamp and SHA256. One substantive product consistency concern identified below. Requirements otherwise explicitly cover the requested button, ten user fields plus three system-managed keys, shared validator, private numeric any-one moderation, admin-only registry, atomic decision/publication/outbox, durable approved search, measurable future AC, admission/retention/privacy, backup and compatible rollback.

## Findings

1. CONCERNS — Exact-distance tie ordering conflicts with the normative baseline. PRD-002 “Moderation, publication and delivery policy” says base order is preserved, overlay follows committed approval order, and “ties следуют legacy стабильному порядку.” Its delta also declares ranking/ties unchanged and AC16 requires applicable baseline AC/AX. However active PRD-001 “Нормативный подбор и ссылки” explicitly requires “exact ties по id ascending”; baseline AC-06 repeats “до округления и id ascending.” Two approved places at identical coordinates with ids z and a approved in that order, or a base z and overlay a at the same coordinates, therefore have two plausible incompatible product outcomes if stable merged order governs ties. SPEC-001 C05/T08 explicitly permits distinct ids with identical coordinates, so the case is valid rather than theoretical invalid input. This is observable ranking behavior and needs an unambiguous normative priority before downstream design: preserve baseline id-ascending ties, or explicitly approve a scoped change to baseline behavior. This review neither changes the target nor prescribes an implementation sorting algorithm. Severity is CONCERNS rather than BLOCKER because the intended baseline preservation is stated and the ambiguity is localized, but this is not a clean PASS.

2. Supported after challenge — Cross-chat delivery and durable acceptance are appropriately separated. The PRD reserves all three moderator intents before submit acceptance and applicant status capacity before a decision; first committed decision, overlay and required intents are atomic, uncertain sends never automatically replay, and /pending plus /suggest recover authoritative state. AC4–7/11–13/17 provide future observable failure oracles. The 10-second attempt, 60-second intent budget and strict 429-only retry with total wait at most 15 seconds preserve the stated baseline policy. Residual risks remain missed notifications and unknown capacity; getChat HTTP 200 is operator-attributed availability information and does not certify actual delivery. No live delivery PASS inferred.

3. Supported after challenge — Privacy and recovery requirements are concrete at PRD stage. Registry access is private/numeric on every page/action, search origin is excluded from durable state, retention and bounded cleanup are explicit, backups require 0600/0700 restricted access with seven-day retention, and NF7/AC12/18 plus the explicit Rollback Plan require a compatible app/schema pair without silently losing approved search. Pending/public records intentionally outlive registry TTL. The operational owner is assigned. Residual risks are unmeasured restore performance, host loss within RPO, semantic quality of approved places and uncapped valid URL transport limits. Existing manual route/URL acceptance remains open. Future SQL, callback serialization and bounds algorithms belong normative RFC work; their absence is not treated as missing completed implementation proof or a demand for an additional SPEC-002.

## Interpretation

CONCERNS for the frozen product requirements revision because of finding 1. This is a product artifact assessment, not a Guardian decision, gate waiver, ADI certification, activation authorization or implementation acceptance. Russian FR phrasing and historical metadata-default prose are not blocking findings. Route 3 / Deep / SPARC + Hexagonal and the accepted scope are respected. S10–S13 independent coverage, active Evidence and fresh Guardian remain separate requirements.

## Congruence Level Justification

CL3: direct examination of the exact frozen target and its authoritative active project constraints in the same context. Measurement is document and pin verification only; no application behavior was measured.

## Related Artifacts

| Artifact | Relation | Revision / use |
|----------|----------|----------------|
| PRD-002 | informs (actual parent link) | deep/draft; 2026-10-19T11:45:23.839091+00:00; reviewed target |
| NOTE-003 | contextual reference | active/deep; 2026-10-19T11:35:41.915321+00:00; accepted scope |
| PRD-001 | contextual reference | active; 2026-10-18T20:51:11.875851+00:00; normative ranking/privacy/acceptance baseline |
| SPEC-001 | contextual reference | active; 2026-10-18T20:51:12.611918+00:00; C01–C08 and relevant T scenarios |

## Limitations

One draft Evidence only. Requested tactical depth cannot be set through the exposed new/update schema; actual metadata defaults standard and is reported honestly for separate Role D. Structural validation is reported by the reviewer after the actual validate call and is not proof of product correctness. No optional web research/lint performed. No private admin IDs read or displayed.

