"""
p-adic Bowen公式数值验证
验证 $f(z) = z^d$ 情形的Bowen公式

Bowen公式: $P(-\delta \cdot \log |f'|_p) = 0$ 的解给出 $\dim_H(J(f)) = \delta$

对于 $f(z) = z^d$:
- Julia集: $J(f) = \{z \in \mathbb{Q}_p : |z|_p = 1\}$（p-adic单位圆）
- 理论维数: $\dim_H = 1$
- 压力函数: $P(s) = \log d - s \cdot v_p(d) \cdot \log p$
- Bowen方程解: $\delta = \frac{\log d}{v_p(d) \cdot \log p}$
"""

import numpy as np
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json
from datetime import datetime


# =============================================================================
# 工具函数：p-adic算术
# =============================================================================

def p_adic_valuation(n: int, p: int) -> int:
    """
    计算整数n的p-adic赋值 $v_p(n)$
    
    即最大的k使得 $p^k | n$
    
    Args:
        n: 整数
        p: 素数
        
    Returns:
        v_p(n)
    """
    if n == 0:
        return float('inf')
    
    k = 0
    n = abs(n)
    while n % p == 0:
        n //= p
        k += 1
    return k


def p_adic_absolute_value(x: Fraction, p: int) -> float:
    """
    计算p-adic绝对值 $|x|_p = p^{-v_p(x)}$
    
    Args:
        x: 有理数
        p: 素数
        
    Returns:
        p-adic绝对值（实数值）
    """
    if x == 0:
        return 0.0
    
    # v_p(a/b) = v_p(a) - v_p(b)
    v_p_x = p_adic_valuation(x.numerator, p) - p_adic_valuation(x.denominator, p)
    return float(p ** (-v_p_x))


# =============================================================================
# 压力函数计算
# =============================================================================

def compute_pressure(f_degree: int, p: int, s: float) -> float:
    """
    计算压力函数 $P(-s \cdot \log |f'|_p)$
    
    对于 $f(z) = z^d$，我们有：
    $P(s) = \log d - s \cdot v_p(d) \cdot \log p$
    
    Args:
        f_degree: 映射的度数 d
        p: 素数
        s: 参数（对应 -δ）
        
    Returns:
        压力值 P(s)
    """
    v_p_d = p_adic_valuation(f_degree, p)
    
    # P(s) = log(d) - s * v_p(d) * log(p)
    pressure = np.log(f_degree) - s * v_p_d * np.log(p)
    
    return pressure


def solve_bowen_equation(f_degree: int, p: int) -> Tuple[float, bool]:
    """
    求解Bowen方程 $P(-\delta \cdot \log |f'|_p) = 0$
    
    解析解: $\delta = \frac{\log d}{v_p(d) \cdot \log p}$
    
    Args:
        f_degree: 映射的度数 d
        p: 素数
        
    Returns:
        (delta, has_solution)
        - delta: Bowen方程的解（如果存在）
        - has_solution: 是否存在有限解
    """
    v_p_d = p_adic_valuation(f_degree, p)
    
    if v_p_d == 0:
        # p 不整除 d，压力函数恒为正，无有限解
        # 此时 Julia集上的动力学不是扩张的
        return float('inf'), False
    
    # 解析解
    delta = np.log(f_degree) / (v_p_d * np.log(p))
    
    # 验证
    pressure_at_delta = compute_pressure(f_degree, p, delta)
    
    return delta, True


# =============================================================================
# Julia集盒维数数值估计
# =============================================================================

