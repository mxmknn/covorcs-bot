---
depth: standard
id: EVID-015
kind: evidence
last_modified_at: 2026-10-18T21:18:04.379702+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: draft
title: Fresh independent RFC documentary ADI — evidence/rfc-adi-20261019-01
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-015: Fresh independent RFC documentary ADI

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: evidence/rfc-adi-20261019-01
reviewer_role: evidence-gatherer
generator_identity: creator/rfc-coworking-20261018-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:13:48.273934+00:00
reviewed_artifact_body_sha256: 42a5e7542164d77030b087c9e2f5ed6ba86de9759d3ca0309e153b341790d034
review_verdict: PASS
review_date: 2026-10-19
scope: document-only, exact frozen revision

Reviewer and generator identities are distinct. PASS means documentary consistency and independently reasoned planning fit only. It does not certify code, runtime, tests, dependency availability, activation eligibility or Build readiness. This Evidence remains draft for the orchestrator.

## Hypothesis

### Hypothesis H1 — the modular RFC is a coherent future implementation contract

Prediction: the single application can preserve approved scope without a database, enrichment or persistent user history, with explicit future proof obligations.
Evidence: RFC Architecture and TC-1–4 allocate shared strict validation, pure selection/routes/rendering, ordered admission and guarded sending; acceptance tables cover FR-01–08, AC-01–18, AX-01–12 and T01–T24. Active metadata controls parents despite historical proposal prose.
Falsification sought: missing scenario, weaker URL/schema acceptance, omitted source label/button, shared origin or implied ADR unlock. None found in the normative RFC comparison. Future counterexamples include incorrect tie order, accepting invalid inactive records, source-message mismatch or wrong URL endpoints; the named future checks explicitly target these.
Disposition: selected for documentary fit, not demonstrated application behavior.

### Hypothesis H2 — finite retry and queue constants conceal delivery or privacy promises the design cannot honor

Prediction: retries could duplicate confirmed cards; bounded admission could silently drop updates; retained queue work or SDK exceptions could leak origins.
Evidence against the strongest form: TC-3 distinguishes confirmed HTTP429 refusal from ambiguous timeout/network/decode/5xx; one current-message retry, no confirmed replay, full waits, request budget, per-attempt timeout and service deadline are explicit. Global64/per-chat8 counts include active requests; one fetched unadmitted update waits before offset advancement. Privacy defines fixed fields before formatting, all process sinks, INFO/DEBUG, loop/top-level exceptions and reference release.
Remaining falsifiers: SDK status classification occurring too late, hidden transport retry, handler retaining raw updates, worker-removal race or cancellation-resistant cleanup. Fake-clock/barrier/session-guard/privacy checks are planned, not observed. Arbitrary stdout/stderr wrappers are particularly invasive and must be tested for recursion and lost safe events.
Disposition: rejected as a proven documentary contradiction; retained as material implementation risk.

### Hypothesis H3 — unrestricted organisation URLs make the entire plan an unjustified completion claim

Prediction: RFC silently adds a URL cap, truncates links, omits buttons or claims all SPEC-valid URLs deliver.
Evidence: TC-1 preserves no extra length cap; Exact Russian UI separates keyboard URLs from message text and explicitly withholds complete AC-15/AX-05/NFR-06 claims pending platform characterization/owner resolution. The conservative visible-text argument uses 1150 field code points, up to2300 UTF-16 units plus256 static allowance; it does not bound keyboard transport. No universal URL-delivery theorem follows.
Falsification: any acceptance claim treating representative URL samples as proof for arbitrary valid lengths, or a hidden cap in implementation, invalidates this documentary support. No such universal completion claim was found in this draft.
Disposition: rejected as grounds to reject an honestly conditional plan; unresolved platform conflict remains a release/acceptance concern.

### Hypothesis H4 — distributed state or external enrichment is necessary to satisfy approved behavior

