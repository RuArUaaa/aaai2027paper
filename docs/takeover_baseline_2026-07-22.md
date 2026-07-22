# Takeover Baseline — 2026-07-22

These commands were run before research work began, from the expected local
repository path. The output is recorded verbatim so that takeover assumptions
remain auditable without relying on session state.

```text
$ git rev-parse --show-toplevel
/Users/zijian_nong/research/aaai2027-new

$ git branch --show-current
main

$ git rev-parse HEAD
ce08e71a5ed5d0f3f945214a589cfe4fc71f6c67

$ git status --short
?? .agents/
?? .claude/
?? .codex/

$ git log --oneline -12
ce08e71 idea: re-run CP4 after gate re-audit (PRIMARY=PENDING_GATE_REAUDIT)
e69028b repro: source manifest, fixtures, deterministic merge, parameterized gate scripts; tests run on fixtures
b23f528 gates/C6: correct verdict to FAIL_MEASUREMENT; downgrade novelty; withdraw unsafe claim
4014fce gates/C3: v2 verdict = NEED_NEW_VERIFIER (commit 3 of 3)
2f54cfa gates/C3: v2 raw results + analysis + tests (commit 2 of 3)
20f6fa8 gates/C3: freeze v2 protocol (commit 1 of 3; no results yet)
adbb744 process: honest provenance addendum; mandate protocol/raw/verdict commit order
252c9b2 idea: select final direction (PRIMARY=NONE) and decision package
ab1ef00 gates: replace preliminary candidate qualification probes
2c765d5 research: complete candidate scoop checks
f27be43 research: add full-text grounding and source manifest
421c976 research: freeze baseline CP0 and open handoff
```

## Takeover check

- Repository: PASS — local root and remote project identity are consistent with
  `aaai2027paper`.
- Branch: PASS — `main`.
- HEAD: PASS — exact expected commit.
- Pre-existing worktree state: three untracked task-configuration directories,
  `.agents/`, `.claude/`, and `.codex/`.
- Preservation rule: the three pre-existing directories will not be deleted,
  moved, cleaned, stashed, or added to any commit.
- History rule: no reset, rebase, stash, clean, or history rewrite is authorized.
- Historical repositories and frozen Route A+ evidence remain read-only.
