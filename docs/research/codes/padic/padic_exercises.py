#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P-adic数计算练习脚本
=====================

本脚本包含全面的p-adic数计算练习，涵盖：
- 不同素数p的p-adic数创建
- 基本运算验证
- p-adic绝对值和赋值计算
- Hensel引理应用
- p-adic级数展开（log, exp, sin, cos）
- p-adic方程求解

作者: 数学学习助手
日期: 2026-02-11
"""

import padic
import numpy as np
from numpy.polynomial import polynomial as P

# 设置全局精度
padic.Padic.PRECISION = 30
padic.Padic.DISPLAY_PRECISION = 15

print("=" * 70)
print("                    P-ADIC数计算练习")
print("=" * 70)


# ============================================================================
# 第一部分: p-adic数的基本创建与表示
# ============================================================================
print("\n" + "=" * 70)
print("第一部分: p-adic数的基本创建与表示")
print("=" * 70)

print("\n--- 练习1.1: 不同素数p的p-adic数创建 ---")

primes = [2, 3, 5, 7]
for p in primes:
    print(f"\n素数 p = {p}:")
    
    # 从整数创建
    a = padic.Padic.from_int(100, p=p, N=20)
    print(f"  整数 100 在 Q_{p} 中: {a}")
    
    # 从分数创建
    b = padic.Padic.from_frac(1, p+1, p=p, N=15)
    print(f"  分数 1/{p+1} 在 Q_{p} 中: {b}")
    
    # 使用构造函数直接创建: p^v * s
    v, s = 3, 2  # p^3 * 2
    c = padic.Padic(20, v, s, p)
    print(f"  {p}^{v} * {s}: {c}")


print("\n--- 练习1.2: p-adic展开式 ---")

def p_adic_expansion(x, p, n_terms=10):
    """
    计算p-adic数的展开式（从低位到高位）
    x = a_0 + a_1*p + a_2*p^2 + ...
    """
    if isinstance(x, padic.Padic):
        # 获取中心值
        center = int(x.center())
        v = padic.Padic.val(x, p)
    else:
        center = x
        v = 0
    
    # 处理赋值
    if v != 0:
        result = f"{p}^{v} * ("
        center = center // (p**v) if v > 0 else center
    else:
        result = ""
    
    coeffs = []
    temp = abs(center)
    for i in range(n_terms):
        coeffs.append(temp % p)
        temp //= p
    
    terms = [f"{c}*{p}^{i}" if i > 0 else str(c) for i, c in enumerate(coeffs) if c != 0]
    expansion = " + ".join(terms) if terms else "0"
    
    if v != 0:
        expansion += ")"
    
    return expansion, coeffs


p = 5
for n in [1, 2, 3, 1/2, 1/3]:
    if isinstance(n, int):
        x = padic.Padic.from_int(n, p=p, N=15)
    else:
        from fractions import Fraction
        f = Fraction(n).limit_denominator(1000)
        x = padic.Padic.from_frac(f.numerator, f.denominator, p=p, N=15)
    
    exp_str, coeffs = p_adic_expansion(x, p, n_terms=8)
    print(f"\n{n} 在 Q_{p} 中的展开: {x}")
    print(f"  展开式: {exp_str}")
    print(f"  系数: {coeffs[:6]}...")


# ============================================================================
# 第二部分: p-adic绝对值与赋值
# ============================================================================
print("\n" + "=" * 70)
print("第二部分: p-adic绝对值与赋值")
print("=" * 70)

print("\n--- 练习2.1: 计算p-adic赋值和绝对值 ---")

def padic_valuation(n, p):
    """计算p-adic赋值 v_p(n)"""
    if n == 0:
        return float('inf')
    val = 0
    while n % p == 0:
        n //= p
        val += 1
    return val


def padic_absolute_value(n, p):
    """计算p-adic绝对值 |n|_p = p^{-v_p(n)}"""
    if n == 0:
        return 0
    return p ** (-padic_valuation(n, p))


print("\np-adic赋值和绝对值表:")
print("-" * 60)
print(f"{'n':>6} | {'v_2(n)':>8} | {'|n|_2':>12} | {'v_3(n)':>8} | {'|n|_3':>12}")
print("-" * 60)

test_numbers = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 81]
for n in test_numbers:
    v2 = padic_valuation(n, 2)
    abs2 = padic_absolute_value(n, 2)
    v3 = padic_valuation(n, 3)
    abs3 = padic_absolute_value(n, 3)
    print(f"{n:>6} | {v2:>8} | {abs2:>12.6f} | {v3:>8} | {abs3:>12.6f}")


print("\n--- 练习2.2: 强三角不等式验证 ---")

print("\n强三角不等式: |x + y|_p ≤ max(|x|_p, |y|_p)")
print("（当|x|_p ≠ |y|_p时，等号成立）")

def verify_strong_triangle_inequality(x, y, p):
    """验证p-adic强三角不等式"""
    if isinstance(x, int):
        x_val = padic_valuation(x, p)
        x_abs = padic_absolute_value(x, p)
    else:
        x_val = padic.Padic.val(x, p)
        x_abs = abs(x)
    
    if isinstance(y, int):
        y_val = padic_valuation(y, p)
        y_abs = padic_absolute_value(y, p)
    else:
        y_val = padic.Padic.val(y, p)
        y_abs = abs(y)
    
    z = x + y if isinstance(x, int) and isinstance(y, int) else x + y
    if isinstance(z, int):
        z_abs = padic_absolute_value(z, p)
    else:
        z_abs = abs(z)
    
    lhs = z_abs
    rhs = max(x_abs, y_abs)
    
    satisfied = lhs <= rhs + 1e-10
    equality = abs(lhs - rhs) < 1e-10
    
    return {
        'x_abs': x_abs, 'y_abs': y_abs, 'z_abs': z_abs,
        'lhs': lhs, 'rhs': rhs,
        'satisfied': satisfied,
        'equality': equality,
        'x_val': x_val, 'y_val': y_val
    }


p = 5
test_cases = [
    (25, 5),    # |25|_5 = 1/25, |5|_5 = 1/5
    (25, 50),   # 相同赋值
    (5, 3),     # 不同赋值
    (125, 25),  # |125|_5 = 1/125, |25|_5 = 1/25
    (1, 4),     # 都是单位
]

print(f"\n在 Q_{p} 中验证:")
print("-" * 80)
for x, y in test_cases:
    result = verify_strong_triangle_inequality(x, y, p)
    status = "✓" if result['satisfied'] else "✗"
    eq_status = "(等号)" if result['equality'] else "(严格)"
    print(f"|{x}+{y}|_{p} = {result['z_abs']:.6f} ≤ max({result['x_abs']:.6f}, {result['y_abs']:.6f}) = {result['rhs']:.6f} {status} {eq_status}")


# ============================================================================
# 第三部分: 基本运算验证
# ============================================================================
print("\n" + "=" * 70)
print("第三部分: p-adic数的基本运算验证")
print("=" * 70)

print("\n--- 练习3.1: 加减乘除运算 ---")

p = 7
N = 15

# 创建测试数
a = padic.Padic.from_int(10, p=p, N=N)
b = padic.Padic.from_int(3, p=p, N=N)
c = padic.Padic.from_frac(1, 2, p=p, N=N)

print(f"\n在 Q_{p} 中 (精度 {N}):")
print(f"  a = 10 = {a}")
print(f"  b = 3 = {b}")
print(f"  c = 1/2 = {c}")

print(f"\n加法:")
print(f"  a + b = {a + b}")
print(f"  验证: 10 + 3 = 13")

print(f"\n减法:")
print(f"  a - b = {a - b}")
print(f"  验证: 10 - 3 = 7")

print(f"\n乘法:")
print(f"  a * b = {a * b}")
print(f"  验证: 10 * 3 = 30")
print(f"  a * c = {a * c}")
print(f"  验证: 10 * 1/2 = 5")

print(f"\n除法:")
print(f"  a / b = {a / b}")
print(f"  a / c = {a / c}")

print(f"\n幂运算:")
print(f"  a^3 = {a ** 3}")
print(f"  验证: 10^3 = 1000")


print("\n--- 练习3.2: 运算性质验证 ---")

print("\n验证结合律: (a+b)+c = a+(b+c)")
p = 5
a = padic.Padic.from_int(2, p=p, N=10)
b = padic.Padic.from_int(3, p=p, N=10)
c = padic.Padic.from_int(4, p=p, N=10)

lhs = (a + b) + c
rhs = a + (b + c)
print(f"  (a+b)+c = {lhs}")
print(f"  a+(b+c) = {rhs}")
print(f"  相等: {lhs == rhs}")

print("\n验证分配律: a*(b+c) = a*b + a*c")
lhs = a * (b + c)
rhs = a * b + a * c
print(f"  a*(b+c) = {lhs}")
print(f"  a*b+a*c = {rhs}")
print(f"  相等: {lhs == rhs}")


# ============================================================================
# 第四部分: Hensel引理应用
# ============================================================================
print("\n" + "=" * 70)
print("第四部分: Hensel引理应用")
print("=" * 70)

print("\n--- 练习4.1: 使用Hensel引理求平方根 ---")
print("\nHensel引理: 若 f(x) ≡ 0 (mod p) 有解且 f'(x) ≢ 0 (mod p)")
print("          则存在唯一的p-adic提升")

# 定义多项式 f(x) = x^2 - a
def find_padic_sqrt_manual(a, p, N=15):
    """
    手动实现Hensel引理在Q_p中寻找sqrt(a)
    条件: a是模p的二次剩余，且p ≠ 2
    """
    # 检查模p是否有解
    approx_root = None
    for x in range(p):
        if (x * x - a) % p == 0:
            approx_root = x
            break
    
    if approx_root is None:
        return None, f"{a} 不是模 {p} 的二次剩余"
    
    # Hensel提升迭代: x_{n+1} = x_n - f(x_n)/f'(x_n)
    # 对于 f(x) = x^2 - a, f'(x) = 2x
    # 迭代: x_{n+1} = x_n - (x_n^2 - a)/(2x_n) = (x_n + a/x_n) / 2
    
    x = padic.Padic.from_int(approx_root, p=p, N=N)
    a_pad = padic.Padic.from_int(a, p=p, N=N)
    
    for i in range(N):
        try:
            # Newton迭代
            x_new = (x + a_pad / x) / 2
            if x_new == x:
                break
            x = x_new
        except:
            break
    
    return x, "成功"


print("\n计算 √2 在 Q_7 中:")
p = 7
a = 2
result, msg = find_padic_sqrt_manual(a, p, N=15)
if result:
    print(f"  √2 = {result}")
    # 验证
    check = result * result
    print(f"  验证: (√2)^2 = {check}")
else:
    print(f"  失败: {msg}")

print("\n计算 √(-1) 在 Q_5 中:")
p = 5
a = -1
result, msg = find_padic_sqrt_manual(a, p, N=15)
if result:
    print(f"  √(-1) = {result}")
    check = result * result
    print(f"  验证: (√(-1))^2 = {check}")
    print(f"  注: ...444在5-adic中表示-1, 因为4(1+5+5²+...) = 4/(1-5) = -1")
else:
    print(f"  失败: {msg}")

print("\n计算 √3 在 Q_11 中:")
p = 11
a = 3
result, msg = find_padic_sqrt_manual(a, p, N=15)
if result:
    print(f"  √3 = {result}")
    check = result * result
    print(f"  验证: (√3)^2 = {check}")
else:
    print(f"  失败: {msg}")

print("\n计算 √2 在 Q_3 中 (预期失败):")
p = 3
a = 2
result, msg = find_padic_sqrt_manual(a, p, N=15)
if result:
    print(f"  √2 = {result}")
else:
    print(f"  预期失败: {msg}")
    print(f"  解释: 2 不是模3的二次剩余")
    print(f"  理论: 对于奇素数 p, 2是模p二次剩余 ⟺ p ≡ ±1 (mod 8)")
    print(f"  验证: 3 ≡ 3 (mod 8), 所以2不是模3二次剩余")


print("\n--- 练习4.2: 解p-adic多项式方程 ---")

def solve_cubic_newton(a, approx, p, N=15):
    """
    使用Newton迭代解 x^3 = a 在 Q_p 中
    迭代: x_{n+1} = (2x_n + a/x_n^2) / 3
    """
    x = padic.Padic.from_int(approx, p=p, N=N)
    a_pad = padic.Padic.from_int(a, p=p, N=N)
    
    for i in range(N):
        try:
            x_new = (2 * x + a_pad / (x * x)) / 3
            if x_new == x:
                break
            x = x_new
        except:
            break
    
    return x


print("\n解方程 x^3 - 2 = 0 在 Q_5 中:")
p = 5
# x^3 ≡ 2 (mod 5): 测试 x=3, 3^3=27≡2 (mod 5)
root = solve_cubic_newton(2, 3, p, N=15)
print(f"  根: {root}")
check = root ** 3
print(f"  验证: 根^3 = {check}")

# 验证模5
print(f"  模5验证: 3^3 = {3**3} ≡ {3**3 % 5} (mod 5) = 2 ✓")


# ============================================================================
# 第五部分: p-adic级数展开
# ============================================================================
print("\n" + "=" * 70)
print("第五部分: p-adic级数展开 (log, exp, sin, cos)")
print("=" * 70)

print("\n--- 练习5.1: p-adic指数函数 exp ---")
print("\nexp(x) 在 |x|_p < p^{-1/(p-1)} 时收敛")

for p in [2, 3, 5, 7]:
    radius = p ** (-1.0 / (p - 1)) if p > 2 else 0.5
    print(f"\n在 Q_{p} 中 (收敛半径 ≈ {radius:.4f}):")
    
    # 选择 |x|_p < 收敛半径的x
    if p == 2:
        x = padic.Padic.from_int(4, p=p, N=15)  # |4|_2 = 1/4 < 1/2
    else:
        x = padic.Padic.from_int(p, p=p, N=15)  # |p|_p = 1/p < p^{-1/(p-1)}
    
    print(f"  x = {x}, |x|_{p} = {abs(x):.6f}")
    
    try:
        exp_x = padic.exp(x, p=p, N=15)
        print(f"  exp(x) = {exp_x}")
        
        # 验证 exp(x) * exp(-x) = 1
        exp_neg_x = padic.exp(-x, p=p, N=15)
        product = exp_x * exp_neg_x
        print(f"  exp(x)*exp(-x) = {product}")
    except Exception as e:
        print(f"  计算失败: {e}")


print("\n--- 练习5.2: p-adic对数函数 log ---")
print("\nlog(x) 在 |x-1|_p < 1 时收敛 (即 x ≡ 1 (mod p))")

for p in [3, 5, 7]:
    print(f"\n在 Q_{p} 中:")
    
    # x = 1 + p
    x = 1 + p
    x_pad = padic.Padic.from_int(x, p=p, N=15)
    print(f"  x = 1 + {p} = {x_pad}")
    
    try:
        log_x = padic.log(x, p=p, N=15)
        print(f"  log(x) = {log_x}")
        
        # 验证 log(exp(x)) = x
        exp_log = padic.exp(log_x, p=p, N=15)
        print(f"  exp(log(x)) = {exp_log}")
    except Exception as e:
        print(f"  计算失败: {e}")


print("\n--- 练习5.3: p-adic三角函数 sin, cos ---")
print("\nsin(x), cos(x) 在 |x|_p < p^{-1/(p-1)} 时收敛")

for p in [3, 5]:
    print(f"\n在 Q_{p} 中:")
    
    # 选择小x
    x = padic.Padic.from_int(p, p=p, N=10)
    print(f"  x = {x}")
    
    try:
        sin_x = padic.sin(x, p=p, N=10)
        cos_x = padic.cos(x, p=p, N=10)
        print(f"  sin(x) = {sin_x}")
        print(f"  cos(x) = {cos_x}")
        
        # 验证 sin^2 + cos^2 = 1
        identity = sin_x * sin_x + cos_x * cos_x
        print(f"  sin²(x) + cos²(x) = {identity}")
    except Exception as e:
        print(f"  计算失败: {e}")


# ============================================================================
# 第六部分: 综合练习与深入探索
# ============================================================================
print("\n" + "=" * 70)
print("第六部分: 综合练习与深入探索")
print("=" * 70)

print("\n--- 练习6.1: p-adic整数的单位群结构 ---")

print("\n在 Q_p 中，p-adic整数 Z_p 的单位群 Z_p^× 的结构:")
print("  Z_p^× ≅ μ_{p-1} × (1 + pZ_p)")
print("  其中 μ_{p-1} 是 (p-1)次单位根群")

for p in [3, 5, 7, 11]:
    print(f"\n  p = {p}:")
    print(f"    Z_{p}^× 有 (p-1) = {p-1} 个(p-1)次单位根")
    print(f"    以及无限 pro-p 群 1 + {p}Z_{p}")


print("\n--- 练习6.2: p-adic球的性质 ---")

def p_adic_ball_properties(p, center, radius):
    """探索p-adic球的性质"""
    print(f"\n  在 Q_{p} 中以 {center} 为中心，半径为 {radius} 的球:")
    print(f"  p-adic球的特殊性质: 每个点都是中心!")
    print(f"  即: 若 y ∈ B(x,r)，则 B(x,r) = B(y,r)")


for p in [2, 3, 5]:
    p_adic_ball_properties(p, 0, p**(-2))


print("\n--- 练习6.3: 二次型在Q_p中的可解性 ---")

def check_quadratic_form(a, b, c, p):
    """
    检查二次型 ax^2 + by^2 + cz^2 = 0 在 Q_p 中是否有非平凡解
    使用Hilbert符号
    """
    # Hilbert符号 (a,b)_p = 1 表示 ax^2 + by^2 = z^2 有非平凡解
    print(f"\n  检查 {a}x² + {b}y² + {c}z² = 0 在 Q_{p} 中的可解性")
    
    # 简化: 检查Legendre符号
    def legendre_symbol(a, p):
        if a % p == 0:
            return 0
        return pow(a, (p - 1) // 2, p)
    
    # 基本检查: 若所有系数都是模p的非剩余，可能无解
    leg_a = legendre_symbol(a, p)
    leg_b = legendre_symbol(b, p)
    leg_c = legendre_symbol(c, p)
    
    print(f"    ({a}/{p}) = {leg_a}, ({b}/{p}) = {leg_b}, ({c}/{p}) = {leg_c}")


for p in [3, 5, 7]:
    check_quadratic_form(1, 1, 1, p)   # x² + y² + z² = 0
    check_quadratic_form(1, 1, -1, p)  # x² + y² - z² = 0


print("\n" + "=" * 70)
print("                       练习完成!")
print("=" * 70)
print("\n总结:")
print("  1. p-adic数创建: 支持从整数、分数和直接构造")
print("  2. 绝对值和赋值: 满足强三角不等式")
print("  3. Hensel引理: 将模p解提升到p-adic解")
print("  4. 级数展开: exp, log, sin, cos 在适当条件下收敛")
print("  5. 特殊性质: p-adic拓扑完全不连通，球具有特殊性质")
print("\n下一步: 探索p-adic模形式和自守形式...")
