---
depth: tactical
id: EVID-008
kind: evidence
last_modified_at: 2026-10-18T20:05:09.048984+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: PRD-001
  relation: informs
status: active
title: Guardian PRD-only frozen revision review — guardian/prd-20261018-01
---

# EVID-008: Guardian PRD-only frozen revision review

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-18 |
| Valid Until | Exact frozen revision only; any target change requires fresh review |
| Target | PRD-001 |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: guardian/prd-20261018-01
reviewer_role: guardian
generator_identity: creator/prd-coworking-20261018-01
reviewed_artifact_id: PRD-001
reviewed_artifact_updated_at: 2026-10-18T19:42:24.390387+00:00
reviewed_artifact_body_sha256: 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d
guardian_verdict: PASS
scope: PRD adequacy, fidelity and independent planning gate only

## Measurement

Read AGENTS.md, guardian role and forgeplan-audit skill at the requested paths. Scoped MCP supplied the full PRD, active Brief and complete EVID-004/005. Read original source sections 1–15, structured PRD, normative constraints, guidance and limitations. Only this Evidence was mutated; no files, reason, score mutation, activation, pipeline transition or application checks.

Full UTF-8 MCP body SHA256 independently computed with Python hashlib: 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d. Direct source byte SHA256: cbde92035f9e674f3a673f380c0f108b4c60f905e84eac8d48dbe70514e6f040. Delimiting the appendix between its heading and BMAD template guidance gives exact source equality after surrounding whitespace trim; both trimmed hashes are 465ecb55ed488831713019dd8f2ac6f2b7a16a215417c1e2581d0a337b8cb409. 

Fresh score obtained BEFORE Evidence creation using only read-only CLI forgeplan context PRD-001 --json: r_eff=0.9, derived_status EVIDENCED, validation passed, zero MUST errors and one SHOULD warning. Scoped get immediately before and after context returned exact frozen updated_at and identical full body. Cached get r_eff_score=0 is stale metadata, not a fresh score or an unexplained quality failure. Context's activation suggestion was not acted on.

## Findings

PASS for this exact PRD-only planning gate. No unresolved material product-scope defect or BLOCKER was found. The weakest evidence is direct document comparison and independently reasoned ADI: it can establish faithful, reviewable requirements but cannot prove demand, real venue quality, provider execution, application behavior or client routing. These limits are stated throughout the PRD and Evidence, so this verdict does not convert uncertainty about future implementation into a pass for implementation.

Scope fidelity: all 8 FR retain the original behavior, and all 18 AC plus 12 AX map to source, future checks and planned U1–U5. Private-chat /start count follows RESULTS_LIMIT, manual location works before /start, venue location remains permitted, /help explains origin/source/straight-line meaning, groups do not search, and only initial live location triggers selection. Exact intro, error/empty texts and ordered cards/buttons remain normative. AX-01..05 close details beyond the original AC list rather than dropping them in summary.

Catalog/ranking preserve finite bounded coordinates, rejection of bool/NaN/infinity, zero/coincident-point acceptance, lengths/dates/trim, unique ids, whole-file startup validation, shared validator and field/id/index diagnostics. Active-only Haversine radius/radians/clamp, exact sorting before rounding, id ties and min(limit,count) remain explicit. No hidden city/radius filter or rating reorder.

Routes and content: explicit origin then destination in lat/lon order, standard HTTPS query encoding, dot decimals up to six places and three explicit rtt modes remain required. Query parsing and separate swap regression are meaningful planned falsifiers. Organization URL does not replace a route. Rating source/date/link constraints prevent catalog ratings being presented as current Yandex ratings; absent fields use exact fallbacks without invented values or descriptions. Escaping and maximum-schema single-message delivery are acceptance obligations.

Challenged request races, exceptions and partial delivery: AC-16/18 and AX-04/06/07/08 preserve reply association, immutable old URLs, FIFO within one chat and isolation between chats. Logs include error/retry paths in the zero-token/coordinate/route-URL rule. Application memory retention is limited to processing, while Telegram history is explicitly outside deletion claims. Blocked users stop their delivery without killing the service; 429 respects retry_after and retries must be finite. Ambiguous delivery remains TC-3 design work, with no blind replay allowed. These are adequate constraints for RFC design, not demonstrated resilience.

Source sections 11–14 preserve five planned units/dependencies and all twelve handover categories. Real catalog initially empty, synthetic example separate, pinned dependencies, validator, tests, Russian docs, containers and honest report remain required. No automatic demo substitution or file-existence proof is allowed.