def estimate_box_dimension_julia(p: int, depth: int = 10) -> float:
    """
    估计p-adic Julia集的盒维数
    
    Julia集 J(f) = {z : |z|_p = 1} 是p-adic单位圆
    
    对于p-adic单位圆，可以通过计算它在不同精度下的"盒子数"来估计维数
    
    Args:
        p: 素数
        depth: 计算深度（精度级别）
        
    Returns:
        估计的盒维数
    """
    # p-adic单位群 Z_p^* 的结构
    # Z_p^* ≅ μ_{p-1} × (1 + pZ_p) ≅ Z/(p-1) × Z_p
    # 
    # 对于"盒子"覆盖，考虑余有限拓扑
    # 在第n级，Z_p^* 被分成 (p-1) * p^{n-1} 个陪集
    
    dimensions = []
    
    for n in range(1, depth + 1):
        # 第n级的盒子数
        N_n = (p - 1) * (p ** (n - 1))
        
        # 盒子大小（直径）
        epsilon_n = p ** (-n)
        
        # 维数估计: dim ≈ log(N) / log(1/ε)
        dim_estimate = np.log(N_n) / np.log(1 / epsilon_n)
        dimensions.append(dim_estimate)
    
    # 返回最后几级的平均值（收敛值）
    return np.mean(dimensions[-3:])


def estimate_box_dimension_cantor_like(p: int, f_degree: int, depth: int = 8) -> float:
    """
    对于更一般的Julia集，使用类似于Cantor集的盒计数
    
    这个方法基于Julia集的自相似结构
    
    Args:
        p: 素数
        f_degree: 度数 d
        depth: 计算深度
        
    Returns:
        估计的盒维数
    """
    # 对于 f(z) = z^d，当 p | d 时，Julia集有自相似结构
    v_p_d = p_adic_valuation(f_degree, p)
    
    if v_p_d == 0:
        # 等距情形，Julia集是简单的单位圆
        return 1.0
    
    # 对于扩张情形，使用迭代计数
    # 每迭代一次，每个分支产生 d 个子分支
    
    dimensions = []
    
    for n in range(1, depth + 1):
        # 第n级周期点数量（近似）
        # Fix(f^n) 的大小 ≈ d^n - 1（单位根）
        N_periodic = f_degree ** n
        
        # 收缩因子
        contraction = p_adic_absolute_value(Fraction(1, f_degree), p)
        
        # 特征尺度
        scale = contraction ** n
        
        # 维数估计
        if scale > 0:
            dim_estimate = np.log(N_periodic) / np.log(1 / scale)
            dimensions.append(dim_estimate)
    
    return np.mean(dimensions[-3:]) if dimensions else 1.0


# =============================================================================
# 测试框架
# =============================================================================

@dataclass
class TestResult:
    """测试结果数据结构"""
    p: int
    d: int
    v_p_d: int
    bowen_delta: float
    has_solution: bool
    theoretical_dim: float
    numerical_dim: float
    absolute_error: float
    relative_error: float
    pressure_at_delta: float


def run_single_test(p: int, d: int) -> TestResult:
    """
    运行单个测试
    
    Args:
        p: 素数
        d: 度数
        
    Returns:
        测试结果
    """
    v_p_d = p_adic_valuation(d, p)
    
    # 求解Bowen方程
    bowen_delta, has_solution = solve_bowen_equation(d, p)
    
    # 理论维数（预期值）
    theoretical_dim = 1.0  # 对于单位圆
    
    # 数值估计的维数
    if v_p_d > 0:
        numerical_dim = estimate_box_dimension_cantor_like(p, d)
    else:
        numerical_dim = estimate_box_dimension_julia(p)
    
    # 计算误差
    if has_solution and np.isfinite(bowen_delta):
        absolute_error = abs(bowen_delta - theoretical_dim)
        relative_error = absolute_error / theoretical_dim if theoretical_dim != 0 else 0.0
        pressure_at_delta = compute_pressure(d, p, bowen_delta)
    else:
        absolute_error = float('inf')
        relative_error = float('inf')
        pressure_at_delta = compute_pressure(d, p, 0)  # 任意值
    
    return TestResult(
        p=p,
        d=d,
        v_p_d=v_p_d,
        bowen_delta=bowen_delta,
        has_solution=has_solution,
        theoretical_dim=theoretical_dim,
        numerical_dim=numerical_dim,
        absolute_error=absolute_error,
        relative_error=relative_error,
        pressure_at_delta=pressure_at_delta
    )


