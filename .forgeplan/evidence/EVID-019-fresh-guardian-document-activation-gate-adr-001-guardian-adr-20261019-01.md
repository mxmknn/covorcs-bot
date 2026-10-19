---
depth: tactical
id: EVID-019
kind: evidence
last_modified_at: 2026-10-18T21:32:09.769832+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: ADR-001
  relation: informs
status: active
title: Fresh Guardian document activation gate ADR-001 guardian adr-20261019-01
---

---
id: EVID-019
status: draft
links:
  - target: ADR-001
    relation: informs
---

# EVID-019: Fresh isolated Guardian document activation gate for ADR-001

| Field | Value |
|-------|-------|
| Status | Draft |
| Review date | 2026-10-19 |
| Target | ADR-001 |
| Valid Until | Exact target and normative parent pins only; repeat review on change |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: guardian/adr-20261019-01
reviewer_role: guardian
generator_identity: creator/architecture-adr-20261018-01
reviewed_artifact_id: ADR-001
reviewed_artifact_updated_at: 2026-10-18T21:08:52.191284+00:00
reviewed_body_sha256: 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5
reviewed_artifact_body_sha256: 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5
guardian_verdict: PASS
review_scope: ADR architecture decision document activation only

## Measurement

Fresh isolated inspection of actual scoped forgeplan_get bodies, not adoption of an earlier Guardian. Read AGENTS.md and .codex/agents/forgeplan-guardian.toml. Inspected target, all four graph-linked Evidence EVID-010/011/012/013, active PRD-001 and SPEC-001, and relevant current RFC-001 proposal sections (architecture, catalogue, UI/payload limits, lifecycle/admission, send states, privacy, pins and residual risks). Bounded rereads recovered truncated combined outputs.

Commands/results actually observed:
- Scoped forgeplan_health: healthy, 23 artifacts, 17 active, 6 draft, 17 advisory early-phase mismatches, no orphans, no stale Evidence, no at-risk items. Generic continue-implementation text is not readiness authorization.
- Scoped forgeplan_phase ADR-001: validate, greenfield, last transition 2026-10-18T20:57:51.341812Z. No phase advance.
- python3 .codex/forgeplan-pipeline.py status: route=1, depth=standard, phase=rfc, dev_unlocked=false, rfc_id=null; pipeline updated_at=2026-10-18T20:51:12.990797+00:00.
- forgeplan --version: 0.33.0. forgeplan context ADR-001 --json (read-only audited path): artifact.r_eff=0.8, derived_status=EVIDENCED, validation passed with 0 MUST errors and 1 SHOULD warning, four linked Evidence. No score, score-all, reason, activation, provider bypass or pipeline mutation invoked.
- Fresh scoped get ADR-001 immediately after context and methodology retained exact frozen timestamp and byte-identical body.
- python3 .codex/forgeplan-methodology-gate.py ADR-001 --mode methodology: S10=2/2, S11=2/2, S12=2/2, S13=2/2, C4=2/2, aggregate 10/10=100%, methodology verdict PASS. Read checker implementation: Standard requires one fresh substantive active non-Guardian/non-evidence-gatherer reviewer; Critical requires two. Its methodology-mode "Guardian: N/A for Tactical depth" is an unconditional display default outside activation mode, not the actual target depth. ADR metadata is Standard; this Evidence supplies its separate fresh Guardian judgment.
- Scoped forgeplan_validate ADR-001: passed=true, 0 errors, 1 SHOULD body-links-drift. Scoped graph explicitly has ADR-001 based_on PRD-001 and SPEC-001; sed of actual ADR projection outer YAML shows both exact based_on links. The body frontmatter also declares them. The warning is a false positive for missing actual parent links, retained without repairs.
- Exact get.body strings were hashed with read-only python3 hashlib.sha256(sys.argv[1].encode()).hexdigest(), with shell-safe argument quoting, no stripping or added newline and no projection substitution. All initial pins below matched.

## Frozen inputs

| Artifact | Authoritative status/depth | Exact updated_at | Exact UTF-8 get.body SHA-256 |
|----------|----------------------------|------------------|-----------------------------|
| ADR-001 | draft / standard | 2026-10-18T21:08:52.191284+00:00 | 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5 |
| PRD-001 | active / standard | 2026-10-18T20:51:11.875851+00:00 | 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d |
| SPEC-001 | active / standard | 2026-10-18T20:51:12.611918+00:00 | 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8 |
| RFC-001 | draft / standard | 2026-10-18T21:21:34.881083+00:00 | e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177 |

Active parent metadata governs their historical draft/proposal prose. RFC is a proposal, not an active dependency or implementation observation.

## Findings

1. Independence and current Evidence meet this Standard document gate. Generator creator/architecture-adr-20261018-01 differs from Guardian guardian/adr-20261019-01, architect reviewer reviewer/adr-architecture-20261019-02 in active EVID-012, and independent ADI author evidence/adr-adi-20261019-02 in active EVID-013. Both current reviews explicitly pin the repaired timestamp and exact body hash, have substantive findings and bounded document PASS. EVID-012 provides the required one independent architectural reviewer. EVID-013 supplies four independently authored hypotheses, consequences, trade-offs and falsification conditions. Its reason attempt was denied by approval policy never; it contains no completed tool ADI output. Its maintenance provenance explicitly corrects this limitation. I weigh the actual independent model ADI, not an invented successful provider call or generator self-review.

