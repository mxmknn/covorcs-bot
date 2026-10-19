---
depth: standard
id: EVID-038
kind: evidence
last_modified_at: 2026-10-19T11:48:03.277517+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: PRD-002
  relation: informs
status: draft
title: Independent PRD ADI evidence/places-prd-adi-20261019-01
---

# EVID-038: Independent frozen PRD ADI

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-19 |
| Target | PRD-002 |
| Review identity | evidence/places-prd-adi-20261019-01 |
| Requested bookkeeping depth | tactical; actual default metadata standard, untouched |

## Structured Fields

evidence_type: analysis
verdict: supports
congruence_level: 3

## Measurement

Fresh actual Role B documentary review through scoped forgeplan_role MCP only. Read the full canonical PRD-002, full active NOTE-003 and NEW EVID-038 template. No files, private IDs, credentials, source, tests, Git, pipeline, network, Docker or Telegram accessed; no implementation performed. Created exactly one Evidence with parent_id PRD-002; only this Evidence body updated. Creator is not verifier.

Exact target independently checked: PRD-002 metadata draft/deep, updated_at=2026-10-19T11:45:23.839091+00:00; SHA256 of returned canonical UTF-8 body=8459daa65970e83588b42f3eb7791729ad61ebada9bea8916a64ee22a4daee09. Computed in-memory SHA256, with abc known-vector check. Target generator creator/places-prd-20261019-01; maintenance maintainer/places-prd-consistency-20261019-01 explicitly attributes send-policy, backup-permissions and operator-responsibility corrections. No target mutation.

NOTE-003 metadata active/deep, updated_at=2026-10-19T11:35:41.915321+00:00; independently computed canonical body SHA256=44705d2681009fce78e87c862ef5ef1536b4fa5783af73454e357ea48cc555b3, matching PRD dependency. Historical draft/depth boilerplate inside bodies does not override metadata. PRD declares based_on NOTE-003/refines PRD-001; pipeline prd/source blocked is operator-provided context, not independently inspected pipeline proof.

Own scoped forgeplan_reason attempted for PRD-002 with save=false. Actual result: “MCP tool call requires approval, but approval policy is never”. No reasoning result exists; no bypass or saved reasoning artifact. Following ADI is this independent reviewer's analysis, not tool-generated proof. Health inspected; existing workspace advisory/duplicate/at-risk findings do not certify or veto this documentary decision.

## Findings

1. Form policy enumerates 10 user fields and 3 system fields, preserves the shared catalogue validator and conditional rating rules, and specifies resume/back/cancel/restart/preview. Numeric proposal coordinates are explicit inputs; every arbitrary location/venue remains search origin. AC1–4/14 provide future oracles. This supports the Brief's separation of proposal data and ephemeral search origin.
2. Any one of three numeric private admins can decide; every privileged command/page/callback reauthorizes. Users/pending pages are 10 rows. Transactional decision/publication/intents, capacity reservation before acceptance, three explicit recipients and no uncertain autoreplay make business outcome distinct from notification delivery (AC5–8/11/13/17).
3. Notice must precede first registry persistence; failed notice attempt postpones registry. Registry 90d inactivity, draft 7d, rejected payload/applicant binding 30d, terminal personal outbox metadata 7d and backup 7d are concrete. Pending/approved remain durable; approved applicant binding expires after 30d. Quotas, bounded cleanup, backup file 0600/directory 0700 and current deployment/repository operator ownership constrain exposure without claiming cryptographic protection.
4. Strict 429-only retry, at most two attempts, 10s attempt/60s intent and <=15s retry waiting are explicitly subordinate to retained finite legacy budgets. Read-only base plus committed approved overlay preserves search ordering rules. Actual schedulability, SQL, state transitions, tombstone nonpersonal content, transport chunking and durability need normative RFC specification and independent runtime proof; selected plan need not create separate SPEC-002.
5. GetChat facts in the active Brief confirm all three identities/private-chat reachability only, attributed to the main orchestrator. This reviewer made no Telegram call. Notification delivery to all three and feature behavior remain unproven; older route/URL manual acceptance remains open.

### Hypothesis