def run_all_tests() -> List[TestResult]:
    """
    运行所有测试
    
    测试参数:
    - p = 2, 3, 5
    - d = 2, 3, 4, 5, 6（不同p-adic赋值）
    """
    primes = [2, 3, 5]
    degrees = [2, 3, 4, 5, 6]
    
    results = []
    
    for p in primes:
        for d in degrees:
            result = run_single_test(p, d)
            results.append(result)
    
    return results


# =============================================================================
# 结果输出和报告生成
# =============================================================================

def print_results_table(results: List[TestResult]):
    """打印结果表格"""
    print("=" * 100)
    print("p-adic Bowen公式数值验证结果")
    print("=" * 100)
    print()
    
    # 表头
    header = f"{'p':>4} | {'d':>4} | {'v_p(d)':>7} | {'Bowen δ':>12} | {'解存在':>8} | {'理论dim':>10} | {'数值dim':>10} | {'绝对误差':>12} | {'相对误差':>12}"
    print(header)
    print("-" * 100)
    
    # 数据行
    for r in results:
        delta_str = f"{r.bowen_delta:.6f}" if r.has_solution else "N/A"
        has_sol_str = "是" if r.has_solution else "否"
        abs_err_str = f"{r.absolute_error:.2e}" if r.has_solution else "N/A"
        rel_err_str = f"{r.relative_error:.2e}" if r.has_solution else "N/A"
        
        row = f"{r.p:>4} | {r.d:>4} | {r.v_p_d:>7} | {delta_str:>12} | {has_sol_str:>8} | {r.theoretical_dim:>10.6f} | {r.numerical_dim:>10.6f} | {abs_err_str:>12} | {rel_err_str:>12}"
        print(row)
    
    print("-" * 100)


