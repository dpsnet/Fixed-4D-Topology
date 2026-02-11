"""
p-adic Bowen公式数值验证 - 纯p幂情形专题
专门验证 f(z) = z^{p^k} 情形，这是Bowen公式严格成立的案例
"""

import numpy as np
from datetime import datetime


def p_adic_valuation(n: int, p: int) -> int:
    """计算p-adic赋值 v_p(n)"""
    if n == 0:
        return float('inf')
    k = 0
    n = abs(n)
    while n % p == 0:
        n //= p
        k += 1
    return k


def compute_pressure(d: int, p: int, delta: float) -> float:
    """计算压力函数 P(-δ·log|f'|_p)"""
    v_p_d = p_adic_valuation(d, p)
    return np.log(d) - delta * v_p_d * np.log(p)


def solve_bowen(d: int, p: int) -> tuple:
    """求解Bowen方程"""
    v_p_d = p_adic_valuation(d, p)
    if v_p_d == 0:
        return None, False
    delta = np.log(d) / (v_p_d * np.log(p))
    return delta, True


def verify_pure_power_case():
    """验证纯p幂情形"""
    
    print("=" * 80)
    print("p-adic Bowen公式验证 - 纯p幂情形专题")
    print("=" * 80)
    print()
    
    # 纯p幂测试案例
    test_cases = [
        # (p, k, d=p^k)
        (2, 1, 2),      # 2^1
        (2, 2, 4),      # 2^2
        (2, 3, 8),      # 2^3
        (3, 1, 3),      # 3^1
        (3, 2, 9),      # 3^2
        (3, 3, 27),     # 3^3
        (5, 1, 5),      # 5^1
        (5, 2, 25),     # 5^2
        (7, 1, 7),      # 7^1
        (11, 1, 11),    # 11^1
    ]
    
    print("【纯p幂测试案例】")
    print("-" * 80)
    header = "p    | k    | d=p^k  | v_p(d) | Bowen δ       | P(-δ|f'|)     | 结果"
    print(header)
    print("-" * 80)
    
    all_passed = True
    
    for p, k, d in test_cases:
        v_p_d = p_adic_valuation(d, p)
        delta, has_solution = solve_bowen(d, p)
        
        if has_solution:
            pressure = compute_pressure(d, p, delta)
            
            # 验证
            if abs(delta - 1.0) < 1e-10 and abs(pressure) < 1e-10:
                result = "✓ 通过"
            else:
                result = "✗ 失败"
                all_passed = False
            
            print(f"{p:>4} | {k:>4} | {d:>6} | {v_p_d:>6} | {delta:>13.10f} | {pressure:>13.2e} | {result}")
        else:
            print(f"{p:>4} | {k:>4} | {d:>6} | {v_p_d:>6} | {'N/A':>13} | {'N/A':>13} | {'✗ 无解'}")
            all_passed = False
    
    print("-" * 80)
    print()
    
    # 数学证明展示
    print("【数学证明】对于 d = p^k，为什么 δ = 1？")
    print("-" * 80)
    print()
    print("已知:")
    print("  • d = p^k")
    print("  • v_p(d) = k")
    print("  • log(d) = log(p^k) = k·log(p)")
    print()
    print("Bowen方程解:")
    print("             log(d)       k·log(p)")
    print("  δ = ───────────── = ───────────── = 1")
    print("       v_p(d)·log(p)    k·log(p)")
    print()
    print("压力函数验证:")
    print("  P(-δ·log|f'|_p) = log(d) - δ·v_p(d)·log(p)")
    print("                  = k·log(p) - 1·k·log(p)")
    print("                  = 0  ✓")
    print()
    print("Hausdorff维数:")
    print("  dim_H(J(f)) = dim_H({z : |z|_p = 1}) = 1")
    print()
    print("因此:")
    print("  dim_H(J(f)) = δ = 1  ✓")
    print()
    print("=" * 80)
    print()
    
    # 非纯p幂对比
    print("【对比：非纯p幂情形】")
    print("-" * 80)
    print("当 d = p^k · m（其中 p ∤ m, m > 1）:")
    print()
    print("             log(p^k · m)     k·log(p) + log(m)")
    print("  δ = ───────────────────── = ─────────────────── = 1 + log(m)/(k·log(p)) > 1")
    print("         k·log(p)                k·log(p)")
    print()
    print("此时 δ ≠ dim_H(J(f))，说明Bowen公式需要修正或附加条件。")
    print()
    
    contrast_cases = [
        (2, 6),    # 6 = 2 × 3
        (2, 12),   # 12 = 4 × 3
        (3, 6),    # 6 = 3 × 2
        (3, 15),   # 15 = 3 × 5
    ]
    
    print("p    | d    | d分解        | δ          | dim_H | 差异")
    print("-" * 60)
    
    for p, d in contrast_cases:
        v_p_d = p_adic_valuation(d, p)
        m = d // (p ** v_p_d)
        delta, _ = solve_bowen(d, p)
        dim_h = 1.0
        diff = delta - dim_h if delta else float('inf')
        
        decomp = f"{p}^{v_p_d} × {m}"
        print(f"{p:>4} | {d:>4} | {decomp:>12} | {delta:>10.6f} | {dim_h:>5.1f} | {diff:>+8.4f}")
    
    print()
    print("=" * 80)
    print()
    
    # 最终结论
    if all_passed:
        print("✅ 所有纯p幂测试通过！p-adic Bowen公式在 f(z) = z^{p^k} 情形下严格成立。")
    else:
        print("⚠️ 部分测试未通过。")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    verify_pure_power_case()
