---
depth: tactical
id: EVID-013
kind: evidence
last_modified_at: 2026-10-18T21:16:00.968797+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: ADR-001
  relation: informs
status: active
title: Fresh independent architecture ADI — ADR-001 repaired pin — evidence/adr-adi-20261019-02
---

---
links:
  - target: ADR-001
    relation: informs
---

# EVID-013: Fresh independent architecture ADI of repaired ADR-001

| Field | Value |
|-------|-------|
| Status | Draft |
| Review date | 2026-10-19 |
| Created | Service metadata reports 2026-10-18T21:12:02.729121+00:00; preserved, not rewritten |
| Valid Until | Exact revision only; no metadata TTL asserted |
| Target | ADR-001 |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3
reviewer_identity: evidence/adr-adi-20261019-02
reviewer_role: evidence-gatherer
generator_identity: creator/architecture-adr-20261018-01
target_id: ADR-001
target_updated_at: 2026-10-18T21:08:52.191284+00:00
target_body_sha256: 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5

## Review Metadata

reviewer_identity: evidence/adr-adi-20261019-02
reviewer_role: evidence-gatherer
generator_identity: creator/architecture-adr-20261018-01
reviewed_artifact_id: ADR-001
reviewed_artifact_updated_at: 2026-10-18T21:08:52.191284+00:00
reviewed_artifact_body_sha256: 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5
review_verdict: PASS

PASS is limited to independent architecture/document consistency at this exact repaired revision. It is neither Guardian approval, activation eligibility, nor application acceptance.

## Measurement

**Artifact under review**: ADR-001, metadata draft/standard, exact revision and UTF-8 body SHA256 above. The hash was calculated from the exact body returned by scoped forgeplan_get, without newline normalization or frontmatter stripping, using read-only Python. Both requested pins matched before any Evidence creation.

**Source inputs**: Actual scoped bodies of active/standard PRD-001 updated_at=2026-10-18T20:51:11.875851+00:00 and active/standard SPEC-001 updated_at=2026-10-18T20:51:12.611918+00:00; ADR-001; AGENTS.md; .codex/agents/forgeplan-evidence-gatherer.toml. EVID-007 was read for canonical Evidence structure, not adopted as fresh ADR conclusions. EVID-010/EVID-011 were not used. Original source version/date 1.0 / 2026-10-18 and ADR/source dates are preserved; the original attachment and external documentation were not independently reverified in this review. PRD's embedded source appendix is provenance, not a new external verification claim.

**Methodology**: Fresh independent model ADI: abduce alternatives, deduce consequences against FR-01–08, AC-01–18, AX-01–12 and C01–C08, then select by requirements fit and explicit falsification. Inspect architecture dependency direction, shared/mutable state, error/retention boundaries and future proof obligations. Metadata controls active parent status despite historical draft/proposal prose. No implementation, tests, browser/live calls or performance measurements occurred.

Scoped MCP connection was confirmed by successful forgeplan_health and scoped get calls. Health returned verdict=healthy, verdict_summary="Project looks healthy.", with 12 advisory phase mismatches; this aggregate is not a gate decision. No begin/unlock-build or pipeline mutation was needed or performed for document review.

**Tool execution status, separate from independent model ADI**: Exactly one actual scoped forgeplan_reason invocation was attempted with id="ADR-001", save=false. Retained observed fields:

The retained orchestrator observation was status=failed and error.message="MCP tool call requires approval, but approval policy is never"; no completed ADI output was retained. No retry, alternate route or bypass was attempted. The following hypotheses are this reviewer's independent model ADI, not successful tool ADI.

maintenance_identity: maintainer/adr-evidence-20261019-01

This narrow provenance correction is based on the captured orchestrator event fields. Independent hypotheses, verdict, and target pins are unchanged.

## Findings

### Hypothesis A — one modular polling process with an immutable validated snapshot

Abduction: The accepted MVP can be represented by a single application with pure selection/routes/rendering and a Telegram adapter. A database or network catalogue is unnecessary if the owner replaces a strict local snapshot only between restarts.

Evidence and deduction: ADR's module table gives models no dependencies, geo only models, routes only models, render models/routes, and startup composition over config/catalog/adapter. Telegram types stay at the edge. A complete immutable tuple, including inactive records, is loaded before constructing the client/polling; the offline entry bypasses token/config/aiogram. This supports SPEC C01/C02 and AX-09/12 with one acceptance boundary. Exact unrounded Haversine ranking, code-point id ties, min(limit,count), no radius/rating reorder and request-specific route endpoints match FR-03/06/07. Explicit lat/lon order, pd/mt/auto and <=6 fractional URL digits preserve the PRD link contract. The C4 diagrams distinguish the executable app from its local file and show the user opening Yandex; they add no app-to-Yandex enrichment edge.

