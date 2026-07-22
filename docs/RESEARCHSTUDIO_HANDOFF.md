# RESEARCHSTUDIO_HANDOFF

CURRENT_PHASE: Academic Pipeline Stage 3 SUBMISSION_PREPARATION;Stage 2.5 PASS_WITH_NOTES 已获负责人接受;远端备份完成;等待隔夜冷读
LAST_COMPLETED: GitHub main fast-forward push并核验 local HEAD=origin/main=remote main=e3867d7;Stage 3 scope/date/artifact gate 与提交记录模板落盘
ACTIVE_WORKERS: 主协调代理;当前无执行子代理;冷读不得早于 2026-07-24
CURRENT_CANDIDATES: PRIMARY=MEASURE_BEFORE_YOU_REUSE_MEASUREMENT_PAPER;ACTUAL_SKIP_HUMANEVALFIX=INELIGIBLE_AS_PROPOSED;AutoGen handoff=Q1/CODE_ONLY;LangGraph two-consumer fixture=Q0/CODE_ONLY;RetryAgent Preselector=Q1/CODE_ONLY
CURRENT_VERDICT: STAGE2_5=ACCEPTED_PASS_WITH_NOTES;STAGE3_SCOPE=SUBMISSION_PREPARATION_ONLY;C6_STRONG_TESTBED=NOT_FOUND;C3_DIRECTED_VERIFIER_CANDIDATE=NOT_FOUND;PRIMARY_PAPER_ROUTE=PURE_MEASUREMENT_AND_METHODOLOGY;EXPERIMENT_AUTHORIZATION=NONE
BLOCKERS: 无科学或仓库 blocker;全文上传按负责人要求主动延迟至冷读后;匿名 supplement 仍不分发全部 aggregate raw inputs;模型/GPU/正式实验继续 BLOCK
LAST_COMMIT: e3867d7b929bbbd7491da2ba27031d7589a3a571 paper: complete Stage 2.5 integrity review
NEXT_ACTION: 2026-07-24至07-25对 manuscript/build/main.pdf 做隔夜冷读;只记录和处理表述/排版问题;最迟2026-07-27 18:00+08:00完成三件套上传
DECISION_REQUIRED: 否;仅当冷读发现需改变数字/主张/方法/引用解释的问题时升级负责人裁决
REPO_PATH: /Users/zijian_nong/research/aaai2027-new(远端 https://github.com/RuArUaaa/aaai2027paper)
BRANCH: main
HEAD: e3867d7b929bbbd7491da2ba27031d7589a3a571(Stage 3 planning commit 的 parent;已与远端同步)
GIT_STATUS: Stage 3 planning/handoff 文档待提交;任务前 .agents/ .claude/ .codex/ 保持未跟踪且不纳入提交
LAST_UPDATED: 2026-07-23T00:29:40+08:00

## Stage 3 owner authorization and remote-backup checkpoint (2026-07-23)

CURRENT_PHASE: Stage 3 SUBMISSION_PREPARATION / ACTIVE
OWNER_DECISION: ACCEPT_STAGE2_5_PASS_WITH_NOTES_AND_AUTHORIZE_STAGE3
AUTHORIZED_SCOPE: push;overnight cold-read polish limited to wording/layout;main PDF+checklist PDF+Code/Data Supplement ZIP upload;submission record archival
FORBIDDEN_SCOPE: all experiments;studied-system model/API calls;GPU;new trajectories;ToolSandbox D0-bis;new testbed search;new citations;changes to numbers,claims,methods,or frozen gate verdicts
PUSH_STATUS: COMPLETE
PUSH_TRANSPORT: GitHub SSH over port 443 after local HTTPS connection timeout;fast-forward only;history unchanged
PUSHED_RANGE: 92d7e91f55f8e2a8dfe786951f98d7fa7639ae5a..e3867d7b929bbbd7491da2ba27031d7589a3a571
REMOTE_VERIFICATION: local HEAD=origin/main=GitHub refs/heads/main=e3867d7b929bbbd7491da2ba27031d7589a3a571
PREEXISTING_UNTRACKED: .agents/;.claude/;.codex/ preserved and excluded
OFFICIAL_FULL_DEADLINE: 2026-07-28T23:59:00-12:00(2026-07-29T19:59:00+08:00)
OFFICIAL_SUPPLEMENT_DEADLINE: 2026-07-31T23:59:00-12:00(2026-08-01T19:59:00+08:00)
INTERNAL_UPLOAD_TARGET: 2026-07-27T18:00:00+08:00;all three artifacts;at least 48h full-paper buffer
COLD_READ_WINDOW: 2026-07-24 through 2026-07-25;PDF-first;read-only findings before edits
BASELINE_MAIN_PDF: manuscript/build/main.pdf;320391 bytes;sha256=c80e67e694e448a1b4aa3a2a2002c969059cf3dd2df72bdbfa69eb9fe235bb68
BASELINE_CHECKLIST_PDF: manuscript/build/reproducibility_checklist.pdf;95691 bytes;sha256=d3a68508bc0e0eaabcb654c32944ed3e744f840d2f259dee22014fc5d782cba5
BASELINE_SUPPLEMENT_ZIP: manuscript/supplement/aaai27_code_data_supplement.zip;76847 bytes;sha256=d73c6fa6949e70c3f5a97c19f163247bf2190ed990b422a563f78fdbd5e3629d
OPENREVIEW_SUBMISSION_NUMBER: 44503
UPLOAD_STATUS: NOT_STARTED_BY_DESIGN;do not upload on 2026-07-23
STAGE3_PLAN: docs/STAGE3_SUBMISSION_PLAN.md
SUBMISSION_RECORD: docs/AAAI27_FULL_SUBMISSION_RECORD.md
EXPERIMENT_AUTHORIZATION: NONE
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LARGE_EXPERIMENTS: 0
NEXT_ACTION: wait overnight;then create manuscript/stage3/cold_read_report.md from rendered-PDF cold read before any wording/layout edit
NEXT_DECISION: only substantive cold-read findings require owner adjudication;otherwise proceed to final build/upload gate
LAST_UPDATED: 2026-07-23T00:29:40+08:00

## Stage 2.5 integrity checkpoint (2026-07-22)

CURRENT_PHASE: Stage 2.5 COMPLETE / PASS_WITH_NOTES / AWAITING OWNER ACCEPTANCE
LAST_COMPLETED: formal citation integrity, raw recount, claim audit, originality screen, anonymous supplement packaging, checklist disposition, and seven-failure-mode review;one correction round used
CURRENT_HEAD: e0f19f500407b72469b3d4052f2306445176b95c(Stage 2.5 package commit 的 parent)
OPENREVIEW_SUBMISSION_NUMBER: 44503
CITATION_AUDIT: 21/21 cited keys resolved and checked against primary records;AgentTrace v4 metadata,AgentReuse journal metadata,AutoGen title/repo binding,SWE-agent repo binding,Agent Workflow Memory mechanism wording,and HumanEvalPack attribution corrected
SHERLOCK_STATUS: arXiv:2511.00330 v1;public record remains within-run verification/speculation/rollback with no cross-run cache/history branch;C3 scoop re-review trigger NOT_MET
DESCRIPTIVE_RECOUNT:
- frozen trajectories=18;cutoff events=8;next assistant-response text differs=6/8;parsed next command differs=4/8;suffix differs=8/8;exit differs=4/8;full next invocation matches=0/8
- registered C6 population=4,968 non-system block--agent incidences;substring zero=98.09%;Jaccard zero=95.69%;median/p90=0;generation-aligned sensitivity excludes 1,092 retriever-side cite/doc incidences and has n=3,876,zero=97.70%/94.71%,median/p90=0
- corrected document-only citation estimand=763 pairs;mentioned=61 with 0 real flips;unmentioned=702 with 36 real flips(5.13%);same 702 identity-control flips=35(4.99%);legacy 53/947 stored only as diagnostic
SCIENTIFIC_EFFECT: NONE;TEXT_USAGE_PROXY remains INVALID;C6_STRONG_TESTBED remains NOT_FOUND;C3 remains NEED_NEW_VERIFIER
SUPPLEMENT: manuscript/supplement/aaai27_code_data_supplement.zip;32 members;76,847 bytes;sha256=d73c6fa6949e70c3f5a97c19f163247bf2190ed990b422a563f78fdbd5e3629d;deterministic build/hash/anonymity scan PASS
SUPPLEMENT_BOUNDARY: tracked archive reproduces focused code paths,fixtures,invariants,and committed static analyses;full aggregate raw inputs remain hash-bound external artifacts and are not redistributed
CHECKLIST: manuscript/ReproducibilityChecklist.tex=immutable official blank source(sha256 06a3459158089bf1c64b738986118f1d1566e816da4b710c6397561e33c3d5e6);manuscript/reproducibility_checklist.tex=completed 31-slot source;only completed standalone PDF is uploaded in the designated OpenReview field;neither TeX source enters supplement
BUILD: main=8 pages(1--7 content,page 8 references only);21 citations;US Letter;embedded non-Type3 fonts;Figure 2 300ppi;title/abstract lock PASS;anonymous PDF PASS
TESTS: C3 v2.1 6/6 PASS;C6 5/5 PASS;selective audit 6/6 PASS;D0 3/3 PASS;D0 source hashes 11/11 PASS;Stage 2.5 recount 2/2 PASS;supplement deterministic package test 1/1 PASS;JSON validation PASS;LaTeX main/checklist compile PASS;manuscript checker PASS;git diff --check PASS
FAILURE_MODE_REVIEW: implementation bug=CLEAR_AFTER_CORRECTION;citation hallucination=CLEAR_AFTER_CORRECTION;hallucinated result=CLEAR;shortcut reliance=CLEAR;bug reframed as insight=CLEAR_AFTER_CORRECTION;methodology fabrication=CLEAR;frame lock=CLEAR
REMAINING_NOTES: full aggregate raw data not independently reproducible from archive alone;cross-model MCP reviewer unavailable and replaced by fresh zero-context independent agents plus coordinator checks;Q rubric lacks inter-rater validation;originality screen sampled 16/~45 paragraphs and did not run author-specific self-overlap under anonymity
EXPERIMENT_AUTHORIZATION: NONE
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LARGE_EXPERIMENTS: 0
NEXT_ACTION: mandatory stop;responsible owner accepts Stage 2.5 before any Stage 3 work
NEXT_DECISION: accept PASS_WITH_NOTES and authorize Stage 3 writing/reviewer work,or request a bounded second correction round;neither option implicitly authorizes experiments
LAST_UPDATED: 2026-07-22T19:21:56+08:00

## Stage 2 manuscript completion checkpoint (2026-07-22)

CURRENT_PHASE: Stage 2 COMPLETE / AWAITING STAGE 2.5 AUTHORIZATION
LAST_COMPLETED: complete anonymous AAAI-27 measurement/methodology draft committed as 13be818;OpenReview Submission Number 44503 title and abstract remain locked
CURRENT_HEAD: 13be8182d89c99ee53db5224b066c3d0707796eb
MANUSCRIPT: manuscript/main.tex;8 pages total;pages 1--7 content;page 8 references only;19 cited keys;official AAAI-27 submission style
CHECKLIST: manuscript/reproducibility_checklist.tex;31/31 response slots completed;standalone 2-page US Letter PDF compiled locally
SCIENTIFIC_POSITIONING: reuse-specific claim-qualification protocol, not general provenance taxonomy, cache mechanism, framework census, deployed saving, or actual-skip experiment
AUDIT_UNIT_SCOPE: AutoGen handoff example=Q1/CODE_ONLY;LangGraph two-consumer fixture=Q0/CODE_ONLY;RetryAgent optional Preselector=Q1/CODE_ONLY
INDEPENDENT_STAGE2_AUDITS: reviewer initial weak-reject/major-revision findings addressed;claim-evidence audit P0=0 with all six P1 corrections incorporated;format P0 fixed(color contrast,300 ppi,fresh build,completed checklist)
BUILD_CHECKS: title/abstract lock PASS;anonymous source PASS;19/19 citation keys resolved;8-page PDF PASS;page 8 reference-only PASS;US Letter PASS;embedded non-Type-3 fonts PASS;Figure 2 300 ppi+manifest hashes PASS;no overfull/undefined warnings PASS
FOCUSED_TESTS: C3 v2.1 6/6 PASS;C6 5/5 PASS;selective audit 6/6 PASS;D0 3/3 PASS;D0 source hashes 10/10 PASS;git diff --check PASS
REPRODUCIBILITY_BOUNDARY: tracked code/fixtures reproduce paths and invariants;aggregate statistics, historical diff JSON, and VRAA injection bundle still require separately preserved SHA-bound external raw files
EXPERIMENT_AUTHORIZATION: NONE
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LARGE_EXPERIMENTS: 0
NEXT_ACTION: owner authorization for mandatory formal Stage 2.5 zero-context integrity verification
NEXT_DECISION: proceed to Stage 2.5, or request targeted Stage 2 wording changes first;do not authorize experiments through this checkpoint
LAST_UPDATED: 2026-07-22T17:16:44+08:00

## OpenReview submission and Stage 2 WRITE checkpoint (2026-07-22)

CURRENT_PHASE: Academic Pipeline Stage 2 WRITE / academic-paper full mode
LAST_COMPLETED: Responsible author manually submitted the frozen abstract to OpenReview as Submission Number 44503
CURRENT_HEAD: df4127c471043f2614cf15629167d55867092d5d(Stage 2 start edits 的 parent)
PAPER_CONFIGURATION: AAAI-27 main technical track;measurement+methodology conference paper;English;official LaTeX;7 content pages+up to 2 reference pages;author-year AAAI bibliography style
ABSTRACT_LOCK: docs/AAAI27_ABSTRACT_SUBMISSION.md;qualitatively unchanged through full-paper deadline
AUTHORIZED_SCOPE: manuscript architecture/drafting;verified citation integration;CPU-only tables/figures;LaTeX compilation;artifact packaging from existing data
FORBIDDEN_SCOPE: studied-system model/API calls;GPU;new trajectories;new harness;cache/replay execution;fourth-framework search;changing frozen C3/C6/C4 results
STAGE2_DELIVERABLES: manuscript/spine.md;manuscript/claims_matrix.md;AAAI LaTeX source+bibliography;complete draft v0;core tables/figures;compile log
NEXT_GATE: Stage 2 completion checkpoint, followed by mandatory Stage 2.5 integrity verification
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LAST_UPDATED: 2026-07-22T16:08:58+08:00

## Owner decision A and D0 checkpoint (2026-07-22)

CURRENT_PHASE: Option A 文档阶段完成;D0 static feasibility gate 已关闭 proposed HumanEvalFix actual-skip route
LAST_COMPLETED: 摘要去实验承诺;Fable 5 disposition;measurement idea card;design-only prereg;read-only D0 audit;source SHA manifest;experiment plan/tracker
CURRENT_HEAD: 74d8660b27e32288603580951c9c157a3a2ee213(本 handoff synchronization commit 的 parent)
UNCOMMITTED_FILES: docs/RESEARCHSTUDIO_HANDOFF.md only;任务前三个工具目录不纳入研究提交
CURRENT_CANDIDATES: paper=MEASURE_BEFORE_YOU_REUSE;HumanEvalFix exact response/tool 2x2=INELIGIBLE_AS_PROPOSED
CURRENT_Q_LEVELS: AutoGen=Q1/CODE_ONLY;LangGraph=Q0/CODE_ONLY;SWE-agent=Q1/CODE_ONLY;无 Q2/Q3 TRACE_CONFIRMED
CURRENT_SCIENTIFIC_STATE: HumanEvalFix native pipeline=Planner→Coder→Reviewer→Fixer + host certificate,非 proposed two-stage tool loop;source/test 在所有 LLM prompt 中;不存在 native tool-result consumer;历史 VRAA 已有 80 producer-node skips,但 comparator 40/40 未形成差异;1,968 是 condition cells,非模型调用;在 identity-only hit+每 cell 两次调用假设下 optimistic two-stage=3,280 calls
AUTHORIZED_SCOPE: 摘要与论文设计文档;只读历史源码/已有 results;CPU-only static checks
FORBIDDEN_SCOPE: 模型/API call;GPU;新 trajectory;新 harness;cache/replay arm 实现;mutation treatment;OpenReview 外部提交
NEXT_COMMAND: git diff --check;提交 handoff synchronization;push main
OPEN_QUESTIONS: 负责人是否已手工提交摘要;是否授权下一阶段 manuscript drafting;不建议为本周期寻找新的 actual-skip testbed
NEXT_DECISION: 接受 D0 no-go 并按 pure measurement/methodology 写作,或另立全新 testbed decision(需要新 prereg 与授权)
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LARGE_EXPERIMENTS: 0
LAST_UPDATED: 2026-07-22T13:08:02+08:00

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

## Selective-consumption protocol freeze checkpoint (2026-07-22)

CURRENT_PHASE: protocol/candidate universe frozen;source/trace evidence 尚未开始
LAST_COMPLETED: result-free protocol commit 74f9c14
CURRENT_HEAD: 74f9c1407735121837becb91169adddd4f94c16f
CURRENT_CANDIDATES:
- autogen@027ecf0a379bcc1d09956d46d12d44a3ad9cee14(event/message routing + delivery log)
- langgraph@31f90df3e6b0268fa77fd2d118a917d420b84a68(typed state + Send projection + task/debug stream)
- swe_agent@3ea751c087f32b16e039a2233dd6eefecef325d5(RetryAgent attempt/reviewer/chooser + public .traj)
PRESCREEN_EXCLUDED: mini-swe-agent(single consumer);ToolSandbox(no multi-consumer delivery path);Route A+/AutoCodeRover(frozen/harness mismatch)
FREEZE_RULE: 不替换;不添加第四候选;trace 缺失只降为 CODE_ONLY_CANDIDATE
RESULTS_PRESENT: NO
Q_LEVELS_ASSIGNED: NO
EXPERIMENT_AUTHORIZATION: NONE
NEXT_ACTION: 为每个 frozen candidate 定位 artifact creation/routing/consumer input/raw bypass/access log/trace serialization 与既有 public trace 实例
LAST_UPDATED: 2026-07-22T10:02:00+08:00

## Selective-consumption source/trace evidence checkpoint (2026-07-22)

CURRENT_PHASE: frozen 三候选源码与既有公开 artifact 取证完成;尚未赋 Q 等级
LAST_COMPLETED: evidence commit d2b30c5 + timestamp correction fd6d7d7
CURRENT_HEAD: fd6d7d769c4facbb5947aca535013c0a276e63f9
CURRENT_CANDIDATES:
- autogen@027ecf0a379bcc1d09956d46d12d44a3ad9cee14:topic subscription 原生 non-delivery;完整 UserTask 直送;MessageEvent 缺 message_id/consumer binding;无公开 OTEL export
- langgraph@31f90df3e6b0268fa77fd2d118a917d420b84a68:Send/PULL 输入组装与 task identity 可定位;CONFIG_KEY_READ raw bypass 存在且无 read log;公开材料仅测试期望
- swe_agent@3ea751c087f32b16e039a2233dd6eefecef325d5:Reviewer/Chooser 为互斥 retry-loop;shipped chooser config 无 preselector;22 个 tracked .traj 均非 RetryAgent
PUBLIC_MECHANISM_TRACE_COUNTS: autogen=0;langgraph=0;swe_agent=0
TRACE_DERIVED_COUNTS: 全部保持 null;静态拓扑数字不得解释为运行 coverage
MAIN_AGENT_SPOT_CHECK:
- AutoGen:_single_threaded_agent_runtime.py envelope/publish/delivery + logging.py MessageEvent + sample consumer input
- LangGraph:types.py Send + _algo.py PUSH task/input identity + _read.py raw shared-state access + debug fixture
- SWE-agent:agents.py ReviewSubmission/serialization + reviewer.py alternative consumer inputs/config union + tracked .traj negative control
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LARGE_EXPERIMENTS: 0
NEXT_ACTION: 生成、校验并单独提交未经解释的 results.json
LAST_UPDATED: 2026-07-22T10:44:34+08:00

## Selective-consumption raw-results checkpoint (2026-07-22)

CURRENT_PHASE: raw descriptive analysis complete;scientific interpretation stored only in later verdict artifacts
LAST_COMPLETED: initial results commit dee550b;consumer-universe locator refresh 97c1272/94525e7;SWE integration-fact refresh 2782fbd/356e9bd
CURRENT_HEAD: 356e9bd8ab5350e7163a23efeb5bc9d7e41ba5fb
RAW_RESULT_INVARIANTS:
- q_levels=null
- interpretation=null
- c6_qualification=null
- c3_directed_verifier_verdict=null
- autogen/langgraph/swe_agent machine_readable_trace_count=0
- trace-derived producer_artifact_count/consumer_edge_count/repeated_consumer_count 全部 null
TESTS: audit parser 6/6 PASS;JSON validation PASS;git diff --check PASS
NEXT_ACTION: 主代理依据 raw evidence 与 frozen decision rules 裁决;若所有候选仅 Q0/Q1/QX/CODE_ONLY,触发 DECISION_EVENT 3 并停止等待负责人
LAST_UPDATED: 2026-07-22T10:56:32+08:00

## Selective-consumption verdict checkpoint (2026-07-22)

DECISION_EVENT: ALL_FROZEN_CANDIDATES_ARE_Q0_Q1_OR_CODE_ONLY
CURRENT_PHASE: bounded phenomenon/testbed qualification complete
VERDICT: AutoGen=Q1/CODE_ONLY;LangGraph=Q0/CODE_ONLY;SWE-agent=Q1/CODE_ONLY;C6_STRONG_TESTBED=NOT_FOUND;C3_DIRECTED_VERIFIER_CANDIDATE=NOT_FOUND
EVIDENCE:
- AutoGen:三 agent consumer universe + topic-specific non-delivery 在 pinned source 中成立;公开 history/测试不是 message-id→consumer trace
- LangGraph:具体双 consumer fixture 接收相同完整 state;单一 Send destination 不足以证明真实 nonrecipient;CONFIG_KEY_READ bypass 无 read log
- SWE-agent:原生 optional Preselector→Chooser 对未选 submission 构成 Q1 non-delivery;shipped config 未启用;22 个公开 .traj 均非 RetryAgent
- 三候选 machine_readable mechanism trace count 均为 0;所有 trace-derived counts 保持 null
FRAMEWORK_RESULTS:
- candidate:autogen;q_level:Q1;evidence_level:CODE_ONLY_CANDIDATE;key_locator:_single_threaded_agent_runtime.py:557-609;main_limit:no public message-id/consumer delivery trace
- candidate:langgraph;q_level:Q0;evidence_level:CODE_ONLY_CANDIDATE;key_locator:test_large_cases.py:3939-4168;main_limit:full-state fan-out + unlogged raw bypass
- candidate:swe_agent;q_level:Q1;evidence_level:CODE_ONLY_CANDIDATE;key_locator:reviewer.py:242-371;main_limit:no public RetryAgent trace;Preselector disabled in shipped config
C3_IMPACT: UNCHANGED;NARROW_GAP + NEED_NEW_VERIFIER;selective routing does not attribute reuse damage
C6_IMPACT: strong testbed not found;strong form does not restart;weak selective-routing direction only
OPTIONS:
- A:关闭 strong C6 testbed 搜索,形成 selective-consumption measurement/testbed position-paper idea card/prereg(推荐)
- B:关闭当前 C3/C6 strong 形式,授权有界重新选题;任何实验前另立 protocol/prereg
RECOMMENDATION: Option A;保留 B 作为负责人判断 measurement gap 不足以投稿时的 fallback
REQUESTED_AUTHORIZATION: 负责人选择 A 或 B;本 checkpoint 不请求模型/GPU/正式实验授权
CURRENT_HEAD: d3ad56e5ea57c9ac719301de34f54b74bd169baf(verdict package commit;本 handoff 同步提交的 parent)
WORKTREE_STATUS: verdict package 已提交;提交后仅任务前 .agents/.claude/.codex 原样未跟踪
HANDOFF: docs/RESEARCHSTUDIO_HANDOFF.md
MODEL_EXPERIMENT_CALLS: 0
GPU_RUNS: 0
NEW_AGENT_TRAJECTORIES: 0
LARGE_EXPERIMENTS: 0
NEXT_ACTION: 停止并等待负责人
LAST_UPDATED: 2026-07-22T10:58:44+08:00

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
- C6:机制未判死也未证实;文本 usage 代理第三次失效;本轮 frozen universe 中 C6 strong testbed=NOT_FOUND,仅 Q1 weak selective routing direction=POSSIBLE。
- C4:维持 HIGH_COLLISION 拒绝(C4-P6 DIRECT)。
- 当前 owner 决策点:采用 measurement/testbed position-paper idea card(推荐),或关闭当前 C3/C6 strong 形式后有界重新选题。

## 冻结资产与纪律

- tag `idea-landscape-v1-pre-fulltext-and-scoop-check`(cab8363)、`researchstudio-v1-gate-review-required`(252c9b2)
- v1 gate 文件全部保留原样;v2 结论不覆盖 v1,仅取代其解释地位
- 模型调用=0,GPU=0,大型实验=0(全程保持)
