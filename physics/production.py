"""
Light H 的各产生道分支比, Type-I 2HDM Light H benchmark
"""
import numpy as np
from . import constants as C
from . import couplings as coup
from . import utils as U


# 式 2.5: B → X_s H
def Br_B_Xs_H(mH, tanb):
    if mH > C.m_B:
        return 0.0
    xi_bs = coup.xi_H_bs(mH, tanb)
    f_ps = U.phase_space_f(C.m_c ** 2 / C.m_b ** 2)

    ratio = (12.0 * np.pi ** 2 * C.v ** 2 / C.m_b ** 2) \
            * (1.0 - mH ** 2 / C.m_B ** 2) ** 2 \
            * (1.0 / f_ps) \
            * abs(xi_bs / C.V_cb) ** 2
    return C.Br_B_Xc_e_nu * ratio


# 式 2.7-2.8: K± → π± H
def Br_K_pi_H(mH, tanb):
    if mH > C.m_K - C.m_pi:
        return 0.0

    xi_W = coup.xi_H_V(tanb)
    xi_ds = coup.xi_H_ds(mH, tanb)
    lam = 3.1e-7
    A_K = 0.0
    f0_Kpi = 0.96

    M1 = C.GF ** 0.5 * (2.0 ** 0.25) * xi_W * (
        7.0 * lam * (C.m_K ** 2 + C.m_pi ** 2 - mH ** 2) / 18.0
        - 7.0 * A_K * C.m_K ** 2 / 9.0
    )
    M2 = (xi_ds / (2.0 * C.v)) * C.m_s * (C.m_K ** 2 - C.m_pi ** 2) / (C.m_s - C.m_d) * f0_Kpi
    M_total = M1 + M2

    lambda_val = U.lambda_kallen(C.m_K ** 2, C.m_pi ** 2, mH ** 2)
    if lambda_val <= 0:
        return 0.0
    p_phi0 = np.sqrt(lambda_val) / (2.0 * C.m_K)

    return (1.0 / C.Gamma_Kaon) * (2.0 * p_phi0 / C.m_K) * (abs(M_total) ** 2) / (16.0 * np.pi * C.m_K)


# 式 2.10: g_{φηπ} 耦合 (内部辅助函数)
def _g_phi_eta_pi(mH, tanb, c_coeff):
    xi_f = coup.xi_H_f(tanb)
    xi_g = coup.xi_H_g(mH, tanb)
    B_tilde = C.m_pi ** 2 / (C.m_u + C.m_d)
    heavy_term = (2.0 / 9.0) * (C.m_u - C.m_d) * (xi_g+3.0*xi_f)
    g = -(1.0 / C.v) * (C.m_u * xi_f - C.m_d * xi_f + heavy_term) * c_coeff * B_tilde
    return g.real


# 式 2.9: η → π H
def Br_eta_pi_H(mH, tanb):
    if mH > C.m_eta - C.m_pi:
        return 0.0

    theta_eta = -13.0 * np.pi / 180.0
    c_coeff = (np.cos(theta_eta) - np.sqrt(2.0) * np.sin(theta_eta)) / np.sqrt(3.0)
    g_val = _g_phi_eta_pi(mH, tanb, c_coeff)

    lambda_val = U.lambda_kallen(C.m_eta ** 2, C.m_pi ** 2, mH ** 2)
    if lambda_val <= 0:
        return 0.0
    p_phi0 = np.sqrt(lambda_val) / (2.0 * C.m_eta)

    return (1.0 / C.Gamma_eta) * (2.0 * p_phi0 / C.m_eta) * (abs(g_val) ** 2) / (16.0 * np.pi * C.m_eta)


# 式 2.9: η′ → π H
def Br_eta_prime_pi_H(mH, tanb):
    if mH > C.m_eta_prime - C.m_pi:
        return 0.0

    theta_eta = -13.0 * np.pi / 180.0
    c_coeff = (np.cos(theta_eta) + np.sqrt(2.0) * np.sin(theta_eta)) / np.sqrt(3.0)
    g_val = _g_phi_eta_pi(mH, tanb, c_coeff)

    lambda_val = U.lambda_kallen(C.m_eta_prime ** 2, C.m_pi ** 2, mH ** 2)
    if lambda_val <= 0:
        return 0.0
    p_phi0 = np.sqrt(lambda_val) / (2.0 * C.m_eta_prime)

    return (1.0 / C.Gamma_eta_prime) * (2.0 * p_phi0 / C.m_eta_prime) * (abs(g_val) ** 2) / (16.0 * np.pi * C.m_eta_prime)


