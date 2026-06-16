"""
式 A.1-A.4: 圈因子 A₀, A₁/₂, A₁ 用于 CP-even 标量的 gg 和 γγ 有效耦合
"""
import numpy as np


# 式 A.4: fτ 函数, τ = m²φ / (4m²i)
def f_tau(tau):
    if tau <= 1:
        return np.arcsin(np.sqrt(tau)) ** 2
    arg = (1.0 + np.sqrt(1.0 - 1.0 / tau)) / (1.0 - np.sqrt(1.0 - 1.0 / tau))
    return -0.25 * (np.log(arg) - 1j * np.pi) ** 2


# 式 A.1: 标量粒子圈因子
def A0_phi(tau):
    return -0.5 * (tau - f_tau(tau)) / tau ** 2


# 式 A.2: 费米子圈因子 (CP-even)
def A_half_phi(tau):
    return (tau + (tau - 1.0) * f_tau(tau)) / tau ** 2


# 式 A.3: W 玻色子圈因子 (CP-even)
def A1_phi(tau):
    return -0.5 * (2.0 * tau ** 2 + 3.0 * tau + 3.0 * (2.0 * tau - 1.0) * f_tau(tau)) / tau ** 2


# 式 A.5: 费米子圈因子 (CP-odd)
def A_half_A(tau):
    return 2.0 / tau * f_tau(tau)