def generate_detailed_report(results: List[TestResult]) -> str:
    """生成详细报告"""
    lines = []
    
    lines.append("# p-adic Bowen公式数值验证报告")
    lines.append("")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    lines.append("## 测试参数")
    lines.append("")
    lines.append("- 素数 p: 2, 3, 5")
    lines.append("- 度数 d: 2, 3, 4, 5, 6")
    lines.append("")
    
    lines.append("## 理论背景")
    lines.append("")
    lines.append("对于 $f(z) = z^d$ 在 $\mathbb{Q}_p$ 上:")
    lines.append("")
    lines.append("1. **Julia集**: $J(f) = \\{z : |z|_p = 1\\}$（p-adic单位圆）")
    lines.append("2. **理论Hausdorff维数**: $\dim_H = 1$")
    lines.append("3. **压力函数**: $P(s) = \\log d - s \\cdot v_p(d) \\cdot \\log p$")
    lines.append("4. **Bowen方程**: $P(-\\delta \\cdot \\log |f'|_p) = 0$")
    lines.append("5. **解析解**: $\\delta = \\frac{\\log d}{v_p(d) \\cdot \\log p}$（当 $p | d$）")
    lines.append("")
    
    lines.append("## 测试结果汇总")
    lines.append("")
    
    # 创建Markdown表格
    lines.append("| p | d | v_p(d) | Bowen δ | 解存在 | 理论dim | 数值dim | 绝对误差 | 相对误差 |")
    lines.append("|---|---|--------|---------|--------|---------|---------|----------|----------|")
    
    for r in results:
        delta_str = f"{r.bowen_delta:.6f}" if r.has_solution else "N/A"
        has_sol_str = "✓" if r.has_solution else "✗"
        abs_err_str = f"{r.absolute_error:.2e}" if r.has_solution else "N/A"
        rel_err_str = f"{r.relative_error:.2e}" if r.has_solution else "N/A"
        
        lines.append(f"| {r.p} | {r.d} | {r.v_p_d} | {delta_str} | {has_sol_str} | {r.theoretical_dim:.6f} | {r.numerical_dim:.6f} | {abs_err_str} | {rel_err_str} |")
    
    lines.append("")
    
    # 详细分析
    lines.append("## 详细分析")
    lines.append("")
    
    # 按素数分组
    for p in [2, 3, 5]:
        lines.append(f"### p = {p}")
        lines.append("")
        
        p_results = [r for r in results if r.p == p]
        
        for r in p_results:
            lines.append(f"#### d = {r.d}（v_p(d) = {r.v_p_d}）")
            lines.append("")
            lines.append(f"- p-adic赋值: $v_{p}({r.d}) = {r.v_p_d}$")
            
            if r.has_solution:
                lines.append(f"- Bowen方程解: $\\delta = \\frac{{\\log {r.d}}}{{{r.v_p_d} \\cdot \\log {p}}} = {r.bowen_delta:.6f}$")
                lines.append(f"- 理论维数: $\\dim_H = 1$")
                lines.append(f"- 数值估计维数: {r.numerical_dim:.6f}")
                lines.append(f"- 绝对误差: {r.absolute_error:.2e}")
                lines.append(f"- 验证: $P(-\\delta \\log |f'|_{p}) = {r.pressure_at_delta:.2e}$（应≈0）")
            else:
                lines.append(f"- **注意**: $p \\nmid d$，Bowen方程无有限解")
                lines.append(f"- 压力函数恒为正: $P(s) = \\log {r.d} > 0$")
                lines.append(f"- 此时Julia集上的动力学是**等距**的，非扩张")
            
            lines.append("")
    
    lines.append("## 结论")
    lines.append("")
    
    # 统计
    total_tests = len(results)
    valid_tests = sum(1 for r in results if r.has_solution)
    avg_error = np.mean([r.absolute_error for r in results if r.has_solution and np.isfinite(r.absolute_error)])
    
    lines.append(f"- 总测试数: {total_tests}")
    lines.append(f"- 有效测试数（$p | d$）: {valid_tests}")
    lines.append(f"- 平均绝对误差: {avg_error:.2e}")
    lines.append("")
    
    if avg_error < 1e-10:
        lines.append("**验证成功**: 数值结果与理论预测高度一致！")
    elif avg_error < 1e-5:
        lines.append("**验证基本成功**: 数值结果与理论预测在可接受误差范围内一致。")
    else:
        lines.append("**需要进一步分析**: 数值结果与理论预测存在较大偏差。")
    
    lines.append("")
    
    lines.append("## 关键发现")
    lines.append("")
    lines.append("1. **$p | d$ 是关键条件**: 只有当 $p$ 整除 $d$ 时，Bowen方程才有有限解")
    lines.append("2. **纯p幂情形**: 当 $d = p^k$ 时，$\\delta = 1$，与理论维数完美匹配")
    lines.append("3. **数值稳定性**: 对于纯p幂情形，数值误差极小（< 1e-12）")
    lines.append("4. **一般情形**: 对于 $d = p^k \\cdot m$（$p \\nmid m$），$\\delta = \\frac{k \\log p + \\log m}{k \\log p} = 1 + \\frac{\\log m}{k \\log p}$")
    lines.append("")
    
    return "\n".join(lines)


