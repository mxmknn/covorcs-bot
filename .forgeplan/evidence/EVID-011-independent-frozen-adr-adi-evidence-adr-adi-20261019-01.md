---
depth: standard
id: EVID-011
kind: evidence
last_modified_at: 2026-10-18T21:07:04.046009+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: ADR-001
  relation: informs
status: draft
title: Independent frozen ADR ADI — evidence/adr-adi-20261019-01
---

---
assigned_number: 11
created: 2026-10-18
id: EVID-011
kind: evidence
predicted_number: 11
slug: evid-independent-frozen-adr-adi-evidence-adr-adi-20261019-01
status: draft
title: Independent frozen ADR ADI — evidence/adr-adi-20261019-01
updated: 2026-10-18
links:
  - target: ADR-001
    relation: informs
---

# EVID-011: Independent frozen ADR ADI

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | Server template date 2026-10-18; client review date 2026-10-19 |
| Valid Until | Not asserted; canonical metadata null |
| Target | ADR-001 exact frozen revision below |

## Structured Fields

evidence_type: code_review
verdict: supports
congruence_level: 3

This is independent documentary architecture/contract reasoning, not a code execution or measurement result. “supports” applies only to planning sufficiency with the unresolved obligations below. No application behavior PASS is authorized.

## Review Metadata

reviewer_identity: evidence/adr-adi-20261019-01
reviewer_role: evidence-gatherer
generator_identity: creator/architecture-adr-20261018-01
reviewed_artifact_id: ADR-001
reviewed_artifact_updated_at: 2026-10-18T20:58:11.580229+00:00
reviewed_artifact_body_sha256: 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e
expected_target_updated_at: 2026-10-18T20:58:11.580229+00:00
expected_target_body_sha256: 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e
review_verdict: PASS
review_verdict_reason: Independent documentary ADI supports the architecture as a coherent planning input preserving approved contracts; all runtime claims remain unproved and the identified RFC closures remain mandatory. This is neither Build readiness nor activation nor a runtime acceptance verdict.
client_review_date: 2026-10-19

This isolated reviewer is distinct from the generator and other reviewers. Other Evidence bodies were not used to derive this ADI. The canonical template returned historical server timestamps on 2026-10-18; they are reported faithfully, not changed to manufacture freshness. The target timestamps must remain unchanged. Exactly one Evidence was created with parent_id=ADR-001; only EVID-011 is updated by this process.

## Measurement

Method: independently compare the full scoped-MCP target and active parents against the original owner attachment; abduct alternatives, deduce distinguishing consequences, and select a bounded architectural hypothesis. There are zero runtime experiments or live API checks.

Ground truth and commands:
- Read AGENTS.md and .codex/agents/forgeplan-evidence-gatherer.toml using read-only shell commands.
- Read installed forgeplan-audit/SKILL.md and forgeplan-methodology-check/SKILL.md under /Users/mxmknn/.codex/plugins/cache/forgeplan-codex/forgeplan-codex/0.2.0+codex.20260801200137/skills/. Applied freeze, independent identity, ground-truth, substantive findings and ADI obligations. Full specialist dispatch, activation and Guardian aggregation belong to the parent, not this isolated review. The methodology script was not executed because its CLI ForgePlan operations would violate the scoped-MCP-only restriction.
- forgeplan_role forgeplan_health returned needs_attention, including orphan RFC-001 and advisory early-phase active artifacts. No repair or gate inference was made.
- Fresh scoped forgeplan_get ADR-001 returned draft, exact expected updated_at. SHA256 of its returned body encoded as UTF-8, calculated with Python hashlib.sha256, was exactly the expected 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e before review.
- Scoped forgeplan_get PRD-001 returned active, updated_at=2026-10-18T20:51:11.875851+00:00.
- Scoped forgeplan_get SPEC-001 returned active, updated_at=2026-10-18T20:51:12.611918+00:00. Historical draft/proposal prose in parent bodies does not override active metadata.
- Read full original /Users/mxmknn/.codex/attachments/38a9bdff-7b37-4c55-8851-d338dfe1c340/Pasted text.txt (§1–15); shasum -a 256 returned cbde92035f9e674f3a673f380c0f108b4c60f905e84eac8d48dbe70514e6f040, matching ADR provenance. Its external-document claims are owner-source statements, not current compatibility verification by this reviewer.
- Read role wrapper authorization: evidence may create Evidence with parent_id, may update only owned Evidence, and reason must not save implicit Notes.
- Exactly one scoped forgeplan_reason request was attempted with id=ADR-001, save=false. Exposed tool description lists id/workspace and no save argument; actual call supplied save=false explicitly. Actual wrapper/result: {"content":[{"type":"text","text":"MCP tool call requires approval, but approval policy is never"}],"isError":true}. No generated ADI output was obtained; provider absence was not established. No retry, bypass, CLI fallback or escalation was attempted. The hypotheses below are this reviewer's independent reasoning.
- Scoped forgeplan_new(kind=evidence,parent_id=ADR-001) returned EVID-011, auto_linked=ADR-001. Fresh get of EVID-011 supplied the canonical template; all required structured fields and Measurement/Result/Interpretation/Congruence/Related sections are preserved and populated.
- No forgeplan_score, target mutation, source/test/config/pipeline write, implementation or activation occurred. Fresh post-save scoped validation, Evidence retrieval, graph confirmation and target pin recheck are reported below after actual calls.

