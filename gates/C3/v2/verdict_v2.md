# C3 Gate v2 Verdict(commit 3 of 3)

日期:2026-07-21 · 主协调代理
本 verdict 只解读 `results_v2.json`(commit `2f54cfa`),不修改之。
v1 结论("经济性判死")按评审判 INVALID,已撤回;v1 文件保留原样。

## 判定

```
C3_GATE_V2 = NEED_NEW_VERIFIER
```

预登记判据复核(v2 protocol §5):
- (a) verifier 可执行率 100% ≥ 95%:PASS(Task A 的 EM 退化已如实标注并排除出经济学);
- (b) 符号地图:
  - GO_NAIVE(ρ_outcome,v=0.01 与 0.1 两档均正):**不成立**(v=0.01 +7.3%,v=0.1 −1.7%);
  - GO_CONDITIONAL(ρ_blame 同两档):**成立**(+12.7% / +3.7%,repair 臂 +10.7% / +1.7%);
  - → NEED_NEW_VERIFIER;
- (c) 接受与有责回退案例:各 arm ≈7 例,PASS;
- (d) 终态语义计数:recompute_still_wrong(Task B)= baseline 错误率 36.6% 中的对应份额,已单列。
focused tests:5/5 通过(`test_gate_v2.py`)。

## 修正后的经济学(Δ/S = s − v − ρ(s+RB),s=0.144,RB=0.01)

| ρ 口径 | v=0.001 | v=0.01 | v=0.1 | 解释 |
|---|---|---|---|---|
| ρ_outcome=0.396(naive outcome verifier) | +8.2% | +7.3% | **−1.7%** | 仅在 verifier 极便宜(≤~8% 完整执行)时为正 |
| ρ_blame=0.043(假设定向 verifier) | +13.6% | +12.7% | +3.7% | 在全部扫描档为正 |

## 主席解读(与 v1 的差异在哪)

1. v1 的实现错误(回滚付 1.0·C_full)把符号在低 v 下反转;按协议语义(只重算被跳过的
   s·C_full),naive 投机在便宜 verifier 下**微利为正**,不是 v1 所说的"判死"。
2. 但 naive 形态的正收益极薄:v=0.1 即转负。outcome verifier 的混淆问题依旧真实——
   它决定了收益窗的上沿(v ≲ 8%)。
3. 定向 verifier(若存在)把收益窗推到 v ≤ 13.7%。**C3 的全部科学重量落在一个
   尚未解决的问题上:能否造出成本 ≤10% 重算、区分"复用引入损坏"与"baseline 错误"
   的 verifier。** NEG-11 记录过文本启发式路线的失败;任何重启必须基于新机制,
   不得复用 difflib/相似度类代理。
4. "免验证复用"在本 regime 仍是强对照(零 verifier 成本,ρ_blame=4.3% 错误增量):
   它意味着 C3 的证伪点清晰——若定向 verifier 不存在且 regime 低扰动,
   验证本身没有存在理由。

## 与 CP4 的联动(详见 decision_v2)

C3_NOVELTY=NARROW_GAP(保留)+ GATE=NEED_NEW_VERIFIER(UNRESOLVED 类)。
C3 不满足"gate 不是 FAIL"的原 CP4 条件,但 v2 证明其并非被证伪;
其命运取决于"定向 verifier"这一可证伪的研究问题本身。
