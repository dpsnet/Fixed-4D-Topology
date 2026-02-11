#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ruelle-Perron-Frobenius算子谱探索脚本

任务: P3-C2-001 - 一般p-adic多项式Gibbs测度存在性证明
功能:
    - 离散化RPF算子
    - 计算谱（特征值）
    - 识别主特征值
    - 分析谱隙
    - 研究谱与Gibbs测度的联系

作者: Research Team
日期: 2026-02-11
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig, eigh
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json
import logging
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# p-adic工具和多项式定义
# ============================================================================

class PAdicTools:
    """p-adic数计算工具"""
    
    @staticmethod
    def valuation(n: int, p: int) -> int:
        """计算p-adic赋值 v_p(n)"""
        if n == 0:
            return float('inf')
        v = 0
        temp = abs(n)
        while temp % p == 0 and temp > 0:
            temp //= p
            v += 1
        return v
    
    @staticmethod
    def abs_p(n: int, p: int) -> float:
        """计算p-adic绝对值 |n|_p = p^{-v_p(n)}"""
        return p ** (-PAdicTools.valuation(n, p))


@dataclass
class PAdicPoly:
    """简化版p-adic多项式"""
    coeffs: List[int]  # 从低次到高次
    p: int
    
    def evaluate(self, z: complex) -> complex:
        """在复数点求值"""
        result = 0
        for i, c in enumerate(self.coeffs):
            result += c * (z ** i)
        return result
    
    def derivative_coeffs(self) -> List[int]:
        """返回导数系数"""
        return [c * i for i, c in enumerate(self.coeffs) if i > 0]
    
    def derivative_at(self, z: int) -> float:
        """在整数点求导数值的p-adic绝对值"""
        deriv_coeffs = self.derivative_coeffs()
        if not deriv_coeffs:
            return 0.0
        
        result = 0
        for i, c in enumerate(deriv_coeffs):
            result += c * (z ** i)
        
        return PAdicTools.abs_p(int(result), self.p)
    
    def __repr__(self):
        terms = []
        for i, c in enumerate(self.coeffs):
            if c != 0:
                if i == 0:
                    terms.append(f"{c}")
                elif i == 1:
                    terms.append(f"{c}z")
                else:
                    terms.append(f"{c}z^{i}")
        return " + ".join(terms) if terms else "0"


def create_test_polynomials(p: int) -> Dict[str, PAdicPoly]:
    """创建测试多项式"""
    return {
        'z2': PAdicPoly([0, 0, 1], p),           # z^2
        'z2_plus_p': PAdicPoly([p, 0, 1], p),    # z^2 + p
        'z2_plus_1': PAdicPoly([1, 0, 1], p),    # z^2 + 1
        'z3': PAdicPoly([0, 0, 0, 1], p),        # z^3
        'z3_plus_pz': PAdicPoly([0, p, 0, 1], p), # z^3 + p*z
    }


# ============================================================================
# RPF算子离散化与谱计算
# ============================================================================

