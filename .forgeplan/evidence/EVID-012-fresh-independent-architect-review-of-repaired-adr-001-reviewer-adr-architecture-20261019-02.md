---
depth: tactical
id: EVID-012
kind: evidence
last_modified_at: 2026-10-18T21:13:02.734210+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: ADR-001
  relation: informs
status: active
title: Fresh independent architect review of repaired ADR-001 — reviewer adr architecture 20261019 02
---

---
id: EVID-012
status: draft
links:
  - target: ADR-001
    relation: informs
---

# EVID-012: Fresh independent architectural review of repaired ADR-001

| Field | Value |
|-------|-------|
| Status | Draft |
| Review date (client) | 2026-10-19 |
| Target | ADR-001 |
| Valid Until | Exact frozen revision only; repeat after target or normative parent changes |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/adr-architecture-20261019-02
reviewer_role: architect-reviewer
generator_identity: creator/architecture-adr-20261018-01
reviewed_artifact_id: ADR-001
reviewed_artifact_updated_at: 2026-10-18T21:08:52.191284+00:00
reviewed_artifact_body_sha256: 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5
reviewed_artifact_status: draft
reviewed_artifact_depth: standard
review_verdict: PASS

## Measurement

Independent Role B document design review only. First fresh scoped forgeplan_get ADR-001 matched draft/standard and exact timestamp. Read-only python3 hashlib.sha256(s.encode('utf-8')).hexdigest(), with s the exact returned body, independently produced the assigned hash above. No trimming, added newline or projection frontmatter entered the hash.

Read AGENTS.md and .codex/agents/forgeplan-reviewer.toml using cat. Read complete returned PRD-001 (active, updated_at=2026-10-18T20:51:11.875851+00:00), SPEC-001 (active, updated_at=2026-10-18T20:51:12.611918+00:00), and historical EVID-010 (draft CONCERNS, target old revision 2026-10-18T20:58:11.580229+00:00), with bounded rereads of parent bodies to avoid combined-output truncation. Active metadata governs historical draft/proposal prose. No external compatibility verification or application testing is claimed.

Scoped health: healthy, 16 artifacts, 12 active and 4 draft before this Evidence, 12 advisory early-phase mismatches, no orphans. Health's generic implementation suggestion is not Build authorization. Exactly one scoped new(kind=evidence,parent_id=ADR-001) created EVID-012 with informs auto-link, followed by get of its canonical installed template. Only this new Evidence may be updated; historical EVID-010 is preserved.

Read-only sed of ADR projection confirmed outer YAML based_on PRD-001/SPEC-001 and draft. Attribution limitation: the assigned generator remains creator/architecture-adr-20261018-01. The task reports separate Role D C4 maintenance; no maintenance identity or maintenance-provenance entry appears in the exact returned body, and rg -n -i 'maintenan|maintainer|role.?d|c4' on the target projection returned only C4 headings/module prose. Outer last_modified_by is codex-mcp-client/0.163.0-alpha.10.2, not an independently identified Role D person. Accordingly this review does not misattribute the C4 maintenance to the generator or invent a maintainer identity. This provenance limitation does not change the architecture assessment.

No score, reason, activation, pipeline writes, CLI writes, source/test changes or runtime checks were performed. Read-only shell commands inspect documents and hashes only.

## Result

PASS for the frozen architectural document design, with 7 substantive challenged findings below. EVID-010's sole C4 notation concern is resolved in the actual repaired text. Its other six-topic review qualifications remain future implementation/RFC obligations, not newly executed proof. Zero runtime tests or live requests; no runtime PASS, compatibility PASS, product acceptance or activation gate is asserted.

## Findings

