---
depth: tactical
id: EVID-020
kind: evidence
last_modified_at: 2026-10-18T21:33:50.078935+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: RFC-001
  relation: informs
status: active
title: Independent Guardian RFC document activation review guardian rfc 20261019 01
---

---
links:
  - target: RFC-001
    relation: informs
---

# EVID-020: Independent Guardian document activation review of RFC-001

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: guardian/rfc-20261019-01
reviewer_role: guardian
generator_identity: creator/rfc-coworking-20261018-01
maintenance_identity: maintainer/rfc-lifecycle-20261019-01
reviewed_artifact_id: RFC-001
reviewed_artifact_updated_at: 2026-10-18T21:21:34.881083+00:00
reviewed_artifact_body_sha256: e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177
guardian_verdict: PASS
client_date: 2026-10-19
review_scope: document activation only

## Measurement

Read AGENTS.md and exact .codex/agents/forgeplan-guardian.toml through read-only shell. This isolated verifier made its own gate decision without delegation or creator certification. Read actual role-scoped forgeplan_get bodies of RFC-001, PRD-001, SPEC-001, corrected ADR-001, and every Evidence linked to RFC in the persisted graph: EVID-014 through EVID-018. Read original findings rather than adopting wrapper assertions. No reason, score, score-all, acceptance tests, package installation, source/test/pipeline edits or lifecycle action performed.

Exact UTF-8 MCP get.body strings, including embedded frontmatter and original newlines, were safely single-quoted into read-only python3 -c using hashlib.sha256(body.encode('utf-8')).hexdigest(). All four commands exited 0 and matched these pins; projection files were not hashed:

| Input | Metadata status/depth | updated_at | Exact get.body SHA256 |
|---|---|---|---|
| RFC-001 | draft/standard | 2026-10-18T21:21:34.881083+00:00 | e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177 |
| PRD-001 | active/standard | 2026-10-18T20:51:11.875851+00:00 | 7b45fd412dde95070622d545f84240a5a77c2b574daf456171984311d05db71d |
| SPEC-001 | active/standard | 2026-10-18T20:51:12.611918+00:00 | 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8 |
| ADR-001 | draft/standard | 2026-10-18T21:08:52.191284+00:00 | 9e2b9ad67078ad2cd3534714efd7a32d3f0ef86ba4899def5bf74091130845b5 |

Fresh scoped gets after methodology/context/validation returned identical bodies and exact stamps for all four before creation of this Evidence. Active metadata governs historical draft/proposal prose in parents. ADR lifecycle activation is separate from its body revision; at this observation it remained draft. No ADR lifecycle change would itself prove a body change.

Read-only command/result evidence:
- python3 .codex/forgeplan-methodology-gate.py RFC-001 --mode methodology: exit 0; S10,S11,S12,S13,C4 each 2/2; 10/10 = 100%, PASS.
- Inspected the gate script itself: it reads get/graph/validate; methodology mode does not check active Guardian. Its “Guardian: N/A for Tactical depth” is a default display artifact, not the Standard RFC's depth or an exemption. No Guardian existed for RFC at this pre-creation check.
- forgeplan context RFC-001 --json: exit 0; artifact.r_eff=0.8 (stored value, never recomputed), draft/standard, exact frozen stamp, depends_on PRD-001/SPEC-001, Evidence EVID-014..018, MUST=0/SHOULD=1. The context hint to activate is advisory only.
- Scoped health: healthy, no stale evidence/orphans/at-risk/blind spots, 17 advisory active/early-phase mismatches. These advisories and generic implementation suggestion do not authorize Build.
- Scoped validate RFC-001: passed=true, error_count=0, warning_count=1, SHOULD body-links-drift. Scoped graph has both based_on edges; direct read of persisted RFC projection outer YAML confirms PRD-001 and SPEC-001 based_on. Embedded body frontmatter also includes them. This diagnostic is false for these verified edges; it is reported without fixing another artifact.
- Scoped phase RFC-001: validate, advanced_at=2026-10-18T21:07:18.856888Z, history shape->validate. No phase advanced.
- python3 .codex/forgeplan-pipeline.py status: exit 0; route=1, depth=standard, phase=rfc, dev_unlocked=false, rfc_id=null. Status only, no begin/unlock or pipeline write.

