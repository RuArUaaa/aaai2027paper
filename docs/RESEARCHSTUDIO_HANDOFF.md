# RESEARCHSTUDIO_HANDOFF

CURRENT_PHASE: CP4 完成(全部阶段已闭合,等待负责人裁决重大决定事件 6)
LAST_COMPLETED: CP4 — PRIMARY_CANDIDATE=NONE;决策包落盘 docs/final_research_direction_decision.md
ACTIVE_WORKERS: 无(C3/C6 gate 子代理因账户配额失败,其任务已由主席亲自完成并复核)
CURRENT_CANDIDATES: PRIMARY=NONE / BACKUP=C6'(重述版) / REJECTED=C4
CURRENT_VERDICT: C3_NOVELTY=NARROW_GAP、C3_GATE=FAIL;C6_NOVELTY=CLEAR_GAP、C6_GATE=FAIL;C4_NOVELTY=HIGH_COLLISION、C4_GATE=REQUIRES_AUTHORIZATION
BLOCKERS: 重大决定事件 6(无候选满足最低条件)——等待负责人在选项 A(选择性消费审计,RECOMMENDED)/B(测量论文后归档)/C(不推荐)间裁决
LAST_COMMIT: (见下方 commit 节,提交后更新)
NEXT_ACTION: 负责人裁决;若选 A,执行公开 agent 框架 trace 的选择性消费审计(CPU-only,1–2 天)
DECISION_REQUIRED: 是(选项 A/B/C,推荐 A)
REPO_PATH: /Users/zijian_nong/research/aaai2027-new(远端 https://github.com/RuArUaaa/aaai2027paper)
BRANCH: main
HEAD: cab8363 → (本轮 4 个逻辑 commit,见下)
GIT_STATUS: 干净(仅 .agents/ .claude/ 未跟踪)
LAST_UPDATED: 2026-07-21T14:40Z

## 冻结资产清单(CP0 记录,不得修改/覆盖)

- Idea Landscape:`reports/idea_landscape_2026-07-21.md` @ cab8363 — tag `idea-landscape-v1-pre-fulltext-and-scoop-check`
- Negative dossier:`inputs/route_a_plus_negative_evidence_dossier.md`
- Seed brief:`inputs/researchstudio_idea_seed_brief.md`
- 旧 gate memo(历史结果,不追认为 PASS):`reports/c3_gate_24h_2026-07-21.md`、`reports/c6_gate_24h_2026-07-21.md`
- Paper-Search 报告:`allinone.md`、`allinone-kv-state-2021-2026.md`
- Route A+ frozen evidence:外部仓库,只读

## 本轮产物(CP1–CP4)

- CP1:`literature/fulltext/`(C3/C6/C4 三份全文核实报告 + 三个 manifest + source_manifest.json 27 篇 + verified_bibliography.bib)
- CP2:`scoop_checks/`(三份 scoop check + collision_matrix.json)、`docs/researchstudio_collision_decision_memo.md`
- CP3:`gates/C3`(protocol/reanalyse_or_simulate.py/results.json/verdict.md/test_gate.py,5 tests PASS)、`gates/C6`(protocol/analyse_workflow.py(主席修 bug)/analyse_doc_level.py/results.json/results_doc_level.json/verdict.md/test_gate.py,5 tests PASS)、`gates/C4`(protocol/results.json/verdict.md = REQUIRES_AUTHORIZATION)
- CP4:`docs/final_research_direction_decision.md`(PRIMARY=NONE + 重大决定包)

## 关键新证据(一句话版)

1. C3:outcome verifier 混淆问题(baseline 错误≈复用错误)→ 投机经济性判死(Δ −0.26~−0.76)。
2. C6:未引用 doc 仍致 5% 下游 flip → query-relative 失效判定在 E0 testbed 不安全;NEG-25 模式在第二 testbed 家族复现。
3. C4:arXiv:2606.17107(Models Take Notes at Prefill)SAME 轴 13/15,DIRECT 撞车。
4. 唯一先决未知量:自然 agent workflow 是否存在原生选择性消费。

## 纪律声明

- 模型调用 = 0,GPU = 0,大型实验 = 0(全程保持)
- 子代理不裁决 novelty/gate;主席已复核全部子代理输出并修复 C6 脚本 bug 一处
- 旧 landscape 排序/gate 结论 = PRELIMINARY,未被本轮追认