1. C4 boundary repair resolves EVID-010 finding 2.
Evidence: ADR C4 L1 literal declarations contain user/owner Persons, bot System and Telegram/Yandex external systems, without snapshot or browser System_Ext. Owner supplies checked data/restarts bot; user opens Yandex through browser. L2 contains exactly Container(app) and ContainerDb(json) inside deployment. Its prose explicitly identifies the latter as a local read-only UTF-8 file, not a database service, and the browser as user-device channel. There is no app-to-Yandex edge or Yandex API call. This corrects the file-as-system and browser-as-external-system ambiguity identified by the old Evidence without adding a process. Residual: Mermaid symbol counting alone could still mislead a reader unfamiliar with datastore notation; explicit prose adequately bounds it.

2. Runtime choice, startup and internal dependencies are coherent.
Evidence: ADR H1-H4, Decision/module table, config/error boundary and PRD baseline/TC-4. Python 3.12, aiogram 3, long polling, one process and local JSON match the approved baseline. Domain models/geo/routes/render have no adapter/config dependency; render receives distance and request Origin. Startup owns immutable Settings and validates full catalogue before client construction/polling. Offline catalog entry imports neither token config nor aiogram and gives explicit exits 0/1/2. BOT_TOKEN required, path/default, RESULTS_LIMIT integer 1..5/default 3 and LOG_LEVEL default INFO match PRD. Exact pins/image and compatibility are expressly future RFC closures. Residual: no installed-version/import/side-effect verification; telegram_app bears substantial scheduling and transport complexity. Document selection does not certify dependency support.

3. Complete immutable snapshot preserves C01-C08 without weakening acceptance.
Evidence: ADR Ownership, Invariants 1-8 versus SPEC API/Data Models/Validation Rules and T01-T24. Whole-file strict UTF-8/JSON rejects BOM, surrogate ambiguity, duplicate members and nonfinite constants; closed 13 fields, no coercion/unknown fields, exact fixed trim set/code-point lengths/case-sensitive normalized ids and finite non-bool coordinates remain normative. Complete ordered snapshot includes inactive; invalid inactive/last record prevents polling. Selection alone filters active; file changes require restart. Optional null/blank/default distinctions, exact Gregorian dates without freshness limits, independent validation of present fields and conditional yandex rating URL/date are retained. C03 diagnostic classes/context and shared startup/offline semantics remain authoritative. C05 real branch/address correspondence stays owner responsibility, with no geocoder/regex fiction. Residual: future model fields must truly be immutable; a tuple alone is insufficient, and safe owner file replacement is not proven by atomic catalogue acceptance.

4. URL, ranking and UI decisions retain active parent fidelity.
Evidence: ADR Invariant 6, Selection/routes/rendering and Risks versus SPEC C06 and PRD AC-03..15/AX-05/09..11. Exact HTTPS allowlisted hosts, literal port policy, raw path/encoding restrictions and preservation after trim defer detailed parsing to normative C06; no fetch, extraction, normalization or added URL length cap. Haversine radius/clamp, unrounded order/ties by id, no city/radius/rating filter, min(limit,count), and explicit 999/1000 half-up display decisions are consistent. All three encoded route modes use request origin first with latitude/longitude and dot decimals up to six places. Russian card/source/date/fallback/order/layout and single escaping boundary are explicit obligations. Residual: unrestricted valid organisation URLs may exceed platform transport limits. ADR correctly requires separate URL-button characterization and maximum entity-parsed text verification; no truncation, omitted buttons or schema rejection may silently close this conflict. Owner resolution precedes AC-15/AX-05 completion if conflict occurs.

5. FIFO is defined at ingress, independent chats can progress and origins remain request-local.
Evidence: ADR Concurrency/delivery and Ownership versus PRD NFR-02/AX-04/06. Synchronous enqueue in polling update order precedes worker launch; one worker finishes complete request/send sequence before next in that chat. Lock-only spawned handlers are explicitly rejected. Other chat workers run concurrently. Origin, destination/reply ids, cards and cursor are envelope-local; old URLs are not rewritten. Idle cleanup must not orphan a newly enqueued update. Residual: actual aiogram ingress wiring, race-safe cleanup and memory admission bounds remain unproved. Retry waits hold that chat's FIFO and queued payloads transiently retain data. RFC must close finite resource/admission policy without silent loss, persistence or privacy weakening; this is a mandatory prerequisite, not executed load evidence.

