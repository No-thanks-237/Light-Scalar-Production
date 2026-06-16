#!/usr/bin/env python
"""
读取 output/br_table.csv，对每个产生道绘制 Br vs m_H 图。
"""

import csv
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    'font.size': 13,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'legend.fontsize': 11,
    'figure.dpi': 150,
})

OUTPUT_DIR = 'output'
CSV_PATH = os.path.join(OUTPUT_DIR, 'br_table.csv')

# 读取 CSV
with open(CSV_PATH) as f:
    reader = csv.DictReader(f)
    data = list(reader)

mH = np.array([float(r['m_H']) for r in data], dtype=float)
tanb = np.array([float(r['tanb']) for r in data], dtype=float)

# 列名 → 显示名
CHANNELS = [
    ('Br_B_Xs_H',       r'$B \to X_s H$'),
    ('Br_B_Xs_HH',      r'$B \to X_s HH$'),
    ('Br_K_pi_H',       r'$K^\pm \to \pi^\pm H$'),
    ('Br_K_pi_HH',      r'$K^\pm \to \pi^\pm HH$'),
    ('Br_eta_pi_H',     r'$\eta \to \pi H$'),
    ('Br_eta_prime_pi_H', r"$\eta' \to \pi H$"),
    ('Br_pi_semilep',   r'$\pi \to H e\nu$'),
    ('Br_K_semilep',    r'$K \to H e\nu$'),
    ('Br_Upsilon_gamma_H', r'$\Upsilon \to \gamma H$'),
]

# 替换零值以便在 log 轴上显示
def safe_br(vals):
    """将 0 替换为 NaN（不显示）或极小值"""
    a = np.array(vals, dtype=float)
    a[a <= 0] = np.nan
    return a

# ─────────────────────────────────────────────
# 图 1：所有道叠加在一张图上
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
for key, label in CHANNELS:
    br = safe_br([r[key] for r in data])
    ax.plot(mH, br, label=label, lw=1.5)

ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel(r'Branching Ratio')
ax.set_yscale('log')
ax.set_ylim(1e-30, 1e-2)
ax.legend(ncol=2, fontsize=10)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_all.png'))
print('Saved: output/br_all.png')

# ─────────────────────────────────────────────
# 图 2：3×3 子图，每个道单独一图
# ─────────────────────────────────────────────
fig, axes = plt.subplots(3, 3, figsize=(14, 10))
axes = axes.flatten()

for ax_i, (key, label) in enumerate(CHANNELS):
    ax = axes[ax_i]
    br = safe_br([r[key] for r in data])
    ax.semilogy(mH, br, lw=1.5)
    ax.set_xlabel(r'$m_H$ [GeV]')
    ax.set_ylabel('Br')
    ax.set_title(label, fontsize=12)
    ax.grid(True, alpha=0.3)
    # 统一 y 范围
    ax.set_ylim(1e-30, 1e-2)

fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_panels.png'))
print('Saved: output/br_panels.png')

# ─────────────────────────────────────────────
# 图 3：B 介子道单独（最重要的道）
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
for key, label in [
    ('Br_B_Xs_H',  r'$B \to X_s H$'),
    ('Br_B_Xs_HH', r'$B \to X_s HH$'),
]:
    br = safe_br([r[key] for r in data])
    ax.semilogy(mH, br, label=label, lw=1.5)

ax.axvline(4.183, color='gray', ls='--', lw=0.8, alpha=0.5, label=r'$m_b$')
ax.axvline(5.279, color='gray', ls=':',  lw=0.8, alpha=0.5, label=r'$m_B$')
ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel('Branching Ratio')
ax.set_title(r'$B$ meson channels')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_B.png'))
print('Saved: output/br_B.png')

# ─────────────────────────────────────────────
# 图 4：介子道单独（K, η, π 等低质量区）
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
for key, label in [
    ('Br_K_pi_H',        r'$K^\pm \to \pi^\pm H$'),
    ('Br_K_pi_HH',       r'$K^\pm \to \pi^\pm HH$'),
    ('Br_K_semilep',     r'$K \to H e\nu$'),
    ('Br_eta_pi_H',      r'$\eta \to \pi H$'),
    ('Br_eta_prime_pi_H', r"$\eta' \to \pi H$"),
    ('Br_pi_semilep',    r'$\pi \to H e\nu$'),
]:
    br = safe_br([r[key] for r in data])
    ax.semilogy(mH, br, label=label, lw=1.5)

# 标记关键阈值
for x, name in [(0.140, r'$m_\pi$'), (0.354, r'$m_K-m_\pi$'),
                (0.494, r'$m_K$'), (0.408, r'$m_\eta-m_\pi$'),
                (0.818, r"$m_{\eta'}-m_\pi$")]:
    ax.axvline(x, color='gray', ls='--', lw=0.6, alpha=0.4)

ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel('Branching Ratio')
ax.set_title('Meson channels')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_meson.png'))
print('Saved: output/br_meson.png')

# ─────────────────────────────────────────────
# 图 5：Upsilon 道单独
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
br = safe_br([r['Br_Upsilon_gamma_H'] for r in data])
ax.semilogy(mH, br, lw=1.5, label=r'$\Upsilon \to \gamma H$')
ax.axvline(9.46, color='gray', ls='--', lw=0.8, alpha=0.5, label=r'$m_\Upsilon$')
ax.set_xlabel(r'$m_H$ [GeV]')
ax.set_ylabel('Branching Ratio')
ax.set_title(r'$\Upsilon(1S)$ channel')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'br_Upsilon.png'))
print('Saved: output/br_Upsilon.png')

plt.close('all')
print('All plots saved.')
