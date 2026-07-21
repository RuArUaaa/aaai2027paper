# C3 Gate Protocol — 投机复用 + 验证 + 回退 (Speculative Reuse + Verify + Rollback) 修订资格门

状态: 本协议由科学主席定义执行语义，数据分析子代理仅负责在冻结数据上执行统计。
判定标准在查看任何结果前预登记于本文件第 4 节。

## 1. 执行语义(主席定义,逐字)

1. 复用对象:E0 冻结 trace 中 producer block 的计算表示被下游 receiver 消费(reuse arm = 下游用复用 KV 续算)。
2. 状态变化:trace 内的自然扰动(E0 设计的 perturbed 变体)。
3. 具体冻结复用策略:reuse-all——每个符合条件的 (block, receiver) 尝试复用(frozen reuse arm 即一次 speculative attempt);repair arm 同理另算。
4. Verifier(outcome 级,冻结数据上可执行):Task A = EM(final_answer, gold_answer);Task B = 单元测试通过,由 orig_correct XOR d3_flip 重构(flip=1 表示通过状态翻转)。
5. Verifier 每次 attempt 都执行,成本计入 C_verify。
6. Verifier false positive/negative:EM/测试为精确判定,记 FP=FN=0(注明这是 benchmark oracle,部署期 runtime verifier 另议——写入 protocol 限制节)。
7. Rollback:拒绝后回退到 producer 输出前的 checkpoint,重算该 receiver 及其下游。
8. 副作用:E0 为无外部副作用 QA/代码任务,记 n/a(写入限制节)。
9. 禁止投机的操作:本 gate 无(写入限制节:有副作用操作应禁止,见 C3-P10 副作用准入三分)。
10. 成本式:C_spec = C_reuse + C_verify + ρ·(C_rollback + C_recompute);Δ = C_full − C_spec;C_verify 必须计入每次 attempt。

## 2. 数据(全部只读,冻结)

| 文件 | 内容 |
|---|---|
| `runs/pairs/taskA_e0_control.jsonl` | 100 traces;`orig_correct, reuse_correct, repair_correct, em_flip_reuse, em_flip_repair, gold_answer` 等 |
| `runs/pairs/taskA_e0_identity_ctrl.jsonl` | 1000 pairs;identity 噪声地板 |
| `runs/pairs/taskB_e0.jsonl` | 164 pairs;`d3_flip_reuse, d3_flip_repair, cost, pair_id` 等 |
| `runs/pairs/taskB_e0_identity_ctrl.jsonl` | 164;`orig_correct, identity_pass_reuse/repair, identity_flip_*` 等 |
| `runs/traces/taskA_e0.jsonl` | 每 trace 4 agent,含 `output_len`(recompute 成本代理) |

## 3. 统计定义

- 每次 (task, arm, pair/trace) 为一次 speculative attempt。Verifier accept = 结果正确
  (Task A: `reuse_correct`/`repair_correct`;Task B: `pass_* = orig_correct XOR d3_flip_*` 重构)。
- `ρ_arm = P(verifier 拒绝 | attempt)`,per task;cluster bootstrap 95% CI
  (cluster = `trace_id`;Task B 若无 `trace_id` 则用 `pair_id` 前两段前缀;10,000 次重抽样,固定种子 20260721)。
- 基线对照:`baseline_reject = 1 − mean(orig_correct)`。
- 有责拒绝率:`ρ_blame = P(拒绝 ∧ orig_correct=1)`(投机把本来对的弄错)。
- 拯救率:`save = P(接受 ∧ orig_correct=0)`(投机把本来错的救对)。
- 案例计数:真实接受数、真实回退(有责)数、拯救数,per task × arm。
- 一致性 sanity check(如实计数报告,不修正):
  - Task A: `reuse_correct == orig_correct XOR em_flip_reuse`(repair 同理)。
  - Task B: 重构 `pass_*` vs `identity_pass_*`;`real_flip_*`(identity 文件内) vs `d3_flip_*`(pairs 文件);
    `orig_correct XOR identity_flip_*` vs `identity_pass_*`(identity 内部一致性)。
