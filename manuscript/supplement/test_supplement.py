#!/usr/bin/env python3
"""Focused tests for deterministic packaging and archive anonymity."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "supplement_builder", HERE / "build_anonymous_supplement.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load supplement builder")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class SupplementTests(unittest.TestCase):
    def test_deterministic_anonymous_archive_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="anonymous-supplement-") as tmp:
            root = Path(tmp)
            zip_a = root / "a.zip"
            zip_b = root / "b.zip"
            manifest_a = root / "a.json"
            manifest_b = root / "b.json"
            report_a = BUILDER.build(zip_a, manifest_a)
            report_b = BUILDER.build(zip_b, manifest_b)

            self.assertEqual(zip_a.read_bytes(), zip_b.read_bytes())
            self.assertEqual(
                report_a["archive_sha256"], report_b["archive_sha256"]
            )
            self.assertEqual(report_a["anonymity_scan"]["status"], "PASS")
            self.assertFalse(
                report_a["scope"]["full_aggregate_inputs_distributed"]
            )

            with zipfile.ZipFile(zip_a) as archive:
                names = archive.namelist()
                self.assertEqual(names, sorted(names))
                self.assertIn(
                    f"{BUILDER.ZIP_PREFIX}/EXTERNAL_INPUTS.json", names
                )
                self.assertNotIn(".git", "\n".join(names))
                data = {name: archive.read(name) for name in names}

            manifest_name = f"{BUILDER.ZIP_PREFIX}/MANIFEST.sha256"
            listed = {}
            for line in data[manifest_name].decode().splitlines():
                digest, name = line.split("  ", 1)
                listed[name] = digest
            self.assertEqual(set(listed), set(data) - {manifest_name})
            for name, digest in listed.items():
                self.assertEqual(hashlib.sha256(data[name]).hexdigest(), digest)
                BUILDER.assert_anonymous(name, data[name])

            parsed = json.loads(manifest_a.read_text())
            self.assertEqual(parsed["member_count"], len(data))


if __name__ == "__main__":
    unittest.main()
