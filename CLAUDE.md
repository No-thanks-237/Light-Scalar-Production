# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

高能物理现象学研究项目，基于论文 "Light Scalars at FASER" (Kling et al., JHEP 2023, arXiv:2212.06186)。目标是编写 Python 程序计算 Type-I 2HDM 中轻 CP-even 标量粒子 (Light H) 的产生和衰变分支比。

## 论文关键信息

### 模型: Type-I 2HDM, 大 tanβ 区域

**Benchmark 场景 (Light H, eq 4.17):**
- $\cos(\beta-\alpha) = 1/\tan\beta$
- $m_A = m_{H^\pm} = 600$ GeV
- $\lambda v^2 = 0$ (理论约束)
- 大 $\tan\beta$ (弱耦合, 长寿命)

### 耦合修饰符 (Type-I 2HDM, 大 tanβ)

| 耦合 | 表达式 | 大 tanβ 行为 |
|------|--------|-------------|
| $\xi_H^f$ (费米子, 式 4.16) | $\cos(\beta-\alpha)(1-\sin(\beta-\alpha))$ | $\propto 1/(2\tan^3\beta)$ |
| $\xi_H^V$ (规范玻色子, 式 4.15) | $\cos(\beta-\alpha)$ | $\propto 1/\tan\beta$ |
| $\xi_A^f$ (赝标量费米子, 式 4.14) | $\cot\beta$ (u), $-\cot\beta$ (d,e) | $\propto 1/\tan\beta$ |
| $\xi_H^g$ (胶子, 式 2.2) | $\sum_f \frac{3}{2}\xi_H^f \mathcal{A}_{1/2}^\phi(\tau_f^\phi)$ | 圈级 |
| $\xi_H^\gamma$ (光子, 式 2.3) | $\sum_f N_c Q_f^2 \xi_H^f \mathcal{A}_{1/2}^\phi + \xi_H^V \mathcal{A}_1^\phi + $ 带电 Higgs 贡献 (式 4.4) | 圈级 |
| $\xi_H^{ij}$ (味改变, 式 4.21) | 圈级通过 $H^\pm$ 和 W 圈 | 复杂 |

### 产生渠道 (Production)

| 过程 | 公式 | 质量范围 | 主要依赖 |
|------|------|---------|---------|
| $B \to X_s H$ | 式 2.5 | $m_H < m_B$ | $\xi_H^{bs}$ |
| $K^\pm \to \pi^\pm H$ | 式 2.7-2.8 | $m_H < m_K$ | $\xi_H^W$, $\xi_H^{ds}$ |
| $\eta^{(\prime)} \to \pi H$ | 式 2.9-2.10 | $m_H < m_\eta$ | $\xi_H^{u,d}$, $\xi_H^g$ |
| 半轻衰变 $X \to H e\nu$ | 式 2.11 | $m_H < m_X$ | $\xi_H^W$ |
| $\Upsilon \to \gamma H$ | 式 2.12 | $m_H < m_\Upsilon$ | $\xi_H^b$ |

## 程序目标

计算 Light H **产生**的各衰变道分支比，即介子衰变产生 H 的几率。

## 关键特征 (大 tanβ, Light H)
- $B \to X_s H$ 是主要产生渠道（$m_H$ 接近 $m_B$ 时仍有效）
- $K^\pm \to \pi^\pm H$ 在低质量区重要
- 所有产生道耦合受 $\propto 1/\tan\beta$ 或更强压制

## 程序结构

```
.
├── main.py                  # 主程序: 扫描参数空间输出 CSV
├── physics/                 # 物理计算模块
│   ├── __init__.py
│   ├── constants.py         # 物理常数、benchmark 参数
│   ├── form_factors.py      # 圈因子 A₀, A₁/₂, A₁ (附录 A)
│   ├── utils.py             # 相空间因子、Källén λ 函数
│   ├── couplings.py         # 耦合修饰符 ξ (式 2.2, 2.3, 4.4, 4.15, 4.16, 4.21, D.1-D.5, E.2-E.5)
│   └── production.py        # 各产生道分支比 (式 2.5, 2.7-2.8, 2.9-2.10, 2.11, 2.12, E.7, E.9)
└── output/                  # 输出 CSV 目录
```

## 物理常数

参考 PDG 值:
- $v = 246$ GeV
- $m_W = 80.377$ GeV, $m_Z = 91.1876$ GeV
- $m_b = 4.18$ GeV, $m_c = 1.3$ GeV, $m_s = 95$ MeV
- $m_u = 2.16$ MeV, $m_d = 4.67$ MeV
- $m_\mu = 105.66$ MeV, $m_\tau = 1.77686$ GeV
- $G_F = 1.1663787 \times 10^{-5}$ GeV$^{-2}$
- $\alpha_s(m_Z) = 0.1179$, $\alpha_{\rm ew} = 1/127.95$
- $m_K = 493.677$ MeV, $m_\pi = 139.57$ MeV, $f_\pi = 93$ MeV
- $m_B = 5.279$ GeV, $m_\Upsilon = 9.46$ GeV
- $\sin^2\theta_W = 0.2312$