Prediction: durable queues, live ratings, geocoding or route-time services are prerequisites.
Evidence against: active FR-06/08 use owner catalogue data, FR-07 requires generated web links, AX-11 forbids network dependence in offline checks. RFC keeps Yandex interaction on the user's browser side, retains stored rating provenance, and defines no automatic coordinate extraction. Crash loss and external history are disclosed rather than solved through persistence.
Falsification: an approved requirement for durable delivery, multiple replicas, live ranking or hot reload would reopen this choice; none appears in the reviewed normative contracts.
Disposition: rejected for current scope. Extra services would add operational and retention costs without satisfying an unmet approved capability.

Selected hypothesis: H1, with H2/H3 residuals and H4 rejected for present scope. Independent model ADI above is this reviewer's reasoning; it is not tool-produced analysis.

## Method

Read repository AGENTS.md and exact .codex/agents/forgeplan-evidence-gatherer.toml using read-only shell cat; rg --files located role files. Used scoped forgeplan_role MCP for health and all artifact reads/writes. No ordinary ForgePlan MCP, CLI mutation, source/test/pipeline edits, score, lifecycle mutation, activation or agents.

Scoped forgeplan_health returned healthy / "Project looks healthy.", with12 advisory active/early-phase mismatches. This is an aggregate observation, not permission to implement. Read full normative RFC in bounded body segments, active PRD FR/AC/AX/NFR and handover obligations, active SPEC C01–C08/T01–T24, and corrected draft ADR architecture input. Full source appendix was not reprinted or independently reverified. EVID-013 was inspected solely for schema headings/structured metadata; its conclusions and reason result were not adopted.

Actual scoped forgeplan_reason(id=RFC-001,save=false) was attempted exactly once. Observed result:
MCP tool call requires approval, but approval policy is never
No returned analysis. No completed tool ADI, provider diagnosis or bypass is claimed.

Exact scoped get .body strings were passed as JSON string input to read-only python3 -c; calculation was hashlib.sha256(x["body"].encode("utf-8")).hexdigest(). No projection, whole MCP response, stripped frontmatter or normalized newline was hashed.

## Results

### Frozen input measurements

| Artifact | Metadata status/depth | updated_at | Exact UTF-8 body SHA256 |
|---|---|---|---|
| RFC-001 | draft/standard | 2026-10-18T21:13:48.273934+00:00 | 42a5e7542164d77030b087c9e2f5ed6ba86de9759d3ca0309e153b341790d034 |
| PRD-001 | active/standard | 2026-10-18T20:51:11.875851+00:00 | 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d |
| SPEC-001 | active/standard | 2026-10-18T20:51:12.611918+00:00 | 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8 |
| ADR-001 | draft/standard | 2026-10-18T21:08:52.191284+00:00 | 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5 |

All supplied frozen pins matched before Evidence creation. ADR is separately gated draft architecture input; it is not an active dependency and never unlocks Build. Body date versus server UTC metadata is preserved, not rewritten.

## Findings

### Requirement and schema fit

FR-01/02/05 map to dynamic exact start text, ordinary request_location keyboard, manual-before-start, venue, group direction and initial-only live location. FR-03/04/06/07 map to active-only exact raw-distance ordering, case-sensitive id ties, per-request origins/replies and parsed route endpoint checks. FR-08 retains rating source/date, absent-rating semantics, short-review/description fallbacks and escaped catalogue text without invention.

C01–03 preserve strict byte/JSON rejection, shared CLI/startup validation and atomic fail-fast including inactive/last records; bot diagnostics deliberately suppress C03 context while standalone retains required context. C04–05 preserve13 fields, exact trim/code-point lengths/default distinctions/unique normalized ids and owner semantic responsibility. Model None is an internal absent-value representation, not permission to change nullable input acceptance. C06 has exact host/path/port/encoding policy with no fetch or length cap. C07–08 preserve Gregorian dates without freshness rules and conditional stored Yandex rating dependencies.

