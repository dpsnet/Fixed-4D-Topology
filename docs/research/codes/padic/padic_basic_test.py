#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p-adic数计算测试脚本
用于p-adic模形式研究

使用的库: padic (Python)
功能:
    - 创建p-adic数 (2-adic, 3-adic, 5-adic等)
    - 基本运算 (+, -, *, /)
    - p-adic绝对值计算
    - 级数展开 (log, exp, sin, cos)
    - Hensel引理应用
"""

from padic import Padic, log, exp, sin, cos, binomial, series, hensel, find_approx_root
from numpy.polynomial import Polynomial
import sys

def test_basic_creation():
    """测试p-adic数的基本创建"""
    print("=" * 60)
    print("1. p-adic数基本创建测试")
    print("=" * 60)
    
    # 设置默认素数
    Padic.DEFAULT_PRIME = 2
    
    # 从整数创建p-adic数
    a = Padic.from_int(17, p=2)  # 17的2-adic表示
    b = Padic.from_int(5, p=2)   # 5的2-adic表示
    
    print(f"17 的 2-adic 表示: {a}")
    print(f"5 的 2-adic 表示: {b}")
    
    # 从字符串创建p-adic数
    c = Padic.from_string("1001", p=2)  # 二进制 1001 = 9
    print(f"字符串 '1001' (二进制) 的 2-adic 表示: {c}")
    
    # 3-adic数
    d = Padic.from_int(10, p=3)
    e = Padic.from_int(7, p=3)
    print(f"10 的 3-adic 表示: {d}")
    print(f"7 的 3-adic 表示: {e}")
    
    # 5-adic数
    f = Padic.from_int(25, p=5)
    print(f"25 的 5-adic 表示: {f}")
    print()
    
    return a, b, d, e


def test_basic_operations():
    """测试p-adic数的基本运算"""
    print("=" * 60)
    print("2. p-adic数基本运算测试")
    print("=" * 60)
    
    p = 2
    
    # 创建测试用的p-adic数
    a = Padic.from_int(17, p=p)  # 17 = 10001_2
    b = Padic.from_int(5, p=p)   # 5 = 101_2
    
    print(f"a = 17 = {a}")
    print(f"b = 5 = {b}")
    print()
    
    # 加法
    add_result = a + b
    print(f"a + b = 17 + 5 = {add_result}")
    print(f"验证: 17 + 5 = 22")
    
    # 减法
    sub_result = a - b
    print(f"a - b = 17 - 5 = {sub_result}")
    print(f"验证: 17 - 5 = 12")
    
    # 乘法
    mul_result = a * b
    print(f"a * b = 17 * 5 = {mul_result}")
    print(f"验证: 17 * 5 = 85")
    
    # 除法
    div_result = a / b
    print(f"a / b = 17 / 5 = {div_result}")
    print(f"验证: 17 / 5 = 3.4")
    print()
    
    # 3-adic运算
    print("--- 3-adic 运算 ---")
    p = 3
    c = Padic.from_int(10, p=p)
    d = Padic.from_int(4, p=p)
    print(f"c = 10 = {c}")
    print(f"d = 4 = {d}")
    print(f"c + d = {c + d}")
    print(f"c - d = {c - d}")
    print(f"c * d = {c * d}")
    print(f"c / d = {c / d}")
    print()


def test_padic_absolute_value():
    """测试p-adic绝对值（赋值）计算"""
    print("=" * 60)
    print("3. p-adic绝对值（赋值）测试")
    print("=" * 60)
    
    # p-adic绝对值定义为 |x|_p = p^{-v_p(x)}
    # 其中 v_p(x) 是p-adic赋值（valuation）
    
    p = 2
    numbers = [1, 2, 4, 8, 16, 3, 6, 12]
    
    print(f"{p}-adic绝对值计算:")
    print("公式: |x|_p = p^(-v_p(x))")
    print()
    
    for n in numbers:
        padic_num = Padic.from_int(n, p=p)
        valuation = Padic.val(n, p)  # p-adic赋值
        abs_value = abs(padic_num)   # p-adic绝对值
        print(f"|{n}|_{p} = {abs_value}")
        print(f"  v_{p}({n}) = {valuation}")
        print(f"  {p}^(-{valuation}) = {abs_value}")
        print()
    
    # 5-adic例子
    print("--- 5-adic 例子 ---")
    p = 5
    numbers = [1, 5, 25, 125, 10, 50]
    for n in numbers:
        padic_num = Padic.from_int(n, p=p)
        valuation = Padic.val(n, p)
        abs_value = abs(padic_num)
        print(f"|{n}|_{p} = {abs_value} (v_{p}({n}) = {valuation})")
    print()


def test_series_expansion():
    """测试p-adic级数展开"""
    print("=" * 60)
    print("4. p-adic级数展开测试")
    print("=" * 60)
    
    p = 7  # 使用较大的素数以获得更好的收敛性
    
    # 创建一个接近1的p-adic数（对数收敛条件）
    x = Padic.from_int(8, p=p)  # 8 = 1 + 7
    print(f"x = 8 = {x}")
    print(f"对于log: x = 1 + O(p) 需要满足")
    
    # p-adic对数
    # log(1 + t) 收敛当 |t|_p < 1，即 t = O(p)
    try:
        log_x = log(x, p=p, N=20)
        print(f"log({x}) = {log_x}")
    except Exception as e:
        print(f"log计算出错: {e}")
    
    # p-adic指数
    # exp(t) 收敛当 |t|_p < p^{-1/(p-1)}
    y = Padic.from_int(7, p=p)  # 7 = p
    try:
        exp_y = exp(y, p=p, N=20)
        print(f"exp({y}) = {exp_y}")
    except Exception as e:
        print(f"exp计算出错: {e}")
    
    # p-adic正弦和余弦
    try:
        sin_y = sin(y, p=p, N=20)
        cos_y = cos(y, p=p, N=20)
        print(f"sin({y}) = {sin_y}")
        print(f"cos({y}) = {cos_y}")
    except Exception as e:
        print(f"sin/cos计算出错: {e}")
    
    print()
    
    # 二项式级数
    print("--- 二项式级数 (1 + x)^a ---")
    z = Padic.from_int(8, p=p)  # 8 = 1 + 7
    a = Padic.from_int(2, p=p)  # 指数
    try:
        binom_result = binomial(z, a, p=p, N=10)
        print(f"(1 + 7)^2 的 {p}-adic 展开 = {binom_result}")
    except Exception as e:
        print(f"二项式级数计算出错: {e}")
    print()


def test_hensel_lemma():
    """测试Hensel引理应用"""
    print("=" * 60)
    print("5. Hensel引理测试 (求多项式根)")
    print("=" * 60)
    
    p = 7
    
    # 创建一个多项式: f(x) = x^2 - 2
    # 在7-adic中寻找sqrt(2)
    # 在Z/7Z中，3^2 = 9 ≡ 2 (mod 7)，所以3是近似根
    
    poly = Polynomial([-2, 0, 1])  # -2 + 0*x + 1*x^2 = x^2 - 2
    print(f"多项式: f(x) = x^2 - 2")
    print(f"在 {p}-adic 中寻找根")
    print(f"在 Z/{p}Z 中，3^2 = 9 ≡ 2 (mod {p})，所以3是近似根")
    
    try:
        # 使用Hensel引理提升近似根
        approx_root = Padic.from_int(3, p=p)
        root = hensel(poly, approx=approx_root, p=p, N=20)
        print(f"近似根: {approx_root}")
        print(f"提升后的根: {root}")
        
        # 验证
        verification = root * root
        print(f"验证: root^2 = {verification}")
        print(f"应该接近 2 = {Padic.from_int(2, p=p)}")
    except Exception as e:
        print(f"Hensel引理应用出错: {e}")
    
    print()
    
    # 另一个例子: x^2 - x - 1 = 0 (黄金比例)
    print("--- 黄金比例方程 x^2 - x - 1 = 0 ---")
    p = 11
    poly2 = Polynomial([-1, -1, 1])  # -1 - x + x^2 = x^2 - x - 1
    try:
        root2 = find_approx_root(poly2, p=p, depth=5)
        print(f"找到的近似根: {root2}")
        
        refined_root = hensel(poly2, approx=root2, p=p, N=20)
        print(f"精确化后的根: {refined_root}")
    except Exception as e:
        print(f"Hensel引理应用出错: {e}")
    print()


def test_precision_settings():
    """测试精度设置"""
    print("=" * 60)
    print("6. 精度设置测试")
    print("=" * 60)
    
    p = 2
    
    # 默认精度
    print(f"默认精度 (PRECISION): {Padic.PRECISION}")
    print(f"整数精度 (INTEGER_PRECISION): {Padic.INTEGER_PRECISION}")
    print(f"显示精度 (DISPLAY_PRECISION): {Padic.DISPLAY_PRECISION}")
    print()
    
    # 创建高精度p-adic数
    Padic.INTEGER_PRECISION = 128
    a = Padic.from_int(123456789, p=p)
    print(f"高精度表示 (128位) 123456789:")
    print(f"  {a}")
    
    # 自定义显示精度
    print()
    print("自定义显示精度示例:")
    big_num = Padic.from_int(2**100 - 1, p=p)
    print(f"2^100 - 1 的完整表示: {big_num:all}")
    print(f"2^100 - 1 的16位精度: {big_num:.16}")
    print()


def test_fraction_conversion():
    """测试分数转换为p-adic数"""
    print("=" * 60)
    print("7. 分数转换为p-adic数测试")
    print("=" * 60)
    
    p = 5
    
    # 将分数转换为p-adic数
    fractions = [(1, 2), (1, 3), (2, 3), (3, 4), (-1, 5)]
    
    for num, den in fractions:
        padic_frac = Padic.from_frac(num, den, p=p)
        print(f"{num}/{den} 的 {p}-adic 表示: {padic_frac}")
        
        # 验证
        reconstructed = padic_frac * den
        expected = Padic.from_int(num, p=p)
        print(f"  验证: ({num}/{den}) * {den} = {reconstructed}")
        print(f"  应该等于 {num} = {expected}")
        print()


def main():
    """主函数：运行所有测试"""
    print("\n" + "=" * 60)
    print("p-adic数计算模块测试")
    print("用于p-adic模形式研究")
    print("=" * 60 + "\n")
    
    try:
        test_basic_creation()
        test_basic_operations()
        test_padic_absolute_value()
        test_series_expansion()
        test_hensel_lemma()
        test_precision_settings()
        test_fraction_conversion()
        
        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
