---
depth: standard
id: EVID-010
kind: evidence
last_modified_at: 2026-10-18T21:05:02.636999+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: ADR-001
  relation: informs
status: draft
title: Independent architectural review — frozen ADR-001 — reviewer adr architecture 20261019 01
---

# EVID-010: Independent architectural review of frozen ADR-001

| Field | Value |
|-------|-------|
| Status | Draft |
| Review date (client) | 2026-10-19 |
| Target | ADR-001 |
| Valid Until | Revision-specific; invalidated by target or normative parent changes |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/adr-architecture-20261019-01
reviewer_role: architect-reviewer
generator_identity: creator/architecture-adr-20261018-01
reviewed_artifact_id: ADR-001
reviewed_artifact_updated_at: 2026-10-18T20:58:11.580229+00:00
reviewed_artifact_body_sha256: 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e
review_verdict: CONCERNS

## Measurement

Independent Role B architectural document review, not implementation certification or creator reasoning. Fresh scoped forgeplan_get ADR-001 preceded all mutations. Exact updated_at matched the assigned pin. Read-only Python hashlib.sha256 over the exact get body encoded UTF-8 returned 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e. No newline stripping or projection metadata substituted for body hashing.

Read AGENTS.md and .codex/agents/forgeplan-reviewer.toml with cat; read normative parents via scoped get: PRD-001 active updated_at=2026-10-18T20:51:11.875851+00:00; SPEC-001 active updated_at=2026-10-18T20:51:12.611918+00:00. Historical draft/proposal prose does not override active metadata. Reviewed ADR against actual PRD FR/AC/AX and SPEC C01-C08/T01-T24, including bounded rereads of contract and acceptance sections. Source attachment not required to resolve these architectural questions; it was not independently read or hashed. No external compatibility claims are independently verified.

Scoped health observed needs_attention, 14 artifacts before creation, orphan RFC-001 and advisory early-phase active artifacts; these do not establish an ADR gate failure or authorize repair. Scoped new(kind=evidence,parent_id=ADR-001) created exactly EVID-010 and its informs edge. Its installed template was inspected through get. New API has no auto_activate argument; no activation was requested or invoked, and link autoactivation was not used. Effective auto_activate=false; status must remain draft.

Read-only graph returned ADR-001 based_on PRD-001 and SPEC-001, and EVID-010 informs ADR-001. sed of ADR projection outer YAML confirmed both based_on links. Correct links were retained. Review date is client 2026-10-19; frozen artifact date 2026-10-18 and MCP-provided creation timestamps are preserved, without clock repair.

No source, tests, pipeline, existing Evidence or target writes; no score, reason, context, begin, unlock-build, code checks or live calls. Commands above inspect documents and pins only.

## Result

CONCERNS for C4 notation precision; no blocking contradiction found in the selected runtime architecture against active parents. Structured verdict supports means qualified support for the single-process decision, not an unqualified review PASS. Six architectural findings below distinguish the notation concern from acceptable mandatory RFC closures. Implementation is absent and receives no PASS.

## Findings

1. Boundaries and dependency direction challenged: supported.
References: ADR Decision / Module map and dependency direction; PRD Product Scope / Out of Scope, FR-06/07/08 and AX-11; SPEC Scope, C01/C02.
The composition root owns config, complete load and startup; catalog takes a path without environment or Telegram dependency; geo/routes/render depend on framework-neutral models, with render receiving computed distance. Adapter owns aiogram, scheduling, exception and send effects. No domain-to-adapter edge, bot-to-Yandex fetch, hidden DB or service was found. The model/Card sharing does not itself introduce a dependency cycle. One deployment matches the absence of durable queues or independent service scaling requirements. Residual risk: telegram_app combines scheduling, adaptation and send/error policy and may become complex; RFC contracts and later import/side-effect verification must show these boundaries survive implementation. A smaller adapter decomposition is not a new product requirement.

2. C4 L1/L2 types challenged: CONCERN, documentation precision, not a runtime blocker.
References: ADR C4 L1 and C4 L2 literal declarations, and paragraph immediately following L2.
L1 declares System_Ext(snapshot, "Owner-controlled JSON snapshot") although its own description says local read-only input. A file is data, not an independently functioning software system. Both levels declare System_Ext(browser, "User browser"), conflating a client application/runtime with an external software-system boundary. L2's ContainerDb(json, ..., "Read-only local UTF-8 JSON file", "Input file, not a database service") can represent a data store: the symbol does not prove a database process. Container(app) is the sole executable application; Python modules correctly are not containers. Explicit prose disambiguates deployment and the diagram has no bot-to-Yandex edge, so this concern does not overturn the one-process choice. Residual risk: readers counting System_Ext or ContainerDb symbols as separately deployed services can infer the wrong ownership/deployment boundary. A future authorized revision should clarify L1 data/dependency notation and the browser's client role while retaining one actual app; reviewer has not edited frozen ADR.