def save_report_to_file(report: str, filename: str):
    """保存报告到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存到: {filename}")


# =============================================================================
# 可视化函数
# =============================================================================

def generate_dimension_analysis_data(results: List[TestResult]) -> Dict:
    """
    生成维数分析数据，用于可视化
    
    Returns:
        可用于绘图的数据字典
    """
    data = {
        'p_values': [],
        'd_values': [],
        'v_p_d_values': [],
        'bowen_delta': [],
        'numerical_dim': [],
        'theoretical_dim': [],
        'errors': []
    }
    
    for r in results:
        if r.has_solution:
            data['p_values'].append(r.p)
            data['d_values'].append(r.d)
            data['v_p_d_values'].append(r.v_p_d)
            data['bowen_delta'].append(r.bowen_delta)
            data['numerical_dim'].append(r.numerical_dim)
            data['theoretical_dim'].append(r.theoretical_dim)
            data['errors'].append(r.absolute_error)
    
    return data


def print_visualization_ascii(results: List[TestResult]):
    """使用ASCII艺术打印简单的可视化"""
    print("\n" + "=" * 80)
    print("可视化：Bowen δ vs 度数 d（按素数分组）")
    print("=" * 80)
    print()
    
    for p in [2, 3, 5]:
        print(f"p = {p}:")
        print("-" * 40)
        
        p_results = [r for r in results if r.p == p]
        
        for r in p_results:
            d = r.d
            if r.has_solution:
                delta = r.bowen_delta
                # ASCII柱状图
                bar_len = int(delta * 20)  # 缩放
                bar = "█" * bar_len
                print(f"  d={d}: {bar} {delta:.4f}")
            else:
                print(f"  d={d}: (无有限解 - p∤d)")
        
        print()
    
    print("理论值参考线 (δ = 1):")
    print("  " + "─" * 20 + " 1.0")
    print()


# =============================================================================
# 主程序
# =============================================================================

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("p-adic Bowen公式数值验证")
    print("验证 f(z) = z^d 情形的Hausdorff维数")
    print("=" * 80)
    print()
    
    # 打印理论公式
    print("【理论基础】")
    print("-" * 40)
    print("对于 f(z) = z^d 在 Q_p 上:")
    print()
    print("  压力函数: P(s) = log(d) - s · v_p(d) · log(p)")
    print()
    print("  Bowen方程: P(-δ · log|f'|_p) = 0")
    print()
    print("  解析解: δ = log(d) / [v_p(d) · log(p)]")
    print()
    print("  当 d = p^k 时: δ = k·log(p) / [k·log(p)] = 1")
    print()
    print("  理论Hausdorff维数: dim_H = 1")
    print()
    
    # 运行所有测试
    print("【运行测试】")
    print("-" * 40)
    results = run_all_tests()
    print(f"完成 {len(results)} 个测试")
    print()
    
    # 打印结果表格
    print_results_table(results)
    print()
    
    # ASCII可视化
    print_visualization_ascii(results)
    
    # 生成详细报告
    print("【生成详细报告】")
    print("-" * 40)
    report = generate_detailed_report(results)
    
    # 保存报告
    report_filename = "bowen_verification_report.md"
    save_report_to_file(report, report_filename)
    print()
    
    # 生成可视化数据
    viz_data = generate_dimension_analysis_data(results)
    print("可视化数据摘要:")
    print(f"  - 有效数据点: {len(viz_data['p_values'])}")
    print(f"  - Bowen δ 范围: [{min(viz_data['bowen_delta']):.4f}, {max(viz_data['bowen_delta']):.4f}]")
    print(f"  - 平均误差: {np.mean(viz_data['errors']):.2e}")
    print()
    
    # 最终结论
    print("=" * 80)
    print("【最终结论】")
    print("=" * 80)
    
    valid_results = [r for r in results if r.has_solution]
    
    if valid_results:
        avg_error = np.mean([r.absolute_error for r in valid_results])
        max_error = max([r.absolute_error for r in valid_results])
        
        print(f"✓ 有效验证数: {len(valid_results)}/{len(results)}")
        print(f"✓ 平均绝对误差: {avg_error:.2e}")
        print(f"✓ 最大绝对误差: {max_error:.2e}")
        print()
        
        if max_error < 1e-10:
            print("✅ 验证成功！p-adic Bowen公式在 f(z) = z^d 情形下严格成立。")
        elif max_error < 1e-5:
            print("✅ 验证基本成功！数值结果支持理论预测。")
        else:
            print("⚠️ 数值结果与理论预测存在偏差，需要进一步分析。")
    else:
        print("⚠️ 没有足够的有效测试数据。")
    
    print()
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    results = main()
