# RESEARCHSTUDIO_HANDOFF

CURRENT_PHASE: C3 v2.1 非 verdict 分析更正完成;准备冻结 selective-consumption protocol/candidate universe
LAST_COMPLETED: gates/C3/v2_1/ 更正+focused tests;data/SOURCE_MANIFEST.json 可复现性边界收紧
ACTIVE_WORKERS: 无
CURRENT_CANDIDATES: C3(NARROW_GAP + NEED_NEW_VERIFIER)/ C6(NARROW_GAP|CONDITIONAL_CLEAR_GAP + FAIL_MEASUREMENT)/ C4(REJECTED)
CURRENT_VERDICT: PRIMARY_CANDIDATE=PENDING_GATE_REAUDIT;EXPERIMENT_AUTHORIZATION=NONE
BLOCKERS: 无;本 Prompt 已授权有边界的选择性消费现象/testbed 资格审计;模型/GPU/正式实验维持 BLOCK
LAST_COMMIT: ce08e71a5ed5d0f3f945214a589cfe4fc71f6c67(C3 v2.1 checkpoint 正在形成提交)
NEXT_ACTION: 预筛并冻结 2–3 个候选;单独提交 audits/selective_consumption/protocol.md + candidate_universe.json,不得含结果
DECISION_REQUIRED: 否(尚未触发重大决定事件)
REPO_PATH: /Users/zijian_nong/research/aaai2027-new(远端 https://github.com/RuArUaaa/aaai2027paper)
BRANCH: main
HEAD: ce08e71a5ed5d0f3f945214a589cfe4fc71f6c67
GIT_STATUS: C3 v2.1 checkpoint 待提交;任务前 .agents/ .claude/ .codex/ 未跟踪且禁止纳入提交
LAST_UPDATED: 2026-07-22T09:51:43+08:00

## TAKEOVER checkpoint (2026-07-22)

TAKEOVER_AGENT: Codex 主协调代理 / 独立科学审查者 / 最终交接负责人
TAKEOVER_HEAD: ce08e71a5ed5d0f3f945214a589cfe4fc71f6c67
TAKEOVER_BRANCH: main
TAKEOVER_STATUS: PASS — repo root、origin、branch、HEAD 全部与接管基线一致;任务前三个未跟踪目录保持原样
FILES_READ:
- docs/RESEARCHSTUDIO_HANDOFF.md
- docs/final_research_direction_decision_v2.md
- docs/process_provenance_addendum.md
- gates/C3/v2/protocol.md
- gates/C3/v2/results_v2.json
- gates/C3/v2/verdict_v2.md
- gates/C3/v2/reanalyse_v2.py
- gates/C3/v2/test_gate_v2.py
- gates/C6/verdict_v2.md
- scoop_checks/C6_novelty_revision.md
- data/SOURCE_MANIFEST.json
- inputs/route_a_plus_negative_evidence_dossier.md
- inputs/researchstudio_idea_seed_brief.md
- reports/idea_landscape_2026-07-21.md
- literature/fulltext/C3_fulltext_review.md
- literature/fulltext/C6_fulltext_review.md
- literature/fulltext/C4_fulltext_review.md
- scoop_checks/C3_scoop_check.md
- scoop_checks/C6_scoop_check.md
- scoop_checks/C4_scoop_check.md
CURRENT_SCIENTIFIC_STATE: C3=NARROW_GAP+NEED_NEW_VERIFIER(v1 经济性判死撤回;rho_blame 仅条件分析);C6=NARROW_GAP|CONDITIONAL_CLEAR_GAP+FAIL_MEASUREMENT(TEXT_USAGE_PROXY INVALID;自然选择性消费 UNRESOLVED);C4=HIGH_COLLISION+REJECTED;PRIMARY=PENDING_GATE_REAUDIT
AUTHORIZED_SCOPE: CPU-only;只读公开源码和已有公开 trace/event log;静态调用链与小型解析;选择性消费 phenomenon/testbed qualification
FORBIDDEN_SCOPE: 模型调用;推理服务;GPU;新 Agent 框架;修改候选框架;正式 mutation/cache/reuse 实验;最终文本 usage 代理;修改旧 Route A+ frozen evidence
NEXT_ACTION: 完成并提交 C3 v2.1 非 verdict 更正,随后单独冻结 selective-consumption protocol 与 candidate universe
LAST_UPDATED: 2026-07-22T09:45:23+08:00

## C3 v2.1 correction checkpoint (2026-07-22)

CURRENT_PHASE: C3 v2.1 非 verdict 更正完成
LAST_COMPLETED: recompute_still_wrong 语义修复;经济性归一化标签修正;reproducibility scope 收紧;tempfile-safe focused test
CURRENT_HEAD: ce08e71a5ed5d0f3f945214a589cfe4fc71f6c67(C3 v2.1 commit 的 parent)
FILES:
- gates/C3/v2_1/analysis_correction.md
- gates/C3/v2_1/reanalyse_v2_1.py
- gates/C3/v2_1/results_v2_1.json
- gates/C3/v2_1/test_gate_v2_1.py
- gates/C3/v2_1/verdict_addendum.md
- data/SOURCE_MANIFEST.json
CORRECTED_COUNTS: TaskA reuse=95/100;TaskA repair=95/100;TaskB reuse=58/164;TaskB repair=57/164
UNCHANGED_FIELDS: rho_outcome;rho_blame;rescue;all economic values/signs;GO_NAIVE=false;GO_CONDITIONAL=true
C3_GATE_EFFECT: UNCHANGED
C3_CURRENT_STATUS: NARROW_GAP + NEED_NEW_VERIFIER;directed runtime verifier absent
TESTS: C3 v2.1 6/6 PASS;C6 focused 5/5 PASS;non-corrected metric equality PASS;git diff --check PASS;frozen gates/C3/v2 diff empty
NEXT_ACTION: 冻结 selective-consumption audit protocol 与 2–3 candidate universe
LAST_UPDATED: 2026-07-22T09:51:43+08:00

## 评审裁决落实表(2026-07-21 REQUEST_CHANGES)

| 评审项 | 状态 | 落实 |
|---|---|---|
| tag researchstudio-v1-gate-review-required | DONE | 冻结于 252c9b2 |
| C3 公式 P0 | DONE | gates/C3/v2/(protocol→raw→verdict 三 commit)= NEED_NEW_VERIFIER |
| C3 v=0.5 不可满足判据 | DONE | v2 删除该档,改符号地图 |
| C6 "机制不安全" P0 | DONE | verdict_v2.md = FAIL_MEASUREMENT,撤回 unsafe;usage 信号合法来源重新定义 |
| C6 novelty 降级 | DONE | scoop_checks/C6_novelty_revision.md = NARROW_GAP/CONDITIONAL_CLEAR_GAP |
| FULLTEXT_GROUNDING 降级 | DONE | process_provenance_addendum §4 = PARTIAL |
| process provenance(P1) | DONE | docs/process_provenance_addendum.md;新 gate 强制 protocol/raw/verdict 分 commit |
| 可复现性(P1) | DONE | data/SOURCE_MANIFEST.json、scripts/export_gate_inputs.py、fixtures、merge_results.py、脚本参数化、tests 在 fixtures 上通过 |
| CP4 重跑 | DONE | decision_v2.md = PENDING_GATE_REAUDIT |

## 当前有效结论(以此为准,v1 冲突处以 v2 为准)

- C3:naive 投机微利窗 v≲8%(不是 v1 说的判死);定向 verifier 存在则窗至 v≤13.7%;**定向 verifier 是否存在 = 核心未决问题**(NEG-11 封死文本启发式)。
- C6:机制未判死也未证实;文本 usage 代理第三次失效(测量层成立,机制层不成立);合法 testbed 特征 = 原生选择性路由。
- C4:维持 HIGH_COLLISION 拒绝(C4-P6 DIRECT)。
- 唯一先决未知量:公开真实 agent workflow 中是否存在原生选择性消费。

## 冻结资产与纪律

- tag `idea-landscape-v1-pre-fulltext-and-scoop-check`(cab8363)、`researchstudio-v1-gate-review-required`(252c9b2)
- v1 gate 文件全部保留原样;v2 结论不覆盖 v1,仅取代其解释地位
- 模型调用=0,GPU=0,大型实验=0(全程保持)
