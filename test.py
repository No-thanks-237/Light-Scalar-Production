#!/usr/bin/env python
"""
Light H 各产生道分支比, Type-I 2HDM Light H benchmark (arXiv:2212.06186)
"""
import sys
import os
import csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from physics.production import total_production


# 固定 tanb, 扫描 m_H
def scan_mH(tbeta, mH_min=0.05, mH_max=5.0, n_points=100):
    results = []
    for x_H in np.logspace(np.log10(mH_min), np.log10(mH_max), n_points):
        results.append(total_production(x_H, tbeta))
    return results


# 固定 m_H, 扫描 tanb
def scan_tbeta(mH, tbeta_min=1.0, tbeta_max=1e4, n_points=80):
    results = []
    for tb in np.logspace(np.log10(tbeta_min), np.log10(tbeta_max), n_points):
        results.append(total_production(mH, tb))
    return results


# 保存 CSV
def save_csv(results, filename):
    if not results:
        return
    keys = list(results[0].keys())
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            writer.writerow({k: (f"{v:.6e}" if isinstance(v, float) else v) for k, v in r.items()})
    print(f"  -> {filename}")


if __name__ == '__main__':
    print("Light H Branching Ratios (Type-I 2HDM, m_A=m_H+=600 GeV, lambda v^2=0)")

    # 1. 固定 tanb 扫描 m_H
    print("[1] Scanning m_H at fixed tanb ...")
    for tb in [10, 100, 1000]:
        save_csv(scan_mH(tb, mH_min=0.1, mH_max=5.0, n_points=50), f"output/scan_mH_tanb{tb:.0f}.csv")

    # 2. 固定 m_H 扫描 tanb
    print("[2] Scanning tanb at fixed m_H ...")
    for mH in [0.1, 1.0, 2.0]:
        save_csv(scan_tbeta(mH, tbeta_min=1.0, tbeta_max=1e4, n_points=60), f"output/scan_tbeta_mH{mH:.1f}.csv")

    # 3. 双标量产生 (对照 Figure 8)
    print("[3] Double scalar channels ...")
    results_b = []
    for mH in np.linspace(0.05, 2.6, 50):
        r = total_production(mH, 10)
        results_b.append({'m_H': mH, 'Br_B_Xs_HH': r['Br_B_Xs_HH']})
    save_csv(results_b, "output/double_B_Xs_HH.csv")

    results_k = []
    for mH in np.linspace(0.01, 0.2, 50):
        r = total_production(mH, 10)
        results_k.append({'m_H': mH, 'Br_K_pi_HH': r['Br_K_pi_HH']})
    save_csv(results_k, "output/double_K_pi_HH.csv")

    # 4. Benchmark 校验
    print("[4] Benchmark:")
    for tb in [5, 10, 100, 1000]:
        r = total_production(1.0, tb)
        print(f"  tanb={tb:6.1f}: B->X_sH={r['Br_B_Xs_H']:.4e} B->X_sHH={r['Br_B_Xs_HH']:.4e}")

    print("Done")
