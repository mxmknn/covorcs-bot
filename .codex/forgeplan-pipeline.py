#!/usr/bin/env python3
"""Manage the fail-closed Brief -> PRD -> RFC -> Build state for Codex."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STANDARD_DEPTHS = {"standard", "deep", "critical"}


class PipelineError(RuntimeError):
    pass


def _workspace(path: str) -> Path:
    current = Path(path).resolve()
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=current,
        text=True,
        capture_output=True,
        check=False,
    )
    return Path(process.stdout.strip()).resolve() if process.returncode == 0 else current


def _state_path(workspace: Path) -> Path:
    return workspace / ".forgeplan" / "codex" / "pipeline.json"


def _read_state(workspace: Path) -> dict[str, Any] | None:
    path = _state_path(workspace)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PipelineError(f"invalid pipeline state: {path}") from exc


def _write_state(workspace: Path, state: dict[str, Any]) -> None:
    path = _state_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _forgeplan_json(workspace: Path, *args: str) -> Any:
    process = subprocess.run(
        ["forgeplan", *args, "--json"],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise PipelineError(process.stderr.strip() or process.stdout.strip())
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise PipelineError(f"forgeplan {' '.join(args)} returned invalid JSON") from exc


def _active_artifact(workspace: Path, artifact_id: str, expected_kind: str) -> dict[str, Any]:
    artifact = _forgeplan_json(workspace, "get", artifact_id)
    actual_kind = str(artifact.get("kind", "")).lower()
    status = str(artifact.get("status", "")).lower()
    if actual_kind != expected_kind or status != "active":
        raise PipelineError(f"{artifact_id} must be an active {expected_kind}; got kind={actual_kind}, status={status}")
    return artifact


def _has_based_on(workspace: Path, source: str, target: str) -> bool:
    graph = _forgeplan_json(workspace, "graph")
    return any(
        str(edge.get("from", "")).upper() == source.upper()
        and str(edge.get("to", "")).upper() == target.upper()
        and str(edge.get("relation", "")).lower() == "based_on"
        for edge in graph.get("edges") or []
    )


def begin(workspace: Path, depth: str, route: str) -> dict[str, Any]:
    if depth.lower() not in STANDARD_DEPTHS:
        raise PipelineError("the guarded pipeline is for Standard, Deep, or Critical work")
    existing = _read_state(workspace)
    if existing and existing.get("phase") not in {"done", "aborted"}:
        raise PipelineError(f"pipeline already active in phase {existing.get('phase')}")
    state = {
        "version": 1,
        "depth": depth.lower(),
        "route": route,
        "phase": "brief",
        "dev_unlocked": False,
        "brief_id": None,
        "prd_id": None,
        "rfc_id": None,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    _write_state(workspace, state)
    return state


def advance(workspace: Path, kind: str, artifact_id: str) -> dict[str, Any]:
    state = _read_state(workspace)
    if not state:
        raise PipelineError("no active guarded pipeline; run begin first")
    if state.get("phase") != kind:
        raise PipelineError(f"expected phase {state.get('phase')}, not {kind}")

    if kind == "brief":
        _active_artifact(workspace, artifact_id, "note")
        state["brief_id"] = artifact_id.upper()
        state["phase"] = "prd"
    elif kind == "prd":
        _active_artifact(workspace, artifact_id, "prd")
        brief_id = state.get("brief_id")
        if not brief_id or not _has_based_on(workspace, artifact_id, brief_id):
            raise PipelineError(f"{artifact_id} must have based_on -> {brief_id}")
        state["prd_id"] = artifact_id.upper()
        state["phase"] = "rfc"
    elif kind == "rfc":
        _active_artifact(workspace, artifact_id, "rfc")
        prd_id = state.get("prd_id")
        if not prd_id or not _has_based_on(workspace, artifact_id, prd_id):
            raise PipelineError(f"{artifact_id} must have based_on -> {prd_id}")
        state["rfc_id"] = artifact_id.upper()
        state["phase"] = "readiness"
    else:
        raise PipelineError(f"unsupported phase kind: {kind}")

    _write_state(workspace, state)
    return state


def unlock_build(workspace: Path, artifact_id: str) -> dict[str, Any]:
    state = _read_state(workspace)
    if not state or state.get("phase") != "readiness":
        raise PipelineError("pipeline must be at readiness before Build can unlock")
    if str(state.get("rfc_id", "")).upper() != artifact_id.upper():
        raise PipelineError(f"Build must use the gated RFC {state.get('rfc_id')}")
    _active_artifact(workspace, artifact_id, "rfc")
    if not _has_based_on(workspace, artifact_id, str(state.get("prd_id", ""))):
        raise PipelineError("RFC lost its based_on link to the active PRD")
    state["phase"] = "build"
    state["dev_unlocked"] = True
    _write_state(workspace, state)
    return state


def finish(workspace: Path, phase: str, reason: str | None = None) -> dict[str, Any]:
    state = _read_state(workspace)
    if not state:
        raise PipelineError("no pipeline state exists")
    if phase == "done" and state.get("phase") != "build":
        raise PipelineError("only a Build-phase pipeline can be completed")
    state["phase"] = phase
    state["dev_unlocked"] = phase == "done"
    if reason:
        state["reason"] = reason
    _write_state(workspace, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default=os.getcwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    begin_parser = subparsers.add_parser("begin")
    begin_parser.add_argument("--depth", required=True, choices=sorted(STANDARD_DEPTHS))
    begin_parser.add_argument("--route", required=True)

    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--kind", required=True, choices=("brief", "prd", "rfc"))
    advance_parser.add_argument("--id", required=True)

    unlock_parser = subparsers.add_parser("unlock-build")
    unlock_parser.add_argument("--rfc", required=True)

    subparsers.add_parser("status")
    subparsers.add_parser("complete")
    abort_parser = subparsers.add_parser("abort")
    abort_parser.add_argument("--reason", required=True)

    args = parser.parse_args()
    workspace = _workspace(args.workspace)
    try:
        if args.command == "begin":
            state = begin(workspace, args.depth, args.route)
        elif args.command == "advance":
            state = advance(workspace, args.kind, args.id)
        elif args.command == "unlock-build":
            state = unlock_build(workspace, args.rfc)
        elif args.command == "complete":
            state = finish(workspace, "done")
        elif args.command == "abort":
            state = finish(workspace, "aborted", args.reason)
        else:
            state = _read_state(workspace)
            if state is None:
                raise PipelineError("no pipeline state exists")
    except PipelineError as exc:
        print(f"BLOCKER: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