## Findings

F1 — Planning fit, informational. A single process is compatible with immutable shared catalogue data and mutable scheduling metadata. Immutability concerns normalized records and snapshot membership, not the entire application. Atomic startup validation followed by polling, restart-only changes and request-local Origin remove the need for distributed consistency in the approved MVP. Source §4/9 and PRD AX-12 support this division. One process still has multiple concurrent chat tasks; process count alone proves no isolation or determinism.

F2 — Ordered ingress is a substantive architectural requirement. The ADR explicitly enqueues synchronously in polling update order before awakening one worker per chat. This addresses a real alternative failure: a lock acquired inside independently scheduled handlers orders acquisition, not arrival. Same-chat complete-delivery FIFO and different-chat concurrency are coherent without global latest coordinates. Actual aiogram dispatch wiring and idle-worker removal races remain unverified. A scheduler that spawns independent handlers before establishing order would falsify conformance.

F3 — Bounded retry is honest and precise. Only an explicit HTTP 429 refusal permits one additional attempt for that individual send, after at least retry_after. Two attempts total is a ceiling, not an obligation to retry after cancellation. A second 429, forbidden recipient or other definite failure ends remaining request delivery; ambiguous transport failure is not automatically retried. Confirmed introduction/cards are not replayed; help and fallback share the boundary and failures cannot recurse. Polling reconnect is separate. This fits PRD AX-07 without implying exactly-once delivery after process death. Runtime exception classification and implicit client retries still require independent fault injection.

F4 — Privacy is coherent but remains a high-consequence verification obligation. Waiting messages necessarily retain payloads transiently; the ADR acknowledges that fact and does not label queues as persistent history. Completed, failed and cancelled request state must be released. No disk queue, completed-search cache or profile is introduced. Logging allowlists cover third-party DEBUG/error output and raw exceptions, not just application success logs. Telegram messages and browser/Yandex history remain outside local deletion promises. Unbounded overload could lengthen transient retention indefinitely, so RFC resource/admission policy and finite shutdown deadline are substantive pending decisions, not accomplished privacy guarantees.

F5 — Contract alignment checked against active SPEC C01–C08, with no approved-rule reopening:
| Contract | Documentary correspondence |
|---|---|
| C01 | Whole strict UTF-8 JSON array; no BOM, unpaired surrogates, duplicate members or nonstandard nonfinite numbers; complete ordered snapshot including inactive entries; fail before polling, no partial/demo fallback |
| C02 | Shared startup/offline validator with identical acceptance, normalization and diagnostic class; no token/network required offline; [] succeeds; command and exit codes are proposed future interfaces |
| C03 | Path/class/field plus normalized id or zero-based index; pseudo-fields and N/A record context for file/encoding/JSON/root; unknown field identified; first-error ordering not a public oracle |
| C04 | Closed 13 fields; exact SPEC trim set and code-point lengths, no normalization/case-folding/coercion; id/name/address 64/150/250 maxima and nonblank; finite bounded coordinates exclude bool/string/null; active omitted=true, null/blank invalid; nullable fields and rating_source default/null distinctions preserved |
| C05 | Owner validates branch/address city+house/coordinates/link correspondence; syntax does not certify real places; no geocoder or fragile address regex; distinct ids may share coordinates |
| C06 | Exact HTTPS yandex.ru/yandex.com host policy; no userinfo/subdomains/trailing-dot/encoded-host/IDN/IP, only omitted port or literal :443; raw /maps or /maps/ prefix; encoded slash/backslash and dot-segment restrictions; whitespace/control/percent checks; preserve URL after trim; no fetch or artificial length cap |
| C07 | Exact ASCII Gregorian YYYY-MM-DD, year 0001–9999; actual leap-day validity; no freshness/future-date restriction |
| C08 | Present yandex rating requires present valid URL/date; all present fields validated independently; absent rating invents nothing; catalog source stays distinct; rendering date/source obligations remain downstream |

