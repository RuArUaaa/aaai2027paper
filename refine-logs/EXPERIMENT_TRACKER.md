# Experiment Tracker

```text
CURRENT_GATE = D0_COMPLETE_INELIGIBLE_AS_PROPOSED
EXPERIMENT_AUTHORIZATION = NONE
MODEL_CALLS = 0
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
LAST_UPDATED = 2026-07-22T12:44:00+08:00
```

| Run ID | Milestone | Purpose | System / variant | Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | Recheck frozen C3/C6/audit claim boundaries | Existing repository artifacts | Frozen | Claim-to-evidence coverage | MUST | DONE | No frozen result changed |
| R002 | M1 | Locate HumanEvalFix invocation assembly and serialized inputs | Historical source, read-only | N/A | Source locators | MUST | DONE | Native path has four LLM nodes and full source/test prompts |
| R003 | M1 | Locate external environment state, execution bits, and outcome oracle | Historical source/artifacts, read-only | N/A | Identity and schema coverage | MUST | DONE | Outcome oracle exists; proposed native tool-result path does not |
| R004 | M1 | Reconstruct calls per full and replay arm | Static call graph | N/A | Call-count bounds | MUST | DONE | 1,968 cells; optimistic two-stage bound 3,280 calls; native no-hit 7,872 |
| R005 | M1 | Issue D0 qualification verdict | Static evidence package | N/A | INELIGIBLE_AS_PROPOSED | MUST | DONE | New two-stage harness would be required |
| R006 | M2 | Freeze task IDs, state variable, hashes, arms, and exclusions | Conditional design | Execution split | Manifest completeness | MUST | STOPPED | D0 failed; not waiting for authorization |
| R007 | M3 | Identity/instrumentation smoke | Conditional replay harness | Small paired set | Actual skips, event invariants, outcome agreement | MUST | STOPPED | No eligible design and no model authorization |
| R008 | M4 | Discovery/pilot | Conditional replay arms | Preregistered execution split | Cost, agreement, false accepts | MUST | STOPPED | No eligible design and no model authorization |
| R009 | M4 | Confirmation | Frozen conditional design | Disjoint execution split | Same endpoints | MUST | STOPPED | No eligible design and no model authorization |
| R010 | M5 | Final manuscript claim audit | Paper draft | N/A | Unsupported core claims | MUST | TODO | Downgrade wording rather than invent evidence |

`STOPPED` means the route failed its prior gate; it is not merely waiting for
compute or unused authorization.
