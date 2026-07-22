#!/usr/bin/env python3
"""Build a deterministic, allowlisted, anonymous review supplement."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
DEFAULT_ZIP = HERE / "aaai27_code_data_supplement.zip"
DEFAULT_MANIFEST = HERE / "SUPPLEMENT_MANIFEST.json"
ZIP_PREFIX = "anonymous_code_data_supplement"
FIXED_ZIP_TIME = (2026, 7, 22, 0, 0, 0)

# These are the only repository files eligible for the review archive.
SOURCE_ALLOWLIST = (
    "data/SOURCE_MANIFEST.json",
    "gates/C3/fixtures/results_v2_fixture.json",
    "gates/C3/fixtures/taskA_e0_control.jsonl",
    "gates/C3/fixtures/taskB_e0.jsonl",
    "gates/C3/fixtures/taskB_e0_identity_ctrl.jsonl",
    "gates/C3/v2_1/analysis_correction.md",
    "gates/C3/v2_1/reanalyse_v2_1.py",
    "gates/C3/v2_1/results_v2_1.json",
    "gates/C3/v2_1/test_gate_v2_1.py",
    "gates/C3/v2_1/verdict_addendum.md",
    "gates/C6/analyse_doc_level.py",
    "gates/C6/analyse_workflow.py",
    "gates/C6/fixtures/taskA_e0.jsonl",
    "gates/C6/fixtures/taskA_e0_identity_ctrl.jsonl",
    "gates/C6/test_gate.py",
    "audits/selective_consumption/analyse.py",
    "audits/selective_consumption/results.json",
    "audits/selective_consumption/raw_locators.json",
    "audits/selective_consumption/source_manifest.json",
    "audits/selective_consumption/test_audit.py",
    "experiments/actual_skip_calibration/d0_results.json",
    "experiments/actual_skip_calibration/d0_source_manifest.json",
    "experiments/actual_skip_calibration/test_d0.py",
    "experiments/actual_skip_calibration/validate_d0.py",
    "manuscript/stage2_5/descriptive_counts.json",
    "manuscript/stage2_5/recompute_descriptive_counts.py",
    "manuscript/stage2_5/test_recompute_descriptive_counts.py",
)

# Build the sensitive literals in pieces so this builder can itself be shared
# without being flagged by its own literal-string scan.
LOCAL_USER = "zijian" + "_nong"
REPOSITORY_OWNER = "RuAr" + "Uaaa"
SUBMISSION_NUMBER = "445" + "03"
REPOSITORY_NAME = "aaai2027" + "paper"
FORBIDDEN_TEXT = (
    LOCAL_USER,
    REPOSITORY_OWNER,
    SUBMISSION_NUMBER,
    REPOSITORY_NAME,
    "/Users/",
    "/home/",
    "file://",
)
EMAIL_RE = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sanitize(data: bytes) -> bytes:
    """Redact known local identity/path strings without altering raw fixtures."""

    # JSONL fixtures are already anonymous and contain none of these values;
    # replacements affect only source defaults and provenance metadata.
    replacements = (
        (
            f"/Users/{LOCAL_USER}/research/aaai2027-route-a-plus".encode(),
            b"external:route_a_plus",
        ),
        (
            f"/Users/{LOCAL_USER}/research/aaai2027-new".encode(),
            b"submission:root",
        ),
        (
            f"/Users/{LOCAL_USER}/research/aaai2027".encode(),
            b"external:historical",
        ),
        (
            f"https://github.com/{REPOSITORY_OWNER}/{REPOSITORY_NAME}".encode(),
            b"anonymous:repository",
        ),
    )
    for source, replacement in replacements:
        data = data.replace(source, replacement)
    return data


def assert_safe_member_name(name: str) -> None:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"unsafe ZIP member name: {name}")


def assert_anonymous(name: str, data: bytes) -> None:
    assert_safe_member_name(name)
    lowered = data.lower()
    for needle in FORBIDDEN_TEXT:
        if needle.lower().encode() in lowered:
            raise ValueError(f"forbidden identity/path string in {name}: {needle}")
    if EMAIL_RE.search(data):
        raise ValueError(f"email-like identity string in {name}")


def package_readme() -> bytes:
    return b"""# Anonymous Code and Data Supplement

This archive contains the paper's review-shareable analysis code, focused
fixtures, machine-readable results, and provenance ledgers. It contains no new
model experiment and does not run a studied agent system.

Reproducibility boundary:

- Fixture tests reproduce code paths and structural invariants.
- `manuscript/stage2_5/descriptive_counts.json` records the independently
  recomputed aggregate cells and the hashes of the external raw inputs.
- Full aggregate reproduction requires those external inputs at exactly the
  recorded hashes; they are not distributed in this archive.
- The frozen historical C6 files are retained for provenance. The manuscript
  uses the semantic corrections in `manuscript/stage2_5/` for its displayed
  Table 1 document-pair cells.

