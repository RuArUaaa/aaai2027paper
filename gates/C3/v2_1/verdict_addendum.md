# C3 Gate v2.1 Verdict Addendum

Date: 2026-07-22

## Verdict

```text
C3_GATE_V2_1 = NEED_NEW_VERIFIER
C3_GATE_EFFECT = UNCHANGED
```

This addendum interprets `results_v2_1.json` and does not modify the frozen v2
protocol, raw results, or verdict.

The only numerical correction is `recompute_still_wrong`: Task A is 95/100 for
both arms; Task B is 58/164 for reuse and 57/164 for repair. Rescues are no
longer double-counted in that terminal baseline-error category.

The economic cells retain every v2 value and sign. Their correct name is now
`Δ/C_full` (`delta_over_full`, a net-saving fraction of the complete baseline
run), rather than `Δ/S`. Thus `v = 0.1` is a verifier cost equal to 10% of a
complete execution.

The original gate logic is unchanged:

- naive outcome verification is positive at `v = 0.01` but negative at
  `v = 0.1`, so `GO_NAIVE` remains false;
- the post-hoc `rho_blame` calculation is positive at both values, so
  `GO_CONDITIONAL` remains true;
- because no runtime-directed verifier implements the `rho_blame` distinction,
  the verdict remains `NEED_NEW_VERIFIER`, not `GO`.

This addendum does not authorize a C3 experiment.