H1 — do nothing: preserve existing search and accept proposals outside the bot.
Evidence for: avoids new personal storage, migrations, queue contention and operational backup duties.
Falsifier: required in-bot ten-field submission, durable moderation, automatic approved search and private users view cannot be demonstrated. The Brief's explicit requested outcome and PRD FR-001–009 already falsify H1 as sufficient scope coverage.
Defaults fit: none needed; lowest new operational cost. Risk/trade-off: manual omission and no recoverable product workflow. Reject for this request; no claim that demand research proves H3 economically preferable.

### Hypothesis

H2 — reduced manual queue: collect proposals in a wizard, queue them for an operator to edit base JSON manually.
Evidence for: structured collection can improve completeness with fewer publication states; suitable if automatic publication and durable status were removed by a later owner decision.
Falsifier: committed approval must become searchable after restart without editing the read-only base (FR-007/AC6), and moderation must have one durable final outcome (AC5/7). Manual publication cannot satisfy that contract as written.
Defaults fit: submission quotas and numeric auth remain useful, but registry/privacy and queue recovery still cost effort. Risk/trade-off: lower initial integration cost shifts work, delays and partial publication failures to the operator. Reject under current agreed scope.

### Hypothesis

H3 — durable selected workflow: SQLite draft/submission/registry/approved overlay/outbox with any-one atomic moderation.
Evidence for: directly covers all nine FRs and the Brief's durability, privacy and auto-inclusion direction; AC1–18 define falsifiable future outcomes rather than claiming executed tests.
Falsifiers: duplicate final decisions/overlay after race or crash; pending searchable; changed base bytes; unauthorized reads; registry before successful notice; preserved search origin; uncertain replay; acceptance without all capacity; exceeded legacy shutdown/send bounds. Any demonstrated violation defeats implementation acceptance.
Defaults fit: one pending/user, three submissions/rolling 24h, 1000 pending, 10000 drafts/registry, 1024 unsettled intents/target and two applicant intents are conservative finite admission defaults for unknown demand. Ten-row pages and 100-record/2s cleanup bound work. They are chosen limits, not measured capacity.
Risks/trade-offs: TTLs minimize exposure but remove old drafts/status bindings; no pending/approved TTL protects accepted obligations but can exhaust disk. Three-intent reservation couples admission to the slowest recipient. No uncertain replay trades missed notices for reduced duplicate-send risk; /pending restores discovery, not delivery. Any-one approval is fast but permits one moderator's quality error. Backups allow up to 24h host-loss exposure and seven-day residual deleted data; RTO <=60min requires a drill.

## Result

Selected H3 independently, verdict supports for the exact frozen product planning revision. H1 and H2 fail mandatory outcomes; H3 specifies them with explicit safety boundaries and future acceptance oracles. No material product-decision blocker found in this comparison. Unknown demand, storage/backup budget, usability and workload remain assumptions. This is documentary planning support only: no implementation proof, Guardian PASS, full Deep PASS or activation authorization.

## Interpretation

Proceed through independent document gates toward a normative RFC that resolves algorithms/state/SQL, validator interface, collision handling, bounded callback/chunking/scheduling, transactions, cleanup/tombstones, migrations and compatible rollback. References to SPEC/ADR/RFC are future specification responsibilities, not a requirement to add SPEC-002. Maintain source blocking until active RFC readiness/unlock; this draft does not unlock any stage. S10 has independent H1/H2/H3 and an honestly refused reason attempt; S11 has problem/journeys/FR/risks; S12 has concrete behavior and future AC; S13 has scoped Evidence creation. This analysis does not certify 100% gate coverage.

## Congruence Level Justification

CL3: same-context analysis of the exact canonical frozen PRD and its active parent, by identity distinct from target generator and maintainer. This measures documentary alignment and falsifiability, not deployed behavior or externally verified reachability.

## Related Artifacts

EVID-038 informs PRD-002 through the single parent_id auto-link created by MCP. NOTE-003 is the read active Brief; PRD-001 and SPEC-001 are normative baseline references named in the target, not independently reread here. No additional links or artifacts created.

## Limitations

Reason tool policy refusal remains recorded without fabricated proof. No source/runtime/Guardian/full Deep verification; no delivery tests or old manual route/URL acceptance. Requested Evidence depth is tactical for bookkeeping; actual NEW default standard metadata remains untouched for separate Role D. Evidence stays draft; activation belongs to the main orchestrator.