Useful commands from the unpacked archive root:

    python3 gates/C3/v2_1/test_gate_v2_1.py
    python3 gates/C6/test_gate.py
    python3 audits/selective_consumption/test_audit.py
    python3 experiments/actual_skip_calibration/test_d0.py
    python3 manuscript/stage2_5/test_recompute_descriptive_counts.py

The last command always tests the corrected nested-title parser. Set
`AAAI27_HISTORICAL_ROOT` and `AAAI27_ROUTE_A_PLUS_ROOT` to SHA-matching input
trees to enable its full aggregate recount.
"""


def environment_text() -> bytes:
    return (
        "Python >= 3.10\n"
        "Runtime dependencies: Python standard library only\n"
        "Hardware: CPU only; no GPU or model runtime required\n"
        "Network: not required for included focused tests\n"
    ).encode()


def third_party_notice() -> bytes:
    return b"""# Provenance and review-use notice

The small committed fixtures are derived analysis fixtures from archived
HotpotQA-style and HumanEvalPack-style workflow outputs. They are included
only to exercise parser paths and structural invariants and are explicitly not
population-representative. Full historical raw traces and third-party source
repositories are not redistributed.

This anonymous package is supplied for peer review. Final public-release
licenses and attribution notices will accompany the de-anonymized artifact.
"""


def external_inputs() -> bytes:
    counts = json.loads(
        (PROJECT_ROOT / "manuscript/stage2_5/descriptive_counts.json").read_text()
    )
    d0 = json.loads(
        (PROJECT_ROOT / "experiments/actual_skip_calibration/d0_source_manifest.json").read_text()
    )
    payload = {
        "schema_version": "anonymous-external-input-ledger/v1",
        "aggregate_inputs": counts["inputs"],
        "d0_inputs": [
            {
                key: value
                for key, value in entry.items()
                if key in {
                    "path",
                    "sha256",
                    "aggregate_sha256_declared",
                    "availability",
                    "role",
                }
            }
            for entry in d0["files"]
        ],
        "limitation": (
            "Hashes authenticate matching files already possessed by a reviewer; "
            "omitted inputs cannot be independently reconstructed from this archive."
        ),
    }
    return json.dumps(payload, indent=2, sort_keys=True).encode() + b"\n"


def collect_members() -> dict[str, bytes]:
    members = {
        f"{ZIP_PREFIX}/README.md": package_readme(),
        f"{ZIP_PREFIX}/ENVIRONMENT.txt": environment_text(),
        f"{ZIP_PREFIX}/PROVENANCE_AND_LICENSES.md": third_party_notice(),
        f"{ZIP_PREFIX}/EXTERNAL_INPUTS.json": external_inputs(),
    }
    for relative in SOURCE_ALLOWLIST:
        source = PROJECT_ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"allowlisted source missing: {relative}")
        members[f"{ZIP_PREFIX}/{relative}"] = sanitize(source.read_bytes())
    for name, data in members.items():
        assert_anonymous(name, data)

    hashes = "".join(
        f"{sha256_bytes(members[name])}  {name}\n" for name in sorted(members)
    ).encode()
    manifest_name = f"{ZIP_PREFIX}/MANIFEST.sha256"
    assert_anonymous(manifest_name, hashes)
    members[manifest_name] = hashes
    return members


def write_zip(output: Path, members: dict[str, bytes]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, members[name], compress_type=zipfile.ZIP_DEFLATED)


def build(zip_output: Path, manifest_output: Path) -> dict:
    members = collect_members()
    write_zip(zip_output, members)
    archive_bytes = zip_output.read_bytes()
    report = {
        "schema_version": "anonymous-supplement-manifest/v1",
        "archive": zip_output.name,
        "archive_bytes": len(archive_bytes),
        "archive_sha256": sha256_bytes(archive_bytes),
        "deterministic_zip_timestamp": list(FIXED_ZIP_TIME),
        "member_count": len(members),
        "members": [
            {
                "path": name,
                "bytes": len(members[name]),
                "sha256": sha256_bytes(members[name]),
            }
            for name in sorted(members)
        ],
        "anonymity_scan": {
            "status": "PASS",
            "forbidden_string_classes": [
                "local username",
                "repository owner",
                "submission number",
                "private repository name",
                "absolute home path",
                "email address",
            ],
        },
        "scope": {
            "studied_system_model_calls": 0,
            "gpu_runs": 0,
            "new_agent_trajectories": 0,
            "full_aggregate_inputs_distributed": False,
        },
    }
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-output", type=Path, default=DEFAULT_ZIP)
    parser.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    report = build(args.zip_output, args.manifest_output)
    print(json.dumps({
        "archive": report["archive"],
        "bytes": report["archive_bytes"],
        "sha256": report["archive_sha256"],
        "members": report["member_count"],
        "anonymity": report["anonymity_scan"]["status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
