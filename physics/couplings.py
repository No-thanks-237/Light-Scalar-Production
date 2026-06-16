"""
耦合修饰符 ξ 的计算, Type-I 2HDM Light H benchmark (式 4.17)
"""
import numpy as np
from . import constants as C
from .form_factors import A_half_phi, A1_phi, A0_phi


# ============================================================
# (a) 简单耦合
# ============================================================

# 式 4.17: cos(β-α) = 1/tanβ
def cos_beta_minus_alpha(tanb):
    return 1.0 / tanb


def sin_beta_minus_alpha(tanb):
    cba = cos_beta_minus_alpha(tanb)
    return np.sqrt(np.maximum(0.0, 1.0 - cba * cba))


# 式 4.15: ξ_H^V = cos(β-α)
def xi_H_V(tanb):
    return cos_beta_minus_alpha(tanb)


# 式 4.16: ξ_H^f = cos(β-α)(1 - sin(β-α)) ≈ 1/(2 tan³β)
def xi_H_f(tanb):
    cba = cos_beta_minus_alpha(tanb)
    sba = sin_beta_minus_alpha(tanb)
    return cba * (1.0 - sba)


# ============================================================
# (b) 间接耦合 (圈级)
# ============================================================

# 式 2.2: ξ_H^g = Σ_{f∈q} (3/2) ξ_H^f A_{1/2}(τ_f)
def xi_H_g(mH, tanb):
    xi_f = xi_H_f(tanb)
    result = 0.0
    for mf in [C.m_u, C.m_d, C.m_s, C.m_c, C.m_b, C.m_t]:
        tau = mH ** 2 / (4.0 * mf ** 2)
        result += (3.0 / 2.0) * xi_f * A_half_phi(tau)
    return result


# 式 C.5: λ_{HH+H-} (λv² = 0)
def lambda_H_Hp_Hm(mH, tanb):
    cba = cos_beta_minus_alpha(tanb)
    return -(1.0 / C.v) * (2.0 * C.m_Hp_bench ** 2 - mH ** 2) * cba


# 式 2.3 + 式 4.4: ξ_H^γ = fermion + W + H± 圈
def xi_H_gamma(mH, tanb):
    xi_f = xi_H_f(tanb)
    xi_V = xi_H_V(tanb)

    # 费米子圈
    fermion_sum = 0.0
    for mf, Nc, Qf in [(C.m_u, 3, 2.0/3.0), (C.m_d, 3, -1.0/3.0), (C.m_s, 3, -1.0/3.0),
                        (C.m_c, 3, 2.0/3.0), (C.m_b, 3, -1.0/3.0), (C.m_t, 3, 2.0/3.0),
                        (C.m_e, 1, -1.0), (C.m_mu, 1, -1.0), (C.m_tau, 1, -1.0)]:
        tau = mH ** 2 / (4.0 * mf ** 2)
        fermion_sum += Nc * Qf ** 2 * xi_f * A_half_phi(tau)

    # W 圈
    tau_W = mH ** 2 / (4.0 * C.mW ** 2)
    W_loop = xi_V * A1_phi(tau_W)

    # 带电 Higgs 圈 (式 4.4)
    tau_Hp = mH ** 2 / (4.0 * C.m_Hp_bench ** 2)
    lam = lambda_H_Hp_Hm(mH, tanb)
    Hp_loop = -(C.v * lam) / (2.0 * C.m_Hp_bench ** 2) * A0_phi(tau_Hp)

    return fermion_sum + W_loop + Hp_loop


# ============================================================
# (c) 味改变耦合 (式 4.21 + 附录 D)
# ============================================================

# 式 D.1: 辅助函数 g₀
def g0(x_k, x_Hp, cotb):
    if abs(x_k - x_Hp) < 1e-10:
        return -cotb ** 2 * (1.0 / (12.0 * x_k))
    return -cotb ** 2 * (3.0 * x_Hp ** 2 - 4.0 * x_Hp * x_k + x_k ** 2
                          - 2.0 * x_k * (2.0 * x_Hp - x_k) * np.log(x_Hp / x_k)) / (16.0 * (x_Hp - x_k) ** 3)


# 式 D.2: 辅助函数 g₁
def g1(x_k, x_Hp, cotb):
    if abs(x_k - x_Hp) < 1e-10:
        return -0.75 - cotb ** 2 * (5.0 / 12.0)
    term = cotb ** 2 * x_k * (5.0 * x_Hp ** 2 - 8.0 * x_Hp * x_k + 3.0 * x_k ** 2
                               - 2.0 * x_Hp * (2.0 * x_Hp - x_k) * np.log(x_Hp / x_k)) / (4.0 * (x_Hp - x_k) ** 3)
    return -0.75 + term


# 式 D.4: 辅助函数 X₁
def X1(x_k, x_Hp):
    if abs(x_k - x_Hp) < 1e-10:
        return 0.25 * (-0.5 + 6.0/((x_Hp - 1.0)**2) 
                       - 3.0*(1.0 + x_Hp)/((x_Hp - 1.0)**3) * np.log(x_Hp))
    if abs(x_k - 1.0) < 1e-10:
        num = (-7.0 + 16.0*x_Hp - 9.0*x_Hp**2 
               + 2.0*x_Hp*(-2.0 + 3.0*x_Hp)*np.log(x_Hp))
        return num / (8.0 * (x_Hp - 1.0)**2)
    term1 = x_Hp / (x_Hp - x_k) - 6.0 / ((x_k - 1.0) ** 2) + 3.0
    term2 = x_Hp * (3.0 * x_Hp - 2.0 * x_k) / ((x_Hp - x_k) ** 2) * np.log(x_Hp)
    term3 = (x_Hp * (3.0 * x_Hp - 2.0 * x_k) / ((x_Hp - x_k) ** 2)
             + 3.0 * (x_k + 1.0) / ((x_k - 1.0) ** 3)) * np.log(x_k)
    return -0.25 * (term1 - term2 + term3)