- 成本(每单位完整工作,S = C_full,报告 Δ/S):
  - Task B: 用 `cost` 字段,`s = 1 − flops_arm/flops_full`(每次成功复用节省的计算比例)。
  - Task A: 用 traces 的 `output_len` 作代理;`S = Σ_agents output_len`,节省比例代理
    `s = (S/4)/S = 0.25`(control 文件无 block 级 receiver 身份,按 4 agent 槽均匀代理,两臂同值)。
  - 回退成本代理:`C_rollback + C_recompute = C_full − C_reuse = s·S`
    (回退恰好重做复用所跳过的 receiver+下游计算;checkpoint 恢复开销近似 0,见限制节)。
  - 由此 `Δ/S = (1−ρ)·s − v`,其中 `v = C_verify/S ∈ {0.001, 0.01, 0.1, 0.5}`。
  - 盈亏平衡:`ρ*(v) = 1 − v/s`(令 Δ = 0 解出)。`ρ*(v) < 0` 表示在该 v 下即使 ρ=0 也不盈亏平衡。
- verifier 可执行率:attempt 中 verifier 所需字段齐全(Task A: `orig_correct`/`reuse_correct`/`repair_correct`
  非缺失;Task B: `d3_flip_*` 非缺失且可按 `pair_id` 联到 `orig_correct`)的比例;缺失记为不可执行并计数。

## 4. 预登记判定标准(先于结果计算写入)

GO 当且仅当以下全部成立:

- (a) verifier 可执行率 ≥ 95%(两个 task 各自);
- (b) ρ_blame 比 ρ*(v=0.5) 低 ≥ 5×,即 `ρ_blame ≤ ρ*(0.5)/5`(task × arm 四个组合各自);
- (c) 真实接受案例数 ≥ 1 且有责回退案例数 ≥ 1(task × arm 四个组合各自)。

任一不满足即 NO-GO(草稿判定,最终由主席签核)。

## 5. 旧负结果解读(新语义 vs 旧 "final-answer flip rate")

旧负结果报告的 "final-answer flip rate" 是**无条件的扰动敏感度**:P(复用后最终答案正确性翻转),
它把三类事件混在一起——基线本来就不对的样本、投机造成的损坏、投机带来的拯救——且未区分
部署策略与 verifier。本 gate 的新语义下,`ρ` 是**具体部署策略(reuse-all)+ 具体 outcome verifier
(EM / 单元测试)下的条件拒绝概率**,并显式分解为:baseline 拒绝率(不投机也会错)、
有责拒绝率 ρ_blame(投机真正造成的损害,即回退的真实成本驱动项)、拯救率(投机的收益项)。
成本分析中只有 ρ_blame 对应"本可避免的回退",而 Δ/S 用的是总 ρ(所有回退都花成本)。
因此旧 flip rate 不能直接当作投机可行性的判决;新指标可直接代入成本式做盈亏平衡判断。

## 6. 限制节(Limitations)

1. **Verifier 为 benchmark oracle**:EM/单元测试视为精确判定,FP=FN=0。部署期的 runtime verifier
   (模型裁判、启发式检查)有非零 FP/FN 与显著更高成本,需另行登记分析;本结论不外推。
2. **副作用 n/a**:E0 全部为无外部副作用的 QA/代码任务;rollback 语义在此条件下良定义。
   有副作用操作(写文件、网络调用、付费 API)应**禁止投机**,本 gate 不含此类操作——
   准入三分见 C3-P10(safe-reversible / compensated / forbidden)。
3. **成本为代理量**:Task B 用记录归一化 FLOPs;Task A 用 `output_len` 均匀槽代理(无 block 级
   receiver 身份),`C_rollback+C_recompute` 近似为复用节省量,checkpoint 恢复开销记 0。
   真实系统的 rollback/restore 开销与 KV 传输成本未计入,Δ/S 为上界估计。
4. **identity 噪声地板非零**:identity ctrl 下 flip 率约 5–7%(见 results.json),
   即部分"翻转"是重跑噪声而非扰动损害;ρ_blame 含此噪声成分,未做噪声扣除(保守方向:
   高估损害)。
5. **Task B 重构依赖 XOR**:`pass_* = orig_correct XOR d3_flip_*` 的重构与 `identity_pass_*`
   存在少量不一致(如实计数于 results.json);不一致样本未剔除。
6. **样本量**:Task A 仅 100 traces 且基线通过率极低(4%),CI 宽;Task B 164 pairs。
   结论的统计功效有限。
7. **无模型调用/GPU**:本分析为纯统计,所有数字可由 `reanalyse_or_simulate.py` 重复产出
   (stdlib only,固定种子)。
