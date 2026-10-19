---
depth: tactical
id: EVID-004
kind: evidence
last_modified_at: 2026-10-18T19:48:37.760020+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: PRD-001
  relation: informs
status: active
title: Independent PRD scope fidelity and ADI — evidence/prd-adi-20261018-01
---

# EVID-004: Independent PRD scope fidelity and ADI

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-18 |
| Valid Until | Frozen revision only; superseded target requires new review |
| Target | PRD-001 |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Measurement

reviewer_identity: evidence/prd-adi-20261018-01
generator_identity: creator/prd-coworking-20261018-01
role: specialist evidence
reviewed_artifact_id: PRD-001
reviewed_artifact_updated_at: 2026-10-18T19:42:24.390387+00:00
reviewed_artifact_body_sha256: 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d
active_brief: NOTE-001
active_brief_updated_at: 2026-10-18T18:29:58.718062+00:00
source_path: /Users/mxmknn/.codex/attachments/38a9bdff-7b37-4c55-8851-d338dfe1c340/Pasted text.txt
source_sha256: cbde92035f9e674f3a673f380c0f108b4c60f905e84eac8d48dbe70514e6f040
review_verdict: PASS
scope: Independent product-scope fidelity and planning sufficiency; neither implementation correctness nor demand proof.

Method: read AGENTS.md, evidence-gatherer role, health, ground-truth MCP PRD and active Brief, and original v1.0 source. Compared every structured PRD section with source §1–15, keeping the source appendix normative. Exact full MCP body UTF-8 hash and metadata matched the frozen pin before artifact creation. Health reported healthy with four advisory early-cycle phase mismatches, not a new activation decision. No score, claim, application tests, implementation, or activation was performed.

Scoped forgeplan_reason was attempted for PRD-001 with save=false. Actual response: "MCP tool call requires approval, but approval policy is never". This diagnoses invocation/approval unavailability only; provider absence is not established. The ADI below is my independent analysis, not provider output. No save=true call was made.

## Result

Planning comparison: 8/8 FR, 18/18 AC and 12/12 AX present with source/check/planned-unit traceability. All 12 source deliverable categories and 5 future units are retained. These counts measure document coverage, not passed application tests. Material scope defects found: 0. Unclosed technical items remain explicitly blocked before Build; token and real catalog remain live-input blockers.

Coverage findings against the original source:

- FR-01/02/05 (§2): dynamic /start count and request_location button, manual point before /start, /help's three explanations, group rejection, initial live only, no edited-message selection, and allowed venue location all survive. AX-01..05 supply the missing detail beyond basic AC. Falsifier: group location or a live edit triggers a search.
- FR-03/04 (§2,8): exact intro, separate distance-ordered cards replying to original message, new origin/new URLs, immutable old URLs. AX-04/06 add same-chat FIFO and cross-chat isolation to AC-16. Falsifier: a second origin overwrites first-request route starts or destination chat.
- FR-06 (§4): JSON UTF-8 array, one branch per record, default path; unique nonempty id/name/address limits 64/150/250; finite numeric lat/lon ±90/±180, no bool/NaN/infinity, zero and same coordinates with different IDs allowed. Optional active:boolean default true; HTTPS allowlisted URL/null; short_review/description/rating_text limits 200/500/50; rating_source catalog/yandex default catalog; checked/updated calendar dates YYYY-MM-DD/null; trim-empty optional strings absent. Yandex rating requires date+URL. Unknown fields, duplicate IDs, wrong types/ranges/JSON reject whole file before polling with field and ID/index diagnostics; empty array valid, missing file configuration error. Shared standalone/bot validator; no runtime URL fetch or address/ll inference. Falsifier: malformed record silently drops while valid records serve.
- FR-06 (§5): origin validation, active filter, Haversine R=6,371,000 m in radians, intermediate clamp [0,1], exact distance sorting before rounding, exact ties id ascending, min(limit,count). No hidden city/radius/rating reorder. Metres below 1000, one-decimal km from 1000, approximate/straight-line wording, honest distant results. AX-10 includes 999/1000 boundary; AC-06/13 cover ties and geography. Falsifier: rounded distances change ranking. Sub-km rounding detail stays TC-2.
- FR-07 (§6): explicit origin lat,lon before destination lat,lon; standard encoded HTTPS route, rtt pd/mt/auto, dot decimals up to six places. No browser location/city/metro substitution; organization link separate. AC-07 parses all queries, AC-08 catches swap, AC-04 new origins, AX-11 offline generation. Falsifier: any route omits destination or keeps prior origin.
- FR-08 (§3,7): normative start/intro/three error texts match; card order number/name, address, approximate straight-line distance, optional rating, review, description, routes, optional organization link. Exact labels: walk/transit first row, car second, optional place row; both missing-text fallbacks retained. Catalog never labeled Yandex; Yandex saved rating includes check date, no currentness promise. Missing rating omits star line, no invented scale/attributes. HTML escaping and max-schema one-message card required. Falsifier: absent description invented or catalog rating called Yandex.