# 式 D.5: 辅助函数 X₂
def X2(x_k, x_Hp):
    if abs(x_k - x_Hp) < 1e-10:
        return -5.0 / 12.0
    term1 = x_k * (5.0 * x_Hp - 3.0 * x_k) / (4.0 * (x_Hp - x_k) ** 2)
    term2 = x_Hp * x_k * (2.0 * x_Hp - x_k) / (2.0 * (x_Hp - x_k) ** 3) * np.log(x_Hp / x_k)
    return term1 - term2


# 式 D.3: 辅助函数 g₂ = cotβ·X₁ + cot³β·X₂
def g2(x_k, x_Hp, cotb):
    return cotb * X1(x_k, x_Hp) + cotb ** 3 * X2(x_k, x_Hp)


# 式 4.21: ξ_H^{ij} 味改变耦合 (通用)
def xi_H_ij(mH, tanb, V_ki_list, V_kj_list, m_k_list):
    cba = cos_beta_minus_alpha(tanb)
    sba = sin_beta_minus_alpha(tanb)
    cotb = 1.0 / tanb

    x_Hp = C.m_Hp_bench ** 2 / C.mW ** 2
    lam = lambda_H_Hp_Hm(mH, tanb)

    prefactor = -4.0 * C.GF * np.sqrt(2.0) / (16.0 * np.pi ** 2)

    total = 0.0
    for V_ki_star, V_kj, mk in zip(V_ki_list, V_kj_list, m_k_list):
        x_k = mk ** 2 / C.mW ** 2
        inner = g1(x_k, x_Hp, cotb) * cba \
                - g2(x_k, x_Hp, cotb) * sba \
                - g0(x_k, x_Hp, cotb) * (2.0 * C.v / C.mW ** 2) * lam
        total += V_ki_star * mk ** 2 * inner * V_kj

    return prefactor * total


# ξ_H^{bs}: B → X_s H (top 主导)
def xi_H_bs(mH, tanb):
    return xi_H_ij(mH, tanb,
                   [C.V_ub, C.V_cb, C.V_tb],
                   [C.V_us, C.V_cs, C.V_ts],
                   [C.m_u, C.m_c, C.m_t])


# ξ_H^{ds}: K → π H
def xi_H_ds(mH, tanb):
    return xi_H_ij(mH, tanb,
                   [C.V_ud, C.V_cd, C.V_td],
                   [C.V_us, C.V_cs, C.V_ts],
                   [C.m_u, C.m_c, C.m_t])


# ============================================================
# (d) 双标量味改变耦合 (附录 E)
# ============================================================

# 式 E.3: 辅助函数 f₀
def f0_double(x_k, x_Hp):
    num = (6.0 * x_k ** 2 - x_k * x_Hp * (x_k ** 2 - 2.0 * x_k + 7.0)
           + 2.0 * x_Hp ** 2 * (x_k - 1.0) ** 2)
    return -num / ((x_k - 1.0) ** 2 * (x_Hp - x_k))


# 式 E.4: 辅助函数 f₁
def f1_double(x_k, x_Hp):
    num = (3.0 * x_k * (x_k + 1.0) - 2.0 * x_Hp * (x_k ** 3 - 3.0 * x_k ** 2 + 6.0 * x_k + 2.0)
           + 3.0 * x_Hp ** 2 * (x_k ** 2 - 3.0 * x_k + 4.0))
    return -num / ((x_k - 1.0) ** 3 * (x_Hp - x_k) ** 2)


# 式 E.5: 辅助函数 f₂
def f2_double(x_k, x_Hp):
    return x_Hp ** 2 * (2.0 * x_Hp - x_k) / ((x_Hp - x_k) ** 2)


# 式 E.2: ξ_{HH}^{ij} 双标量味改变耦合(通用)
def xi_HH_ij(mH, tanb, V_ki_list, V_kj_list, m_k_list):
    prefactor = C.GF * C.mW ** 2 * 4.0 * np.sqrt(2.0) / (64.0 * np.pi ** 2)
    x_Hp = C.m_Hp_bench ** 2 / C.mW ** 2

    total = 0.0
    for V_ki_star, V_kj, mk in zip(V_ki_list, V_kj_list, m_k_list):
        x_k = mk ** 2 / C.mW ** 2
        inner = f0_double(x_k, x_Hp) + f1_double(x_k, x_Hp) * np.log(x_k) + f2_double(x_k, x_Hp) * np.log(x_Hp)
        total += V_ki_star * inner * V_kj
    return prefactor * total


# ξ_{HH}^{sb}: B → X_s HH
def xi_HH_sb(mH, tanb):
    return xi_HH_ij(mH, tanb,
                    [C.V_ub, C.V_cb, C.V_tb],
                    [C.V_us, C.V_cs, C.V_ts],
                    [C.m_u, C.m_c, C.m_t])


# ξ_{HH}^{ds}: K → π HH
def xi_HH_ds(mH, tanb):
    return xi_HH_ij(mH, tanb,
                    [C.V_ud, C.V_cd, C.V_td],
                    [C.V_us, C.V_cs, C.V_ts],
                    [C.m_u, C.m_c, C.m_t])
