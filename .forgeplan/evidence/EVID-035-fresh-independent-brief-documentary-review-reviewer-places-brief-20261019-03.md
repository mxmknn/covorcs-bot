---
depth: tactical
id: EVID-035
kind: evidence
last_modified_at: 2026-10-19T11:27:10.581241+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: NOTE-003
  relation: informs
status: active
title: Fresh independent Brief documentary review reviewer places brief 20261019 03
---

---
status: draft
links:
  - target: NOTE-003
    relation: informs
---

# EVID-035: Fresh independent frozen Brief documentary review

Status: Draft
parent_id: NOTE-003
requested_depth: tactical
actual_metadata_depth: standard (creation default; separate Role D adjustment required)

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata
reviewer_identity: reviewer/places-brief-20261019-03
reviewer_role: artifact-reviewer
generator_identity: creator/places-brief-20261019-01
reviewed_artifact_id: NOTE-003
reviewed_artifact_updated_at: 2026-10-19T11:24:37.191777+00:00
review_verdict: PASS

## Measurement

Read complete canonical NOTE-003, EVID-032, EVID-033 and EVID-034 through forgeplan_get, and this new Evidence's generated template through get. Health inspected before review: existing at-risk RFC, duplicate and phase advisories; no unrelated remediation or gate inference. This is independent documentary Brief review, not creator reasoning or implementation certification.

Authoritative target metadata is deep/draft. Read-only python3 -c using hashlib.sha256(body.encode('utf-8')).hexdigest() on the literal complete MCP body without normalization exited 0 and returned 44705d2681009fce78e87c862ef5ef1536b4fa5783af73454e357ea48cc555b3. Timestamp exactly matches the assigned freeze. Read-only python3 -c using pathlib.Path(".venv/verification/moderation/admin-chat-recheck.json").read_text() exited 0: checked_at_utc 2026-10-19T11:21:35.891445+00:00, expected_username anastyyyyad, reachable/private_chat/username_matches true, http_status 200, messages_sent 0. This local operator-produced record contains no numeric private IDs. No live API verification was performed.

Historical evidence read unchanged: EVID-033 draft updated_at 2026-10-19T11:14:50.706356+00:00 and EVID-032 draft updated_at 2026-10-19T11:14:11.242459+00:00 pin NOTE-003 2026-10-19T11:11:38.745005+00:00 / e074040bf5100840052f3ee6034c379caba639f8368daf0f2bd9aa33e3d30536. EVID-034 draft updated_at 2026-10-19T11:22:37.916628+00:00 pins 2026-10-19T11:19:23.313481+00:00 / 40c2cc3b04616906dedadfbf8fb61abae99b77a1e6bf23ad7e576d42bdb04f53. Their CONCERNS or contextual conclusions are historical, not rewritten by this PASS.

## Findings

1. Both prior documentary concerns are resolved in this freeze. EVID-033 finding 1's rollout assumption is replaced by explicit operator-only chronology: initial getChat 200 for @mxmknn and @oks_ssn, 400 for @anastyyyyad, then the timestamped 200/private/username-matching recheck. The safe local proof corroborates only the later third-chat check; the first two and initial 400 remain attributed operator observations rather than independently reproduced API facts. Risks correctly separates all-three recorded getChat accessibility from future notification delivery and requires deployment recheck. /start remains a platform prerequisite; /pending is recovery, not a substitute for initiating conversation. Intake scopes the creator's no-API statement to its physical run. Maintenance identities and their narrow factual repairs are explicit.

2. EVID-034 finding 2's stale unqualified unconfirmed-reachability sentence is absent. Official references now directs readers to Risks and says delivery is a future live check. This agrees with the repaired chronology and does not elevate getChat into sendMessage, new-feature, runtime or activation acceptance. Residual risk is changing accessibility and unproved delivery, explicitly acknowledged rather than hidden.

3. Request fidelity is preserved: exact «Предложить место»; all 13 JSON keys enumerated; id/active/updated_at system-owned and ten remaining wizard fields user-facing; @anastyyyyad, @mxmknn and @oks_ssn; administrator-only registry. Shared validator/default/conditional semantics, numeric sender authorization and private context on every privileged command/callback/page are explicit; usernames confer no rights. Approved-only durable overlay, readonly base JSON, SQLite and any-one first-committed atomic decision match the approved Route 3 SPARC + Hexagonal Deep direction. This checks documentary commitments, not baseline code.