Falsification: Future startup polling on an invalid last/inactive record, different offline acceptance, mutable nested catalogue state, adapter-derived global origins, app-to-Yandex requests, or changed query ordering would refute this fit. Future load measurements showing one process cannot meet an approved workload would reopen the topology, rather than retroactively establish failure now.

Trade-offs: Whole-file failure sacrifices availability for integrity; updates require restart; process death loses transient work. O(n log n) sorting and retained in-memory snapshot have no established capacity. These costs are explicit and consistent with an unmeasured MVP. Selected.

### Hypothesis B — independently spawned handlers plus locks, or a global sequential worker

Abduction: aiogram tasks with a per-chat lock might appear sufficient for isolation; one global worker might simplify ordering.

Evidence and deduction: A lock only orders acquisition after scheduling and does not establish ingress order. A global worker lets one chat's retry_after delay every chat. Both alternatives undermine AX-06's combination of same-chat FIFO and cross-chat progress. The repaired ADR instead enqueues synchronously in polling order before waking a sole per-chat worker and completes each request/send sequence before the next. It also explicitly calls for race-safe idle-worker removal so a concurrent enqueue is not orphaned. Mutable queue metadata is distinguished from request-local origin, reply id, Cards and cursor.

Falsification: Deterministic interleavings showing reordered accepted updates, two workers for one chat, cross-chat origin/reply mixing, or a queue cleanup race losing an accepted message would reject the selected scheduler implementation. Conversely, a concrete alternate design proving these exact ordering/progress properties could replace the mechanism at RFC review without weakening the contract.

Trade-offs: Chat workers provide isolation but add lifecycle/resource complexity. Queue admission bounds, overload behavior, drain deadline and cancellation ownership remain RFC obligations. This ADR supplies invariants, not executable scheduling or shutdown proof. Rejected alternatives do not justify claiming the proposed scheduler already works.

### Hypothesis C — durable services/queues or remote enrichment

Abduction: A broker/database and multiple services might offer replay and scaling; live ratings/geocoding could reduce owner preparation.

Evidence and deduction: No accepted requirement demands durability, replicas or enrichment. Persistent queued locations introduce retention and coordination obligations conflicting with the chosen no-history boundary unless separately approved. Geocoding, page fetching, route-time ranking or live ratings change FR-06/08 and AX-11, and cannot substitute for the owner's one-branch semantic acceptance. The ADR's one polling instance per token, no overlapping rollout, explicit restart losses and no bot-to-Yandex calls preserve scope.

Falsification: An approved durable-work or measured scale requirement would undermine the current topology selection. Discovery of mandatory hidden Yandex credentials, fetches, redirects, coordinate extraction or persistent location storage would contradict the current architecture immediately. No such dependency is introduced in this text.

Trade-offs: More infrastructure could offer resilience but raises deployment, retained-data and duplicate-delivery complexity. Enrichment offers different features with external availability and data-use contracts. Reject both for this MVP; no economic superiority or demand is measured.

### Hypothesis D — replay on uncertain delivery or restrict catalogue URLs to guarantee sending

Abduction: Retrying timeouts could improve apparent completion; imposing a URL cap could make transport easier.

Evidence and deduction: Both shortcuts undermine accepted boundaries. The ADR permits at most one additional attempt for an explicit retryable Telegram 429/RetryAfter refusal, waits at least retry_after and makes cancellation interruptible. A second refusal ends remaining delivery. Forbidden/blocked stops immediately; ambiguous timeout/transport failure is never automatically replayed. The confirmed-send cursor prevents resending the introduction/cards and prevents restarting the set. The boundary covers help/fallback and avoids recursive failure notification. Polling reconnection does not authorize search replay. This implements a defensible document policy for AX-07 rather than promising exactly-once delivery.

SPEC C04/C06 has no additional organisation-URL length cap. Putting URLs in keyboard data separates them from HTML text but cannot prove button transport support for every syntactically valid URL. The repaired Risks section explicitly forbids silently capping, trimming, dropping buttons or rejecting a valid catalogue, and requires RFC compatibility characterization plus owner resolution of any demonstrated conflict.

Falsification: A third send attempt, replay after ambiguous acceptance, duplication of confirmed cards, recursive notification, or an added validator URL cap would directly violate this architecture. Future proof of an undeliverable SPEC-valid URL would establish a requirement/platform conflict needing explicit resolution; it would not license a hidden schema change.

Trade-offs: Conservative replay policy accepts partial delivery and possible loss instead of duplicate delivery. Unrestricted URL syntax retains catalogue fidelity while leaving a real transport-compatibility risk. Reject shortcuts; retain the proposed bounded refusal-only policy and explicit RFC closure.

