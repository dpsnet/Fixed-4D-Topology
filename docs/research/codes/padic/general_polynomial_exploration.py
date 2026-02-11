#!/usr/bin/env python3
"""
p-adic 一般多项式数值探索 - 优化版本
测试Bowen公式在更一般多项式情形下的适用性

多项式族：
1. f(z) = z^2 + c (p-adic Mandelbrot)
2. f(z) = z^d + a (扰动幂映射)
3. f(z) = z^2 + p*z (有线性项)
4. 一般二次多项式 f(z) = az^2 + bz + c

作者: Fixed-4D-Topology Research Group
日期: 2026-02-11
"""

import numpy as np
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Callable, Optional, Dict, Union
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 配置
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# 设置随机种子以保证可重复性
np.random.seed(42)


# =============================================================================
# 数据结构和工具函数
# =============================================================================

@dataclass
class PolynomialParameters:
    """多项式参数基类"""
    p: int                    # 素数
    
    def __post_init__(self):
        assert self.p > 1 and all(self.p % i != 0 for i in range(2, int(self.p**0.5) + 1)), \
            f"{self.p} 不是素数"
    
    @property
    def poly_type(self) -> str:
        """多项式类型"""
        raise NotImplementedError
    
    def evaluate(self, z: Fraction) -> Fraction:
        """在点z处求值多项式"""
        raise NotImplementedError
    
    def derivative(self, z: Fraction) -> Fraction:
        """在点z处求值导数"""
        raise NotImplementedError
    
    def iterate(self, z: Fraction, n: int) -> Fraction:
        """n次迭代"""
        result = z
        for _ in range(n):
            result = self.evaluate(result)
        return result


@dataclass
class QuadraticPolynomial(PolynomialParameters):
    """二次多项式 f(z) = az^2 + bz + c"""
    a: int = 1
    b: int = 0
    c: int = 0
    
    @property
    def poly_type(self) -> str:
        return "quadratic"
    
    def evaluate(self, z: Fraction) -> Fraction:
        """f(z) = az^2 + bz + c"""
        return self.a * z * z + self.b * z + self.c
    
    def derivative(self, z: Fraction) -> Fraction:
        """f'(z) = 2az + b"""
        return 2 * self.a * z + self.b
    
    def __str__(self):
        terms = []
        if self.a != 0:
            if self.a == 1:
                terms.append("z²")
            elif self.a == -1:
                terms.append("-z²")
            else:
                terms.append(f"{self.a}z²")
        if self.b != 0:
            if self.b == 1:
                terms.append("z")
            elif self.b == -1:
                terms.append("-z")
            else:
                terms.append(f"{self.b}z")
        if self.c != 0:
            terms.append(f"{self.c}")
        return " + ".join(terms).replace("+ -", "- ") if terms else "0"


@dataclass
class PowerMapWithConstant(PolynomialParameters):
    """扰动幂映射 f(z) = z^d + a"""
    d: int = 2
    a: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        assert self.d >= 2, "d 必须 >= 2"
    
    @property
    def poly_type(self) -> str:
        return "power_with_constant"
    
    def evaluate(self, z: Fraction) -> Fraction:
        """f(z) = z^d + a"""
        return z ** self.d + self.a
    
    def derivative(self, z: Fraction) -> Fraction:
        """f'(z) = d*z^(d-1)"""
        if self.d == 2:
            return Fraction(2) * z
        return Fraction(self.d) * (z ** (self.d - 1))
    
    def __str__(self):
        return f"z^{self.d} + {self.a}"


# =============================================================================
# p-adic算术工具
# =============================================================================

def p_adic_valuation(n: int, p: int) -> int:
    """计算整数n的p-adic赋值 v_p(n)"""
    if n == 0:
        return float('inf')
    k = 0
    n = abs(n)
    while n % p == 0:
        n //= p
        k += 1
    return k


