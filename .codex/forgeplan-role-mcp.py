#!/usr/bin/env python3
"""Role-scoped stdio proxy for the ForgePlan MCP server.

Codex custom agents inherit MCP servers from their parent. This proxy narrows the
ForgePlan surface per CRUD-R-A role and enforces argument-level constraints that
an MCP tool allow-list cannot express, such as "reviewers may create Evidence
only" and "creators may update only artifacts created in this agent process".
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import threading
from typing import Any


READ_TOOLS = {
    "forgeplan_activity",
    "forgeplan_activity_stats",
    "forgeplan_anomalies",
    "forgeplan_blindspots",
    "forgeplan_blocked",
    "forgeplan_calibrate",
    "forgeplan_claims",
    "forgeplan_contradictions",
    "forgeplan_coverage",
    "forgeplan_coverage_business",
    "forgeplan_decay",
    "forgeplan_dispatch",
    "forgeplan_drift",
    "forgeplan_estimate",
    "forgeplan_export",
    "forgeplan_fpf_check",
    "forgeplan_fpf_list",
    "forgeplan_fpf_rules",
    "forgeplan_fpf_search",
    "forgeplan_fpf_section",
    "forgeplan_get",
    "forgeplan_graph",
    "forgeplan_guard",
    "forgeplan_health",
    "forgeplan_hypothesis_status",
    "forgeplan_journal",
    "forgeplan_list",
    "forgeplan_order",
    "forgeplan_orphans",
    "forgeplan_phase",
    "forgeplan_playbook_list",
    "forgeplan_playbook_show",
    "forgeplan_playbook_validate",
    "forgeplan_plugins_doctor",
    "forgeplan_plugins_info",
    "forgeplan_plugins_list",
    "forgeplan_progress",
    "forgeplan_release_notes",
    "forgeplan_review",
    "forgeplan_route",
    "forgeplan_score",
    "forgeplan_search",
    "forgeplan_session",
    "forgeplan_stale",
    "forgeplan_status",
    "forgeplan_validate",
}

ROLE_TOOLS = {
    "creator": READ_TOOLS | {"forgeplan_link", "forgeplan_new", "forgeplan_reason", "forgeplan_update"},
    "reviewer": READ_TOOLS | {"forgeplan_link", "forgeplan_new", "forgeplan_update"},
    "evidence": READ_TOOLS | {"forgeplan_link", "forgeplan_new", "forgeplan_reason", "forgeplan_update"},
    "guardian": READ_TOOLS | {"forgeplan_link", "forgeplan_new", "forgeplan_update"},
    "maintainer": READ_TOOLS
    | {
        "forgeplan_deprecate",
        "forgeplan_link",
        "forgeplan_supersede",
        "forgeplan_unlink",
        "forgeplan_update",
    },
    "coder": READ_TOOLS,
    "researcher": READ_TOOLS,
    "smith": READ_TOOLS,
}

ARTIFACT_ID = re.compile(r"\b(?:PRD|EPIC|SPEC|RFC|ADR|PROB|SOL|EVID|NOTE|REFRESH)-\d+\b", re.I)


class PolicyError(ValueError):
    pass


def _require(value: bool, message: str) -> None:
    if not value:
        raise PolicyError(message)


def _body_has(body: str, pattern: str) -> bool:
    return re.search(pattern, body, re.I | re.M) is not None


def authorize(role: str, tool: str, arguments: dict[str, Any], owned: dict[str, str]) -> None:
    """Raise PolicyError when a role must not make this call."""

    _require(role in ROLE_TOOLS, f"unknown ForgePlan role: {role}")
    _require(tool in ROLE_TOOLS[role], f"role {role} cannot call {tool}")

    if tool == "forgeplan_new":
        kind = str(arguments.get("kind", "")).lower()
        if role == "creator":
            _require(kind and kind != "evidence", "creator may create planning artifacts, not Evidence")
            _require(arguments.get("parent_id") in (None, ""), "parent_id is only valid for Evidence")
        elif role in {"reviewer", "evidence", "guardian"}:
            _require(kind == "evidence", f"role {role} may create Evidence only")
            _require(bool(arguments.get("parent_id")), "Evidence must be created with parent_id for an informs link")

    if tool == "forgeplan_reason":
        _require(role in {"creator", "evidence"}, "only creator or evidence-gatherer may run ADI reasoning")
        _require(not arguments.get("save", False), "reason output must be persisted as attributable Evidence, not an implicit Note")
        if role == "creator":
            target = str(arguments.get("id", "")).upper()
            _require(target in owned, "creator may reason only about its newly created draft")

    if tool == "forgeplan_update":
        target = str(arguments.get("id", "")).upper()
        status = arguments.get("status")
        _require(str(status).lower() != "active", "activation is reserved for the main orchestrator")

        if role in {"creator", "reviewer", "evidence", "guardian"}:
            _require(target in owned, f"role {role} may update only artifacts created in this agent process")
            _require(status in (None, ""), f"role {role} may not change lifecycle status")

        body = arguments.get("body")
        if body is not None and role in {"reviewer", "guardian"}:
            text = str(body)
            _require(_body_has(text, r"^## Review Metadata\s*$"), "review Evidence requires ## Review Metadata")
            _require(_body_has(text, r"^reviewer_identity:\s*\S+"), "review Evidence requires reviewer_identity")
            _require(_body_has(text, r"^reviewer_role:\s*\S+"), "review Evidence requires reviewer_role")
            _require(_body_has(text, r"^reviewed_artifact_id:\s*\S+"), "review Evidence requires reviewed_artifact_id")
            _require(_body_has(text, r"^reviewed_artifact_updated_at:\s*\S+"), "review Evidence requires the exact reviewed revision")
            _require(_body_has(text, r"^## Findings\s*$"), "review Evidence requires ## Findings")
            _require(_body_has(text, r"^(?:review|guardian)_verdict:\s*(?:PASS|CONCERNS|BLOCKER)\s*$"), "review Evidence requires a gate verdict")
        if body is not None and role == "evidence":
            count = len(re.findall(r"^### Hypothesis(?:\s|$)", str(body), re.I | re.M))
            _require(count >= 3, "ADI Evidence requires at least three ### Hypothesis sections")

    if tool == "forgeplan_link":
        relation = str(arguments.get("relation", "informs")).lower()
        source = str(arguments.get("source", "")).upper()
        _require(not arguments.get("auto_activate_source_if_complete", False), "implicit activation through forgeplan_link is forbidden")
        if role == "creator":
            _require(source in owned, "creator may link only its newly created artifact")
            _require(relation in {"based_on", "refines"}, "creator links must use based_on or refines")
        elif role in {"reviewer", "evidence", "guardian"}:
            _require(source in owned, f"role {role} may link only its own Evidence")
            _require(relation == "informs", "Evidence links must use informs")


def _extract_ids(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        direct = value.get("id")
        if isinstance(direct, str) and ARTIFACT_ID.fullmatch(direct.strip()):
            found.append(direct.upper())
        for item in value.values():
            found.extend(_extract_ids(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_extract_ids(item))
    elif isinstance(value, str):
        found.extend(match.group(0).upper() for match in ARTIFACT_ID.finditer(value))
    return found


class Proxy:
    def __init__(self, role: str) -> None:
        self.role = role
        self.child = subprocess.Popen(
            ["forgeplan", "serve"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.pending: dict[Any, dict[str, Any]] = {}
        self.list_requests: set[Any] = set()
        self.owned: dict[str, str] = {}
        self.stdout_lock = threading.Lock()

    def emit(self, payload: dict[str, Any]) -> None:
        with self.stdout_lock:
            sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
            sys.stdout.flush()

    def client_to_server(self) -> None:
        assert self.child.stdin is not None
        for line in sys.stdin:
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                self.child.stdin.write(line)
                self.child.stdin.flush()
                continue

            request_id = message.get("id")
            method = message.get("method")
            if method == "tools/list" and request_id is not None:
                self.list_requests.add(request_id)
            elif method == "tools/call":
                params = message.get("params") or {}
                tool = str(params.get("name", ""))
                arguments = params.get("arguments") or {}
                try:
                    authorize(self.role, tool, arguments, self.owned)
                except PolicyError as exc:
                    self.emit(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32001, "message": f"ForgePlan role policy: {exc}"},
                        }
                    )
                    continue
                if request_id is not None:
                    self.pending[request_id] = {"tool": tool, "arguments": arguments}

            self.child.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
            self.child.stdin.flush()

        self.child.stdin.close()

    def server_to_client(self) -> None:
        assert self.child.stdout is not None
        for line in self.child.stdout:
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                sys.stdout.write(line)
                sys.stdout.flush()
                continue

            request_id = message.get("id")
            if request_id in self.list_requests:
                tools = ((message.get("result") or {}).get("tools") or [])
                message["result"]["tools"] = [tool for tool in tools if tool.get("name") in ROLE_TOOLS[self.role]]
                self.list_requests.discard(request_id)

            pending = self.pending.pop(request_id, None)
            if pending and pending["tool"] == "forgeplan_new" and "error" not in message:
                ids = _extract_ids(message.get("result"))
                if ids:
                    self.owned[ids[0]] = str(pending["arguments"].get("kind", "")).lower()

            self.emit(message)

    def forward_stderr(self) -> None:
        assert self.child.stderr is not None
        for line in self.child.stderr:
            sys.stderr.write(line)
            sys.stderr.flush()

    def run(self) -> int:
        threads = [
            threading.Thread(target=self.server_to_client, daemon=True),
            threading.Thread(target=self.forward_stderr, daemon=True),
        ]
        for thread in threads:
            thread.start()
        self.client_to_server()
        return self.child.wait()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, choices=sorted(ROLE_TOOLS))
    args = parser.parse_args()
    return Proxy(args.role).run()


if __name__ == "__main__":
    raise SystemExit(main())
