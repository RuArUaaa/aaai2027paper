# C3 v2.1 Analysis Correction

Date: 2026-07-22

This is a non-verdict correction layered on top of the frozen C3 v2 record.
The following files remain historical and are not modified:

- `gates/C3/v2/protocol.md`
- `gates/C3/v2/results_v2.json`
- `gates/C3/v2/verdict_v2.md`

## 1. Correct `recompute_still_wrong`

The v2 implementation counted every baseline error:

```python
not orig_correct
```

That incorrectly included rescue cases. Under the existing encoding,
`flip == 1` means that the arm result differs from the from-scratch result.
The complete truth table is:

| `orig_correct` | `flip` | arm outcome | category |
|---|---:|---|---|
| true | 0 | correct | accepted |
| true | 1 | wrong | `rho_blame` |
| false | 0 | wrong | `recompute_still_wrong` |
| false | 1 | correct | `rescue` |

The corrected event is therefore:

```python
(not orig_correct) and (not flip)
```

Equivalently, it is `orig_wrong AND arm_wrong`: the verifier rejects and the
subsequent from-scratch recomputation is still wrong. Two accounting identities
must now hold for every task and arm:

```text
rho_outcome = rho_blame + recompute_still_wrong
baseline_error_rate = rescue + recompute_still_wrong
```

Corrected full-data values:

| task | arm | old rate | corrected count / n | corrected rate |
|---|---|---:|---:|---:|
| A | reuse | 0.96 | 95 / 100 | 0.95 |
| A | repair | 0.96 | 95 / 100 | 0.95 |
| B | reuse | 0.3658536585 | 58 / 164 | 0.3536585366 |
| B | repair | 0.3658536585 | 57 / 164 | 0.3475609756 |

No other outcome statistic changes: `rho_outcome`, `rho_blame`, and `rescue`
retain their v2 values.

## 2. Correct the economic label, not the value

The formula normalizes all costs by a complete baseline execution:

```text
C_full = 1
Δ/C_full = s - v - rho(s + RB)
```

The v2 label `Δ/S` / `delta_over_S` was therefore wrong. v2.1 uses:

- display label: `Δ/C_full`;
- machine key: `delta_over_full`;
- semantic name: `net_saving_fraction_of_full_run`.

All numeric economic values, signs, and break-even rates are unchanged. In
particular, `v = 0.1` means that the verifier costs 10% of one complete baseline
execution; it does not mean 10% of the avoided subgraph cost.

## 3. Reproducibility boundary

The committed fixtures reproduce only analysis code paths, fixture-level
focused tests, and structural invariants. They do not reproduce the complete
aggregate gate statistics.

Full aggregate values require the original files listed in
`data/SOURCE_MANIFEST.json`, after verifying every recorded SHA-256. The C3
Task B fixture contains every flip case plus sampled non-flip cases, so it is
deliberately enriched and must not be interpreted as representative. The C6
fixture contains only two traces and is likewise restricted to path and
structural testing.

## 4. Workspace-safe tests

`test_gate_v2_1.py` writes analysis output only into a temporary directory,
hashes fixtures before and after execution, and never uses a local absolute
path. The historical tracked `gates/C3/fixtures/results_v2_fixture.json` is not
read or overwritten by the v2.1 test.

## 5. Scientific impact

This correction does not change:

- `rho_outcome`;
- `rho_blame`;
- `rescue`;
- any economic value or its sign;
- `GO_NAIVE = false`;
- `GO_CONDITIONAL = true`;
- `C3_GATE_V2_1 = NEED_NEW_VERIFIER`.

The conditional caveat remains load-bearing: `rho_blame` uses post-hoc baseline
labels, and no runtime-executable directed verifier currently exists.
