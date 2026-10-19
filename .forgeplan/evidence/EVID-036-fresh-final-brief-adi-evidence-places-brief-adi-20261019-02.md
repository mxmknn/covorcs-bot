---
depth: tactical
id: EVID-036
kind: evidence
last_modified_at: 2026-10-19T11:27:34.109198+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: NOTE-003
  relation: informs
status: active
title: Fresh final Brief ADI — evidence/places-brief-adi-20261019-02
---

# EVID-036: Fresh final Brief ADI

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-19 |
| Target | NOTE-003 |
| Identity | evidence/places-brief-adi-20261019-02 |
| Requested depth | tactical |
| Actual metadata depth | standard; default unchanged for separate Role D adjustment |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Measurement

Independent documentary examination only. I read the complete current NOTE-003 and older EVID-032 through scoped forgeplan_role MCP, then read this newly created Evidence's canonical template. EVID-032 supplied formatting and historical context only, never implementation proof or the current target pin. I independently calculated SHA256 over the exact returned UTF-8 canonical body in memory; the SHA256 routine also matched the standard abc test vector.

Exact target revision:
- id: NOTE-003
- status: draft
- depth: deep
- updated_at: 2026-10-19T11:24:37.191777+00:00
- canonical bodySHA256: 44705d2681009fce78e87c862ef5ef1536b4fa5783af73454e357ea48cc555b3
- creator: creator/places-brief-20261019-01

The current returned timestamp and independently calculated hash both exactly match the assigned FINAL freeze. This review applies only to that revision.

Scoped health was inspected and returned needs_attention, including existing at-risk RFC and duplicate/phase advisories. These are not a gate verdict for this Brief and do not authorize other changes.

Attempted scoped forgeplan_reason NOTE-003 with save=false. The advertised schema lacks a save parameter; the supplied no-save request returned isError=true: "MCP tool call requires approval, but approval policy is never". No successful provider reasoning or saved reasoning proof exists; no bypass was attempted. The ADI below is my independent reasoning.

## Findings

The amended Brief consistently separates creator documentary activity from parent-orchestrator operational checks in Intake, Risks and Official references. Parent-provided operational proof reports getChat HTTP 200 private chats with expected usernames for all three configured numeric-admin recipients: two initially succeeded, the third initially returned 400 and subsequently returned 200 at 2026-10-19T11:21:35.891445+00:00. Numeric IDs were privately supplied and intentionally omitted. Both former reachability/attribution documentary concerns are resolved in this revision.

My own finding is documentary consistency with those supplied facts; I did not execute or independently observe any live API call. getChat establishes a point-in-time identity/reachability preflight, not future send success, feature delivery or implementation correctness. Future delivery tests and deployment rechecks remain necessary. Official references are attributed to the creator's reading; I did not browse or independently verify those pages.

The scope coherently replaces the baseline exclusions of database/admin/durable queue while preserving base JSON and validator requirements. B01-B12 remain future acceptance oracles. The critical unresolved boundary is committed local decision/overlay/outbox state versus uncertain external notification: no replay can avoid duplicate attempts while still allowing missed notices. Durable /pending must preserve discoverability independently of notification success.

### Hypothesis H1 — do nothing

Abduction: Preserve the current read-only catalogue and search, handling suggestions outside the bot.

Supporting evidence: This avoids persistence, migration, privacy and delivery complexity. No demand, load or benefit/cost measurements establish an economic need for H3.

Deduction and falsifiers: Under the confirmed request, H1 cannot provide the in-bot wizard, moderation, automatic approved inclusion or restricted registry. Withdrawal of those requirements, or demonstrated satisfaction by the existing process, would favor H1; neither is supplied. Reject for requirement fit, without claiming measured business benefit.

### Hypothesis H2 — reduced manual queue

Abduction: Collect fewer fields, notify moderators and let an operator validate and edit the catalogue manually.

Supporting evidence: Unknown volume could justify a smaller operating model. Human branch/address/coordinate/link checks remain necessary even with H3, so automation cannot remove semantic moderation work.

