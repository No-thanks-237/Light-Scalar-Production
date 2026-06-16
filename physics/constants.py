#物理常数和 benchmark 模型参数

import numpy as np

# ===== 基本物理常数 =====
v = 246.0  # Higgs VEV [GeV]
GF = 1.1663787e-5  # Fermi 常数 [GeV^-2]
alpha_ew = 1.0 / 127.95  # 精细结构常数
alpha_s_MZ = 0.1180  # α_s(m_Z)
sin2_theta_W = 0.2312  # sin²θ_W
mW = 80.377  # W 质量 [GeV]
mZ = 91.1876  # Z 质量 [GeV]

# ===== 费米子质量 [GeV] =====
m_u = 0.00216
m_d = 0.00470
m_s = 0.0935
m_c = 1.273
m_b = 4.183
m_t = 172.69
m_e = 0.000511
m_mu = 0.10566
m_tau = 1.77693

# ===== 介子质量 [GeV] =====
m_pi = 0.13957  # π±
m_pi0 = 0.13498
m_K = 0.493677  # K±
m_K0 = 0.497614
m_eta = 0.54786
m_eta_prime = 0.95778
m_B = 5.279  # B±
m_B0 = 5.280
m_D = 1.86484  # D0
m_Upsilon = 9.46
m_Jpsi = 3.0969

f_pi = 0.0922  # 衰变常数 [GeV] (PDG 130.2 MeV / √2)

# ===== Benchmark 参数 (Light H, 式 4.17) =====
m_A_bench = 600.0  # [GeV]
m_Hp_bench = 600.0  # 带电 Higgs 质量 [GeV]
lambda_v2 = 0.0  # λv² ≡ m_H² - m₁₂²/(sinβ cosβ) = 0

# 介子衰变分支比 (PDG)
Br_B_Xc_e_nu = 0.104  # Br(B → X_c e ν), 对 B0 和 B±
Br_Upsilon_ee = 0.0252  # Br(Υ(1S) → e⁺e⁻)

# 介子全宽度 [GeV]
# τ_B ~ 1.519e-12 s → Γ = ħ/τ
hbar = 6.582119569e-22  # GeV·s
Gamma_Kaon = hbar / 1.2380e-8  # Γ_{K±}, τ = 1.2380e-8 s
Gamma_eta = 1.31e-6  # Γ_η = 1.31 keV
Gamma_eta_prime = 0.188e-3  # Γ_η' = 0.188 MeV (PDG 2024)
Gamma_Upsilon = 54.02e-6  # Γ_Υ(1S) = 54.02 keV
Gamma_B = hbar / 1.519e-12  # Γ_B, τ ~ 1.519e-12 s (B0)

# CKM 矩阵元 (Wolfenstein 参数化)
V_ud = 0.97435
V_us = 0.2250
V_ub = 0.00373
V_cd = 0.2250
V_cs = 0.9735
V_cb = 0.0418
V_td = 0.0086
V_ts = 0.0415
V_tb = 1.0  # ~1
