<!-- forgeplan-codex-operating-contract:v2 -->
## ForgePlan Operating Contract

Use ForgePlan for decisions and evidence that must survive beyond the current task.

- Inspect `forgeplan health` before routing substantial work.
- Use `$forgeplan-smith` when the workflow or required rigor is unclear.
- Standard, Deep, and Critical work follows Route -> Brief(active) -> PRD(active) -> RFC(active)
  -> Build -> Prove -> Ship. Draft planning artifacts never unlock the next stage.
- Create or update artifacts through ForgePlan MCP tools when available; use the CLI as fallback.
- Separate generators from verifiers. The agent that changes code does not certify it.
- Evidence supporting an artifact uses the `informs` relation.
- Before every Standard+ activation, require 100% applicable S10-S13 coverage, active independent
  Evidence, and a fresh Guardian PASS. Critical work requires two distinct reviewer identities.
- Never use `forgeplan activate --force`, direct `status=active`, or link auto-activation.
- Start guarded work with `.codex/forgeplan-pipeline.py begin`; source/test writes remain blocked
  until an active RFC passes readiness and `unlock-build` succeeds.
- Keep source edits, artifact mutations, and gate decisions attributable to distinct roles.

Codex role templates live in `.codex/agents/`. Invoke them as focused subagents and wait for all
required reviewers before synthesizing a gate decision.
<!-- /forgeplan-codex-operating-contract:v2 -->
