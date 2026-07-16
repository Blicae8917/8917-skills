import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "8917-expert-panel"
    / "scripts"
    / "run_contract.py"
)
HASH = "a" * 64


def success_branch(branch_id: str = "branch-1") -> dict:
    return {
        "branch_id": branch_id,
        "expert": "Reality Checker",
        "source": "persona-injected",
        "native_id": "reality-checker",
        "dispatch_key": "general-purpose",
        "card_sha256": HASH,
        "role_projection_sha256": HASH,
        "attempts": [
            {
                "attempt": 1,
                "prompt_sha256": HASH,
                "status": "success",
                "latency_ms": 1200,
                "error": None,
                "output": {"verdict": "needs-work"},
            }
        ],
        "final_status": "success",
    }


def valid_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "output_schema_version": "review-1.0",
        "run_id": "run-1",
        "host": "codex",
        "mode": "review",
        "tier": "heavy",
        "trace_level": "reproducible",
        "skill_sha256": HASH,
        "input_sha256": HASH,
        "context_sha256": HASH,
        "input_snapshot_ref": "secure://runs/run-1/input",
        "context_snapshot_ref": "secure://runs/run-1/context",
        "model": {"id": "test-model", "parameters": {"reasoning": "high"}},
        "executor": {"name": "test-executor", "version": "1.0"},
        "persistence": {"location": "secure://runs/run-1/manifest"},
        "started_at": "2026-07-15T12:00:00Z",
        "ended_at": "2026-07-15T12:00:02Z",
        "requested": 1,
        "waves": 1,
        "degraded_reasons": [],
        "roster": [
            {
                "canonical_id": "reality-checker",
                "native_id": "reality-checker",
                "dispatch_key": "general-purpose",
                "source": "persona-injected",
                "card_sha256": HASH,
                "role_projection_sha256": HASH,
            }
        ],
        "branches": [success_branch()],
        "final_status": "complete",
    }


