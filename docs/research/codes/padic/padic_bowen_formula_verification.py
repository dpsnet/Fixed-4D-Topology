#!/usr/bin/env python3
"""
p-adic Bowen公式数值验证代码

本代码实现：
1. p-adic压力函数计算
2. Bowen方程求解
3. 维数比较验证
4. 可视化结果

作者: Fixed-4D-Topology Research Group
日期: 2026-02-11
"""

import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Tuple, Callable, Optional
import json
from pathlib import Path

# 配置
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


@dataclass
class PadicParameters:
    """p-adic参数类"""
    p: int          # 素数
    d: int          # 映射度
    
    def __post_init__(self):
        assert self.p > 1 and all(self.p % i != 0 for i in range(2, int(self.p**0.5) + 1)), \
            f"{self.p} 不是素数"
        assert self.d >= 2, "d 必须 >= 2"
    
    @property
    def vp_d(self) -> int:
        """d的p-adic赋值 v_p(d)"""
        val = 0
        temp = self.d
        while temp % self.p == 0:
            temp //= self.p
            val += 1
        return val
    
    @property
    def is_pure_p_power(self) -> bool:
        """检查d是否是纯p幂"""
        temp = self.d
        while temp % self.p == 0:
            temp //= self.p
        return temp == 1
    
    @property
    def m_factor(self) -> int:
        """d = p^k * m 中的m因子"""
        temp = self.d
        while temp % self.p == 0:
            temp //= self.p
        return temp


def compute_pressure_exact(params: PadicParameters, s: float) -> float:
    """
    计算压力函数 P(s) = log(d) + s * v_p(d) * log(p)
    
    对于 f(z) = z^d，压力函数有显式公式
    
    参数:
        params: p-adic参数
        s: 势函数参数
    
    返回:
        P(s)的精确值
    """
    return np.log(params.d) + s * params.vp_d * np.log(params.p)


def compute_pressure_numerical(params: PadicParameters, s: float, n_max: int = 50) -> List[float]:
    """
    通过周期点数值计算压力函数
    
    参数:
        params: p-adic参数
        s: 势函数参数
        n_max: 最大迭代次数
    
    返回:
        各步压力估计的列表
    """
    pressures = []
    
    for n in range(1, n_max + 1):
        # n-周期点数 (非零): d^n - 1
        num_periodic = params.d**n - 1
        
        # |(f^n)'|_p = |d^n|_p = p^(-n * v_p(d))
        derivative_norm = params.p**(-n * params.vp_d)
        
        # 划分函数 Z_n(s)
        Z_n = num_periodic * (derivative_norm ** (-s))
        
        # 压力估计
        P_n = np.log(Z_n) / n
        pressures.append(P_n)
    
    return pressures


def solve_bowen_equation_exact(params: PadicParameters) -> float:
    """
    解析求解Bowen方程 P(-δ) = 0
    
    P(-δ) = log(d) - δ * v_p(d) * log(p) = 0
    => δ = log(d) / (v_p(d) * log(p))
    
    参数:
        params: p-adic参数
    
    返回:
        Bowen方程的解δ
    """
    if params.vp_d == 0:
        raise ValueError(f"p={params.p} 不整除 d={params.d}，Bowen方程无有限解")
    
    delta = np.log(params.d) / (params.vp_d * np.log(params.p))
    return delta


def solve_bowen_equation_numerical(params: PadicParameters, tol: float = 1e-12) -> float:
    """
    数值求解Bowen方程
    
    使用二分法
    
    参数:
        params: p-adic参数
        tol: 收敛阈值
    
    返回:
        Bowen方程的数值解
    """
    if params.vp_d == 0:
        raise ValueError(f"p={params.p} 不整除 d={params.d}，Bowen方程无有限解")
    
    # P(-s) = log(d) - s * v_p(d) * log(p)
    # 当s=0时，P(0) = log(d) > 0
    # 当s足够大时，P(-s) < 0
    
    s_low, s_high = 0.0, 10.0 * np.log(params.d) / np.log(params.p)
    
    # 确保区间内有根
    while compute_pressure_exact(params, -s_high) > 0:
        s_high *= 2
    
    # 二分法
    while s_high - s_low > tol:
        s_mid = (s_low + s_high) / 2
        P_mid = compute_pressure_exact(params, -s_mid)
        
        if P_mid > 0:
            s_low = s_mid
        else:
            s_high = s_mid
    
    return (s_low + s_high) / 2


def compute_julia_dimension(params: PadicParameters) -> float:
    """
    计算Julia集的Hausdorff维数
    
    对于 f(z) = z^d，Julia集是单位圆，维数=1
    
    参数:
        params: p-adic参数
    
    返回:
        Julia集的Hausdorff维数
    """
    return 1.0


