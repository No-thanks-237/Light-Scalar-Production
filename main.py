#!/usr/bin/env python

import sys
import os
import csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from physics.production import total_production

# 填入要扫描的 m_H (GeV) 和 tanb 值
mH_list = np.linspace(0.01, 10.0, 100)  
tanb_list = np.logspace(1, 4, 100)  

keys = ['m_H', 'tanb', 'Br_B_Xs_H', 'Br_K_pi_H', 'Br_eta_pi_H',
        'Br_eta_prime_pi_H', 'Br_pi_semilep', 'Br_K_semilep',
        'Br_Upsilon_gamma_H', 'Br_B_Xs_HH', 'Br_K_pi_HH']

with open('output/br_table.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(keys)
    for mH in mH_list:
        print(f"mH={mH:.2f} GeV")
        for tb in tanb_list:
            r = total_production(mH, tb)
            w.writerow([f'{r[k]:.10e}' if isinstance(r[k], float) else r[k] for k in keys])

print("Done! Results have been saved to output/br_table.csv")
