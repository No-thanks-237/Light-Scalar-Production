"""
辅助函数: 相空间因子、Källén λ 函数等
"""
import numpy as np


# Källén λ 函数: λ(a,b,c) = (a-b-c)² - 4bc
def lambda_kallen(a, b, c):
    return (a - b - c) ** 2 - 4.0 * b * c


# 式 2.5: 相空间因子 f(x) = (1-8x+x²)(1-x²) - 12x² ln x, x = m_c²/m_b²
def phase_space_f(x):
    return (1.0 - 8.0 * x + x ** 2) * (1.0 - x ** 2) - 12.0 * x ** 2 * np.log(x)


# 式 E.8: 双标量相空间函数, x = m_φ/m_b
def phase_space_f_double(x):
    sqrt_term = np.sqrt(1.0 - 4.0 * x ** 2)
    term1 = (1.0 / 3.0) * sqrt_term * (1.0 + 5.0 * x ** 2 - 6.0 * x ** 4)
    log_arg = (1.0 + sqrt_term) / (2.0 * x)
    term2 = 4.0 * x ** 2 * (1.0 - 2.0 * x ** 2 + 2.0 * x ** 4) * np.log(log_arg)
    return term1 - term2