T01–05 have explicit defaults/required/length/absence/type checks; T06–09 cover numeric extremes/samecoords/identity; T10–11 dates; T12–16 URL acceptance/refusal; T17–18 rating dependencies; T19 cardinalities; T20–22 inactive and atomic input failures; T23 preservation versus renderer escaping; T24 owner boundary. These are future scenarios, not test results. RFC's full AC/AX mapping includes cross-chat barrier overlap, FIFO cleanup race, old URL immutability, finite delivery faults and all-sink privacy.

### Delivery, admission and lifecycle challenge

A90s service deadline excludes queue wait: it is not a response-latency guarantee. A slow saturated chat can block ordered ingress for later chats, while already admitted other-chat workers progress. This matches the disclosed trade-off and lacks a contradictory load SLA.64+1 bounds local envelope count, not catalogue bytes, payload byte size, Telegram retention or queue residence time. A prolonged unavailable network/load still needs operational measurement.

Source-deleted sends stop with allow_sending_without_reply=False instead of producing detached replies. Ambiguous failures stop remaining delivery; partial delivery is explicitly permitted, not represented as full success. Offset advance after admission is not durable completion. The10s drain and2s session-close policy is concrete, but relies on cancellation cooperation and correct await/finally paths. Crash loss, no queue replay and no downstream deletion are honestly scoped.

### Privacy and observability challenge

The all-process allowlist is stronger than ordinary exception redaction and addresses raw SDK response/method/cause paths. Its complexity is substantial: bootstrap/import failures, loop contexts, warnings, lastResort and uncontrolled stdout/stderr must actually be contained. Suppression can hide useful diagnostics; fixed event coverage must retain enough stage information. Standalone catalogue context is deliberately separate from bot logs. No assertion here proves secrets are absent from a future process or physically zeroized memory.

### URL and build realism challenge

The visible card size argument is plausible as a conservative documentary bound and preserves six-line source semantics; it does not establish actual HTML parser or URL-button acceptance. Arbitrarily long valid organisation URLs remain the weakest product/platform compatibility point. Owner conflict resolution cannot silently narrow active SPEC, and representative testing cannot establish acceptance for every unbounded input.

TC-4 names Python3.12.15, aiogram3.31.0, pydantic2.13.5/core2.46.5, pytest9.1.1 and a digest-pinned image, while explicitly identifying supplied research provenance and pending full transitive locks. This is a concrete future target, not independently verified availability or compatibility. No external documentation, registry, package installation, runtime or container was accessed in this review. Future real3.12 resolver/hash installation and pinned session-guard behavior are necessary; host3.14 results would not establish target compatibility. Unborn-git inventory and compatible image/catalogue rollback are addressed without assuming HEAD.

### Methodology coverage and trade-offs

S10: four independent hypotheses, falsifiers, deduction and selected inference; actual tool reasoning was denied and is recorded separately. S11: FR/AC/AX/NFR challenge and product risks. S12: normative contracts and scenario mapping. S13: exact frozen scoped bodies, one owned Evidence with parent_id and informs, validation/readback/graph verification. This documents applicable coverage; it does not declare all activation prerequisites satisfied.

Single process and pure boundaries reduce coordination and retention, at the cost of restart updates, whole-file startup rejection, volatile work and ingress head-of-line blocking. Conservative ambiguous-stop policy reduces duplicate risk at cost of missing remaining cards. Fixed sink schemas reduce leak paths at cost of debugging detail. No external enrichment avoids unapproved contracts at cost of owner data work and stored-rating staleness.

## Conclusion

review_verdict: PASS

Documentary approval only for RFC-001 exact revision above. H1 is selected because the plan preserves active requirements, makes hard runtime boundaries explicit and does not disguise unresolved URL/platform or dependency proof as completed acceptance. Residual risks are unbounded URL delivery, load/queue residence and byte resources, cancellation/SDK guard correctness, all-process privacy, full target-runtime locks/install, owner semantic data and later live checks. Any changed target/input revision requires refreshed review.

No implementation readiness, runtime/build/test PASS, Guardian PASS, activation or Build unlock is inferred. Leave EVID-015 draft. Own-ID validation, readback, relation inspection and final frozen-pin rechecks are reported by actual tool results in the handoff.