## Findings

### Independent resolution of historical concerns

EVID-014 is draft CONCERNS against older RFC stamp 2026-10-18T21:13:48.273934+00:00/hash 42a5e7542164d77030b087c9e2f5ed6ba86de9759d3ca0309e153b341790d034. Its first material finding was silent cancellation/drain of already admitted untouched work on ordinary worker exit. Actual current TC-3, Invariants 4/6, pseudocode and rollout now agree that untouched FIFO envelopes are scheduler-owned. Ordinary death terminalizes only active work exactly once as controlled/ambiguous failure, preserves queued envelopes and transfers to exactly one identity-checked supervised successor. Stale finally cannot remove the successor. No active partial batch or confirmed prefix is replayed. Successor creation failure retains queue and fail-stops; intentional shutdown cancellation is explicitly separate. worker_death_queued_successor_fifo and worker_death_partial_send_no_replay require multiple queued requests, exact counters/ownership/FIFO and other-chat progress. This closes the design omission rather than treating an old concern as stale by date alone.

Its second material finding was missing admission and repeated-cancellation contracts. Current admission commits reservation, enqueue, worker ownership and cursor as one no-await transaction; task-creation failure rolls back the complete pretransaction state and cursor. Precommit cancellation admits nothing; postcommit cancellation before feed return leaves exactly one scheduler-owned admission and committed next-fetch cursor. Terminal accounting/ownership release is exactly-once and independent of cancellable notification awaits; supervised outer finally covers request-finally failure. admission_cancel_capacity_full, admission_commit_feed_return_cursor, admission_worker_creation_rollback, repeated_cancel_worker_finally_notification and worker_finally_exception specify meaningful boundary/fault assertions.

One shielded supervisor coordinator uses nonresetting monotonic stages: ingress join 2s, drain <=10s, worker cancel/join 2s, outer-finally session close 2s, total cooperative bound 16s. Repeated signals defer caller cancellation without resetting deadlines. Startup-acquired session and earlier-stage error paths still reach close. session_close_exception_timeout, startup_failure_before_Bot, shutdown_stage_deadlines_outer_finally and cooperative_cleanup_terminal_counters_offsets require bounded outcomes and exact terminal state. Fail-stop on cancellation/close deadline failure is not claimed as successful leak-free cleanup or arbitrary noncooperative cancellation proof. Compose grace is explicitly future 20s. Specification, pseudocode and named fault matrix agree. These are documentary repairs, with no runtime observation inferred.

### Current evidence, independence and coverage

EVID-015 is draft old-revision ADI, missed EVID-014's material concerns and does not count as current proof. Current metadata makes EVID-016, EVID-017 and EVID-018 ACTIVE despite historical body text saying leave draft.
- EVID-016: evidence/rfc-adi-20261019-02, independent evidence-gatherer, four own-model hypotheses with falsifiers/tradeoffs and explicit repaired-contract challenge.
- EVID-017: reviewer/rfc-system-20261019-02, system-dev PASS; expressly resolves both historical findings on the exact current stamp/hash.
- EVID-018: reviewer/rfc-architecture-20261019-01, architect-reviewer PASS; independently compares parents, corrected architecture and repairs on the same exact stamp/hash.

All three pin the frozen RFC and normative inputs. Identities differ from creator, maintainer and this Guardian. Two distinct current specialist identities exceed Standard's one-reviewer requirement; Critical would require two. No unresolved current BLOCKER was found. S10=2/2 is supported by independent EVID-016 ADI, not a successful reason tool call: recorded actual reason attempts were policy-never denied, with no returned tool analysis. S11=2/2 has two fresh independent specialists. S12=2/2 has real active PRD/SPEC based_on edges and strict normative contract/scenario traceability. S13=2/2 has schema MUST pass and verified lifecycle/graph wiring. C4=2/2 is substantive: L1 people/software context, L2 one executable plus file datastore, user browser channel and no bot-to-Yandex edge. Aggregate applicable coverage is 100%.