class RunContractCliTests(unittest.TestCase):
    def run_with_json(self, command: str, flag: str, payload: dict, *args: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "payload.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), command, flag, str(path), *args],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

    def test_blocks_reproducible_heavy_run_when_trace_capabilities_are_missing(self):
        capabilities = {
            "isolated_context": True,
            "timeout_cancel": True,
            "workflow_or_equivalent": True,
            "orchestration_opt_in": True,
            "trace_persistence": False,
            "snapshot_persistence": False,
        }

        result = self.run_with_json(
            "gate",
            "--capabilities",
            capabilities,
            "--requested-tier",
            "heavy",
            "--require-reproducible",
        )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "blocked")
        self.assertEqual(
            payload["missing"], ["trace_persistence", "snapshot_persistence"]
        )

    def test_blocks_audit_heavy_run_without_trace_persistence(self):
        capabilities = {
            "isolated_context": True,
            "timeout_cancel": True,
            "workflow_or_equivalent": True,
            "orchestration_opt_in": True,
            "trace_persistence": False,
            "snapshot_persistence": False,
        }

        result = self.run_with_json(
            "gate",
            "--capabilities",
            capabilities,
            "--requested-tier",
            "heavy",
        )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "blocked")
        self.assertEqual(payload["missing"], ["trace_persistence"])

    def test_allows_audit_heavy_run_without_snapshot_persistence(self):
        capabilities = {
            "isolated_context": True,
            "timeout_cancel": True,
            "workflow_or_equivalent": True,
            "orchestration_opt_in": True,
            "trace_persistence": True,
            "snapshot_persistence": False,
        }

        result = self.run_with_json(
            "gate",
            "--capabilities",
            capabilities,
            "--requested-tier",
            "heavy",
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "proceed")
        self.assertEqual(payload["executed_tier"], "heavy")

    def test_allows_explicit_downgrade_but_never_labels_it_heavy(self):
        capabilities = {
            "isolated_context": True,
            "timeout_cancel": True,
            "workflow_or_equivalent": False,
            "orchestration_opt_in": True,
            "trace_persistence": False,
            "snapshot_persistence": False,
        }

        result = self.run_with_json(
            "gate",
            "--capabilities",
            capabilities,
            "--requested-tier",
            "heavy",
            "--require-reproducible",
            "--allow-downgrade",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "downgraded")
        self.assertEqual(payload["executed_tier"], "light")

    def test_blocks_heavy_run_without_orchestration_opt_in(self):
        capabilities = {
            "isolated_context": True,
            "timeout_cancel": True,
            "workflow_or_equivalent": True,
            "orchestration_opt_in": False,
            "trace_persistence": True,
            "snapshot_persistence": True,
        }

        result = self.run_with_json(
            "gate",
            "--capabilities",
            capabilities,
            "--requested-tier",
            "heavy",
        )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "blocked")
        self.assertEqual(payload["missing"], ["orchestration_opt_in"])

    def test_validates_complete_reproducible_manifest(self):
        result = self.run_with_json(
            "validate", "--manifest", valid_manifest()
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(json.loads(result.stdout)["valid"])

    def test_rejects_reproducible_manifest_without_snapshot_references(self):
        manifest = valid_manifest()
        del manifest["context_snapshot_ref"]

        result = self.run_with_json("validate", "--manifest", manifest)

        self.assertEqual(result.returncode, 2)
        errors = json.loads(result.stdout)["errors"]
        self.assertIn("missing field: context_snapshot_ref", errors)

    def test_rejects_invalid_roster_provenance_hash(self):
        manifest = valid_manifest()
        manifest["roster"][0]["role_projection_sha256"] = "not-a-hash"

        result = self.run_with_json("validate", "--manifest", manifest)

        self.assertEqual(result.returncode, 2)
        errors = json.loads(result.stdout)["errors"]
        self.assertIn("roster[0].role_projection_sha256 is required", errors)

    def test_rejects_missing_dispatch_key(self):
        manifest = valid_manifest()
        del manifest["roster"][0]["dispatch_key"]
        del manifest["branches"][0]["dispatch_key"]

        result = self.run_with_json("validate", "--manifest", manifest)

        self.assertEqual(result.returncode, 2)
        errors = json.loads(result.stdout)["errors"]
        self.assertIn("roster[0] is incomplete", errors)
        self.assertIn("branches[0].dispatch_key is required", errors)

    def test_preserves_partial_attempt_before_successful_retry(self):
        manifest = valid_manifest()
        branch = manifest["branches"][0]
        first_attempt = deepcopy(branch["attempts"][0])
        first_attempt.update(
            {
                "status": "partial",
                "error": "schema validation failed",
                "output": {"verdict": "needs-work"},
            }
        )
        second_attempt = deepcopy(branch["attempts"][0])
        second_attempt["attempt"] = 2
        branch["attempts"] = [first_attempt, second_attempt]

        result = self.run_with_json("validate", "--manifest", manifest)

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_derives_partial_run_from_success_and_timeout(self):
        manifest = valid_manifest()
        timeout_branch = success_branch("branch-2")
        timeout_branch["expert"] = "Workflow Architect"
        timeout_branch["native_id"] = "workflow-architect"
        timeout_branch["attempts"][0].update(
            {"status": "timed_out", "error": "30s timeout", "output": None}
        )
        timeout_branch["final_status"] = "timed_out"
        manifest["requested"] = 2
        manifest["roster"].append(
            {
                "canonical_id": "workflow-architect",
                "native_id": "workflow-architect",
                "dispatch_key": "general-purpose",
                "source": "persona-injected",
                "card_sha256": HASH,
                "role_projection_sha256": HASH,
            }
        )
        manifest["branches"].append(timeout_branch)
        manifest["final_status"] = "partial"

        result = self.run_with_json("validate", "--manifest", manifest)

        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
