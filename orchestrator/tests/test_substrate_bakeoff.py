from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import jsonschema


REPOSITORY = Path(__file__).resolve().parents[2]
SCRIPT = REPOSITORY / "orchestrator/tools/run_substrate_bakeoff.py"
SCHEMA = REPOSITORY / "orchestrator/tools/substrate-bakeoff.schema.json"


def load_runner():
    spec = importlib.util.spec_from_file_location("substrate_bakeoff", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_custom_and_temporal_results_share_the_versioned_schema(tmp_path) -> None:
    runner = load_runner()
    custom = runner.custom_case(SCRIPT)
    temporal = runner.temporal_case()
    report = {
        "schema_version": "1.0.0",
        "source": {
            "manifest_path": "evaluation/manifests/phase1a-source.json",
            "manifest_sha256": "a" * 64,
            "source_tree_digest": "b" * 64,
            "base_commit": "c" * 40,
        },
        "scenario_version": runner.SCENARIO_VERSION,
        "generated_at": "2026-07-14T00:00:00+00:00",
        "results": [custom, custom, temporal],
    }
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(report)
    assert custom["effects"] == runner.EFFECTS
    assert custom["duplicates"] == 0
    assert custom["raw"]["crash_returncode"] == 77
    assert custom["raw"]["pause_run_returncode"] == 73
    assert temporal["status"] == "not_runnable"
    assert temporal["semantic_digest"] is None


def test_semantic_digest_excludes_timing_and_substrate_identity() -> None:
    runner = load_runner()
    evidence = runner.normalized(runner.EFFECTS, "LOCAL_CANDIDATE_READY")
    assert runner.canonical_digest(evidence) == runner.canonical_digest(dict(evidence))
    assert "timings_ms" not in evidence
    assert "substrate" not in evidence