# 式 2.11: π → H e ν 半轻衰变
def Br_semileptonic_pion(mH, tanb):
    if mH > C.m_pi:
        return 0.0
    xi_W = coup.xi_H_V(tanb)
    x = mH ** 2 / C.m_pi ** 2
    f_x = U.phase_space_f(x)

    return (np.sqrt(2.0) * C.GF * C.m_pi ** 4 * abs(xi_W) ** 2
            / (96.0 * np.pi ** 2 * C.m_mu ** 2 * (1.0 - C.m_mu ** 2 / C.m_pi ** 2) ** 2)) \
           * 0.9999 * f_x * (1.0 - 2.0 * 3.0 / (33.0 - 2.0 * 3.0)) ** 2


# 式 2.11: K → H e ν 半轻衰变
def Br_semileptonic_kaon(mH, tanb):
    if mH > C.m_K:
        return 0.0
    xi_W = coup.xi_H_V(tanb)
    x = mH ** 2 / C.m_K ** 2
    f_x = U.phase_space_f(x)

    return (np.sqrt(2.0) * C.GF * C.m_K ** 4 * abs(xi_W) ** 2
            / (96.0 * np.pi ** 2 * C.m_mu ** 2 * (1.0 - C.m_mu ** 2 / C.m_K ** 2) ** 2)) \
           * 0.6356 * f_x * (1.0 - 2.0 * 3.0 / (33.0 - 2.0 * 3.0)) ** 2


# 式 2.12: Υ → γ H
def Br_Upsilon_gamma_H(mH, tanb):
    if mH > C.m_Upsilon:
        return 0.0
    xi_b = coup.xi_H_f(tanb)
    ratio = (C.GF * C.m_b ** 2 * abs(xi_b) ** 2 / (np.sqrt(2.0) * np.pi * C.alpha_ew)) \
            * (1.0 - mH ** 2 / C.m_Upsilon ** 2) \
            * (2.0 / 3.0) * (1.0 - mH ** 6 / C.m_Upsilon ** 6)
    return 0.0238 * ratio


# 式 E.7-E.8: B → X_s HH (双标量)
def Br_B_Xs_HH(mH, tanb):
    if mH * 2 > C.m_b:
        return 0.0
    xi = coup.xi_HH_sb(mH, tanb)
    x = mH / C.m_b
    if x <= 0.0 or x > 0.5:
        return 0.0
    f_double = U.phase_space_f_double(x)
    Gamma = abs(xi) ** 2 * C.m_b ** 5 / (64.0 * np.pi ** 3 * C.v ** 4) * f_double
    return Gamma / C.Gamma_B


# 式 E.9-E.10: K → π HH (双标量, 对 q² 数值积分)
def Br_K_pi_HH(mH, tanb):
    if mH * 2 > C.m_K - C.m_pi:
        return 0.0
    
    xi = coup.xi_HH_ds(mH, tanb)
    f0_Kpi = 0.96

    q2_min = 4.0 * mH ** 2
    q2_max = (C.m_K - C.m_pi) ** 2
    if q2_min >= q2_max:
        return 0.0

    def integrand(q2):
        M_amp = (xi / C.v ** 2) * C.m_s * (C.m_K ** 2 - C.m_pi ** 2) / (C.m_s - C.m_d) * f0_Kpi
        lam = U.lambda_kallen(C.m_K ** 2, C.m_pi ** 2, q2)
        if lam <= 0 or q2 <= 4.0 * mH ** 2:
            return 0.0
        return (abs(M_amp) ** 2) * np.sqrt(1.0 - 4.0 * mH ** 2 / q2) * np.sqrt(lam)

    # 自适应梯形积分
    n_steps = max(100, int(np.sqrt(q2_max / q2_min) * 50))
    q2_vals = np.logspace(np.log10(q2_min), np.log10(q2_max), n_steps)
    f_vals = np.array([integrand(q) for q in q2_vals])
    integral = np.trapezoid(f_vals, q2_vals)

    return (1.0 / (512.0 * np.pi ** 3 * C.m_K ** 3 * C.Gamma_Kaon)) * integral


# 汇总所有产生道
def total_production(mH, tanb):
    result = {
        'm_H': mH,
        'tanb': tanb,
        'Br_B_Xs_H': Br_B_Xs_H(mH, tanb),
        'Br_K_pi_H': Br_K_pi_H(mH, tanb),
        'Br_eta_pi_H': Br_eta_pi_H(mH, tanb),
        'Br_eta_prime_pi_H': Br_eta_prime_pi_H(mH, tanb),
        'Br_pi_semilep': Br_semileptonic_pion(mH, tanb),
        'Br_K_semilep': Br_semileptonic_kaon(mH, tanb),
        'Br_Upsilon_gamma_H': Br_Upsilon_gamma_H(mH, tanb),
        'Br_B_Xs_HH': Br_B_Xs_HH(mH, tanb),
        'Br_K_pi_HH': Br_K_pi_HH(mH, tanb),
    }
    result['total'] = sum(v for k, v in result.items() if k not in ('m_H', 'tanb'))
    return result
