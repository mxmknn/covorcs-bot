---
depth: tactical
id: EVID-018
kind: evidence
last_modified_at: 2026-10-18T21:24:45.460113+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Independent frozen RFC architecture review — reviewer/rfc-architecture-20261019-01
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-018: Independent frozen RFC architecture review

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/rfc-architecture-20261019-01
reviewer_role: architect-reviewer
generator_identity: creator/rfc-coworking-20261018-01
maintenance_identity: maintainer/rfc-lifecycle-20261019-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:21:34.881083+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
review_verdict: PASS
client_date: 2026-10-19
review_scope: frozen document design only
status: draft

Reviewer is distinct from generator and maintainer. PASS certifies this architectural document comparison only. It is not runtime, source/test, dependency installation, container, Guardian, activation or Build proof.

## Method

Read AGENTS.md and .codex/agents/forgeplan-reviewer.toml with read-only cat, exit 0. Scoped forgeplan_health returned healthy with 12 advisory active/early-phase mismatches; its generic implementation suggestion does not override the gate. Read scoped forgeplan_get bodies for RFC-001, active PRD-001 and SPEC-001, corrected draft ADR-001, EVID-014 and historical EVID-015. Challenged specification, pseudocode, dependencies, ownership, failure outcomes and future acceptance rather than adopting another review's verdict. No reason or score call.

Exact returned body strings, including embedded frontmatter and original newlines, were supplied with shell-safe single quoting to:
python3 -c 'import sys,hashlib; print(hashlib.sha256(sys.argv[1].encode("utf-8")).hexdigest())'
All four commands exited 0. These are MCP get.body hashes, never projection-file hashes.

| Input | Ground-truth status/depth | updated_at | UTF-8 body SHA256 |
|---|---|---|---|
| RFC-001 | draft/standard | 2026-10-18T21:21:34.881083+00:00 | e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177 |
| PRD-001 | active/standard | 2026-10-18T20:51:11.875851+00:00 | 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d |
| SPEC-001 | active/standard | 2026-10-18T20:51:12.611918+00:00 | 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8 |
| ADR-001 | draft/standard | 2026-10-18T21:08:52.191284+00:00 | 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5 |

Active parent metadata prevails over historical proposal/draft prose. ADR is separately gated architecture input and supplies no Build authorization. EVID-015 reviewed the older 21:13:48 revision, missed material concerns and is not current proof.

Read-only rg --files --hidden excluding .git/.forgeplan/.codex returned only AGENTS.md and .gitignore outside governance material; no application or tests exist. cat .forgeplan/codex/pipeline.json returned phase=rfc, depth=standard, route=1, dev_unlocked=false, rfc_id=null. git status --porcelain -uall showed untracked planning/guard material. No runtime test was possible or claimed. No source, tests, config, pipeline or existing artifact was changed. Exactly one scoped new(kind=evidence,parent_id=RFC-001) created EVID-018 with informs; only this new EVID body is updated.

## Findings

### 1. Supported architecture and requirement fidelity

Architecture module table and corrected ADR agree: models/config are inward foundations; catalog/geo/routes use models; render uses models/routes and never geo; telegram_app owns SDK adaptation and receives Settings/snapshot; __main__ composes. Inert package and stdlib shared CLI keep token/aiogram/network out of standalone validation. C4 L1 correctly uses people/software systems; L2 has one executable Container and a ContainerDb symbol explicitly representing a JSON file, not a second executable/database service. Browser is a user channel and there is no bot-to-Yandex edge.

FR01–08 and all AC01–18/AX01–12 have owned future checks: dynamic exact start/request_location, manual-before-start/venue/initial live and edited suppression, group direction/help, active-only exact raw-distance/id ordering, extreme origins, parsed three-mode/two-origin links, exact source/date/fallback/HTML UI, full startup validation, FIFO/isolation, fault containment and all-sink privacy. No hidden radius/rating sort, enrichment, LLM or invented data. These mappings establish design traceability only.

### 2. Supported strict contract; internal None is a representation boundary

TC-1 preserves all C01–C08: strict UTF-8/BOM/surrogates/duplicate members/nonfinite rejection; closed 13 fields, exact trim set and code-point lengths, case-sensitive normalized ids, no Unicode normalization/coercion; strict numeric bounds and active/source null/default distinctions; nullable absence; exact Gregorian ASCII dates without freshness; conditional stored yandex rating dependencies. C06 retains precise authority/port/path/percent/control rules, exact accepted URL preservation and no URL cap or fetch. C03 remains shared diagnostic class/context with a deliberate standalone contextual channel and fixed safe bot event. Inactive/last defects reject the entire file.

T01–T24 mapping covers defaults/types/absence/limits, coordinates/identity, dates, URL valid/refusal/encoding/shortlinks, rating dependencies, cardinalities, inactive/atomic input failure, exact preservation and owner semantics. Owner branch/city+house/coordinate/link/phrase acceptance is distinct from syntax; ll/address cannot replace coordinates.

SPEC's normalized missing-key semantics were specifically challenged against frozen dataclass None. RFC calls None an internal absent representation and expressly preserves required/default null distinctions. This is coherent only as a semantic representation: it does not authorize emitting explicit null keys where the normalized external contract requires absence, nor accepting null for active/rating_source. No serialization contract or implementation exists here; the future T04/shared-entrypoint checks must verify that boundary. Tuple immutability likewise preserves complete ordered success semantics, not partial acceptance.

### 3. EVID-014 material lifecycle concerns repaired in this exact document

