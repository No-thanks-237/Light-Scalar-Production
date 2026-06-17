#!/usr/bin/env python
"""
绘制本程序 (tanb=1) 与 SensCalc 数据 (theta=1) 的对比图。
只对两个数据都有的衰变道进行绘图。
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from physics.production import (
    Br_B_Xs_H, Br_K_pi_H, Br_Upsilon_gamma_H, Br_B_Xs_HH
)

plt.rcParams.update({
    'font.size': 13,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'legend.fontsize': 11,
    'figure.dpi': 150,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output2')
os.makedirs(OUT_DIR, exist_ok=True)

TANB = 1.0

# ========== 1. 生成我们的数据 (tanb=1) ==========
print("生成本程序数据 (tanb=1)...")

# B → X_s S: mH in [0, 5.5] GeV, 匹配 SensCalc 范围
mH_BXs = np.linspace(0.001, 5.5, 300)
our_B_Xs = np.array([Br_B_Xs_H(m, TANB) for m in mH_BXs])

# K → π S: mH in [0, m_K - m_pi]
mH_Kpi = np.linspace(0.001, 0.493677 - 0.13957, 300)
our_K_pi = np.array([Br_K_pi_H(m, TANB) for m in mH_Kpi])

# Υ → γ S: mH in [0, 9.46] GeV
mH_Ups = np.linspace(0.001, 9.46, 500)
our_Ups_gamma_H = np.array([Br_Upsilon_gamma_H(m, TANB) for m in mH_Ups])

# B → X_s SS: mH in [0, 5.5/2] GeV (因为产生两个标量)
mH_BXss = np.linspace(0.001, 2.75, 300)
our_B_Xs_HH = np.array([Br_B_Xs_HH(m, TANB) for m in mH_BXss])

# ========== 2. 读取 SensCalc 数据 ==========
print("读取 SensCalc 数据...")

def read_senscalc_2col(filepath):
    """读取 SensCalc 两列数据: mH, BR"""
    data = np.loadtxt(filepath)
    return data[:, 0], data[:, 1]

# B → X_s S (总)
mH_sc_BXs, br_sc_BXs = read_senscalc_2col(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_from_senscalc', 'BtoXsStotal.dat'))

# K^+ → π^+ S
mH_sc_Kpi, br_sc_Kpi = read_senscalc_2col(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_from_senscalc', 'KplustoPiS.dat'))

# Υ → γ S
mH_sc_Ups, br_sc_Ups = read_senscalc_2col(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_from_senscalc', 'UpsilonToSgamma.dat'))

# B → X_s SS (总)
mH_sc_BXss, br_sc_BXss = read_senscalc_2col(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_from_senscalc', 'BplustoXsSStotal.dat'))

# ========== 3. 定义绘图函数 ==========
def plot_channel(ax, mH_our, br_our, label_our, mH_sc, br_sc, label_sc, xlabel, ylabel, title, xlim=None):
    """在给定轴上绘制对比图"""
    # SensCalc 数据
    ax.plot(mH_sc, br_sc, '-', color='#E24A33', linewidth=1.8,
            label=label_sc, zorder=3)
    # 我们的数据
    ax.plot(mH_our, br_our, '--', color='#348ABD', linewidth=1.8,
            label=label_our, zorder=3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if xlim is not None:
        ax.set_xlim(xlim)
    ax.legend()
    ax.grid(True, alpha=0.3)
    # 只有在数值都为正时才用 log scale
    if np.any(br_our > 0) and np.any(br_sc > 0):
        ax.set_yscale('log')

def ratio_plot(ax, mH_our, br_our, mH_sc, br_sc, ratio_label='Our / SensCalc'):
    """绘制比率图 (插值我们的数据到 SensCalc 的 mH 点上)"""
    br_our_interp = np.interp(mH_sc, mH_our, br_our, left=np.nan, right=np.nan)
    ratio = np.where((br_sc > 0) & (br_our_interp > 0),
                     br_our_interp / br_sc, np.nan)
    ax.plot(mH_sc, ratio, '-', color='#555555', linewidth=1.2)
    ax.axhline(1.0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_xlabel(r'$m_H$ [GeV]')
    ax.set_ylabel('Ratio')
    ax.set_title(ratio_label)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)

# ========== 4. 绘制对比图 ==========
print("绘制对比图...")

pair_to_save = []

# --- (a) B → X_s S ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
plot_channel(ax1, mH_BXs, our_B_Xs, r'This work ($\tan\beta=1$)',
             mH_sc_BXs, br_sc_BXs, r'SensCalc ($\theta=1$)',
             '', 'BR', r'$B \to X_s H$')
ratio_plot(ax2, mH_BXs, our_B_Xs, mH_sc_BXs, br_sc_BXs, 'Ratio')
ax2.set_xlabel(r'$m_H$ [GeV]')
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'compare_B_Xs_H.png'), bbox_inches='tight')
plt.close(fig)
print("  [OK] B -> X_s H")

# --- (b) K^+ → π^+ S ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
plot_channel(ax1, mH_Kpi, our_K_pi, r'This work ($\tan\beta=1$)',
             mH_sc_Kpi, br_sc_Kpi, r'SensCalc ($\theta=1$)',
             '', 'BR', r'$K^+ \to \pi^+ H$', xlim=(0, 0.36))
ratio_plot(ax2, mH_Kpi, our_K_pi, mH_sc_Kpi, br_sc_Kpi, 'Ratio')
ax2.set_xlabel(r'$m_H$ [GeV]')
ax2.set_xlim(0, 0.36)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'compare_K_pi_H.png'), bbox_inches='tight')
plt.close(fig)
print("  [OK] K+ -> pi+ H")

# --- (c) Υ → γ S ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
plot_channel(ax1, mH_Ups, our_Ups_gamma_H, r'This work ($\tan\beta=1$)',
             mH_sc_Ups, br_sc_Ups, r'SensCalc ($\theta=1$)',
             '', 'BR', r'$\Upsilon \to \gamma H$')
ratio_plot(ax2, mH_Ups, our_Ups_gamma_H, mH_sc_Ups, br_sc_Ups, 'Ratio')
ax2.set_xlabel(r'$m_H$ [GeV]')
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'compare_Upsilon_gamma_H.png'), bbox_inches='tight')
plt.close(fig)
print("  [OK] Upsilon -> gamma H")

# --- (d) B → X_s SS ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
plot_channel(ax1, mH_BXss, our_B_Xs_HH, r'This work ($\tan\beta=1$)',
             mH_sc_BXss, br_sc_BXss, r'SensCalc ($\theta=1$)',
             '', 'BR', r'$B \to X_s HH$')
ratio_plot(ax2, mH_BXss, our_B_Xs_HH, mH_sc_BXss, br_sc_BXss, 'Ratio')
ax2.set_xlabel(r'$m_H$ [GeV]')
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'compare_B_Xs_HH.png'), bbox_inches='tight')
plt.close(fig)
print("  [OK] B -> X_s HH")

# ========== 5. 汇总图 (所有通道在同一张图上) ==========
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()

# B → X_s H
plot_channel(axes[0], mH_BXs, our_B_Xs, r'This work ($\tan\beta=1$)',
             mH_sc_BXs, br_sc_BXs, r'SensCalc ($\theta=1$)',
             r'$m_H$ [GeV]', 'BR', r'$B \to X_s H$')

# K^+ → π^+ H
plot_channel(axes[1], mH_Kpi, our_K_pi, r'This work ($\tan\beta=1$)',
             mH_sc_Kpi, br_sc_Kpi, r'SensCalc ($\theta=1$)',
             r'$m_H$ [GeV]', 'BR', r'$K^+ \to \pi^+ H$',
             xlim=(0, 0.36))

# Υ → γ H
plot_channel(axes[2], mH_Ups, our_Ups_gamma_H, r'This work ($\tan\beta=1$)',
             mH_sc_Ups, br_sc_Ups, r'SensCalc ($\theta=1$)',
             r'$m_H$ [GeV]', 'BR', r'$\Upsilon \to \gamma H$')

# B → X_s HH
plot_channel(axes[3], mH_BXss, our_B_Xs_HH, r'This work ($\tan\beta=1$)',
             mH_sc_BXss, br_sc_BXss, r'SensCalc ($\theta=1$)',
             r'$m_H$ [GeV]', 'BR', r'$B \to X_s HH$')

fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'compare_all_panels.png'), bbox_inches='tight')
plt.close(fig)
print("  [OK] 汇总面板图")

print(f"\n所有图片已保存到 {OUT_DIR}")
