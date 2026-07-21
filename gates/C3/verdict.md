# C3 Gate Verdict

**C3_GATE = FAIL(经济性判死 naive 形式;抢救路径已精确定位)**

日期:2026-07-21 · 主协调代理(主席终裁,非 DRAFT)

## 关键数字(全部来自冻结 trace,CPU-only,可复现:`reanalyse_or_simulate.py`)

| 量 | Task A(HotpotQA, n=100) | Task B(HumanEvalFix, n=164) |
|---|---|---|
| baseline 准确率(from-scratch) | 0.04(**数据退化**:E0 最终答案被截断,EM 几乎全灭) | 0.634 |
| ρ_outcome(outcome verifier 拒绝率) | 0.99(不可解释,见退化注记) | 0.390–0.396 |
| ρ_blame(有责拒绝:orig 对而 arm 错) | 0.04 / 0.04(reuse/repair) | 0.043 / 0.043 |
| rescue(orig 错而 arm 对) | 0.01 | 0.012–0.018 |
| 单次尝试 FLOP 节省 S | 无成本字段(见下) | **0.144(reuse)/ 0.122(repair)** |

经济学(Task B,成本字段实测):Δ/C_full = S − v − ρ·(1+rb)。
- **outcome-verified 投机**:ρ_outcome ≈ 0.40,Δ ≈ **−0.26 ~ −0.76**(v∈[0.001, 0.5])——在每个 v 下都大幅亏损。原因:EM/测试把**任务本身做错**也判为拒绝,每次 baseline 错误都触发一次无谓回滚;verifier 无法区分"复用引入的错误"与"本来就做错的题"。
- **假设存在定向 verifier**(只有复用引入的损坏触发回滚,ρ_blame=0.043):Δ 在 v=0.001 时 +0.10,在 v=0.1 时 ≈ 0——**正收益要求 verifier 成本 ≤ 重算的 ~10%**,余量极薄。
- **第三臂:免验证复用**(NEG-01 已测):成本 = flops_reuse,错误增量与噪声不可区分——在本 regime 下它同时优于事前判定与投机验证。

## 预登记判据复核

- (a) verifier 可执行率 100%:PASS(但 Task A 的 EM 因答案截断而退化,如实记录);
- (b) ρ_blame 比 ρ*(v=0.5) 低 ≥5×:**FAIL**——ρ*(0.5)<0,判据不可满足;即便 v=0.01,余量也只有 ~3.1×;
- (c) 接受与有责回退案例均 ≥1:PASS(各 arm 约 7 例有责回退)。

→ overall = FAIL(判据 b)。focused tests:5/5 通过(`test_gate.py`)。

## 这个 FAIL 教给我们什么(主席解读,不是美化)

1. **C3 的 naive 形式(默认复用 + outcome verifier + 回退)在 S≈14%、baseline 准确率 ≤63% 的 regime 下被经济性判死。** 这不是测量失败——verifier 可执行、案例齐全、数字可复现。
2. **判死机制是新知识**:outcome verifier 的"混淆问题"(baseline 错误 vs 复用引入错误不可分)使 ρ_outcome ≈ 1−accuracy ≫ ρ*。这是旧项目从未写出的因果账。
3. **抢救路径被精确定位**:投机要赢,要么 (i) S 远大于 14%(更长上游链、更贵重算),要么 (ii) 存在成本 ≤10% 重算的**定向损坏 verifier**——而后者正是旧项目在文本启发式上失败过的对象(NEG-11:difflib Oracle 行为级 false cutoff 6/8)。没有新机制的定向 verifier,C3 不得重启。
4. **"免验证复用"在本 regime 占优**(NEG-01 证据),这反过来削弱了"验证"本身的存在理由——C3 的论文若存在,必须建立在 verifier 必要性成立的 regime(高 mutation、强外部状态变更),而那些 regime 里 outcome verifier 又因混淆问题失效。这个两难是 C3 的核心科学困难,不是工程困难。

## 与 CP2 的联动

CP2 判 C3 = NARROW_GAP(novelty 可防守)。本 gate 证明其**默认实验形式不可行**。
按 CP4 规则("gate 不是 FAIL"为必要条件),C3 不得成为主候选。其 salvage 条件
(定向 verifier + 大 S regime)记入 `docs/researchstudio_collision_decision_memo.md`。