3. Immutable snapshot and exact approved C01-C08 challenged: supported, subject to later proof.
References: ADR Ownership/data lifecycle; Invariants 1-7; Selection/routes/rendering; SPEC C01-C08 and T01-T24; PRD AC-14, AX-09/12.
Whole-file startup validation includes inactive and invalid-last records, preserves input order, retains inactive in the immutable snapshot, and filters only at selection. Offline and startup share validation without token/network; missing file is not [] and no demo fallback exists. Closed 13-field schema, finite numeric non-bool coordinates, exact trim/code-point/case-sensitive identity, nullable/default distinctions, independent validation of present optional fields, Gregorian dates without freshness restrictions and conditional yandex rating dependencies remain normative. C06 is explicitly authoritative for detailed parsing; exact hosts/port/raw-path/encoding rules and preservation after trim remain, with no invented URL length cap. No silent normalization, hot reload or semantic geocoding was introduced. Residual risk: an immutable tuple alone cannot freeze nested record values; models must actually be immutable, and RFC must specify faithful normalized representations and diagnostics. Atomic acceptance means no partial accepted catalogue, not proof of an atomic filesystem publication; safe replacement is owner/deployment work.

4. FIFO, parallel chats and request-local state challenged: supported as a design.
References: ADR Concurrency/delivery, Ownership/data lifecycle and Invariant 8; PRD NFR-02, AC-04/16 and AX-04/06.
ADR explicitly rejects lock-only independently spawned handlers and specifies enqueue in polling update order before worker launch, one complete request/send worker per chat and concurrent workers across chats. Origin, message/reply destination, cards and send cursor belong to the request envelope; no shared latest origin or rewritten old URLs. Cleanup must not orphan newly enqueued work. These obligations address actual parent requirements rather than adding a global serialization requirement. Residual risks: the precise aiogram ingress hook and scheduler cleanup races are unproved, queue growth can retain waiting payloads, and one chat's retry wait causes head-of-line delay. Explicit admission/resource policy is a mandatory RFC closure; it cannot silently drop accepted work, add persistence or weaken privacy. No load SLA has been invented.

5. Retry refusal versus ambiguity challenged: supported as a bounded design choice.
References: ADR Concurrency/delivery boundary; PRD NFR-03, AC-17 and AX-07.
Only explicit 429 permits one additional attempt of the individual send, at least retry_after, two attempts total. Second 429 terminates remaining request delivery; blocked terminates immediately. Confirmed introduction/cards are not resent; ambiguous transport/timeout is not automatically retried because acceptance may already have occurred. Help/fallback shares the boundary without recursive error notifications; polling reconnect is separately distinguished. PRD AX-07 requires a finite RFC budget, not a specific larger count, so choosing one additional retry does not conflict. Residual risks: correct exception classification and any hidden library middleware retries require future exact-version compatibility/fault-injection checks. A cursor tracks confirmed sends, not exactly-once delivery across death. Partial delivery remains honest and unproved in runtime.

6. Lifecycle, privacy and payload closures challenged: supported with explicit mandatory closures.
References: ADR Privacy/threat/error boundaries, Consequences / Risks, Pre-conditions, Evidence Requirements and Rollback Plan; PRD NFR-01/06, AC-15/18, AX-05/08/11/12; SPEC C04 yandex_maps_url row and Traceability.
Validation precedes client construction/polling; reload only on restart, single token polling instance, paired image/catalogue rollback, finite future shutdown drain with cancellation/session close and no queue dump are coherent. Logging allowlists exclude raw updates, identifiers, origins, full URLs/cards and sensitive exception payloads even at DEBUG or library boundaries. Telegram/browser/Yandex history is correctly outside local deletion promises; owner semantic data acceptance is separate from syntactic success.
RFC must set finite drain timing and admission bounds, and prove maximum entity-parsed card text plus separately characterize URL-button transport. SPEC imposes no URL length cap; ADR explicitly requires owner resolution of any resulting platform conflict before claiming AC-15/AX-05 complete, without truncation, omitted required buttons or rejection of SPEC-valid catalogue. These are clear prerequisite closures rather than concealed guarantees; not reasons to demand an implementation PASS now. Residual risks: library logging, cancellation-held references, actual transport limits and owner data remain unverified. Compatible exact dependency pins and later independent observations are required before Build/product acceptance.

## Interpretation

Qualified architectural support only for this frozen decision and active normative revisions. C4 concern is a representation/ownership risk; mandatory RFC closures remain pending and cannot be counted as completed checks. No implementation, full AC/AX acceptance, independent ADI, S10-S13 activation coverage or Guardian gate is certified. This Evidence alone never unlocks Build or activates an artifact.

## Congruence Level Justification

CL3: same workspace, exact frozen ground-truth ADR body/timestamp and both active normative parents. Measurement denotes document/pin/graph consistency inspection, not executed application tests.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| ADR-001 | informs |

links:
  - target: ADR-001
    relation: informs

## Freeze and Validation Protocol

After this own-EVID write: scoped validate EVID-010 and get EVID-010; inspect actual graph and projection YAML if link drift is reported. Fresh get ADR-001 must retain exact assigned updated_at and exact body SHA256. Report actual validation and final pins externally, without editing target or other Evidence. Leave EVID-010 draft. No score or activation.