### Contract comparison and substantive-defect assessment

C01–C03: ADR preserves strict UTF-8, no BOM/unpaired surrogates/duplicate members/nonstandard numbers, root array/object entries, atomic fail-fast across inactive rows, and identical startup/offline diagnostics. Path/class/field plus normalized id or zero-based index, with specified file/root pseudo-fields, remain required. Ordering of first errors is not falsely standardized.

C04/C05: Closed 13 fields; exact trim set; lengths in code points; no Unicode/case/internal whitespace rewriting; normalized case-sensitive id uniqueness; finite inclusive numeric bounds excluding bool/string/null; same coordinates allowed. Omitted active=true differs correctly from null/blank invalid. Nullable optional omitted/null/blank become absent; rating_source omitted/blank=catalog but null invalid. Semantic address/branch/link correctness stays with owner, without geocoder or city-house regex.

C06–C08: Exact HTTPS authority/host/path/port/percent-control rules remain normative through C06, with no network resolution and accepted URL preserved after trim. Dates are strict ASCII Gregorian 0001–9999 without freshness/future restrictions. Present yandex rating requires valid present URL/check date; absent rating invents nothing; all present fields validate even if unused. Historical SPEC proposal language is expressly not grounds to relax its active contract.

PRD presentation, privacy and lifecycle: ADR retains exact Russian UI/fallback obligations, card/button order, source/date labels, origin-bound replies, initial live versus edited update behavior and private-chat restriction. Escape catalogue HTML once; route coordinates are URL data. Logs use allowlisted stage/code/random request id and exclude raw updates, identifiers, token, origin, URL/Card, exception payload and third-party DEBUG dumps. Local completion/error/cancellation releases request state; waiting payload retention is acknowledged rather than denied. Telegram/browser history is outside local deletion promises.

No substantive contradiction requiring ADR repair was identified at this pin. Specific unresolved risks are the real URL transport conflict possibility, unbounded queue growth before RFC admission design, idle-worker/cancellation cleanup races, and library error-log leakage. These are material future proof obligations, explicitly acknowledged in this repaired ADR. The architecture verdict would change if they were claimed solved or schema/retention/FIFO semantics were weakened. They are not misrepresented as runtime PASS.

## Result

**Selected hypothesis**: A — single modular long-polling application with strict immutable startup snapshot, together with the FIFO, refusal-only retry and privacy boundaries defended above.

**Verification method**: Direct document comparison of exact scoped target and active parent bodies; independent model abduction/deduction/induction; exact returned target-body SHA256 calculation. Four distinct hypotheses evaluated; one architecture selected; zero runtime tests performed. The one tool reason attempt was refused as recorded.

**Result**: review_verdict=PASS and canonical verdict=supports for document-level architectural fit only. Future RFC must close exact compatible dependency pins, bounded resources/admission without silent loss or retention changes, finite shutdown drain/cancellation and session closure, HTML text and URL-button payload characterization, deterministic concurrency/fault injection and log-capture verification. A demonstrated transport conflict must be resolved before claiming AC-15/AX-05 completion.

## Interpretation

This Evidence supports use of this exact ADR as architecture input to future RFC design. It proves no implementation correctness, FIFO timing, queue capacity, cleanup, reliability, dependency compatibility, external service behavior, real-place accuracy, demand, live acceptance or activation readiness. Source dates are not changed to the review date. Structural validation of this Evidence is a separate schema check, not an ADI provider result or Guardian decision.

## Congruence Level Justification

CL3: direct same-context review of the exact target against its actual active normative parents. This measures contextual congruence, not runtime confidence or reliability score. Generator and reviewer identities are distinct. No scores, lifecycle/activation decisions, source/test/pipeline edits or other Evidence updates are authorized or performed.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| ADR-001 | EVID-013 informs ADR-001 |

The relation is created through parent_id=ADR-001 on this Evidence only. PRD-001 and SPEC-001 are read-only source inputs, not newly mutated parents. EVID-013 remains draft pending the main orchestrator's separate workflow.

## Evidence integrity checks

Scoped forgeplan_validate(EVID-013) returned passed=true, error_count=0, warning_count=1. The remaining SHOULD body-links-drift finding claims ADR-001 is absent from frontmatter links; read-only inspection of the actual projection outer YAML shows target: ADR-001, relation: informs, and the body also declares that link. Scoped graph explicitly shows EVID-013 -->|informs| ADR-001, with no reverse ADR-001-to-EVID-013 edge. The warning persists despite matching declarations; no extra link mutation or parent edit is used to suppress it. This structural warning does not invalidate the observed direction and is not an activation decision.