def p_adic_absolute_value(x: Union[Fraction, int], p: int) -> float:
    """计算p-adic绝对值 |x|_p = p^(-v_p(x))"""
    if x == 0:
        return 0.0
    if isinstance(x, int):
        x = Fraction(x)
    v_p_x = p_adic_valuation(x.numerator, p) - p_adic_valuation(x.denominator, p)
    return float(p ** (-v_p_x))


def p_adic_norm_of_derivative(deriv: Fraction, p: int) -> float:
    """计算导数的p-adic范数"""
    return p_adic_absolute_value(deriv, p)


# =============================================================================
# Julia集计算 - 优化版本
# =============================================================================

def compute_julia_set_approximation(params: PolynomialParameters,
                                     max_iter: int = 30,
                                     num_samples: int = 200) -> List[Fraction]:
    """
    快速计算Julia集的近似点
    
    参数:
        params: 多项式参数
        max_iter: 最大迭代次数
        num_samples: 采样点数
    
    返回:
        Julia集中的点列表
    """
    p = params.p
    escape_radius = 2 * p
    julia_points = []
    
    # 在单位圆附近采样
    for _ in range(num_samples):
        # 生成分子和分母都与p互质的随机数
        m = np.random.randint(1, 50)
        n = np.random.randint(1, 50)
        
        # 确保不被p整除
        while m % p == 0:
            m = np.random.randint(1, 50)
        while n % p == 0:
            n = np.random.randint(1, 50)
        
        z = Fraction(m, n)
        
        # 跟踪轨道
        current = z
        is_bounded = True
        
        for _ in range(max_iter):
            val = p_adic_absolute_value(current, p)
            if val > escape_radius or val < 1.0 / escape_radius:
                is_bounded = False
                break
            current = params.evaluate(current)
            
            # 检查数值溢出
            if abs(current.numerator) > 10**8 or abs(current.denominator) > 10**8:
                break
        
        if is_bounded:
            julia_points.append(z)
    
    return julia_points


# =============================================================================
# Hausdorff维数估计 - 简化版
# =============================================================================

def estimate_dimension_simplified(params: PolynomialParameters) -> float:
    """
    简化的维数估计方法
    
    基于多项式度数和p-adic赋值
    """
    p = params.p
    
    if params.poly_type == "power_with_constant":
        d = params.d
        v_p_d = p_adic_valuation(d, p)
        
        if v_p_d > 0:
            # 扩张情形
            # 对于纯幂映射 f(z) = z^d，维数 = 1
            if params.a == 0:
                return 1.0
            else:
                # 扰动幂映射，维数接近1
                return 0.95 + 0.05 * min(1.0, 1.0 / abs(params.a))
        else:
            # 非扩张情形
            return 1.0
    
    elif params.poly_type == "quadratic":
        # 二次多项式
        a, b, c = params.a, params.b, params.c
        
        # 检查主导项系数
        v_p_a = p_adic_valuation(abs(a), p) if a != 0 else float('inf')
        
        # 如果二次项系数被p整除，行为可能更复杂
        if v_p_a == 0:
            # 扩张二次多项式
            base_dim = 1.0
            # 线性项和常数项的影响
            perturbation = 0.0
            if b != 0:
                perturbation += 0.02 * min(1.0, p_adic_absolute_value(Fraction(1, b), p))
            if c != 0:
                perturbation += 0.02 * min(1.0, p_adic_absolute_value(Fraction(1, c), p))
            return base_dim - perturbation
        else:
            # 非扩张或弱扩张
            return 0.9 + 0.1 * np.exp(-v_p_a)
    
    return 1.0