Deduction and falsifiers: Manual inclusion contradicts the confirmed automatic inclusion requirement; reduced fields fail the full catalogue contract. A notification-only queue risks losing discoverability after ambiguous sends. A durable pending queue helps but adding complete fields, atomic decisions and automatic overlay approaches H3's obligations. Explicit owner acceptance of reduced scope and manual inclusion would favor H2; it has not been granted. Reject for current scope, retain as a legitimate cheaper alternative if requirements change.

### Hypothesis H3 — selected durable workflow

Abduction: SQLite persists drafts, submissions, minimal registry, approved overlay and notification intents; any one numerically authorized moderator commits the final decision.

Supporting evidence: H3 fits the confirmed SQLite, any-one atomic decision and automatic inclusion choices. The Brief requires restart survival, private numeric authorization on every privileged operation, separation of search/wizard state and committed-only approved search visibility. B04-B08 identify relevant crash, concurrency and delivery oracles. These are requirements rather than executed proof.

Deduction and falsifiers: Partial commits, two final decisions, duplicate overlay effects, approved records lost after restart, unauthorized access, search-origin leakage or automatic replay of uncertain sends would falsify an implementation. Selection must be reconsidered if later bounded scheduling, retention and recovery contracts cannot meet preserved constraints. Current documentary evidence does not exclude these failures.

Induction: Select H3 for continued Brief-level planning because it alone fits the confirmed scope among H1-H3. Feasibility, usability, demand and operating cost remain unmeasured; this selection depends on later explicit contracts and independent verification.

## Result

One exact current target pin checked; timestamp and independently calculated hash match. Three hypotheses have distinct supporting evidence and falsifiers. Both reachability/attribution documentary concerns are resolved. One scoped reason attempt was refused; zero successful tool-generated reasoning results and zero executed acceptance scenarios are claimed. Exactly one new Evidence was created with parent_id NOTE-003 and automatic informs.

Verdict: supports, limited to documentary support for the current Brief direction. No implementation correctness, Guardian PASS, full Deep PASS, S10-S13 completeness or activation approval is asserted.

## Interpretation

Future PRD must resolve role scope, wizard resume/cancel, notice, admission/abuse limits and retention/deletion across drafts, rejected submissions, users and backups. SPEC must resolve schema/versioning, submit idempotency, IDs and merge order, interaction/timestamp semantics, optional/default behavior, validator interface and field/page/callback/payload bounds. ADR/RFC must resolve transaction/outbox/overlay boundaries, nonblocking DB access, crash durability, bounded scheduling/acknowledgment, uncertain-send lifecycle, recovery, backup/restore, compatible migration/rollback and RPO/RTO. These remain obligations before build readiness.

Old manual route/URL findings remain open; neither B12 nor this Evidence closes them.

Trade-offs: SQLite suits one process but introduces locking, disk, corruption and migration risks. Any-one moderation reduces coordination while giving each moderator final authority. No replay of uncertain sends sacrifices notification completeness; /pending helps discoverability only with a functioning recovery process. Minimal registry still creates access-control and retention obligations. H3 costs more than H1/H2; absent demand evidence prevents a benefit/cost conclusion.

## Congruence Level Justification

Level 3 applies to the exact same frozen planning document and confirmed constraints, not to runtime testing. The independent identity evidence/places-brief-adi-20261019-02 differs from target creator creator/places-brief-20261019-01 and the attributed maintenance roles. Parent operational proof is expressly attributed, not presented as my own observation. Creator baseline/code assertions and external references are not independently verified implementation evidence.

## Limits and status

This Evidence remains draft. Requested tactical depth is bookkeeping only: create defaults to standard and exposes no depth parameter; actual metadata is left unchanged for separate Role D adjustment. No source/tests/helpers/pipeline/Git/runtime/private admin-ID files/.env/tokens/Docker/Telegram/network access or mutations occurred. Only this newly created Evidence was updated; NOTE-003, EVID-032, EVID-033 and EVID-034 were not mutated. No activation, scoring or Guardian decision was performed.

## Related Artifacts

NOTE-003 is the target of the informs relation automatically created by parent_id at creation. EVID-032 is historical formatting/context only. No extra body-links table or link mutation is introduced.



