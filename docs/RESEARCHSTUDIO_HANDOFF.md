# RESEARCHSTUDIO_HANDOFF

CURRENT_PHASE: CP4 v2 完成(评审 REQUEST_CHANGES 已逐项落实,等待负责人对"修订后的选择性消费审计"授权)
LAST_COMPLETED: CP4 v2 — PRIMARY=PENDING_GATE_REAUDIT;docs/final_research_direction_decision_v2.md
ACTIVE_WORKERS: 无
CURRENT_CANDIDATES: C3(NARROW_GAP + NEED_NEW_VERIFIER)/ C6(NARROW_GAP|CONDITIONAL_CLEAR_GAP + FAIL_MEASUREMENT)/ C4(REJECTED)
CURRENT_VERDICT: PRIMARY_CANDIDATE=PENDING_GATE_REAUDIT;EXPERIMENT_AUTHORIZATION=NONE
BLOCKERS: 等待负责人授权"修订后的选择性消费审计"(CPU-only);模型/GPU/正式实验维持 BLOCK
LAST_COMMIT: 见 git log(评审整改批次)
NEXT_ACTION: 负责人授权后,按 protocol→raw→verdict 三 commit 流程执行选择性消费审计
DECISION_REQUIRED: 是(授权审计 or 转测量论文归档)
REPO_PATH: /Users/zijian_nong/research/aaai2027-new(远端 https://github.com/RuArUaaa/aaai2027paper)
BRANCH: main
HEAD: 评审整改批次最新 commit
GIT_STATUS: 干净(仅 .agents/ .claude/ 未跟踪)
LAST_UPDATED: 2026-07-21T15:20Z

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