6. One extra retry only for explicit refusal avoids blind duplicate delivery.
Evidence: ADR Concurrency/delivery versus PRD NFR-03/AC-17/AX-07. Explicit 429 permits only one additional attempt of that send, at least retry_after, cancellable; second 429 ends remaining request delivery. Blocked/forbidden ends immediately. Other definite failures stop that request, not other workers. Ambiguous timeout/transport is not automatically retried; confirmed sends/cursor prevent wholesale restart. Help/fallback also use the boundary, failure notification does not recurse, and polling reconnect is separate from send retry. This satisfies a finite budget without inventing exactly-once delivery. Residual: hidden dependency retries and exception classification need pinned-version/fault-injection verification; process death can lose queued work and ambiguous accepted sends cannot be recalled.

7. Privacy, lifecycle and downstream closures remain explicit and mandatory.
Evidence: ADR Privacy, Pre-conditions, Evidence Requirements and Rollback versus PRD NFR-01/AC-18/AX-08/11/12. Allowlisted logs exclude token, identifiers, coordinates, route URLs, cards/raw updates and sensitive exception/traceback payloads including library DEBUG. Opaque ids are not derived from private data. Completed/cancelled request state is released; no disk queue/history/cache. Telegram/browser history and clicked endpoints remain outside local deletion claims. Single polling instance, stop-before-start rollout, validated image/catalogue rollback, ingress stop, finite RFC-defined drain then cancellation/session closure are coherent. Residual: actual library logging, shutdown-held references, cancellation behavior, drain deadline, queue policy and transport compatibility are unverified. These are RFC/Build/independent proof obligations; their presence is not evidence of functioning runtime.

## Interpretation

The repaired notation removes the historical documentation concern. No contradictory architectural choice against the complete active PRD/SPEC was found. Remaining risks identified in EVID-010 findings 1 and 3-6 persist as explicitly bounded downstream work, not unresolved concealment in this design decision. PASS is limited to document design at the exact frozen pins. Independent ADI, applicable S10-S13 activation coverage and fresh Guardian gate remain separate; this Evidence stays draft and cannot unlock Build.

## Congruence Level Justification

CL3: same workspace and exact ground-truth frozen target with independently computed body hash, complete active normative parents and historical review. Measurement means document/pin consistency examination, not application behavior.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| ADR-001 | informs |

links:
  - target: ADR-001
    relation: informs

PRD-001 and SPEC-001 are normative read-only context; EVID-010 is historical read-only context. No extra graph edges are requested.

## Freeze and Validation Protocol

After own-Evidence update, validate only EVID-012, fetch its final body and hash exact UTF-8, inspect graph and outer YAML for EVID-012 informs ADR-001, then fresh get ADR-001 and recheck draft/standard, exact updated_at and exact body hash. A known SHOULD body-links-drift warning is recorded if observed even when graph/YAML agree; preserve both links and other artifacts. Final observed checks are reported to the orchestrator. Leave draft; never activate.

## Observed Final Checks

Scoped validate EVID-012 returned passed=true, 0 errors, 1 SHOULD body-links-drift warning. Scoped graph explicitly contains EVID-012 -->|informs| ADR-001; read-only sed of Evidence projection shows matching informs ADR-001 in both outer YAML and body YAML. The warning is therefore retained as observed tooling drift, not suppressed by deleting links or changing other artifacts.

Fresh scoped get ADR-001 after Evidence creation/update retained draft, standard, updated_at=2026-10-18T21:08:52.191284+00:00 and byte-identical returned body; independent Python UTF-8 SHA256 again returned 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5. After this final own-Evidence annotation the same validation/get/hash checks are repeated for the concise final report. No activation occurred.