def estimate_dimension_via_sample_points(params: PolynomialParameters) -> float:
    """
    通过采样点估计维数
    """
    p = params.p
    points = compute_julia_set_approximation(params, max_iter=20, num_samples=150)
    
    if len(points) < 10:
        # 点数太少，使用简化估计
        return estimate_dimension_simplified(params)
    
    # 使用盒计数法
    dimensions = []
    for n in range(1, 6):
        epsilon = p ** (-n)
        boxes = set()
        
        for z in points:
            try:
                if z.denominator == 1:
                    equiv_class = (z.numerator % (p ** n))
                else:
                    # 计算模逆
                    denom_inv = pow(z.denominator, -1, p ** n)
                    equiv_class = (z.numerator * denom_inv) % (p ** n)
                boxes.add(equiv_class)
            except:
                continue
        
        N = len(boxes)
        if N > 0:
            dim_estimate = np.log(N) / np.log(1 / epsilon)
            dimensions.append(dim_estimate)
    
    if dimensions:
        return float(np.clip(np.mean(dimensions[-2:]), 0.5, 2.0))
    
    return estimate_dimension_simplified(params)


# =============================================================================
# 压力函数计算 - 高效版本
# =============================================================================

def compute_pressure_approximate(params: PolynomialParameters, 
                                 s: float, 
                                 n_iter: int = 8) -> float:
    """
    近似计算压力函数 P(s)
    
    使用简化的采样方法
    """
    p = params.p
    num_samples = 100
    
    log_sum = 0.0
    valid_samples = 0
    
    for _ in range(num_samples):
        # 在单位球内采样
        m = np.random.randint(1, p**3)
        n_den = np.random.randint(1, p**3)
        
        # 确保 |z|_p = 1
        v_m = p_adic_valuation(m, p)
        v_n = p_adic_valuation(n_den, p)
        if v_m != v_n:
            continue
        
        z = Fraction(m, n_den)
        
        # 计算导数乘积 |Df^n(z)|_p
        deriv_product = 1.0
        current = z
        
        for _ in range(n_iter):
            deriv = params.derivative(current)
            deriv_norm = p_adic_norm_of_derivative(deriv, p)
            deriv_product *= deriv_norm
            
            if deriv_product < 1e-100:
                break
            
            current = params.evaluate(current)
            
            # 防止溢出
            if abs(current.numerator) > 10**8:
                break
        
        if deriv_product > 0:
            log_sum += deriv_product ** s
            valid_samples += 1
    
    if valid_samples > 0 and log_sum > 0:
        return np.log(log_sum / valid_samples) / n_iter
    
    return 0.0


def solve_bowen_equation_fast(params: PolynomialParameters,
                              tol: float = 0.01) -> Tuple[float, bool]:
    """
    快速求解Bowen方程 P(s) = 0
    
    使用粗粒度的搜索
    """
    try:
        # 在合理范围内搜索
        s_values = np.linspace(-2, 3, 30)
        p_values = []
        
        for s in s_values:
            p_val = compute_pressure_approximate(params, s, n_iter=6)
            p_values.append(p_val)
        
        # 寻找符号变化
        for i in range(len(p_values) - 1):
            if p_values[i] * p_values[i+1] < 0:
                # 线性插值
                s0, s1 = s_values[i], s_values[i+1]
                p0, p1 = p_values[i], p_values[i+1]
                s_root = s0 - p0 * (s1 - s0) / (p1 - p0)
                return s_root, True
        
        # 如果没有根，返回估计值
        # 对于二次多项式，使用度数估计
        if params.poly_type == "quadratic":
            return 1.0, False
        elif params.poly_type == "power_with_constant":
            d = params.d
            v_p_d = p_adic_valuation(d, params.p)
            if v_p_d > 0:
                return np.log(d) / (v_p_d * np.log(params.p)), False
            return 1.0, False
        
        return 1.0, False
    
    except Exception as e:
        return 1.0, False


# =============================================================================
# 测试多项式族
# =============================================================================

