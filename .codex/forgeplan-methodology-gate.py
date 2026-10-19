#!/usr/bin/env python3
"""Deterministic S10-S13 coverage and activation gate for ForgePlan artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


STANDARD_DEPTHS = {"standard", "deep", "critical"}
PARENT_RULES = {
    "prd": ({"note", "problem", "solution"}, "active Brief NOTE/PROBLEM/SOLUTION"),
    "spec": ({"prd", "note"}, "active PRD or Brief NOTE"),
    "rfc": ({"prd", "spec"}, "active PRD or SPEC"),
}
PLACEHOLDER = re.compile(r"(?:\{[^}]+\}|\bTODO\b|nothing wrong|no findings?)", re.I)


@dataclass
class Layer:
    name: str
    score: int | None
    maximum: int
    detail: str
    action: str | None = None


class GateError(RuntimeError):
    pass


def _run_json(workspace: Path, *args: str) -> Any:
    process = subprocess.run(
        ["forgeplan", *args, "--json"],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise GateError(process.stderr.strip() or process.stdout.strip() or f"forgeplan {' '.join(args)} failed")
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise GateError(f"forgeplan {' '.join(args)} returned invalid JSON") from exc


def _section(body: str, title: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(title)}\s*$\n(.*?)(?=^##\s+|\Z)",
        body,
        re.I | re.M | re.S,
    )
    return match.group(1).strip() if match else ""


def _field(body: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.+?)\s*$", body, re.I | re.M)
    return match.group(1).strip() if match else ""


def _substantive(text: str) -> bool:
    cleaned = re.sub(r"[`#>*_|\-]", " ", text).strip()
    return bool(cleaned) and len(cleaned.split()) >= 3 and not PLACEHOLDER.search(cleaned)


def _module_count(body: str) -> int:
    affected = _section(body, "Affected Files")
    roots: set[str] = set()
    for path in re.findall(r"(?:^|[\s`|*-])([A-Za-z0-9_.-]+/[A-Za-z0-9_./*{}-]+)", affected, re.M):
        parts = [part for part in path.strip("` ,|").split("/") if part and part not in {"*", "**"}]
        if parts:
            roots.add("/".join(parts[:2]))
    return len(roots)


def _review_identity(body: str) -> str:
    return _field(body, "reviewer_identity")


def _is_fresh(body: str, target: dict[str, Any]) -> bool:
    target_id = _field(body, "reviewed_artifact_id").upper()
    target_revision = _field(body, "reviewed_artifact_updated_at")
    return target_id == str(target.get("id", "")).upper() and target_revision == str(target.get("updated_at", ""))


def _get_artifacts(workspace: Path, ids: set[str]) -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    for artifact_id in sorted(ids):
        try:
            artifacts[artifact_id] = _run_json(workspace, "get", artifact_id)
        except GateError:
            continue
    return artifacts


def evaluate(workspace: Path, artifact_id: str, mode: str = "methodology") -> dict[str, Any]:
    target = _run_json(workspace, "get", artifact_id)
    graph = _run_json(workspace, "graph")
    validation = _run_json(workspace, "validate", artifact_id)
    edges = graph.get("edges") or []
    target_id = str(target["id"]).upper()
    related_ids = {
        str(edge.get("from", "")).upper()
        for edge in edges
        if str(edge.get("to", "")).upper() == target_id
    } | {
        str(edge.get("to", "")).upper()
        for edge in edges
        if str(edge.get("from", "")).upper() == target_id
    }
    related_ids.discard("")
    related = _get_artifacts(workspace, related_ids)
    informs_ids = {
        str(edge.get("from", "")).upper()
        for edge in edges
        if str(edge.get("to", "")).upper() == target_id and str(edge.get("relation", "")).lower() == "informs"
    }
    evidence = [
        related[evidence_id]
        for evidence_id in sorted(informs_ids)
        if evidence_id in related and str(related[evidence_id].get("kind", "")).lower() == "evidence"
    ]

    depth = str(target.get("depth", "tactical")).lower()
    kind = str(target.get("kind", "")).lower()
    standard_plus = depth in STANDARD_DEPTHS
    layers: list[Layer] = []

    if standard_plus:
        adi_active = [
            item
            for item in evidence
            if str(item.get("status", "")).lower() == "active"
            and len(re.findall(r"^### Hypothesis(?:\s|$)", str(item.get("body", "")), re.I | re.M)) >= 3
        ]
        adi_partial = [
            item
            for item in evidence
            if len(re.findall(r"^### Hypothesis(?:\s|$)", str(item.get("body", "")), re.I | re.M)) > 0
        ]
        if adi_active:
            layers.append(Layer("S10 FPF ADI", 2, 2, f"{adi_active[0]['id']} is active and contains >=3 hypotheses"))
        elif adi_partial:
            layers.append(Layer("S10 FPF ADI", 1, 2, "ADI Evidence exists but is incomplete or inactive", "Activate an EVID with three ### Hypothesis sections"))
        else:
            layers.append(Layer("S10 FPF ADI", 0, 2, "No linked ADI Evidence", "Dispatch forgeplan_evidence_gatherer and link its EVID with informs"))

        reviewers: list[dict[str, Any]] = []
        partial_review = False
        for item in evidence:
            body = str(item.get("body", ""))
            role = _field(body, "reviewer_role").lower()
            findings = _section(body, "Findings")
            verdict = _field(body, "review_verdict").upper()
            reviewer_identity = _review_identity(body)
            generator_identity = _field(body, "generator_identity")
            if findings:
                partial_review = True
            if (
                role
                and role not in {"guardian", "evidence-gatherer"}
                and _substantive(findings)
                and verdict == "PASS"
                and str(item.get("status", "")).lower() == "active"
                and reviewer_identity
                and generator_identity
                and reviewer_identity != generator_identity
                and _is_fresh(body, target)
            ):
                reviewers.append(item)
        identities = {_review_identity(str(item.get("body", ""))) for item in reviewers}
        required_reviewers = 2 if depth == "critical" else 1
        if len(identities) >= required_reviewers:
            layers.append(Layer("S11 BMAD review", 2, 2, f"{len(identities)} fresh independent reviewer identity(s)"))
        elif reviewers or partial_review:
            layers.append(Layer("S11 BMAD review", 1, 2, "Review Evidence is incomplete, stale, inactive, or lacks distinct identity", f"Record {required_reviewers} fresh PASS reviewer EVID(s) with non-empty ## Findings"))
        else:
            layers.append(Layer("S11 BMAD review", 0, 2, "No qualifying reviewer Evidence", f"Dispatch {required_reviewers} independent reviewer(s)"))
    else:
        layers.append(Layer("S10 FPF ADI", None, 2, "N/A for Tactical depth"))
        layers.append(Layer("S11 BMAD review", None, 2, "N/A for Tactical depth"))

    target_edges = [
        edge
        for edge in edges
        if target_id in {str(edge.get("from", "")).upper(), str(edge.get("to", "")).upper()}
    ]
    orphan_allowed = kind in {"note", "problem", "solution", "refresh"}
    link_ok = bool(target_edges) or orphan_allowed
    parent_ok = True
    parent_detail = "parent rule not applicable"
    if kind in PARENT_RULES:
        allowed_kinds, expected = PARENT_RULES[kind]
        parent_candidates = []
        for edge in edges:
            if str(edge.get("from", "")).upper() != target_id or str(edge.get("relation", "")).lower() != "based_on":
                continue
            candidate = related.get(str(edge.get("to", "")).upper())
            if candidate:
                parent_candidates.append(candidate)
        parent_ok = any(
            str(parent.get("kind", "")).lower() in allowed_kinds
            and str(parent.get("status", "")).lower() == "active"
            for parent in parent_candidates
        )
        parent_detail = expected
    elif kind == "evidence":
        parent_ok = any(
            str(edge.get("from", "")).upper() == target_id and str(edge.get("relation", "")).lower() == "informs"
            for edge in edges
        )
        parent_detail = "informs target"

    supersede_edges = [edge for edge in target_edges if str(edge.get("relation", "")).lower() == "supersedes"]
    delta_ok = True
    if supersede_edges:
        body_upper = str(target.get("body", "")).upper()
        delta_ok = all(marker in body_upper for marker in ("ADDED", "MODIFIED", "REMOVED", "UNCHANGED"))

    if link_ok and parent_ok and delta_ok:
        layers.append(Layer("S12 OpenSpec", 2, 2, f"graph links valid; {parent_detail}"))
    elif link_ok or parent_ok:
        layers.append(Layer("S12 OpenSpec", 1, 2, "Graph, parent activation, or supersede delta is incomplete", "Repair based_on/informs links and required delta sections"))
    else:
        layers.append(Layer("S12 OpenSpec", 0, 2, "Artifact is orphaned or its required parent is not active", f"Link to {parent_detail}"))

    validation_results = validation.get("results") or []
    validation_ok = bool(validation_results) and all(
        bool(result.get("passed")) and int(result.get("errors", 0)) == 0 for result in validation_results
    )
    if validation_ok and link_ok and parent_ok:
        layers.append(Layer("S13 ForgePlan", 2, 2, "schema validation and lifecycle wiring pass"))
    elif validation_ok:
        layers.append(Layer("S13 ForgePlan", 1, 2, "schema passes but lifecycle wiring is incomplete", "Repair graph wiring before activation"))
    else:
        layers.append(Layer("S13 ForgePlan", 0, 2, "forgeplan validate has MUST failures", "Resolve every MUST validation finding"))

    c4_applicable = kind in {"rfc", "adr"} and _module_count(str(target.get("body", ""))) >= 3
    if c4_applicable:
        body = str(target.get("body", ""))
        l1 = re.search(r"(?:C4\s+L1|SYSTEM\s+CONTEXT)", body, re.I)
        l2 = re.search(r"(?:C4\s+L2|CONTAINER\s+DIAGRAM)", body, re.I)
        c4_score = int(bool(l1)) + int(bool(l2))
        layers.append(Layer("C4", c4_score, 2, "C4 L1/L2 coverage for a 3+ module decision", None if c4_score == 2 else "Add both C4 L1 and C4 L2 diagrams"))
    else:
        layers.append(Layer("C4", None, 2, "N/A: fewer than three detected modules or non-architectural kind"))

    applicable = [layer for layer in layers if layer.score is not None]
    earned = sum(int(layer.score or 0) for layer in applicable)
    maximum = sum(layer.maximum for layer in applicable)
    percentage = round(earned * 100 / maximum) if maximum else 100

    guardian_pass = True
    guardian_detail = "N/A for Tactical depth"
    if standard_plus and mode == "activation":
        guardians = []
        for item in evidence:
            body = str(item.get("body", ""))
            if (
                _field(body, "reviewer_role").lower() == "guardian"
                and _field(body, "guardian_verdict").upper() == "PASS"
                and _substantive(_section(body, "Findings"))
                and str(item.get("status", "")).lower() == "active"
                and _review_identity(body)
                and _field(body, "generator_identity")
                and _review_identity(body) != _field(body, "generator_identity")
                and _is_fresh(body, target)
            ):
                guardians.append(item)
        guardian_pass = bool(guardians)
        guardian_detail = f"fresh Guardian PASS: {guardians[0]['id']}" if guardians else "missing fresh active Guardian PASS Evidence"

    passed = percentage == 100 and guardian_pass
    return {
        "artifact_id": target_id,
        "kind": kind,
        "depth": depth,
        "status": target.get("status"),
        "mode": mode,
        "layers": [asdict(layer) for layer in layers],
        "earned": earned,
        "maximum": maximum,
        "percentage": percentage,
        "guardian_pass": guardian_pass,
        "guardian_detail": guardian_detail,
        "passed": passed,
        "actions": [layer.action for layer in layers if layer.action],
    }


def _render(report: dict[str, Any]) -> str:
    lines = [
        f"Methodology coverage for {report['artifact_id']}",
        "=" * (25 + len(report["artifact_id"])),
    ]
    for layer in report["layers"]:
        score = "N/A" if layer["score"] is None else f"{layer['score']}/{layer['maximum']}"
        lines.append(f"{layer['name']:<22}: {score:<5} - {layer['detail']}")
    lines.extend(
        [
            "",
            f"Aggregate: {report['earned']}/{report['maximum']} = {report['percentage']}%",
            f"Guardian: {report['guardian_detail']}",
            f"Verdict: {'PASS' if report['passed'] else 'BLOCKER'}",
        ]
    )
    if report["actions"]:
        lines.append("")
        lines.append("Action items:")
        lines.extend(f"{index}. {action}" for index, action in enumerate(report["actions"], 1))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_id")
    parser.add_argument("--workspace", default=os.getcwd())
    parser.add_argument("--mode", choices=("methodology", "activation"), default="methodology")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        report = evaluate(Path(args.workspace).resolve(), args.artifact_id, args.mode)
    except (GateError, KeyError, OSError) as exc:
        payload = {"artifact_id": args.artifact_id, "passed": False, "error": str(exc)}
        print(json.dumps(payload) if args.json else f"BLOCKER: {exc}")
        return 2
    print(json.dumps(report, indent=2) if args.json else _render(report))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
