#!/usr/bin/env python3
"""Focused tests for the selective-consumption audit parser."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


D = Path(__file__).parent


def load_module():
    spec = importlib.util.spec_from_file_location("selective_analyse", D / "analyse.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ANALYSIS = load_module()


def locator(locator_id, role):
    return {
        "id": locator_id,
        "role": role,
        "path": "src/runtime.py",
        "symbol": locator_id,
        "start_line": 1,
        "end_line": 2,
        "sha256": "0" * 64,
        "fact": f"synthetic {role}",
    }


def observation(kind, consumer, fingerprint, representation="typed_projection"):
    return {
        "kind": kind,
        "artifact_id": "artifact-1",
        "producer_node": "producer",
        "consumer_execution_id": consumer,
        "scientific_consumer": True,
        "native_record_id": "message-1",
        "input_representation": representation,
        "projection_id": fingerprint,
        "input_sha256": fingerprint,
        "delivered_fields": ["record"],
        "full_input_reconstructable": True,
        "source_locator": "trace.json:1",
    }


def raw_fixture():
    roles = [
        "artifact_creation",
        "routing_or_projection",
        "consumer_input",
        "raw_bypass",
        "trace_serialization",
    ]
    observations = [
        observation("delivery", "consumer-a", "a" * 64),
        observation("delivery", "consumer-a", "a" * 64),
        observation("delivery", "consumer-b", "b" * 64),
        observation("non_delivery", "consumer-c", None, representation="none"),
    ]
    return {
        "schema_version": "1.0",
        "protocol": "audits/selective_consumption/protocol.md",
        "protocol_commit": "f" * 40,
        "candidates": [
            {
                "id": "synthetic",
                "repository": "https://example.invalid/repo",
                "pinned_commit": "e" * 40,
                "semantic_proxy_used": False,
                "measurement_signals": ["native_delivery_record"],
                "source_locators": [
                    locator(f"loc-{index}", role) for index, role in enumerate(roles)
                ],
                "trace_instances": [
                    {
                        "trace_id": "trace-1",
                        "public_locator": "repo@commit:trace.json",
                        "machine_readable": True,
                        "observations": observations,
                    }
                ],
                "raw_bypass": {
                    "status": "PRESENT_MODELLED",
                    "details": "synthetic modelled bypass",
                },
                "outcome_oracle": {"possible": True},
                "integration": {"framework_modification_required": False},
                "c3_directed_verifier": {"native_certificate_present": False},
                "evidence_gaps": [],
            }
        ],
    }


def test_delivery_dedup_and_counts():
    result = ANALYSIS.analyse(raw_fixture())["candidate_results"][0]
    assert result["producer_artifact_count"] == 1
    assert result["consumer_edge_count"] == 2
    assert result["repeated_consumer_count"] == 2
    assert result["repeated_artifact_count"] == 1


def test_projection_and_non_delivery_observations():
    result = ANALYSIS.analyse(raw_fixture())["candidate_results"][0]
    assert result["typed_projection_observed"] is True
    assert result["selective_non_delivery_observed"] is True
    assert result["access_record_observed"] is False


def test_bypass_and_evidence_completeness():
    result = ANALYSIS.analyse(raw_fixture())["candidate_results"][0]
    assert result["raw_bypass_status"] == "PRESENT_MODELLED"
    assert result["all_required_source_roles_present"] is True
    assert result["outcome_oracle_possible"] is True
    assert result["framework_modification_required"] is False


def test_missing_trace_yields_null_counts():
    raw = raw_fixture()
    raw["candidates"][0]["trace_instances"] = []
    result = ANALYSIS.analyse(raw)["candidate_results"][0]
    assert result["trace_observed"] is False
    for key in (
        "producer_artifact_count",
        "consumer_edge_count",
        "repeated_consumer_count",
        "typed_projection_observed",
        "access_record_observed",
    ):
        assert result[key] is None


def test_semantic_proxy_rejected():
    raw = raw_fixture()
    raw["candidates"][0]["measurement_signals"].append("substring")
    try:
        ANALYSIS.analyse(raw)
    except ValueError as error:
        assert "prohibited proxy" in str(error)
    else:
        raise AssertionError("prohibited proxy was accepted")


def test_deterministic_tempfile_cli():
    raw = raw_fixture()
    with tempfile.TemporaryDirectory(prefix="selective-audit-test-") as tmp_dir:
        tmp = Path(tmp_dir)
        input_path = tmp / "raw.json"
        output_a = tmp / "a.json"
        output_b = tmp / "b.json"
        input_path.write_text(json.dumps(raw))
        for output in (output_a, output_b):
            subprocess.run(
                [
                    sys.executable,
                    str(D / "analyse.py"),
                    "--input",
                    str(input_path),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
            )
        assert output_a.read_bytes() == output_b.read_bytes()
        parsed = json.loads(output_a.read_text())
        assert parsed["q_levels"] is None
        assert parsed["interpretation"] is None


if __name__ == "__main__":
    tests = [value for key, value in sorted(globals().items()) if key.startswith("test_")]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"{len(tests)} tests passed")