def verify_bowen_formula(params: PadicParameters, verbose: bool = True) -> dict:
    """
    验证Bowen公式
    
    参数:
        params: p-adic参数
        verbose: 是否打印详细信息
    
    返回:
        验证结果字典
    """
    result = {
        'p': params.p,
        'd': params.d,
        'vp_d': params.vp_d,
        'is_pure_p_power': params.is_pure_p_power,
    }
    
    # 检查p是否整除d
    if params.vp_d == 0:
        result['status'] = 'skipped'
        result['reason'] = f'p={params.p} 不整除 d={params.d}'
        if verbose:
            print(f"跳过: p={params.p}, d={params.d} ({params.p} ∤ {params.d})")
        return result
    
    # 解析解
    delta_exact = solve_bowen_equation_exact(params)
    result['delta_exact'] = float(delta_exact)
    
    # 数值解
    delta_numerical = solve_bowen_equation_numerical(params)
    result['delta_numerical'] = float(delta_numerical)
    result['delta_error'] = float(abs(delta_exact - delta_numerical))
    
    # Julia集维数
    dim_julia = compute_julia_dimension(params)
    result['dim_julia'] = dim_julia
    
    # 验证
    result['difference'] = float(abs(delta_exact - dim_julia))
    result['relative_error'] = float(abs(delta_exact - dim_julia) / dim_julia)
    
    if params.is_pure_p_power:
        result['bowen_formula_holds'] = abs(delta_exact - dim_julia) < 1e-10
    else:
        result['bowen_formula_holds'] = False
        result['note'] = 'd不是纯p幂，Bowen公式可能需要修正'
    
    if verbose:
        print(f"\n验证: p={params.p}, d={params.d}")
        print(f"  纯p幂: {params.is_pure_p_power}")
        print(f"  Bowen δ (解析): {delta_exact:.10f}")
        print(f"  Bowen δ (数值): {delta_numerical:.10f}")
        print(f"  Julia维数: {dim_julia}")
        print(f"  差异: {result['difference']:.10f}")
        print(f"  Bowen公式: {'✓ 成立' if result['bowen_formula_holds'] else '✗ 不成立'}")
    
    return result


def test_convergence(params: PadicParameters, s: float = -1.0) -> None:
    """
    测试压力函数的收敛性
    
    参数:
        params: p-adic参数
        s: 势函数参数
    """
    print(f"\n收敛性测试: p={params.p}, d={params.d}, s={s}")
    
    pressures = compute_pressure_numerical(params, s, n_max=30)
    P_exact = compute_pressure_exact(params, s)
    
    print(f"精确值 P({s}) = {P_exact:.10f}")
    print("n\tP_n(s)\t\t误差")
    print("-" * 50)
    
    for n, P_n in enumerate(pressures[:20], 1):
        error = abs(P_n - P_exact)
        print(f"{n}\t{P_n:.10f}\t{error:.2e}")


def plot_pressure_function(params: PadicParameters, save_path: Optional[Path] = None) -> None:
    """
    绘制压力函数
    
    参数:
        params: p-adic参数
        save_path: 保存路径
    """
    s_range = np.linspace(-3, 3, 500)
    P_values = [compute_pressure_exact(params, s) for s in s_range]
    
    # 找到Bowen方程的解
    delta = solve_bowen_equation_exact(params)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(s_range, P_values, 'b-', linewidth=2, label=f'P(s) = log({params.d}) + s·{params.vp_d}·log({params.p})')
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.axvline(x=-delta, color='r', linestyle='--', linewidth=1.5, label=f'Bowen方程解: δ = {delta:.4f}')
    ax.set_xlabel('s', fontsize=12)
    ax.set_ylabel('P(s)', fontsize=12)
    ax.set_title(f'p-adic压力函数 (p={params.p}, d={params.d})', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"图形保存到: {save_path}")
    else:
        plt.savefig(RESULTS_DIR / f'pressure_p{params.p}_d{params.d}.png', dpi=150, bbox_inches='tight')
    
    plt.close()


def run_comprehensive_tests() -> List[dict]:
    """
    运行全面的测试
    
    返回:
        所有测试结果列表
    """
    # 测试用例
    test_cases = [
        # 纯p幂情形
        (2, 2), (2, 4), (2, 8), (2, 16),
        (3, 3), (3, 9), (3, 27),
        (5, 5), (5, 25),
        (7, 7),
        
        # 非纯p幂情形 (p | d)
        (2, 6), (2, 10), (2, 12),
        (3, 6), (3, 12), (3, 15),
        (5, 10), (5, 15),
        
        # p ∤ d 情形 (跳过)
        (2, 3), (3, 2), (5, 3),
    ]
    
    results = []
    
    print("=" * 70)
    print("p-adic Bowen公式全面验证")
    print("=" * 70)
    
    for p, d in test_cases:
        try:
            params = PadicParameters(p=p, d=d)
            result = verify_bowen_formula(params, verbose=True)
            results.append(result)
            
            # 绘制压力函数（仅限前几个）
            if len(results) <= 6:
                plot_pressure_function(params)
        
        except ValueError as e:
            print(f"\n跳过: p={p}, d={d} - {e}")
            results.append({
                'p': p, 'd': d, 'status': 'skipped', 'reason': str(e)
            })
    
    return results