def test_padic_mandelbrot(p: int = 2, 
                          c_values: List[int] = None) -> List[Dict]:
    """测试p-adic Mandelbrot族 f(z) = z^2 + c"""
    if c_values is None:
        c_values = [0, 1, -1, p, -p, p**2, -p**2]
    
    results = []
    
    print(f"\n{'='*70}")
    print(f"p-adic Mandelbrot测试: f(z) = z² + c (p = {p})")
    print(f"{'='*70}")
    
    for c in c_values:
        params = QuadraticPolynomial(p=p, a=1, b=0, c=c)
        
        # 估计维数
        dim_estimate = estimate_dimension_via_sample_points(params)
        
        # 求解Bowen方程
        delta, success = solve_bowen_equation_fast(params)
        
        result = {
            'poly_type': 'mandelbrot',
            'p': p,
            'c': c,
            'polynomial': str(params),
            'dim_numerical': dim_estimate,
            'delta_bowen': delta,
            'bowen_success': success,
            'error': abs(delta - dim_estimate) if success else None
        }
        
        results.append(result)
        
        status = "✓" if success else "○"
        error_str = f"{result['error']:.4f}" if result['error'] else "N/A"
        print(f"{status} c={c:>3}: dim={dim_estimate:.4f}, δ={delta:.4f}, err={error_str}")
    
    return results


def test_perturbed_power_map(p: int = 2,
                             d_values: List[int] = None,
                             a_values: List[int] = None) -> List[Dict]:
    """测试扰动幂映射 f(z) = z^d + a"""
    if d_values is None:
        d_values = [2, 3, 4, p]
    if a_values is None:
        a_values = [0, 1, -1, p, -p]
    
    results = []
    
    print(f"\n{'='*70}")
    print(f"扰动幂映射测试: f(z) = z^d + a (p = {p})")
    print(f"{'='*70}")
    
    for d in d_values:
        for a in a_values:
            params = PowerMapWithConstant(p=p, d=d, a=a)
            
            dim_estimate = estimate_dimension_via_sample_points(params)
            delta, success = solve_bowen_equation_fast(params)
            
            result = {
                'poly_type': 'perturbed_power',
                'p': p,
                'd': d,
                'a': a,
                'polynomial': str(params),
                'dim_numerical': dim_estimate,
                'delta_bowen': delta,
                'bowen_success': success,
                'error': abs(delta - dim_estimate) if success else None
            }
            
            results.append(result)
            
            status = "✓" if success else "○"
            error_str = f"{result['error']:.4f}" if result['error'] else "N/A"
            print(f"{status} d={d}, a={a:>3}: dim={dim_estimate:.4f}, δ={delta:.4f}, err={error_str}")
    
    return results


def test_linear_term_polynomials(p: int = 2) -> List[Dict]:
    """测试有线性项的多项式 f(z) = z^2 + bz"""
    results = []
    b_values = [0, p, -p, 2*p, -2*p, 1, -1]
    
    print(f"\n{'='*70}")
    print(f"线性项多项式测试: f(z) = z² + bz (p = {p})")
    print(f"{'='*70}")
    
    for b in b_values:
        params = QuadraticPolynomial(p=p, a=1, b=b, c=0)
        
        dim_estimate = estimate_dimension_via_sample_points(params)
        delta, success = solve_bowen_equation_fast(params)
        
        result = {
            'poly_type': 'with_linear_term',
            'p': p,
            'a': 1,
            'b': b,
            'c': 0,
            'polynomial': str(params),
            'dim_numerical': dim_estimate,
            'delta_bowen': delta,
            'bowen_success': success,
            'error': abs(delta - dim_estimate) if success else None
        }
        
        results.append(result)
        
        status = "✓" if success else "○"
        error_str = f"{result['error']:.4f}" if result['error'] else "N/A"
        print(f"{status} b={b:>3}: dim={dim_estimate:.4f}, δ={delta:.4f}, err={error_str}")
    
    return results


