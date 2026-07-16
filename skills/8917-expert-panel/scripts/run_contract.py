#!/usr/bin/env python3
"""Gate heavy runs and validate expert-panel run manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
BRANCH_STATUSES = {"success", "partial", "failed", "timed_out", "cancelled"}
RUN_STATUSES = {"complete", "partial", "degraded", "failed", "cancelled"}
SOURCES = {"native", "persona-injected", "generated"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object")
    return payload


def decide_gate(
    capabilities: dict[str, Any],
    requested_tier: str,
    require_reproducible: bool,
    allow_downgrade: bool,
) -> dict[str, Any]:
    if requested_tier == "light":
        return {
            "decision": "proceed",
            "requested_tier": "light",
            "executed_tier": "light",
            "missing": [],
        }

    required = [
        "isolated_context",
        "timeout_cancel",
        "workflow_or_equivalent",
        "orchestration_opt_in",
        "trace_persistence",
    ]
    if require_reproducible:
        required.append("snapshot_persistence")
    missing = [name for name in required if capabilities.get(name) is not True]

    if not missing:
        decision = "proceed"
        executed_tier = "heavy"
    elif allow_downgrade:
        decision = "downgraded"
        executed_tier = "light"
    else:
        decision = "blocked"
        executed_tier = None

    return {
        "decision": decision,
        "requested_tier": requested_tier,
        "executed_tier": executed_tier,
        "require_reproducible": require_reproducible,
        "missing": missing,
    }


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and HASH_PATTERN.fullmatch(value) is not None


def expected_run_status(manifest: dict[str, Any]) -> str:
    statuses = [branch.get("final_status") for branch in manifest.get("branches", [])]
    successes = statuses.count("success")
    if manifest.get("degraded_reasons") and successes:
        return "degraded"
    if statuses and successes == len(statuses):
        return "complete"
    if successes:
        return "partial"
    if statuses and all(status == "cancelled" for status in statuses):
        return "cancelled"
    return "failed"


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_fields = [
        "schema_version",
        "output_schema_version",
        "run_id",
        "host",
        "mode",
        "tier",
        "trace_level",
        "skill_sha256",
        "input_sha256",
        "context_sha256",
        "model",
        "executor",
        "persistence",
        "started_at",
        "ended_at",
        "requested",
        "waves",
        "degraded_reasons",
        "roster",
        "branches",
        "final_status",
    ]
    for field in required_fields:
        if field not in manifest:
            errors.append(f"missing field: {field}")

    if errors:
        return errors

    if manifest["schema_version"] != "1.0":
        errors.append("schema_version must be 1.0")
    if manifest["host"] not in {"claude-code", "codex"}:
        errors.append("host must be claude-code or codex")
    if manifest["mode"] not in {"discussion", "review", "planning"}:
        errors.append("invalid mode")
    if manifest["tier"] != "heavy":
        errors.append("run manifest validator only accepts heavy tier")
    if manifest["trace_level"] not in {"audit", "reproducible"}:
        errors.append("trace_level must be audit or reproducible")
    if manifest["final_status"] not in RUN_STATUSES:
        errors.append("invalid final_status")

    for field in ("skill_sha256", "input_sha256", "context_sha256"):
        if not is_hash(manifest[field]):
            errors.append(f"{field} must be a lowercase SHA-256")

    if manifest["trace_level"] == "reproducible":
        for field in ("input_snapshot_ref", "context_snapshot_ref"):
            if not manifest.get(field):
                errors.append(f"missing field: {field}")

    model = manifest["model"]
    if not isinstance(model, dict) or not model.get("id"):
        errors.append("model.id is required")
    elif not isinstance(model.get("parameters"), dict):
        errors.append("model.parameters must be an object")

    executor = manifest["executor"]
    if not isinstance(executor, dict) or not executor.get("name") or not executor.get("version"):
        errors.append("executor.name and executor.version are required")

    persistence = manifest["persistence"]
    if not isinstance(persistence, dict) or not persistence.get("location"):
        errors.append("persistence.location is required")

    requested = manifest["requested"]
    roster = manifest["roster"]
    branches = manifest["branches"]
    if not isinstance(requested, int) or requested < 1:
        errors.append("requested must be a positive integer")
    if not isinstance(manifest["waves"], int) or manifest["waves"] < 1:
        errors.append("waves must be a positive integer")
    if not isinstance(manifest["degraded_reasons"], list):
        errors.append("degraded_reasons must be an array")
    if not isinstance(roster, list) or len(roster) != requested:
        errors.append("roster length must equal requested")
    if not isinstance(branches, list) or len(branches) != requested:
        errors.append("branches length must equal requested")
        return errors

    roster_fields = {
        "canonical_id",
        "native_id",
        "dispatch_key",
        "source",
        "card_sha256",
        "role_projection_sha256",
    }
    for index, member in enumerate(roster if isinstance(roster, list) else []):
        if not isinstance(member, dict) or not roster_fields.issubset(member):
            errors.append(f"roster[{index}] is incomplete")
            continue
        if member["source"] not in SOURCES:
            errors.append(f"roster[{index}].source is invalid")
        if not isinstance(member["dispatch_key"], str) or not member["dispatch_key"].strip():
            errors.append(f"roster[{index}].dispatch_key is required")
        if member["source"] != "generated" and not is_hash(member["card_sha256"]):
            errors.append(f"roster[{index}].card_sha256 is required")
        if not is_hash(member["role_projection_sha256"]):
            errors.append(f"roster[{index}].role_projection_sha256 is required")

    branch_ids: set[str] = set()
    for index, branch in enumerate(branches):
        prefix = f"branches[{index}]"
        if not isinstance(branch, dict):
            errors.append(f"{prefix} must be an object")
            continue

        branch_id = branch.get("branch_id")
        if not branch_id or branch_id in branch_ids:
            errors.append(f"{prefix}.branch_id must be non-empty and unique")
        else:
            branch_ids.add(branch_id)

        source = branch.get("source")
        if source not in SOURCES:
            errors.append(f"{prefix}.source is invalid")
        if not isinstance(branch.get("dispatch_key"), str) or not branch["dispatch_key"].strip():
            errors.append(f"{prefix}.dispatch_key is required")
        if source != "generated" and not is_hash(branch.get("card_sha256")):
            errors.append(f"{prefix}.card_sha256 is required for library cards")
        if not is_hash(branch.get("role_projection_sha256")):
            errors.append(f"{prefix}.role_projection_sha256 is required")

        attempts = branch.get("attempts")
        if not isinstance(attempts, list) or not 1 <= len(attempts) <= 2:
            errors.append(f"{prefix}.attempts must contain one or two attempts")
            continue
        for attempt_index, attempt in enumerate(attempts, start=1):
            attempt_prefix = f"{prefix}.attempts[{attempt_index - 1}]"
            if not isinstance(attempt, dict):
                errors.append(f"{attempt_prefix} must be an object")
                continue
            if attempt.get("attempt") != attempt_index:
                errors.append(f"{attempt_prefix}.attempt must be {attempt_index}")
            if attempt.get("status") not in BRANCH_STATUSES:
                errors.append(f"{attempt_prefix}.status is invalid")
            if not is_hash(attempt.get("prompt_sha256")):
                errors.append(f"{attempt_prefix}.prompt_sha256 is required")
            latency = attempt.get("latency_ms")
            if not isinstance(latency, int) or latency < 0:
                errors.append(f"{attempt_prefix}.latency_ms must be non-negative")

        if branch.get("final_status") != attempts[-1].get("status"):
            errors.append(f"{prefix}.final_status must match the last attempt")

    expected = expected_run_status(manifest)
    if manifest["final_status"] != expected:
        errors.append(
            f"final_status must be {expected} for the recorded branch outcomes"
        )
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    gate = subparsers.add_parser("gate")
    gate.add_argument("--capabilities", type=Path, required=True)
    gate.add_argument("--requested-tier", choices=("light", "heavy"), required=True)
    gate.add_argument("--require-reproducible", action="store_true")
    gate.add_argument("--allow-downgrade", action="store_true")

    validate = subparsers.add_parser("validate")
    validate.add_argument("--manifest", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "gate":
            payload = decide_gate(
                load_json(args.capabilities),
                args.requested_tier,
                args.require_reproducible,
                args.allow_downgrade,
            )
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2 if payload["decision"] == "blocked" else 0

        errors = validate_manifest(load_json(args.manifest))
        payload = {"valid": not errors, "errors": errors}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if not errors else 2
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)]}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