Technical uncertainty is bounded and owned: TC-1 exact domain allowlist and negative URL cases belongs to catalog contract/RFC agreement; TC-2 exact sub-kilometre rounding belongs to RFC; TC-3 finite retry/send-state/ambiguous outcomes belongs to RFC; TC-4 compatible pinned dependencies, architecture, lifecycle and chat queue belongs to RFC. Each has a before-Build deadline and associated future checks. These are genuine unresolved technical obligations, not unresolved product choices that invalidate this PRD. They must remain open until their own proof exists. SPEC-001 is a separate draft based on the Brief, not this PRD's parent; it was not reviewed or certified here.

## Result

Methodology command: python3 .codex/forgeplan-methodology-gate.py PRD-001 --json, exit 0. S10 FPF ADI 2/2: active EVID-004 contains four substantive hypotheses. S11 BMAD 2/2: one fresh independent artifact-reviewer identity. S12 OpenSpec 2/2: valid graph and active Brief parent. S13 ForgePlan 2/2: schema/lifecycle wiring passed. Total 8/8, 100% applicable S10–S13. C4 is N/A for this non-architectural PRD. Report passed=true. Its guardian_detail says N/A for Tactical despite target standard; that generic/misleading field is not used to certify this Guardian gate. The actual independent decision is recorded here.

Scoped validation: PRD-001 passed, 0 errors, body-links-drift SHOULD plus prd-fr-format COULD. EVID-004 passed, 0 errors, body-links-drift SHOULD. EVID-005 passed, 0 errors, no warnings. The FR format advisory cannot establish absence of requirements: eight actor/capability rows with journey links were directly read. The drift advisory conflicts with real graph links: PRD based_on NOTE-001 and both Evidence informs PRD are present, matching their body declarations. Scoped get exposes a body/frontmatter representation without graph links, so the advisory is treated as representation/tool drift rather than a missing relationship; no relinking or target mutation is warranted. Raw projection YAML was not accessed outside scoped MCP to evade the artifact-read boundary.

Health is healthy, stale_count=0, no at-risk artifacts or blind spots. Eight early-cycle phase advisories span active planning Evidence/Brief, not eight proved implementation failures. PRD advisory phase is validate; independent pipeline.json is phase=prd, route=1, depth=standard, dev_unlocked=false, prd_id=null and rfc_id=null. These are distinct phase systems. Neither phase was advanced. The pipeline is still awaiting its authorized maintainer transition.

## Independence and freshness

Active NOTE-001 updated_at is 2026-10-18T18:29:58.718062+00:00, matching the parent pin. EVID-004 is active/tactical, updated_at 2026-10-18T20:00:41.266465+00:00, identity evidence/prd-adi-20261018-01. EVID-005 is active/tactical, updated_at 2026-10-18T20:00:41.670365+00:00, identity reviewer/prd-artifact-20261018-01. Both explicitly review the exact target revision; both contain substantive challenges and qualify their claims. Historical Draft body rows do not override active MCP lifecycle metadata.

Generator, ADI reviewer, artifact reviewer and this Guardian have distinct attributable identities. Standard's required independent artifact-reviewer coverage is satisfied; Critical's two-reviewer requirement is not applied to this Standard target. EVID-004's attempted reason call encountered runtime approval-policy-never; it explicitly identifies its ADI as independent analysis, not provider output. No provider absence or successful external reasoning run is inferred. Identity attribution supports separation within the recorded workflow, not external organizational independence.

## Interpretation

This draft supports a later maintainer-controlled PRD gate only. It is not activation, an RFC decision, approval of the parallel SPEC, a source/test write permit, runtime certification or demand validation. Actual token/records, owner data checks, compatibility, privacy/fault tests and two-origin/three-mode live checks remain future work. External documentation statements retain source provenance; this review makes no new provider/API guarantee.

Precise next action: maintainer inspects this draft and its validation, handles required Evidence classification separately without altering the frozen PRD, and obtains any required explicit approval before activating qualifying Guardian Evidence first and then the target. If the target changes, this verdict expires and independent review must be renewed. After lawful PRD progression, RFC must close TC-1..4 and pass its own independent readiness gates before any Build unlock. No lifecycle action is authorized or performed by this review.

## Congruence Level Justification

CL3: direct original-source and same-workspace comparison against the exact frozen PRD and active prerequisite, with separate verifier identity. This describes document-review congruence, not measured application performance.

## Related Artifacts

This Evidence informs PRD-001 via the parent_id edge created by scoped forgeplan_new. EVID-004 and EVID-005 are reviewed supporting records; NOTE-001 is prerequisite context. No extra link or artifact mutation is requested.