Finding 1's ordinary worker-death queue loss is removed. TC-3, Invariants 4/6 and worker outer-finally now make untouched FIFO scheduler-owned; ordinary death terminalizes/releases only active work once, preserves queued work and transfers to exactly one identity-checked supervised successor. Stale finally cannot remove successor; active ambiguous send and confirmed prefix never replay. Successor-creation failure retains queue and fail-stops explicitly rather than discarding work while claiming continuation. worker_death_queued_successor_fifo, worker_death_partial_send_no_replay and worker_finally_exception specify corresponding independent future fault oracles, including other-chat progress and exact counters.

Finding 2 now has a no-await reservation/enqueue/worker-ownership/committed-cursor transaction, task-creation rollback to pretransaction state, precommit cancellation admitting nothing, postcommit cancellation preserving one admission and the next fetch cursor. admission_cancel_capacity_full, admission_commit_feed_return_cursor and admission_worker_creation_rollback explicitly cover former race gaps.

Shutdown is separate from ordinary worker death. One shielded supervisor coordinator defers repeated caller cancellation; no-await accounting survives notification/finally faults. Nonresetting stage deadlines are ingress join 2 + drain 10 + worker cancel/join 2 + outer-finally session close 2 = 16 seconds cooperatively, with future compose 20-second grace. Startup-acquired session is tracked before successful Bot construction; earlier cleanup errors still reach close. Close timeout/error has no unbounded follow-up join. Named repeated-cancel, close-timeout, startup and stage-deadline tests plus terminal counters/offsets match specification and pseudocode. This is an adequate repaired design/test obligation, not executed cancellation proof or a guarantee against a blocked event loop.

### 4. Delivery/resources/privacy challenged with explicit limits

Exact per-request immutable Origin, source/reply/destination, result/cards and cursor prevent a shared latest-origin design. All sends use source ReplyParameters with allow_sending_without_reply=False; deleted-source failure stops. Ordered limit=1 ingress admits before fetching next; global64/chat8 include active and allow one fetched unadmitted payload. Queue wait is outside 90-second service. A saturated chat can block ingress for later chats; admitted other chats progress. This bounds local envelope count, not bytes, catalogue size, external retention, queue residence or latency.

Only confirmed raw HTTP429 refusal permits one current-message retry with full waits/budget; ambiguous timeout/network/decode/5xx stop. Raw status guard precedes SDK classification. sdk_guard_raw_status_edges and transitive_transport_no_replay now include zero retry_after, malformed/ok/mismatched429, 5xx+retry_after and actual transport attempts. This addresses EVID-014 finding 3 as future proof, not verified SDK behavior.

All-process fixed-field sinks before Bot include DEBUG, root/library/warnings, loop/top-level and stdout/stderr. Cleanup forbids retained completed history but does not promise physical zeroization or deletion of Telegram/browser history. Future adversarial retained-sink and lifecycle checks remain essential; sink replacement could suppress useful diagnostics or leak on bootstrap failure if implemented incorrectly.

### 5. Text, URL, dependency and handover limitations remain honest

RFC text arithmetic uses 1150 catalogue code points, at most2300 UTF-16 units plus256 static units, below4096 after entity parsing; escaped wire expansion is distinct from visible text and URLs are keyboard data. Max-astral/HTML/source/date tests remain future. Unlimited organisation URL transport cannot be proved by this arithmetic or representative platform samples. The RFC preserves the button and schema without a cap and withholds complete AC15/AX05/NFR06 acceptance pending actual characterization/conflict resolution. No universal URL guarantee is approved.

TC-4 gives exact proposed direct Python/SDK/model/test/image pins, but expressly requires complete transitive runtime/dev locks, hashes, real3.12.15 resolver/install/test and separate container proof. I did not authenticate external registries, versions or image digest and do not certify availability/compatibility. Host3.14 is insufficient. TDD U1–U5 ownership/delta, future RED/GREEN/REFACTOR records, unborn Git inventory without assumed HEAD, single-poller rollout and compatible image/catalogue rollback are realistic future obligations. No safe prior pair means remain stopped; interrupted work is not durably replayed.

## Result

PASS for the exact frozen document design only. EVID-014's material design omissions are actually repaired across the normative lifecycle, pseudocode and fault acceptance matrix. No additional material architectural contradiction found under active parents. Unbounded URL delivery remains an explicit unresolved acceptance risk, not hidden completion.

## Interpretation

S10 alternatives/tradeoffs and creator reason-attempt limitations, S11 FR/AC/AX/NFR fidelity, S12 C01–C08/T01–T24/specification/pseudocode/TDD, and S13 exact freeze/independent identity/evidence attribution were challenged within this specialist scope. This is not independent ADI or complete multi-role activation coverage. Active independent Evidence and fresh Guardian remain separate obligations; no activation, score or Build unlock.

## Congruence Level Justification

CL3: direct exact-revision documentary comparison in the target workspace by an assigned architect reviewer distinct from creator/maintainer. Measurement consists of get bodies, exact hashes and read-only repository observations; no application behavior was measured.

## Residual Risk

Real lifecycle/scheduler/SDK transport and all-sink privacy correctness, None-to-absence boundary behavior, unbounded valid URL platform acceptance, byte/load/queue-residence resources, owner semantic data, full dependency locks/3.12 installation/container and manual two-origin/three-mode checks remain unproved. Cooperative shutdown is conditional; fail-stop is not leak-free successful cleanup. Changed frozen inputs invalidate this review.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | EVID-018 informs RFC-001 |

PRD-001/SPEC-001 and draft ADR-001 are read-only review inputs pinned above, not additional Evidence links. Own validation, graph/YAML inspection, final body hash and unchanged-target/parent rechecks are reported from actual subsequent observations in the handoff.