4. Cross-chat and failure requirements are substantive: exactly three explicit private recipient intents in B07, no transferred applicant reply binding, bounded per-target serialization, no automatic replay of ambiguous sends even after restart, and authorized durable /pending discovery in B08. B05 requires a single decision/effect under concurrency and crash. A failed or missing notification cannot undo committed business state. Concrete atomic transaction/outbox/visibility, retry, fairness and callback budgets are explicitly future ADR/RFC decisions; their absence as algorithms does not defeat Brief-stage PASS.

5. Minimal private-human registry starts with new interactions, stores five stated field categories and excludes historical reconstruction, search origins/text, phones, raw updates and message history. B03/B09/B10 challenge isolation and privacy with synthetic inspection; authorized bounded pagination and notice are required. Retention/deletion including backups, notice timing, role separation and admission abuse remain explicit PRD decisions. B11/B12 preserve scheduler/shutdown and offline regressions, consistent backup/restore, compatible application/schema rollback and no state erasure or uncertain-send replay. These future acceptance oracles are requirements, none executed.

6. EVID-032 is hypothesis context ONLY. Current H1 still omits in-bot submission/moderation/registry; H2 still reduces fields and requires manual publication; H3 still supplies durable atomic approved publication at persistence/privacy/delivery cost. Current B01–B12 and the earlier independent reviews agree on these requirement-fit comparisons and oracles; maintenance explicitly says these sections are unchanged. No prior canonical full body is supplied by its hash, so a byte-for-byte historical diff is not claimed. The amended accessibility facts neither supply H1's missing feature nor make reduced H2 meet full-field automatic inclusion; H3 still requires uncertain-send recovery and operators using /pending even when getChat succeeds. Thus the older ADI remains relevant to selection, without becoming fresh review of the amended factual paragraph. Any claim of fresh current-pin ADI gate coverage needs separately pinned independent reasoning that explicitly reassesses accessibility changes against H3 feasibility and recovery; EVID-032 alone cannot provide it. Its refused reason call is not successful tool proof.

7. Future boundaries are clear: PRD owns product/retention/admission decisions, SPEC owns schema/identity/merge/field and interaction contracts, ADR/RFC owns durable lifecycle, bounded scheduling, transactions, recovery and rollout. No demand or economic benefit is invented. Old full Guardian, manual-route and uncapped-URL concerns are not closed; B12 expressly preserves old live acceptance as pending. No implemented feature, full S10–S13 coverage, readiness, release or activation is certified.

## Result

Exact target timestamp and SHA256 match. PASS at documentary Brief stage: both historical documentary concerns are resolved and the requested direction, requirements and future acceptance remain coherent. Historical evidence verdicts/status/body/expiry were untouched.

Exactly one new Evidence created with parent_id NOTE-003 and automatic informs relation. Only this new Evidence body updated; it remains draft. Actual metadata depth at creation is standard; available new/update schema has no depth field. Requested tactical depth is not falsely represented as indexed metadata and is left for separate Role D handling. Initial validation passed all MUST, 0 errors, with one SHOULD body-links-drift warning. Explicit body frontmatter did not clear that warning. The redundant table row was removed; NOTE-003's existing automatic informs relation is stated in prose below. Final validation is reported separately.

## Interpretation

Supports continued planning direction, subject to later active independent evidence and Guardian requirements. Recorded getChat results are operator observations, not delivered-notification proof. Local proof inspection establishes documentary consistency only. No target fix or creator reasoning performed.

## Congruence Level Justification

CL3: exact same project and exact frozen canonical Brief assessed against the supplied owner constraints. This is same-context document fidelity, not runtime or code measurement. Historical ADI applies only as older hypothesis context; external reference URLs were not visited or independently verified.

## Limits

No source/tests/helpers/Git/pipeline/private numeric IDs/.env/secrets were read or changed. No pre-existing artifact was mutated. No tests, imports, Telegram, Docker or network actions, reason, score or activation calls were performed. Only the permitted safe JSON proof and literal-body hashing used python3 -c; no temporary files or shell writes.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
 
NOTE-003 is the target of the automatic informs relation created by parent_id. The table has no redundant artifact row.