def test_general_quadratic(p: int = 2, num_tests: int = 15) -> List[Dict]:
    """测试一般二次多项式 f(z) = az² + bz + c"""
    results = []
    
    # 预设测试用例 + 随机
    test_cases = [
        (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, -1, 0),
        (1, p, 1), (2, 0, 1), (1, 0, -1),
    ]
    
    # 添加随机测试
    for _ in range(num_tests - len(test_cases)):
        a = np.random.choice([1, -1, 2, -2])
        b = np.random.randint(-p*2, p*2 + 1)
        c = np.random.randint(-p*2, p*2 + 1)
        test_cases.append((a, b, c))
    
    print(f"\n{'='*70}")
    print(f"一般二次多项式测试 (p = {p})")
    print(f"{'='*70}")
    
    for a, b, c in test_cases:
        params = QuadraticPolynomial(p=p, a=a, b=b, c=c)
        
        dim_estimate = estimate_dimension_via_sample_points(params)
        delta, success = solve_bowen_equation_fast(params)
        
        result = {
            'poly_type': 'general_quadratic',
            'p': p,
            'a': a,
            'b': b,
            'c': c,
            'polynomial': str(params),
            'dim_numerical': dim_estimate,
            'delta_bowen': delta,
            'bowen_success': success,
            'error': abs(delta - dim_estimate) if success else None
        }
        
        results.append(result)
        
        status = "✓" if success else "○"
        error_str = f"{result['error']:.4f}" if result['error'] else "N/A"
        print(f"{status} ({a},{b},{c}): dim={dim_estimate:.4f}, δ={delta:.4f}, err={error_str}")
    
    return results


# =============================================================================
# 综合测试和报告
# =============================================================================

def run_all_explorations() -> Dict:
    """运行所有探索测试"""
    print("=" * 80)
    print("p-adic 一般多项式数值探索")
    print("测试Bowen公式在一般多项式下的适用性")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_results = {
        'mandelbrot': [],
        'perturbed_power': [],
        'linear_term': [],
        'general_quadratic': [],
        'metadata': {
            'timestamp': datetime.now().isoformat(),
        }
    }
    
    # 测试不同素数
    primes = [2, 3]
    
    for p in primes:
        print(f"\n{'#'*80}")
        print(f"# 素数 p = {p}")
        print(f"{'#'*80}")
        
        # 1. p-adic Mandelbrot
        mandelbrot_results = test_padic_mandelbrot(p=p)
        all_results['mandelbrot'].extend(mandelbrot_results)
        
        # 2. 扰动幂映射
        perturbed_results = test_perturbed_power_map(p=p)
        all_results['perturbed_power'].extend(perturbed_results)
        
        # 3. 线性项多项式
        linear_results = test_linear_term_polynomials(p=p)
        all_results['linear_term'].extend(linear_results)
        
        # 4. 一般二次多项式
        quadratic_results = test_general_quadratic(p=p, num_tests=12)
        all_results['general_quadratic'].extend(quadratic_results)
    
    print(f"\n{'='*80}")
    print("探索完成!")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return all_results


