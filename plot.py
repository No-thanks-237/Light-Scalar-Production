#!/usr/bin/env python
"""
扫描 m_H 并实时计算各产生道的 Br，绘制分支比曲线。
Upsilon 单独成图，不纳入总分支比。
"""
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from physics.production import (
    Br_B_Xs_H, Br_B_Xs_HH,
    Br_K_pi_H, Br_K_pi_HH,
    Br_eta_pi_H, Br_eta_prime_pi_H,
    Br_semileptonic_pion, Br_semileptonic_kaon,
    Br_Upsilon_gamma_H,
)
from physics import constants as C

matplotlib.rcParams.update({
    'font.size': 13,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'legend.fontsize': 11,
    'figure.dpi': 150,
})

OUTPUT_DIR = 'output'
TANB = 1000.0  # 大 tanβ benchmark

# 扫描 m_H 范围 (GeV)
mH_vals = np.linspace(0.01, 10.0, 500)

# 计算各道 Br
channels = [
    ('Br_B_Xs_H',       r'$B \to X_s H$',       lambda m: Br_B_Xs_H(m, TANB)),
    ('Br_B_Xs_HH',      r'$B \to X_s HH$',      lambda m: Br_B_Xs_HH(m, TANB)),
    ('Br_K_pi_H',       r'$K^\pm \to \pi^\pm H$', lambda m: Br_K_pi_H(m, TANB)),
    ('Br_K_pi_HH',      r'$K^\pm \to \pi^\pm HH$', lambda m: Br_K_pi_HH(m, TANB)),
    ('Br_eta_pi_H',     r'$\eta \to \pi H$',    lambda m: Br_eta_pi_H(m, TANB)),
    ('Br_eta_prime_pi_H', r"$\eta' \to \pi H$", lambda m: Br_eta_prime_pi_H(m, TANB)),
    ('Br_pi_semilep',   r'$\pi \to H e\nu$',    lambda m: Br_semileptonic_pion(m, TANB)),
    ('Br_K_semilep',    r'$K \to H e\nu$',      lambda m: Br_semileptonic_kaon(m, TANB)),
    ('Br_Upsilon_gamma_H', r'$\Upsilon \to \gamma H$', lambda m: Br_Upsilon_gamma_H(m, TANB)),
]

# 计算并存储
data = {key: np.array([func(m) for m in mH_vals], dtype=float) for key, _, func in channels}

# 排除 Upsilon 计算总分支比
keys_for_total = [k for k, _, _ in channels if k != 'Br_Upsilon_gamma_H']
total_br = sum(data[k] for k in keys_for_total)

# 将 <= 0 的值变为 NaN (log 轴上不显示)
def safe_br(arr):
    a = arr.copy()
    a[a <= 0] = np.nan
    return a

# ─────────────────────────────────────────────
# 图 1：所有道(不含 Upsilon) + 总分支比
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6.5))

for key, label, _ in channels:
    if key == 'Br_Upsilon_gamma_H':
        continue
    ax.plot(mH_vals, safe_br(data[key]), label=label, lw=1.5)

# 总分支比（虚线、加粗）
ax.plot(mH_vals, safe_br(total_br), label=r'Total (excl. $\Upsilon$)', lw=2.5,
        ls='--', color='black', alpha=0.8)

ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel(r'Branching Ratio')
ax.set_yscale('log')
ax.set_ylim(1e-30, 1)
ax.legend(ncol=2, fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_all.png'))
print('Saved: output/br_all.png')

# ─────────────────────────────────────────────
# 图 2：3×3 子图，每个道单独一图（含 Upsilon）
# ─────────────────────────────────────────────
fig, axes = plt.subplots(3, 3, figsize=(14, 10))
axes = axes.flatten()

for ax_i, (key, label, _) in enumerate(channels):
    ax = axes[ax_i]
    ax.semilogy(mH_vals, safe_br(data[key]), lw=1.5)
    ax.set_xlabel(r'$m_H$ [GeV]')
    ax.set_ylabel('Br')
    ax.set_title(label, fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(1e-30, 1e-2)

fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_panels.png'))
print('Saved: output/br_panels.png')

# ─────────────────────────────────────────────
# 图 3：B 介子道
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
for key, label, _ in channels:
    if 'B_' not in key:
        continue
    ax.semilogy(mH_vals, safe_br(data[key]), label=label, lw=1.5)

ax.axvline(C.m_b, color='gray', ls='--', lw=0.8, alpha=0.5, label=r'$m_b$')
ax.axvline(C.m_B, color='gray', ls=':',  lw=0.8, alpha=0.5, label=r'$m_B$')
ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel('Branching Ratio')
ax.set_title(r'$B$ meson channels')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_B.png'))
print('Saved: output/br_B.png')

# ─────────────────────────────────────────────
# 图 4：介子道 (K, η, π)
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
for key, label, _ in channels:
    if 'B_' in key or 'Upsilon' in key:
        continue
    ax.semilogy(mH_vals, safe_br(data[key]), label=label, lw=1.5)

for x, name in [(0.140, r'$m_\pi$'), (0.354, r'$m_K-m_\pi$'),
                (0.494, r'$m_K$'), (0.408, r'$m_\eta-m_\pi$'),
                (0.818, r"$m_{\eta'}-m_\pi$")]:
    ax.axvline(x, color='gray', ls='--', lw=0.6, alpha=0.4)

ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel('Branching Ratio')
ax.set_title(r'Meson channels (excl. $B$, $\Upsilon$)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_meson.png'))
print('Saved: output/br_meson.png')

# ─────────────────────────────────────────────
# 图 5：Upsilon 道单独
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(mH_vals, safe_br(data['Br_Upsilon_gamma_H']), lw=1.5,
            label=r'$\Upsilon \to \gamma H$')
ax.axvline(C.m_Upsilon, color='gray', ls='--', lw=0.8, alpha=0.5, label=r'$m_\Upsilon$')
ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel('Branching Ratio')
ax.set_title(r'$\Upsilon(1S)$ channel (excluded from Total)')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_Upsilon.png'))
print('Saved: output/br_Upsilon.png')

plt.close('all')
print('All plots saved.')
