# Refine-Logs Manifest

| Output | Version | Purpose | Status |
|---|---|---|---|
| `EXPERIMENT_PLAN.md` | 2026-07-22-B | Claim-driven plan; D0 closed the proposed calibration | Current |
| `EXPERIMENT_TRACKER.md` | 2026-07-22-B | Gate-aware tracker with D1–D4 stopped | Current |
| `../experiments/actual_skip_calibration/d0_static_audit.md` | 2026-07-22-A | Source-backed D0 qualification verdict | Current |
| `../experiments/actual_skip_calibration/d0_source_manifest.json` | 2026-07-22-A | SHA-256 manifest for read-only historical evidence | Current |
| `../experiments/actual_skip_calibration/d0_results.json` | 2026-07-22-A | Machine-readable D0 verdict and call-budget reconstruction | Current |
| `../experiments/actual_skip_calibration/validate_d0.py` | 2026-07-22-A | Read-only source-hash and arithmetic validator | Current |
| `../experiments/actual_skip_calibration/test_d0.py` | 2026-07-22-A | Tempfile-safe focused regression tests | Current |

The shared output-versioning and output-manifest references named by the local
`experiment-plan` skill were not present at their declared filesystem path.
This manifest therefore follows the repository's existing dated-artifact and
explicit-status convention. No model experiment was run to create these files.