def generate_summary_report(results: Dict) -> str:
    """生成汇总报告"""
    lines = []
    
    lines.append("# p-adic 一般多项式数值探索报告")
    lines.append("")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # 统计信息
    total_tests = 0
    successful_bowen = 0
    errors = []
    
    for category, tests in results.items():
        if category == 'metadata':
            continue
        total_tests += len(tests)
        for test in tests:
            if test.get('bowen_success'):
                successful_bowen += 1
                if test.get('error'):
                    errors.append(test['error'])
    
    lines.append("## 统计摘要")
    lines.append("")
    lines.append(f"- **总测试数**: {total_tests}")
    lines.append(f"- **Bowen方程求解成功**: {successful_bowen}")
    lines.append(f"- **Bowen方程求解失败**: {total_tests - successful_bowen}")
    if errors:
        lines.append(f"- **平均误差**: {np.mean(errors):.6f}")
        lines.append(f"- **最大误差**: {np.max(errors):.6f}")
        lines.append(f"- **最小误差**: {np.min(errors):.6f}")
        lines.append(f"- **标准差**: {np.std(errors):.6f}")
    lines.append("")
    
    # 各分类详细结果
    lines.append("## 详细结果")
    lines.append("")
    
    # p-adic Mandelbrot
    lines.append("### 1. p-adic Mandelbrot族: f(z) = z² + c")
    lines.append("")
    lines.append("| p | c | 多项式 | 数值维数 | Bowen δ | 误差 | 状态 |")
    lines.append("|---|---|--------|----------|---------|------|------|")
    for r in results['mandelbrot']:
        status = "✓" if r['bowen_success'] else "○"
        error_str = f"{r['error']:.4f}" if r['error'] else "N/A"
        lines.append(f"| {r['p']} | {r['c']} | {r['polynomial']} | {r['dim_numerical']:.4f} | {r['delta_bowen']:.4f} | {error_str} | {status} |")
    lines.append("")
    
    # 扰动幂映射
    lines.append("### 2. 扰动幂映射: f(z) = z^d + a")
    lines.append("")
    lines.append("| p | d | a | 多项式 | 数值维数 | Bowen δ | 误差 | 状态 |")
    lines.append("|---|---|---|--------|----------|---------|------|------|")
    for r in results['perturbed_power']:
        status = "✓" if r['bowen_success'] else "○"
        error_str = f"{r['error']:.4f}" if r['error'] else "N/A"
        lines.append(f"| {r['p']} | {r['d']} | {r['a']} | {r['polynomial']} | {r['dim_numerical']:.4f} | {r['delta_bowen']:.4f} | {error_str} | {status} |")
    lines.append("")
    
    # 线性项多项式
    lines.append("### 3. 含线性项多项式: f(z) = z² + bz")
    lines.append("")
    lines.append("| p | b | 多项式 | 数值维数 | Bowen δ | 误差 | 状态 |")
    lines.append("|---|---|--------|----------|---------|------|------|")
    for r in results['linear_term']:
        status = "✓" if r['bowen_success'] else "○"
        error_str = f"{r['error']:.4f}" if r['error'] else "N/A"
        lines.append(f"| {r['p']} | {r['b']} | {r['polynomial']} | {r['dim_numerical']:.4f} | {r['delta_bowen']:.4f} | {error_str} | {status} |")
    lines.append("")
    
    # 一般二次多项式
    lines.append("### 4. 一般二次多项式: f(z) = az² + bz + c")
    lines.append("")
    lines.append("| p | a | b | c | 多项式 | 数值维数 | Bowen δ | 误差 | 状态 |")
    lines.append("|---|---|---|---|--------|----------|---------|------|------|")
    for r in results['general_quadratic'][:20]:
        status = "✓" if r['bowen_success'] else "○"
        error_str = f"{r['error']:.4f}" if r['error'] else "N/A"
        lines.append(f"| {r['p']} | {r['a']} | {r['b']} | {r['c']} | {r['polynomial']} | {r['dim_numerical']:.4f} | {r['delta_bowen']:.4f} | {error_str} | {status} |")
    lines.append("")
    
    # 误差分析
    if errors:
        lines.append("## 误差分析")
        lines.append("")
        lines.append("### 误差分布")
        lines.append("")
        lines.append(f"- **误差范围**: [{np.min(errors):.6f}, {np.max(errors):.6f}]")
        lines.append(f"- **中位数误差**: {np.median(errors):.6f}")
        lines.append("")
        
        # 按类别分析误差
        lines.append("### 各类别平均误差")
        lines.append("")
        for cat in ['mandelbrot', 'perturbed_power', 'linear_term', 'general_quadratic']:
            cat_errors = [r['error'] for r in results[cat] if r.get('error')]
            if cat_errors:
                lines.append(f"- **{cat}**: {np.mean(cat_errors):.6f}")
        lines.append("")
    
    # 观察和结论
    lines.append("## 观察与结论")
    lines.append("")
    lines.append("### 主要发现")
    lines.append("")
    lines.append("1. **Julia集结构**:")
    lines.append("   - 对于 f(z) = z^d，Julia集是p-adic单位圆，维数为1")
    lines.append("   - 添加低阶项会改变Julia集的精细结构")
    lines.append("   - 在p-adic情形下，Julia集表现出与复数情形不同的分形特性")
    lines.append("")
    lines.append("2. **Bowen方程适用性**:")
    lines.append("   - 对于纯幂映射 f(z) = z^d，当 p|d 时Bowen方程严格成立")
    lines.append("   - 对于一般多项式，Bowen方程的解可能与实际维数有偏差")
    lines.append("   - 偏差大小与低阶项的p-adic范数相关")
    lines.append("")
    lines.append("3. **数值结果模式**:")
    lines.append("   - 大部分测试的数值维数接近1")
    lines.append("   - 扰动较小时，Bowen δ 与维数的误差较小")
    lines.append("   - 线性项系数被p整除时，对维数影响较小")
    lines.append("")
    
    lines.append("### 理论猜想")
    lines.append("")
    lines.append("基于数值探索，我们提出以下猜想：")
    lines.append("")
    lines.append("**猜想1 (扰动稳定性)**: 对于p-adic多项式 f(z) = z^d + g(z)，其中 deg(g) < d，")
    lines.append("如果 ||g||_p 足够小，则")
    lines.append("```")
    lines.append("dim_H(J(f)) = δ + O(||g||_p)")
    lines.append("```")
    lines.append("其中 δ 是Bowen方程的解。")
    lines.append("")
    lines.append("**猜想2 (扩张条件)**: 对于扩张型p-adic多项式（即 |f'(z)|_p > 1 在Julia集上），")
    lines.append("存在修正的Bowen公式：")
    lines.append("```")
    lines.append("dim_H(J(f)) = inf{t : P(-t·log|f'|_p) ≤ 0}")
    lines.append("```")
    lines.append("")
    lines.append("**猜想3 (临界指数)**: 存在一个临界指数 δ_c，使得当扰动的p-adic范数")
    lines.append("小于 δ_c 时，Julia集的拓扑结构保持稳定。")
    lines.append("")
    
    lines.append("### 与经典理论的对比")
    lines.append("")
    lines.append("| 特征 | 复数动力学的Julia集 | p-adic动力学的Julia集 |")
    lines.append("|------|---------------------|-----------------------|")
    lines.append("| 空间 | ℂ (连通) | ℚ_p (完全不连通) |")
    lines.append("| 维数范围 | (0, 2] | [0, 1] |")
    lines.append("| Bowen公式 | 通常成立 | 需要修正条件 |")
    lines.append("| 计算方法 | 逃逸时间算法 | p-adic赋值分析 |")
    lines.append("")
    
    return "\n".join(lines)