All AC checked individually: 01 start; 02 pre-start manual; 03 known synthetic order/file permutation; 04 deliberately different origin orders/new starts; 05 active catalog only; 06 pre-round sort/ties; 07 queries; 08 coordinate swap; 09 straight-line/no route duration; 10 texts/no invention; 11 provenance; 12 empty/1/2/no-active; 13 geographic edges; 14 startup rejection; 15 HTML; 16 cross-user isolation; 17 errors/blocked; 18 logs. All map to future CK/unit labels, not results.
All AX checked individually: 01 help; 02 group; 03 live/venue; 04 reply linkage; 05 count/text/layout/max card; 06 FIFO/isolation; 07 failures; 08 privacy; 09 schema; 10 distance boundaries; 11 offline/no demo fallback; 12 restart/shared validator. These add source detail without replacing AC.

Failure/privacy fidelity (§8–9): finite retries required, 429 retry_after honored; blocked user stops their delivery without process crash. AX-07 forbids replay of confirmed cards and blind whole-result replay after partial/ambiguous sends. NFR/AX-08 explicitly covers exceptions as well as normal/retry logs: no token, precise coordinates or complete route URL; only code/stage/anonymous request ID. Request coordinates/history not retained by application after processing; Telegram history and old links are expressly not deleted. Falsifier: raw exception logging includes the coordinate-bearing request URL.

Delivery fidelity (§11–14): 12 categories retained: application source, fixed dependencies, empty-token example, secrets ignore, initially empty real catalog, separate labeled synthetic catalog, standalone validator, automated acceptance checks, Russian README, Dockerfile/compose, ForgePlan documents, honest implemented/checked/missing-input report. U1 configuration, U2 catalog, U3 selection/routes dependent on U2 contract, U4 Telegram after contracts, U5 checks/docs/container after prerequisites are all planned. File existence is not evidence of behavior. Owner supplies token and validated real records; address-only/link-only inputs require separate coordinate preparation. No automatic synthetic fallback. Manual two-origin/three-mode route checks remain unperformed without live inputs.

## Interpretation

### Hypothesis H1 — Catalog-only MVP (selected)

Abduction: accepted source §1–7 behavior needs curated records, geometric ranking and explicit links, without API enrichment.
Deduction: FR must retain AC/AX and future-unit coverage; lost provenance, routes or error contracts falsify sufficiency. Offline checks must not claim live correctness.
Induction: comparison preserves 8 FR, 18 AC, 12 AX and owner inputs; no hidden API dependency appears.
Trade-off: data freshness depends on owner and distance is geometric, not travel time. Select for scope fidelity, not demand proof; retain accepted Standard BMAD + Spec Kit.

### Hypothesis H2 — Do nothing / retain source only

Abduction: the detailed original could avoid another planning representation.
Deduction: original-only delivery fails requested ForgePlan PRD/RFC/Spec handoff (introduction, §11–12); an authorized waiver would falsify this rejection, and none was found.
Induction: PRD adds explicit future check/unit traceability while retaining normative source.
Trade-off: less documentation effort loses the requested planning deliverable. Reject for task fidelity, without speculative economics.

### Hypothesis H3 — Names and distances only

Abduction: fewer fields/modes simplify UI and data preparation.
Deduction: removal of descriptions, provenance or route modes fails §3/6/7, FR-07/08, AC-07/10/11. Owner-authorized reduction would falsify rejection; none exists.
Induction: source explicitly requires three routes and catalog descriptions/review, with exact fallbacks for missing values.
Trade-off: smaller interface loses requested context and transport choice. Reject; accepted catalog-only scope does not authorize those omissions.

### Hypothesis H4 — API enrichment / travel-time ranking now

Abduction: enrichment could provide other information.
Deduction: mandatory live retrieval conflicts with §1/7/13 and offline/no-key behavior. A new requirement for current ratings or durations would falsify exclusion; none exists.
Induction: PRD puts enrichment in future scope and keeps geometric meaning.
Trade-off: potential freshness requires new access/contracts and verification. Exclude from MVP; no commercial or API-availability claim.

Before-Build closures are legitimate technical delegation: TC-1 exact domain allowlist owned by catalog SPEC author with RFC agreement, checked by CK-schema; TC-2 exact sub-km rounding by RFC author with CK-distance boundaries; TC-3 finite retry budget/retry_after/send-state and ambiguous partial delivery by RFC author with CK-delivery; TC-4 pinned compatible versions, architecture/lifecycle/chat queue by RFC author with U1/U4 checks. All have before-Build deadlines. Telegram max-message constraints are preserved by NFR-06, AX-05 maximum-schema single-card check and TC-4 architecture responsibility, rather than silently waived. Active RFC readiness and unlock-build remain prerequisites; this Evidence does not close those obligations.

## Congruence Level Justification

CL3: same workspace, exact frozen target, original source and active parent context; independent reviewer differs from generator. This is direct document comparison in the same context, not external analogy. PASS means no material planning fidelity defect found in the reviewed revision. It does not certify implementation, prove demand, constitute main Guardian PASS, authorize activation, or unblock Build. Reason provider execution, application tests, external documentation revalidation and live/manual checks remain unperformed. A fresh Guardian decision and lawful lifecycle actions belong to other roles.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| PRD-001 | informs |



