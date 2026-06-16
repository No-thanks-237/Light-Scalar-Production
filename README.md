# Light Scalars Production

基于论文 **"Light Scalars at FASER"** (Kling et al., JHEP 2023, [arXiv:2212.06186](https://arxiv.org/abs/2212.06186)) 的高能物理现象学计算程序。

计算 Type-I 双希格斯二重态模型 (2HDM) 中轻 CP-even 标量粒子 (Light H) 在各种介子衰变中的**产生分支比**。该程序数值实现了论文中的耦合修饰符公式和一环 QCD/电弱圈函数，支持在 $m_H$ 和 $\tan\beta$ 参数空间扫描，输出 CSV 数据表用于进一步分析和绘图。

## 项目结构

```
.
├── main.py                    # 主程序: 扫描 m_H 和 tanβ 参数空间, 输出 CSV
├── physics/                   # 物理计算模块
│   ├── __init__.py
│   ├── constants.py           # 物理常数、Benchmark 参数、介子数据
│   ├── form_factors.py        # 圈因子 A₀, A₁/₂, A₁ (附录 A)
│   ├── utils.py               # Källén λ 函数、相空间因子
│   ├── couplings.py           # 耦合修饰符 ξ (2HDM 耦合)
│   └── production.py          # 各产生道分支比
├── output/                    # 输出 CSV 目录
├── document/                  # 论文解析中间文件
├── "Light Scalars at FASER.pdf"  # 原始论文 (arXiv:2212.06186)
└── README.md
```

## Benchmark 参数

基于论文 **式 4.17** 的 Light H benchmark 场景:

- $\cos(\beta-\alpha) = 1/\tan\beta$
- $m_A = m_{H^\pm} = 600$ GeV (伪标量和带电 Higgs 质量)
- $\lambda v^2 = 0$ (理论约束)
- 大 $\tan\beta$ (弱耦合极限, Light H 长寿命)

## 耦合修饰符函数

耦合修饰符定义在 [physics/couplings.py](physics/couplings.py) 中，用于描述 Light H 与标准模型粒子的相对耦合强度。

| 函数 | 符号 | 物理含义 | 大 tanβ 行为 | 论文公式 |
|------|------|---------|-------------|---------|
| `cos_beta_minus_alpha(tanb)` | $\cos(\beta-\alpha)$ | Mixing 角度 | $\propto 1/\tan\beta$ | 式 4.17 |
| `xi_H_V(tanb)` | $\xi_H^V$ | 规范玻色子耦合 ($W/Z$) | $\propto 1/\tan\beta$ | 式 4.15 |
| `xi_H_f(tanb)` | $\xi_H^f$ | 费米子耦合 ($f\bar{f}H$) | $\propto 1/(2\tan^3\beta)$ | 式 4.16 |
| `xi_H_g(mH, tanb)` | $\xi_H^g$ | 有效胶子耦合 ($ggH$) | 圈级压制 | 式 2.2 |
| `xi_H_gamma(mH, tanb)` | $\xi_H^\gamma$ | 有效光子耦合 ($\gamma\gamma H$) | 圈级压制 | 式 2.3 + 4.4 |
| `xi_H_bs(mH, tanb)` | $\xi_H^{bs}$ | 味改变耦合 ($b\to s H$) | 圈级, top 主导 | 式 4.21, D.1-D.5 |
| `xi_H_ds(mH, tanb)` | $\xi_H^{ds}$ | 味改变耦合 ($d\to s H$) | 圈级, top 主导 | 式 4.21, D.1-D.5 |
| `xi_HH_sb(mH, tanb)` | $\xi_{HH}^{sb}$ | 双标量味改变 ($b\to s HH$) | 圈级 | 式 E.2-E.5 |
| `xi_HH_ds(mH, tanb)` | $\xi_{HH}^{ds}$ | 双标量味改变 ($d\to s HH$) | 圈级 | 式 E.2-E.5 |

### 辅助圈函数 (附录 A)

定义在 [physics/form_factors.py](physics/form_factors.py) 中。

| 函数 | 符号 | 物理含义 | 论文公式 |
|------|------|---------|---------|
| `A0_phi(tau)` | $A_0^\phi$ | 标量粒子圈因子 | 式 A.1 |
| `A_half_phi(tau)` | $A_{1/2}^\phi$ | 费米子圈因子 (CP-even) | 式 A.2 |
| `A1_phi(tau)` | $A_1^\phi$ | W 玻色子圈因子 | 式 A.3 |
| `A_half_A(tau)` | $A_{1/2}^A$ | 费米子圈因子 (CP-odd) | 式 A.5 |

### 味改变耦合辅助函数 (附录 D)

定义在 [physics/couplings.py](physics/couplings.py) 中，用于构建 $\xi_H^{ij}$。

| 函数 | 符号 | 含义 | 论文公式 |
|------|------|------|---------|
| `g0(x_k, x_Hp, cotb)` | $g_0$ | 标量型辅助函数 | 式 D.1 |
| `g1(x_k, x_Hp, cotb)` | $g_1$ | 矢量型辅助函数 | 式 D.2 |
| `g2(x_k, x_Hp, cotb)` | $g_2$ | 轴向型辅助函数 = $\cot\beta\cdot X_1 + \cot^3\beta\cdot X_2$ | 式 D.3 |
| `X1(x_k, x_Hp)` | $X_1$ | 1-loop 函数 | 式 D.4 |
| `X2(x_k, x_Hp)` | $X_2$ | 1-loop 函数 | 式 D.5 |

### 双标量味改变耦合辅助函数 (附录 E)

定义在 [physics/couplings.py](physics/couplings.py) 中，用于构建 $\xi_{HH}^{ij}$。

| 函数 | 符号 | 含义 | 论文公式 |
|------|------|------|---------|
| `f0_double(x_k, x_Hp)` | $f_0$ | 双标量辅助函数 | 式 E.3 |
| `f1_double(x_k, x_Hp)` | $f_1$ | 双标量辅助函数 | 式 E.4 |
| `f2_double(x_k, x_Hp)` | $f_2$ | 双标量辅助函数 | 式 E.5 |

## 产生道分支比函数

各产生道分支比定义在 [physics/production.py](physics/production.py) 中。计算 Light H 在各种介子衰变中的产生几率。

| 函数 | 产生过程 | 有效质量范围 | 所用耦合 | 论文公式 |
|------|---------|-------------|---------|---------|
| `Br_B_Xs_H(mH, tanb)` | $B \to X_s H$ | $m_H < m_B = 5.279\ \text{GeV}$ | $\xi_H^{bs}, V_{cb}$ | 式 2.5 |
| `Br_K_pi_H(mH, tanb)` | $K^\pm \to \pi^\pm H$ | $m_H < m_K - m_\pi = 0.354\ \text{GeV}$ | $\xi_H^V, \xi_H^{ds}$ | 式 2.7-2.8 |
| `Br_eta_pi_H(mH, tanb)` | $\eta \to \pi H$ | $m_H < m_\eta - m_\pi = 0.408\ \text{GeV}$ | $\xi_H^f, \xi_H^g$ | 式 2.9-2.10 |
| `Br_eta_prime_pi_H(mH, tanb)` | $\eta' \to \pi H$ | $m_H < m_{\eta'} - m_\pi = 0.818\ \text{GeV}$ | $\xi_H^f, \xi_H^g$ | 式 2.9-2.10 |
| `Br_semileptonic_pion(mH, tanb)` | $\pi \to H e \nu$ | $m_H < m_\pi = 0.140\ \text{GeV}$ | $\xi_H^V$ | 式 2.11 |
| `Br_semileptonic_kaon(mH, tanb)` | $K \to H e \nu$ | $m_H < m_K = 0.494\ \text{GeV}$ | $\xi_H^V$ | 式 2.11 |
| `Br_Upsilon_gamma_H(mH, tanb)` | $\Upsilon \to \gamma H$ | $m_H < m_\Upsilon = 9.460\ \text{GeV}$ | $\xi_H^f$ (b 夸克) | 式 2.12 |
| `Br_B_Xs_HH(mH, tanb)` | $B \to X_s HH$ | $2m_H < m_b \Rightarrow m_H < 2.092\ \text{GeV}$ | $\xi_{HH}^{sb}$ | 式 E.7-E.8 |
| `Br_K_pi_HH(mH, tanb)` | $K \to \pi HH$ | $2m_H < m_K - m_\pi \Rightarrow m_H < 0.177\ \text{GeV}$ | $\xi_{HH}^{ds}$ | 式 E.9-E.10 |

## 辅助函数

定义在 [physics/utils.py](physics/utils.py) 中。

| 函数 | 含义 | 公式 |
|------|------|------|
| `lambda_kallen(a, b, c)` | Källén 函数 $\lambda(a,b,c) = (a-b-c)^2 - 4bc$ | 运动学 |
| `phase_space_f(x)` | $B\to X_s$ 相空间因子, $x=m_c^2/m_b^2$ | 式 2.5 |
| `phase_space_f_double(x)` | 双标子相空间函数, $x=m_\phi/m_b$ | 式 E.8 |

## 输出说明

主程序 [main.py](main.py) 扫描 $m_H$ 和 $\tan\beta$ 参数空间，将计算结果输出到 `output/br_table.csv`。

每行包含:
- `m_H`: 轻 Higgs 质量 [GeV]
- `tanb`: $\tan\beta$
- `Br_B_Xs_H`, `Br_K_pi_H`, 等: 各产生道分支比