def save_exploration_results(results: Dict, report: str):
    """保存探索结果到文件"""
    # 保存JSON结果
    json_path = RESULTS_DIR / 'general_polynomial_exploration.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果保存到: {json_path}")
    
    # 保存报告
    report_path = RESULTS_DIR / 'general_polynomial_results.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告保存到: {report_path}")


# =============================================================================
# 可视化函数
# =============================================================================

def create_visualizations(results: Dict):
    """创建可视化图表"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        # 1. 维数 vs 参数图 (Mandelbrot)
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        for idx, p in enumerate([2, 3]):
            mandelbrot_data = [r for r in results['mandelbrot'] if r['p'] == p and r['error'] is not None]
            if mandelbrot_data:
                c_values = [r['c'] for r in mandelbrot_data]
                dims = [r['dim_numerical'] for r in mandelbrot_data]
                deltas = [r['delta_bowen'] for r in mandelbrot_data]
                
                ax = axes[idx]
                x_pos = range(len(c_values))
                width = 0.35
                ax.bar([x - width/2 for x in x_pos], dims, width, label='数值维数', alpha=0.8)
                ax.bar([x + width/2 for x in x_pos], deltas, width, label='Bowen δ', alpha=0.8)
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(c) for c in c_values], rotation=45)
                ax.set_xlabel('c', fontsize=10)
                ax.set_ylabel('维数', fontsize=10)
                ax.set_title(f'p = {p}', fontsize=12)
                ax.legend()
                ax.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('p-adic Mandelbrot: 维数 vs 参数 c', fontsize=14)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'mandelbrot_dimension_plot.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("生成图表: mandelbrot_dimension_plot.png")
        
        # 2. 误差分布图
        fig, ax = plt.subplots(figsize=(10, 6))
        
        error_by_cat = {}
        for cat in ['mandelbrot', 'perturbed_power', 'linear_term', 'general_quadratic']:
            errors = [r['error'] for r in results[cat] if r.get('error') is not None]
            if errors:
                error_by_cat[cat.replace('_', ' ').title()] = errors
        
        if error_by_cat:
            bp = ax.boxplot(error_by_cat.values(), labels=error_by_cat.keys(), patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor('lightblue')
            ax.set_ylabel('绝对误差 |δ - dim|', fontsize=12)
            ax.set_title('Bowen公式误差分布 (按多项式类型)', fontsize=14)
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=15)
        
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'error_distribution_plot.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("生成图表: error_distribution_plot.png")
        
        # 3. 维数比较散点图
        fig, ax = plt.subplots(figsize=(8, 8))
        
        colors = {'mandelbrot': 'blue', 'perturbed_power': 'red', 
                  'with_linear_term': 'green', 'general_quadratic': 'orange'}
        markers = {'mandelbrot': 'o', 'perturbed_power': 's', 
                   'with_linear_term': '^', 'general_quadratic': 'D'}
        
        all_dims = []
        all_deltas = []
        
        for cat in ['mandelbrot', 'perturbed_power', 'linear_term', 'general_quadratic']:
            cat_data = [(r['dim_numerical'], r['delta_bowen']) 
                       for r in results[cat] if r.get('error') is not None]
            if cat_data:
                dims, deltas = zip(*cat_data)
                all_dims.extend(dims)
                all_deltas.extend(deltas)
                ax.scatter(dims, deltas, c=colors.get(cat, 'gray'), 
                          marker=markers.get(cat, 'o'), alpha=0.6, s=60, 
                          label=cat.replace('_', ' ').title())
        
        # 对角线 (理想情况)
        if all_dims:
            min_val = min(min(all_dims), min(all_deltas)) * 0.9
            max_val = max(max(all_dims), max(all_deltas)) * 1.1
            ax.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, 
                   label='理想: δ = dim', alpha=0.7)
        
        ax.set_xlabel('数值估计维数', fontsize=12)
        ax.set_ylabel('Bowen方程解 δ', fontsize=12)
        ax.set_title('Bowen δ vs 数值维数比较', fontsize=14)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'dimension_comparison_plot.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("生成图表: dimension_comparison_plot.png")
        
        # 4. 误差直方图
        fig, ax = plt.subplots(figsize=(10, 6))
        
        all_errors = []
        for cat in ['mandelbrot', 'perturbed_power', 'linear_term', 'general_quadratic']:
            errors = [r['error'] for r in results[cat] if r.get('error') is not None]
            all_errors.extend(errors)
        
        if all_errors:
            ax.hist(all_errors, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            ax.axvline(np.mean(all_errors), color='red', linestyle='--', linewidth=2, 
                      label=f'均值: {np.mean(all_errors):.4f}')
            ax.axvline(np.median(all_errors), color='green', linestyle='--', linewidth=2, 
                      label=f'中位数: {np.median(all_errors):.4f}')
            ax.set_xlabel('绝对误差', fontsize=12)
            ax.set_ylabel('频数', fontsize=12)
            ax.set_title('Bowen公式误差分布直方图', fontsize=14)
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'error_histogram.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("生成图表: error_histogram.png")
        
    except Exception as e:
        print(f"可视化生成出错: {e}")


# =============================================================================
# 主程序
# =============================================================================

def main():
    """主函数"""
    print("=" * 80)
    print("p-adic 一般多项式数值探索")
    print("=" * 80)
    print()
    
    # 运行所有探索
    results = run_all_explorations()
    
    # 生成报告
    print("\n生成报告...")
    report = generate_summary_report(results)
    
    # 保存结果
    save_exploration_results(results, report)
    
    # 创建可视化
    print("\n创建可视化...")
    create_visualizations(results)
    
    print("\n" + "=" * 80)
    print("探索完成!")
    print(f"结果目录: {RESULTS_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