class DiscretizedRPF:
    """
    离散化的Ruelle-Perron-Frobenius算子
    
    算子定义: (L_s f)(x) = Σ_{y∈φ^{-1}(x)} |φ'(y)|_p^{-s} f(y)
    """
    
    def __init__(self, poly: PAdicPoly, s: float, 
                 n_points: int = 100, domain: Tuple[float, float] = (-2, 2)):
        """
        初始化离散RPF算子
        
        Args:
            poly: p-adic多项式
            s: 维数参数
            n_points: 离散化点数
            domain: 定义域
        """
        self.poly = poly
        self.s = s
        self.p = poly.p
        self.n_points = n_points
        self.domain = domain
        
        # 创建离散网格
        self.points = np.linspace(domain[0], domain[1], n_points)
        self.dx = (domain[1] - domain[0]) / (n_points - 1)
        
        # 矩阵表示
        self.matrix = None
        self.eigenvalues = None
        self.eigenvectors = None
        
    def weight_function(self, y: float) -> float:
        """
        权重函数 w(y) = |φ'(y)|_p^{-s}
        
        Args:
            y: 点
            
        Returns:
            权重值
        """
        deriv_abs = self.poly.derivative_at(int(y))
        if deriv_abs == 0:
            return 0.0
        return deriv_abs ** (-self.s)
    
    def construct_matrix_dense(self) -> np.ndarray:
        """
        构造稠密矩阵表示
        
        L[i,j] = weight(y_j) 如果 f(y_j) ≈ x_i
        
        Returns:
            n_points × n_points 矩阵
        """
        n = self.n_points
        L = np.zeros((n, n))
        
        logger.info(f"构造 {n}×{n} RPF矩阵...")
        
        for j, y in enumerate(self.points):
            # 计算 f(y)
            f_y = self.poly.evaluate(y)
            
            # 找到最接近的网格点
            i = np.argmin(np.abs(self.points - f_y))
            
            # 添加权重
            weight = self.weight_function(y)
            L[i, j] += weight
        
        self.matrix = L
        return L
    
    def construct_matrix_sparse(self, tolerance: float = 0.1) -> csr_matrix:
        """
        构造稀疏矩阵表示
        
        Args:
            tolerance: 映射容差
            
        Returns:
            稀疏矩阵
        """
        n = self.n_points
        row_indices = []
        col_indices = []
        data = []
        
        for j, y in enumerate(self.points):
            f_y = self.poly.evaluate(y)
            
            # 找到在容差范围内的所有点
            distances = np.abs(self.points - f_y)
            close_indices = np.where(distances < tolerance)[0]
            
            weight = self.weight_function(y)
            
            for i in close_indices:
                row_indices.append(i)
                col_indices.append(j)
                data.append(weight / len(close_indices))
        
        L = csr_matrix((data, (row_indices, col_indices)), shape=(n, n))
        self.matrix = L
        return L
    
    def compute_spectrum(self, k: int = 10, use_sparse: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算矩阵的谱
        
        Args:
            k: 计算前k个特征值
            use_sparse: 是否使用稀疏矩阵
            
        Returns:
            (特征值, 特征向量)
        """
        if self.matrix is None:
            if use_sparse:
                self.construct_matrix_sparse()
            else:
                self.construct_matrix_dense()
        
        logger.info("计算特征值...")
        
        if use_sparse and isinstance(self.matrix, csr_matrix):
            eigenvalues, eigenvectors = eigs(self.matrix, k=k, which='LM')
            eigenvalues = eigenvalues.real
        else:
            eigenvalues, eigenvectors = eig(self.matrix)
        
        # 按实部降序排列
        idx = np.argsort(-eigenvalues.real)
        self.eigenvalues = eigenvalues[idx]
        self.eigenvectors = eigenvectors[:, idx]
        
        return self.eigenvalues, self.eigenvectors
    
    def get_principal_eigenpair(self) -> Tuple[complex, np.ndarray]:
        """
        获取主特征对
        
        Returns:
            (主特征值, 主特征向量)
        """
        if self.eigenvalues is None:
            self.compute_spectrum()
        
        return self.eigenvalues[0], self.eigenvectors[:, 0]
    
    def compute_spectral_gap(self) -> Dict:
        """
        计算谱隙相关指标
        
        Returns:
            谱隙分析结果
        """
        if self.eigenvalues is None:
            self.compute_spectrum()
        
        evals_real = self.eigenvalues.real
        
        # 主特征值
        lambda_1 = evals_real[0]
        
        # 第二特征值
        lambda_2 = evals_real[1] if len(evals_real) > 1 else 0
        
        # 谱隙
        spectral_gap = lambda_1 - lambda_2 if lambda_2 < lambda_1 else 0
        
        # 相对谱隙
        relative_gap = spectral_gap / abs(lambda_1) if lambda_1 != 0 else 0
        
        # 谱半径比 (次主导/主导)
        ratio = abs(lambda_2 / lambda_1) if lambda_1 != 0 else float('inf')
        
        return {
            'lambda_1': float(lambda_1),
            'lambda_2': float(lambda_2),
            'spectral_gap': float(spectral_gap),
            'relative_gap': float(relative_gap),
            'second_to_principal_ratio': float(ratio),
            'has_spectral_gap': spectral_gap > 1e-6
        }


# ============================================================================
# 谱分析与可视化
# ============================================================================

class SpectrumAnalyzer:
    """RPF谱分析器"""
    
    def __init__(self, rpf: DiscretizedRPF):
        self.rpf = rpf
        self.poly = rpf.poly
        self.s = rpf.s
        
    def analyze_convergence(self, n_list: List[int]) -> Dict:
        """
        分析不同离散化程度下的收敛性
        
        Args:
            n_list: 离散化点数列表
            
        Returns:
            收敛性分析结果
        """
        results = {
            'n_points': n_list,
            'principal_eigenvalues': [],
            'spectral_gaps': [],
            'second_eigenvalues': []
        }
        
        for n in n_list:
            logger.info(f"分析 n={n}...")
            rpf = DiscretizedRPF(self.poly, self.s, n_points=n)
            rpf.compute_spectrum()
            
            gap_info = rpf.compute_spectral_gap()
            results['principal_eigenvalues'].append(gap_info['lambda_1'])
            results['spectral_gaps'].append(gap_info['spectral_gap'])
            results['second_eigenvalues'].append(gap_info['lambda_2'])
        
        return results
    
    def analyze_parameter_dependence(self, s_values: np.ndarray) -> Dict:
        """
        分析谱对参数s的依赖性
        
        Args:
            s_values: 参数值数组
            
        Returns:
            参数依赖性分析
        """
        results = {
            's_values': s_values.tolist(),
            'lambda_1': [],
            'lambda_2': [],
            'spectral_gap': [],
            'log_lambda_1': []
        }
        
        for s in s_values:
            logger.info(f"分析 s={s:.3f}...")
            rpf = DiscretizedRPF(self.poly, s, n_points=self.rpf.n_points)
            rpf.compute_spectrum()
            
            gap_info = rpf.compute_spectral_gap()
            results['lambda_1'].append(gap_info['lambda_1'])
            results['lambda_2'].append(gap_info['lambda_2'])
            results['spectral_gap'].append(gap_info['spectral_gap'])
            results['log_lambda_1'].append(np.log(max(gap_info['lambda_1'], 1e-10)))
        
        return results
    
    def plot_spectrum(self, save_path: Optional[str] = None):
        """
        绘制谱分布图
        
        Args:
            save_path: 保存路径
        """
        if self.rpf.eigenvalues is None:
            self.rpf.compute_spectrum(k=50)
        
        evals = self.rpf.eigenvalues
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. 复平面上的特征值分布
        ax = axes[0, 0]
        ax.scatter(evals.real, evals.imag, alpha=0.6, s=50)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        ax.set_xlabel('Real Part')
        ax.set_ylabel('Imaginary Part')
        ax.set_title(f'Eigenvalue Distribution (p={self.poly.p}, s={self.s})')
        ax.grid(True, alpha=0.3)
        
        # 标记主特征值
        principal = evals[0]
        ax.scatter([principal.real], [principal.imag], 
                  color='red', s=200, marker='*', label='Principal', zorder=5)
        ax.legend()
        
        # 2. 特征值排序图
        ax = axes[0, 1]
        sorted_evals = np.sort(evals.real)[::-1]
        ax.semilogy(range(len(sorted_evals)), sorted_evals, 'b-o', markersize=4)
        ax.set_xlabel('Index')
        ax.set_ylabel('Eigenvalue (log scale)')
        ax.set_title('Eigenvalue Decay')
        ax.grid(True, alpha=0.3)
        
        # 3. 主特征向量
        ax = axes[1, 0]
        principal_vec = np.abs(self.rpf.eigenvectors[:, 0])
        ax.plot(self.rpf.points, principal_vec, 'g-', linewidth=2)
        ax.set_xlabel('x')
        ax.set_ylabel('|h(x)|')
        ax.set_title('Principal Eigenfunction')
        ax.grid(True, alpha=0.3)
        
        # 4. 矩阵热图
        ax = axes[1, 1]
        im = ax.imshow(self.rpf.matrix, cmap='hot', interpolation='nearest')
        ax.set_title('RPF Matrix Structure')
        ax.set_xlabel('Column (y)')
        ax.set_ylabel('Row (x)')
        plt.colorbar(im, ax=ax)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"谱分布图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()


# ============================================================================
# Gibbs测度关联分析
# ============================================================================

class GibbsConnectionAnalyzer:
    """分析谱与Gibbs测度的联系"""
    
    def __init__(self, poly: PAdicPoly):
        self.poly = poly
        self.p = poly.p
    
    def verify_rpf_theorem(self, s: float, n_points: int = 100) -> Dict:
        """
        验证RPF定理的关键断言
        
        1. 谱半径 = e^{P(φ)}
        2. 主特征值简单
        3. 正特征函数存在
        4. 谱隙存在
        
        Args:
            s: 参数
            n_points: 离散化点数
            
        Returns:
            验证结果
        """
        rpf = DiscretizedRPF(self.poly, s, n_points=n_points)
        
        # 计算谱
        eigenvalues, eigenvectors = rpf.compute_spectrum(k=20)
        
        # 1. 谱半径
        spectral_radius = np.max(np.abs(eigenvalues))
        
        # 2. 主特征值是否简单
        principal = eigenvalues[0]
        is_simple = np.abs(eigenvalues[1] - principal) > 1e-6
        
        # 3. 正特征函数
        principal_vec = eigenvectors[:, 0]
        is_positive = np.all(principal_vec.real > -1e-10)
        min_val = np.min(principal_vec.real)
        
        # 4. 谱隙
        gap_info = rpf.compute_spectral_gap()
        
        # 验证收敛性
        # λ^{-n} L^n ψ → (∫ψ dν) h
        test_func = np.ones(n_points)
        n_iterations = 5
        
        convergences = []
        for n in range(1, n_iterations + 1):
            L_n = np.linalg.matrix_power(rpf.matrix, n)
            normalized = L_n @ test_func / (principal ** n)
            
            # 应该收敛到主特征向量的倍数
            correlation = np.abs(np.dot(normalized, principal_vec)) / (
                np.linalg.norm(normalized) * np.linalg.norm(principal_vec)
            )
            convergences.append(correlation)
        
        return {
            's': s,
            'spectral_radius': float(spectral_radius),
            'principal_eigenvalue': complex(principal),
            'is_simple': bool(is_simple),
            'is_positive': bool(is_positive),
            'min_eigenfunction_value': float(min_val),
            'spectral_gap': gap_info,
            'convergence_correlations': convergences,
            'rpf_verified': bool(is_simple and is_positive and gap_info['has_spectral_gap'])
        }
    
    def compute_pressure_from_spectrum(self, s_values: np.ndarray, 
                                      n_points: int = 100) -> Dict:
        """
        从谱计算压力函数
        
        关系: P(s) = log λ_1(s)
        
        Args:
            s_values: 参数值
            n_points: 离散化点数
            
        Returns:
            压力函数数据
        """
        pressures = []
        
        for s in s_values:
            rpf = DiscretizedRPF(self.poly, s, n_points=n_points)
            eigenvalues, _ = rpf.compute_spectrum(k=5)
            
            principal = eigenvalues[0].real
            pressure = np.log(max(principal, 1e-10))
            pressures.append(pressure)
        
        return {
            's_values': s_values.tolist(),
            'pressures': pressures,
            'pressure_function': list(zip(s_values.tolist(), pressures))
        }
    
    def construct_gibbs_measure(self, s: float, n_points: int = 100) -> Dict:
        """
        从RPF算子构造Gibbs测度
        
        μ = h · ν
        其中 h 是主特征函数，ν 是主特征测度
        
        Args:
            s: 参数
            n_points: 离散化点数
            
        Returns:
            Gibbs测度数据
        """
        rpf = DiscretizedRPF(self.poly, s, n_points=n_points)
        
        # 计算特征对
        eigenvalues, eigenvectors = rpf.compute_spectrum()
        
        # 主特征函数 h
        h = np.abs(eigenvectors[:, 0].real)
        h = h / np.sum(h)  # 规范化
        
        # 主特征测度 ν（通过左特征向量）
        # 这里简化为使用h作为密度
        nu = h / np.sum(h)
        
        # Gibbs测度 μ = h · ν
        mu = h * nu
        mu = mu / np.sum(mu)
        
        return {
            'points': rpf.points.tolist(),
            'measure': mu.tolist(),
            'eigenfunction': h.tolist(),
            'principal_eigenvalue': float(eigenvalues[0].real)
        }


# ============================================================================
# 综合探索流程
# ============================================================================

class SpectrumExploration:
    """RPF谱综合探索"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}
    
    def explore_polynomial(self, name: str, poly: PAdicPoly, 
                          s_values: np.ndarray = None) -> Dict:
        """
        对单个多项式进行完整探索
        
        Args:
            name: 多项式名称
            poly: 多项式
            s_values: 测试的s值
            
        Returns:
            探索结果
        """
        if s_values is None:
            s_values = np.linspace(0.5, 3.0, 10)
        
        logger.info(f"\n{'='*70}")
        logger.info(f"探索多项式: {name} = {poly} (p={poly.p})")
        logger.info(f"{'='*70}")
        
        result = {
            'name': name,
            'polynomial': str(poly),
            'p': poly.p
        }
        
        # 1. 基本谱分析
        logger.info("\n[1/5] 基本谱分析...")
        rpf = DiscretizedRPF(poly, s=1.0, n_points=100)
        analyzer = SpectrumAnalyzer(rpf)
        
        # 计算谱
        eigenvalues, eigenvectors = rpf.compute_spectrum(k=20)
        gap_info = rpf.compute_spectral_gap()
        
        result['basic_spectrum'] = {
            'top_10_eigenvalues': eigenvalues[:10].tolist(),
            'spectral_gap': gap_info
        }
        
        logger.info(f"主特征值: {gap_info['lambda_1']:.4f}")
        logger.info(f"谱隙: {gap_info['spectral_gap']:.4f}")
        logger.info(f"相对谱隙: {gap_info['relative_gap']:.4f}")
        
        # 保存可视化
        plot_path = self.output_dir / f"spectrum_{name}_p{poly.p}.png"
        analyzer.plot_spectrum(save_path=str(plot_path))
        
        # 2. 收敛性分析
        logger.info("\n[2/5] 收敛性分析...")
        n_list = [50, 100, 150, 200]
        convergence = analyzer.analyze_convergence(n_list)
        result['convergence_analysis'] = convergence
        
        logger.info("不同离散化程度的主特征值:")
        for n, lam in zip(n_list, convergence['principal_eigenvalues']):
            logger.info(f"  n={n}: λ_1 = {lam:.4f}")
        
        # 3. 参数依赖性
        logger.info("\n[3/5] 参数依赖性分析...")
        parameter_dep = analyzer.analyze_parameter_dependence(s_values)
        result['parameter_dependence'] = parameter_dep
        
        # 4. RPF定理验证
        logger.info("\n[4/5] 验证RPF定理...")
        gibbs_analyzer = GibbsConnectionAnalyzer(poly)
        rpf_verification = gibbs_analyzer.verify_rpf_theorem(s=1.0)
        result['rpf_verification'] = rpf_verification
        
        logger.info(f"RPF定理验证:")
        logger.info(f"  - 主特征值简单: {rpf_verification['is_simple']}")
        logger.info(f"  - 特征函数正定: {rpf_verification['is_positive']}")
        logger.info(f"  - 谱隙存在: {rpf_verification['spectral_gap']['has_spectral_gap']}")
        logger.info(f"  - RPF验证通过: {rpf_verification['rpf_verified']}")
        
        # 5. 压力函数与Gibbs测度
        logger.info("\n[5/5] 压力函数与Gibbs测度...")
        pressure_data = gibbs_analyzer.compute_pressure_from_spectrum(s_values)
        gibbs_measure = gibbs_analyzer.construct_gibbs_measure(s=1.0)
        
        result['pressure_function'] = pressure_data
        result['gibbs_measure'] = gibbs_measure
        
        # 求解Bowen方程
        s_test = np.linspace(0.1, 5.0, 50)
        pressures = gibbs_analyzer.compute_pressure_from_spectrum(s_test)
        
        # 找到P(s) ≈ 0的点
        pressures_arr = np.array(pressures['pressures'])
        idx_zero = np.argmin(np.abs(pressures_arr))
        delta_estimate = s_test[idx_zero]
        
        result['bowen_estimate'] = {
            'delta': float(delta_estimate),
            'pressure_at_delta': float(pressures_arr[idx_zero])
        }
        
        logger.info(f"Bowen方程估计: δ ≈ {delta_estimate:.4f}")
        
        self.results[name] = result
        return result
    
    def generate_report(self) -> str:
        """生成综合报告"""
        report_path = self.output_dir / "spectrum_exploration_report.json"
        
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"\n报告已保存: {report_path}")
        
        # 生成摘要
        summary = []
        summary.append("=" * 70)
        summary.append("RPF算子谱探索综合报告")
        summary.append("=" * 70)
        
        for name, result in self.results.items():
            summary.append(f"\n{name}:")
            
            basic = result.get('basic_spectrum', {})
            gap = basic.get('spectral_gap', {})
            summary.append(f"  主特征值: {gap.get('lambda_1', 'N/A'):.4f}")
            summary.append(f"  谱隙: {gap.get('spectral_gap', 'N/A'):.4f}")
            summary.append(f"  RPF验证: {result.get('rpf_verification', {}).get('rpf_verified', False)}")
            
            bowen = result.get('bowen_estimate', {})
            summary.append(f"  Bowen估计: δ ≈ {bowen.get('delta', 'N/A'):.4f}")
        
        summary_text = "\n".join(summary)
        
        summary_path = self.output_dir / "spectrum_exploration_summary.txt"
        with open(summary_path, 'w') as f:
            f.write(summary_text)
        
        return summary_text


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主函数"""
    
    print("=" * 70)
    print("Ruelle-Perron-Frobenius算子谱探索")
    print("任务: P3-C2-001")
    print("=" * 70)
    
    # 创建探索器
    exploration = SpectrumExploration(output_dir="results")
    
    # 测试的素数和多项式
    test_cases = [
        (2, 'z2'),
        (2, 'z2_plus_p'),
        (3, 'z2'),
        (3, 'z3'),
        (5, 'z2'),
    ]
    
    for p, name in test_cases:
        polynomials = create_test_polynomials(p)
        if name in polynomials:
            poly = polynomials[name]
            exploration.explore_polynomial(
                name=f"{name}_p{p}", 
                poly=poly,
                s_values=np.linspace(0.5, 3.0, 15)
            )
    
    # 生成报告
    print("\n" + "=" * 70)
    summary = exploration.generate_report()
    print(summary)
    
    print("\n" + "=" * 70)
    print("探索完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()