2. Historical Evidence is weaker and does not supply current gate proof. EVID-010 and EVID-011 remain draft and pin the older 2026-10-18T20:58:11.580229+00:00 revision/hash 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e. EVID-010 is CONCERNS over C4 precision; EVID-011's bounded document support is stale. Their real informs edges do not make them active/fresh. R_eff=0.8 is the actual fresh aggregate, not a probability of runtime correctness; no numeric improvement or exclusion of historical Evidence is fabricated.

3. EVID-010 finding 2 is resolved in the actual repaired diagrams, independently inspected. L1 now has user/owner Persons, bot System, Telegram/Yandex external systems. No snapshot System_Ext and no browser System_Ext remain. Owner supplies checked local data/restarts bot; user opens the route via browser. L2 has sole executable Container(app) and ContainerDb(json), explicitly a read-only local UTF-8 input file, not a DB process/service. Modules are components, not containers. Browser is expressly a user-device channel. Both levels have user-to-Yandex route-opening relationships and no bot/app-to-Yandex edge. Actual artifact graph independently retains the two based_on parents. EVID-012 finding 1 agrees with these literal repairs. Residual notation risk from the datastore symbol is adequately bounded by the adjacent prose; no unresolved C4 blocker remains.

4. Parent alignment supports the architecture document. Composition owns config and full validation before client/polling; catalog's offline path excludes token/aiogram/network; domain dependency direction is acyclic and render receives computed distance plus request Origin. Immutable whole snapshot includes inactive records; selection alone filters active; restart changes snapshot. ADR retains strict C01-C08 fields/types/defaults/trim/date/URL/diagnostic rules and owner-only semantic place acceptance. No extra organisation URL cap or network enrichment appears. Haversine, exact unrounded ranking/id ties, min(limit,count), request-bound three route modes, source/date labels, exact Russian UI obligations and HTML boundary preserve PRD behavior. This is documentary contract correspondence, not executed acceptance.

5. Delivery/privacy design is explicit, with real downstream risks. Ingress FIFO precedes worker launch; one complete worker/chat and concurrent chats prevent reliance on lock-acquisition order or global origin. One extra send attempt only after explicit 429 refusal, no automatic ambiguous resend, confirmed-prefix cursor and honest partial delivery are coherent. Logs exclude private payloads including library DEBUG/error paths; queued data is transient and downstream Telegram/browser history is not claimed deleted. These are obligations, not measured properties. Transitive immutability, scheduler cleanup races, hidden SDK retries, exception classification and sensitive logging remain unproved.

6. Current RFC proposes closure without becoming proof. It specifies active-inclusive 64 global/8 per-chat bounds with one fetched update and backpressure, atomic admission/cursor ownership, supervised untouched-queue succession, bounded 2+10+2+2 shutdown, status-aware send classification, controlled sinks and parsed-text size reasoning. It retains unrestricted valid organisation URLs and explicitly unresolved actual platform delivery. Exact pins are research inputs and full lock/install/container checks remain future work. These proposal details make the ADR's delegation concrete but do not certify RFC activation, Build readiness, unlock, dependency compatibility or behavior. Overload head-of-line blocking, noncooperative shutdown and URL transport remain material risks.

7. Coverage is complete for document activation, not product completion. S10=independent four-hypothesis active EVID-013; S11=one current independent active architect EVID-012 with substantive findings; S12=actual based_on active parents and normative contract correspondence; S13=zero MUST validation errors and correct lifecycle graph; C4=both levels with substantive boundary repair. Checker 100% is independently corroborated rather than treated as sufficient by itself. No unresolved BLOCKER to the bounded ADR decision was found. Uncertainty about implementation is explicitly outside this PASS and remains unresolved.

## Result

guardian_verdict PASS for activation of the exact frozen ADR-001 architecture decision document only. Required Standard reviewer count=1; qualifying independent current architect identities=1, plus a distinct independent ADI author and this Guardian. All five applicable layers are 2/2, aggregate 100%; read-only pre-creation R_eff=0.8.

No application code/tests exist yet in this lifecycle and no runtime checks were performed. Build remains locked. Zero implementation, RFC activation, unlock-build, shipment, demand, capacity, compatibility or live-route PASS is asserted.

## Interpretation

Weakest evidence is static documentary review rather than actual platform/runtime observation; historical drafts are stale, and EVID-013 tool-generated reasoning is unavailable. Those limitations do not conceal a missing ADR document obligation: the selected architecture and repair are supported by current independent reviews and actual parent/diagram inspection. They must not migrate into claims of product correctness.

Precise next step: main orchestrator rechecks these pins, validates and activates this draft Guardian Evidence first, then separately activates ADR-001 through the normal guarded gate. Any target or normative parent change invalidates this verdict. RFC must independently pass its own reviewers/Guardian/activation/readiness before lawful unlock-build; later independent verification must measure scheduler/fault/privacy and text/URL transport behavior. If a SPEC-valid URL conflicts with the platform, obtain explicit owner requirement resolution before claiming AC-15/AX-05/NFR-06 complete; do not silently cap, trim or omit.

## Congruence Level Justification

CL3: same workspace and exact scoped target body with active normative parent pins, actual graph/YAML and fresh read-only gate inspection. measurement denotes document integrity and gate observations only, not application measurements.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| ADR-001 | informs |

Exactly one new Evidence was created via scoped forgeplan_role forgeplan_new(kind=evidence,parent_id=ADR-001). Only this owned Evidence is updated. All other artifacts, source/tests/config/guardrails and pipeline are read-only. No lifecycle status was assigned or activated.

## Final verification protocol

After this body save, validate EVID-019, fresh get/hash EVID-019 and all four frozen inputs, inspect its real informs edge and projection outer YAML/path, and confirm draft/standard metadata. Report actual results and exact Evidence body hash externally. Leave draft. No additional Evidence, score, reason or activation.