def generate_report(results: List[dict]) -> str:
    """
    生成验证报告
    
    参数:
        results: 测试结果列表
    
    返回:
        报告字符串
    """
    report = []
    report.append("=" * 80)
    report.append("p-adic Bowen公式验证报告")
    report.append("=" * 80)
    report.append("")
    
    # 统计
    total = len([r for r in results if r.get('status') != 'skipped'])
    passed = len([r for r in results if r.get('bowen_formula_holds', False)])
    failed = total - passed
    
    report.append(f"总测试数: {total}")
    report.append(f"Bowen公式成立: {passed}")
    report.append(f"Bowen公式不成立: {failed}")
    report.append("")
    
    # 详细结果表
    report.append("详细结果:")
    report.append("-" * 80)
    report.append(f"{'p':>3} {'d':>4} {'v_p(d)':>6} {'纯p幂':>6} {'δ':>12} {'维数':>8} {'差异':>12} {'状态':>10}")
    report.append("-" * 80)
    
    for r in results:
        if r.get('status') == 'skipped':
            report.append(f"{r['p']:>3} {r['d']:>4} {'-':>6} {'-':>6} {'-':>12} {'-':>8} {'-':>12} {'跳过':>10}")
        else:
            pure = '是' if r['is_pure_p_power'] else '否'
            status = '✓ 成立' if r['bowen_formula_holds'] else '✗ 不成立'
            report.append(
                f"{r['p']:>3} {r['d']:>4} {r['vp_d']:>6} {pure:>6} "
                f"{r['delta_exact']:>12.6f} {r['dim_julia']:>8.1f} "
                f"{r['difference']:>12.6f} {status:>10}"
            )
    
    report.append("-" * 80)
    report.append("")
    
    # 纯p幂情形的详细验证
    report.append("纯p幂情形详细验证:")
    report.append("-" * 80)
    for r in results:
        if r.get('is_pure_p_power') and r.get('status') != 'skipped':
            report.append(f"p={r['p']}, d={r['d']}:")
            report.append(f"  Bowen δ = {r['delta_exact']:.12f}")
            report.append(f"  Julia维数 = {r['dim_julia']}")
            report.append(f"  数值误差 = {r['delta_error']:.2e}")
            report.append("")
    
    # 非纯p幂情形的分析
    non_pure = [r for r in results if not r.get('is_pure_p_power') and r.get('status') != 'skipped']
    if non_pure:
        report.append("非纯p幂情形分析:")
        report.append("-" * 80)
        report.append("当d包含非p因子时，Bowen方程给出的δ不等于Julia集维数")
        report.append("这表明需要修正的Bowen公式或更复杂的分析")
        report.append("")
        for r in non_pure:
            d = r['d']
            p = r['p']
            vp = r['vp_d']
            m = r['d'] // (p ** vp)
            report.append(f"p={p}, d={d} = {p}^{vp} × {m}:")
            report.append(f"  Bowen δ = log({d})/({vp}·log({p})) = {r['delta_exact']:.6f}")
            report.append(f"  Julia维数 = {r['dim_julia']}")
            report.append(f"  差异 = {r['difference']:.6f}")
            report.append("")
    
    report.append("=" * 80)
    
    return "\n".join(report)


def save_results(results: List[dict], report: str) -> None:
    """
    保存结果到文件
    
    参数:
        results: 测试结果列表
        report: 报告字符串
    """
    # 保存JSON结果
    json_path = RESULTS_DIR / 'bowen_verification_results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n结果保存到: {json_path}")
    
    # 保存报告
    report_path = RESULTS_DIR / 'bowen_verification_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告保存到: {report_path}")


def main():
    """主函数"""
    print("=" * 80)
    print("p-adic Bowen公式数值验证")
    print("=" * 80)
    print()
    
    # 运行全面测试
    results = run_comprehensive_tests()
    
    # 生成报告
    report = generate_report(results)
    print("\n" + report)
    
    # 保存结果
    save_results(results, report)
    
    # 收敛性测试示例
    print("\n" + "=" * 80)
    print("收敛性测试示例")
    print("=" * 80)
    
    test_cases = [
        PadicParameters(p=2, d=2),
        PadicParameters(p=3, d=3),
        PadicParameters(p=2, d=6),
    ]
    
    for params in test_cases:
        test_convergence(params, s=-1.0)
    
    print("\n" + "=" * 80)
    print("验证完成!")
    print(f"结果保存在: {RESULTS_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