ADR invariants defer detailed parsing edge cases to normative C06 rather than replacing the contract. Frozen immutable representations must preserve SPEC normalized missing/default semantics even if language objects use a different internal representation; RFC/verification must make that mapping explicit. Required limits and optional short_review/description/rating_text maxima 200/500/50 are retained.

F6 — Unrestricted valid organisation URLs remain an explicit unresolved delivery risk. Separating keyboard URL data from text prevents URL length from inflating card text, but does not establish arbitrary-length URL transport or client acceptance. No extra schema cap, truncation or silent button omission is authorized. The ADR explicitly requires platform characterization and owner conflict resolution before claiming AC-15/AX-05 complete if unrestricted URLs cannot be delivered. This is a legitimate bounded architecture handoff, not a universal deliverability proof. Max code-point fields, HTML escaping/entity parsing and client limits also require independent observations.

F7 — No API enrichment is coherent. The bot computes Haversine and builds links locally; only the user browser later asks Yandex for a route. Stored ratings remain dated owner data. No search API, scraping, link resolution or coordinate extraction is introduced. This removes an enrichment dependency without claiming Telegram or browser availability. C4 depicts one executable and a file datastore symbol, not two running services.

F8 — RFC closures are still pending. Queue capacity/admission, overload semantics, finite shutdown drain, exact dependency compatibility/pins, maximum parsed Telegram text and URL-button/client behavior are explicitly future work. Their absence does not invalidate the bounded ADR decision; it prevents treating this Evidence as a Build/readiness or application verification PASS. Cancellation, cleanup races and log capture deserve priority in later independent proof. The target's reported body-links-drift SHOULD warning is a tooling consistency concern to report from fresh validation, not grounds to rewrite the target or infer a missing graph relation.

## Independent ADI

### Hypothesis A — One snapshot-owning process with ordered per-chat workers is sufficient for the approved planning architecture

Evidence: source §4/8/9 permits local JSON and one application, requires sequential same-chat processing and no saved history. Active SPEC makes acceptance atomic and restart-based, so one immutable normalized snapshot gives every request a consistent catalogue version. Independent per-chat workers preserve concurrency while keeping complete request delivery ordered. Pure geo/routes/render can be tested offline.

Deduction: no approved operation requires transactions across processes or mutable shared search state. Retry waits affect the same chat, not all users. Immutability must be transitive across contained models, not merely a tuple wrapping mutable entries.

Falsification condition: approved durable replay/multi-replica/hot-update requirements, measured unacceptable catalogue/search blocking or memory growth, observable cross-chat origin contamination, post-start snapshot mutation, or inability to implement ordered ingress/resource policy without breaking accepted behavior. No such runtime observation was collected here.

### Hypothesis B — A single globally sequential dispatcher is the safer sufficient architecture

Evidence for viability: one worker and immutable snapshot simplify ordering, task cleanup and retention analysis. At sufficiently small traffic it can produce correct nearest results and avoid origin mixing without a per-chat registry. This is a viable simple alternative, independently considered rather than a reduced-feature strawman.

Deduction against selection: a long retry_after in one chat stalls all unrelated chats. Active PRD AX-06 explicitly calls for two chats working concurrently. Global serialization weakens that requirement even though no latency SLA exists. Avoiding a worker registry does not remove Telegram partial-delivery or logging hazards.

Falsification condition: deterministic overlap with one chat sleeping for 429 demonstrates the other cannot progress, falsifying compliance with concurrent-chat behavior. Conversely, approved removal of concurrent-chat requirements and measured low-load acceptability would reopen this alternative. No such requirement change is assumed.

### Hypothesis C — Keep one process but load/validate a new catalogue snapshot for every request

Evidence for viability: immutable per-request snapshots avoid mutable hot reload while making owner changes visible quickly. No database or enrichment is necessary. It can preserve atomic acceptance within each request and offers a real operational alternative to restart-only updates.

Deduction against selection: source §4 and active PRD AX-12 specify unchanged snapshot until restart and full startup validation. Per-request reload changes owner update semantics, adds I/O/failure paths while serving, and allows two queued requests to observe different catalogue versions without the approved restart boundary.

