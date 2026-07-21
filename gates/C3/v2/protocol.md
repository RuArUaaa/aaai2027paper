# C3 Gate v2 Protocol — 投机复用经济学(修订版,冻结于任何 v2 结果之前)

日期:2026-07-21 · 主协调代理
本文件是 v2 协议。v1(`gates/C3/protocol.md` + `results.json`)因"成本公式与协议语义矛盾"
被评审判 INVALID,保留原样作历史记录;v2 与 v1 的全部差异列于 §6。

## 1. 执行语义(与 v1 相同的部分)

复用对象、冻结策略(reuse-all / repair-all)、verifier 定义(Task A: EM;Task B: 测试通过,
orig_correct XOR d3_flip 重构)、数据文件,均与 v1 一致,不再重复(见 v1 protocol §1–§2)。

## 2. 修订的拒绝-重算语义(v1 的错误在此)

1. **重算范围**:verifier 拒绝后,回滚到 checkpoint,**只重算被投机跳过的 receiver 及其下游
   子图**,其成本为被跳过的量 `s·C_full`(与本次投机试图节省的量相同),而不是再付一次
   完整执行 `1.0·C_full`。
2. **单次回滚,不再验证**:重算产出即 from-scratch 结果(构造上无投机成分),直接接受,
   不进入第二次验证循环。
3. **重算后仍错误的终态**:若 from-scratch 重算仍错误(baseline 本来就是错的),记为
   **baseline error,不算投机失败**;系统接受该结果并终止,不重试。该数量在结果中
   单列(`recompute_still_wrong`),不得计入投机机制的失败。

## 3. 修订的成本公式

```
C_full  = 1
C_spec  = (1 − s) + v + ρ·(s + RB)
Δ/S     = s − v − ρ·(s + RB)          RB = 0.01
```

其中:
- `s` = 单次投机尝试节省的相对工作量(Task B 由 cost 字段实测:reuse 0.1440,repair 0.1224);
- `ρ` = P(verifier 拒绝 | 该冻结策略的一次投机尝试),与 v1 定义一致;
- `v` = verifier 成本 / C_full,扫描网格 {0.001, 0.01, 0.1},**删除 v=0.5 档**
  (该档成本高于任何可能节省,把它设为硬门是 v1 的设计错误);
- 盈亏平衡:`Δ/S > 0 ⟺ ρ < (s − v)/(s + RB)`。

## 4. 分离报告的三个 ρ(v1 混淆的在此拆开)

- `ρ_outcome`:outcome verifier(EM/测试)拒绝率 = 1 − 准确率。它把 baseline 错误
  与复用引入错误混在一起,是**naive 部署形态**的拒绝率;
- `ρ_blame`:有责拒绝率(orig 对而 arm 错)。它是"假设存在定向 verifier(只识别复用引入
  的损坏)"时的拒绝率。**注意:ρ_blame 用 baseline 对错标签事后计算,当前不存在
  对应的运行时 verifier(NEG-11 已证明文本启发式路线失败)——以此得出的经济性
  是有条件的,标注为 CONDITIONAL**;
- `rescue`:orig 错而 arm 对的比例;
- `recompute_still_wrong`:见 §2.3。

## 5. 预登记判据(v2,可满足性已自检)

- (a) verifier 可执行率 ≥ 95%;
- (b) 经济学符号地图:在 v 网格上报告 Δ/S 的正负;**不设任何先验不可满足的硬阈值**。
  判定:
  - `GO_NAIVE`:ρ_outcome 下 Δ/S 在 v=0.01 与 v=0.1 两档均 > 0;
  - `GO_CONDITIONAL`:ρ_blame 下 Δ/S 在 v=0.01 与 v=0.1 两档均 > 0;
  - `NEED_NEW_VERIFIER`:GO_NAIVE 不成立而 GO_CONDITIONAL 成立;
  - `NO_GO`:两者均不成立;
- (c) 接受案例与有责回退案例均 ≥ 1;
- (d) §2 终态语义已在结果中单独计数(recompute_still_wrong)。

Task A 仅报告 ρ 各值(其 EM 因答案截断退化,且 traces 无成本字段;s 不可得,
不进入经济学,如实记录)。经济学以 Task B 为准。

## 6. v1 → v2 差异清单

| 项 | v1(判 INVALID) | v2 |
|---|---|---|
| 回滚重算成本 | 1.0·C_full(与协议矛盾) | s·C_full(与协议一致) |
| 成本公式 | s − v − ρ(1+RB) | s − v − ρ(s+RB) |
| v 网格 | {0.001, 0.01, 0.1, 0.5} | {0.001, 0.01, 0.1} |
| 判据 (b) | ρ_blame ≤ ρ*(0.5)/5(先验不可满足) | 符号地图 + GO_NAIVE/GO_CONDITIONAL/NEED_NEW_VERIFIER/NO_GO |
| 终态语义 | 未定义 | 单次回滚不再验证;baseline 错误单列 |
| ρ 报告 | 混用 | ρ_outcome / ρ_blame / rescue / recompute_still_wrong 分列 |