Actual parent comparison preserves FR-01..08, AC-01..18, AX-01..12 and C01..08/T01..24: exact Russian content/source/date/fallbacks; raw Haversine/id ranking; two-origin explicit route endpoints; strict full-file/inactive validation; exact trim/default/null/URL/date rules; token-free shared CLI; immutable snapshot; per-chat isolation and no hidden enrichment. Internal None denotes absence, not permission to emit normalized null keys or accept invalid default-field nulls; T04/shared-entrypoint future verification must retain this boundary. Every mapped test remains future, including HTML/max text, SDK raw429/zero retry_after/5xx guard and transitive transport no-replay.

### Weakest evidence and unresolved gates

The weakest product/platform evidence is delivery of unrestricted-length SPEC-valid organisation URLs: visible card-text arithmetic does not prove keyboard transport acceptance, and representative samples cannot establish universal acceptance. No extra URL cap, truncation, button omission or universal delivery claim is approved. Characterize actual pinned adapter/platform outcomes; if a valid input conflicts with platform constraints, obtain an explicit owner requirement resolution before complete AC-15/AX-05/NFR-06 or release acceptance.

Scheduler successor/atomic admission/accounting, repeated cancellation and all-process privacy are sophisticated unimplemented contracts. No executed acceptance, privacy proof, physical zeroization, dependency compatibility, full locked installation, Python3.12.15 run, image digest authentication or container proof exists. SDK/transport claims here are assessed as planned guard obligations, not newly verified external behavior. Owner real catalogue/token and semantic branch/address/coordinate/link checks are missing; demand/load/byte bounds are unmeasured. Volatile crash/shutdown loss, ingress head-of-line blocking and downstream Telegram/browser history remain explicit limits.

These uncertainties remain unproved acceptance gates, and receive no runtime PASS. They do not contradict an honestly conditional future implementation document. Document activation can proceed because the current design repairs the material omissions, has complete applicable independent methodology evidence and no unresolved document BLOCKER. This Guardian PASS is limited to the exact frozen document and inputs.

## Result

guardian_verdict: PASS

Leave this Evidence draft. Exactly one Evidence was created with parent_id RFC-001 and automatic informs relation; only this Evidence body is updated. No target, parent, other Evidence, source/tests, pipeline or status/activation changes are authorized or performed.

## Interpretation

Precise next action for main orchestrator: fresh-check target and parent body pins, validate/read back this Evidence and verify its persisted informs edge, activate EVID-020 first, then activate RFC-001 through normal guarded activation. Separately complete ADR-001's independent activation before Build; an active RFC alone never unlocks source/test writes. Then run readiness and unlock-build through the authorized pipeline. Future Build/proof must execute the named oracles, real target-runtime locked installation and independent verification; retain URL/live/container limits until actually resolved.

## Congruence Level Justification

CL3 project-specific document/hash/graph measurements and independent textual comparison. No application behavior measurement is represented.

## Related Artifacts

| Artifact | Relation |
|---|---|
| RFC-001 | EVID-020 informs RFC-001 |

## Validation Observations

Post-save scoped validate EVID-020 returned passed=true, 0 errors and 1 SHOULD body-links-drift warning. Fresh own get returned draft/standard and exact saved body. Scoped persisted graph explicitly contains EVID-020 -->|informs| RFC-001; read-only sed of its absolute markdown projection confirms the same informs link in outer YAML and embedded body frontmatter. Thus this warning is false for the inspected relation; no link repair is necessary or performed. Fresh post-save gets of RFC/PRD/SPEC/ADR returned all exact pinned stamps, lifecycle statuses and identical bodies. Final own-body SHA256 is reported in handoff after this owned update and fresh get. Nothing was activated.