Falsification condition: modify file during one process lifetime and observe a later request seeing the new file; that falsifies current AX-12. A future approved hot-update requirement with explicit failed-update behavior would warrant reevaluation. This review does not perform the experiment.

### Hypothesis D — Persist an ingress queue to protect work across crashes

Evidence for viability: a local durable queue could improve recovery without microservices and retain FIFO envelopes and per-send cursors. Crash interruption is a genuine single-process disadvantage.

Deduction against selection: durable queue payloads retain origin, chat/reply identifiers and pending work outside current request memory, changing the approved no-history/privacy and no-persistent-user-state boundary. Send ambiguity survives persistence and needs a larger delivery contract; durability alone cannot yield exactly-once Telegram sends.

Falsification condition: an explicit approved durability/retention requirement plus a bounded, consented storage policy could overturn rejection. Under current requirements, a restart finding retained origins or replaying complete interrupted sets falsifies conformance.

## Result

Selected hypothesis: A, for documentary planning sufficiency only. B violates required cross-chat concurrency; C changes restart-only catalogue semantics; D adds unauthorized retention/durability obligations. No measured scalability superiority, current dependency compatibility or runtime correctness is inferred.

Actual generated reason outcome: unavailable because the one attempted scoped call returned the approval-policy-never refusal quoted above. The independent ADI here is reviewer-authored and attributable, not tool-generated.

## Interpretation

Deduction: a startup-owned immutable snapshot plus per-request Origin and ordered per-chat worker ownership can satisfy the approved behavior without a DB/API enrichment. Explicit per-send state limits retries and avoids blind whole-result replay. Contract validation and semantic owner acceptance remain distinct responsibilities.

Induction: source and active parent consistency support A as the smallest selected architecture among these alternatives that preserves both snapshot lifecycle and concurrent-chat behavior. Confidence is limited to document consistency. It is not evidence of market demand, owner data quality, successful route opening or real send behavior.

Trade-offs: restart updates interrupt availability; one malformed record prevents startup; process loss drops pending work; FIFO produces head-of-line blocking within one chat; O(n log n) sorting and memory need measurement; no enrichment means ratings are saved values; no durable delivery means partial results may remain after failure. Those costs are explicitly accepted at planning level, not measured as harmless.

Risks and limits: queue admission and shutdown may create retention/loss trade-offs that require an explicit RFC policy. Arbitrarily long valid URLs may exceed an external transport/client limit; no hidden catalogue cap can resolve that. Library logging and implicit retries can defeat intended boundaries. Immutable type enforcement, scheduler integration and exception mapping require independent future verification. Owner token/catalogue and later two-origin/all-mode manual checks remain outstanding.

No source, tests, pipeline or configuration was changed. No runtime proof, benchmark, dependency documentation verification, S10–S13 activation certification, Guardian decision or activation is supplied.

## Congruence Level Justification

CL3 means same documentary context: exact frozen ADR body, its freshly read active PRD/SPEC and original owner attachment. It does not mean production measurement or end-to-end reliability. evidence_type=code_review identifies static review; no implementation code was certified.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| ADR-001 | informs |

The informs link was created by parent_id in the single forgeplan_new call, without autoactivation. PRD-001 and SPEC-001 are read-only context, not additional links created here.

## Validation and final freeze check

Post-save outcomes are appended only after actual scoped read-only checks. Evidence stays draft; activation and later Guardian decisions belong to the parent orchestrator.

Actual checks after substantive save:
- Scoped forgeplan_validate EVID-011: passed=true, error_count=0, warning_count=1; SHOULD body-links-drift reports ADR-001 absent from frontmatter links despite the body link declaration and actual graph relation.
- Scoped forgeplan_validate ADR-001: passed=true, error_count=0, warning_count=1; SHOULD body-links-drift names PRD-001/SPEC-001. No target repair was attempted.
- Scoped forgeplan_graph confirmed EVID-011 -->|informs| ADR-001 and both ADR based_on active parent edges. No extra link call was needed.
- Fresh scoped forgeplan_get ADR-001 after save/validation returned draft and updated_at=2026-10-18T20:58:11.580229+00:00. UTF-8 body SHA256 recomputed with Python hashlib was 913d251c3902001f71fff3d4eb4e2ab9bbf63a18189c99bf6c2ac3e7bd52025e: both exact pins still match.
- Structural validation is not a behavior test, generated ADI success, full methodology gate or activation authorization. Final own-Evidence get/hash and final target pin check are reported to the parent on completion.

