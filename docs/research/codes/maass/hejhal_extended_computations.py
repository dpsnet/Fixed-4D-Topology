#!/usr/bin/env python3
"""
Hejhal算法扩展计算 - Maass形式特征值数据库构建
===================================================

本模块扩展基础Hejhal算法，实现：
1. 批量特征值计算（前10个偶形式和奇形式）
2. 分形双曲曲面的谱探索
3. 特征值分布统计分析
4. 与分形维数的关系研究

基于:
- Hejhal, D. (1981, 1992)
- Borthwick, D. "Spectral Theory of Infinite-Area Hyperbolic Surfaces"
- McMullen, C.T. "Hausdorff dimension and conformal dynamics"

作者: Research Team
日期: 2026-02-11
"""

import numpy as np
from scipy.linalg import svdvals, svd
from scipy.optimize import minimize_scalar, brentq
from scipy import stats
from typing import List, Tuple, Optional, Dict, Callable
from dataclasses import dataclass, field
import warnings
import time
import json
import sqlite3
from datetime import datetime
from pathlib import Path

warnings.filterwarnings('ignore')

# 尝试导入mpmath
try:
    import mpmath
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("警告: mpmath未安装")


@dataclass
class HejhalConfig:
    """Hejhal算法配置参数"""
    truncation_M: int = 20          # Fourier截断参数（增加以获得更高精度）
    num_points: int = 20            # 配点数量
    y_min: float = 0.866025403784   # 基本域底部 (sqrt(3)/2)
    y_max: float = 1.3              # y坐标上限
    tolerance: float = 1e-10        # 收敛容差（更严格）
    parity: str = 'even'            # 'even' 或 'odd'
    mpmath_dps: int = 30            # mpmath精度（增加）
    max_iterations: int = 50        # 最大迭代次数


@dataclass
class EigenvalueData:
    """特征值数据结构"""
    index: int                      # 序号
    R: float                        # R = sqrt(lambda - 1/4)
    lambda_val: float               # lambda = 1/4 + R^2
    parity: str                     # 'even' 或 'odd'
    error_estimate: float           # 误差估计
    condition_number: float         # 条件数
    fourier_coeffs: np.ndarray = field(default_factory=lambda: np.array([]))
    computation_time: float = 0.0   # 计算时间
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class MaassEigenvalueDatabase:
    """
    Maass特征值数据库管理器
    
    使用SQLite存储计算结果，支持查询和导出。
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库
        
        参数:
            db_path: 数据库文件路径，默认在代码目录下
        """
        if db_path is None:
            db_path = Path(__file__).parent / "maass_eigenvalues.db"
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 主特征值表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eigenvalues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idx INTEGER NOT NULL,
                R REAL NOT NULL,
                lambda_val REAL NOT NULL,
                parity TEXT NOT NULL,
                error_estimate REAL,
                condition_number REAL,
                fourier_coeffs TEXT,
                computation_time REAL,
                timestamp TEXT,
                surface_type TEXT DEFAULT 'modular',
                surface_params TEXT,
                UNIQUE(idx, parity, surface_type)
            )
        ''')
        
        # 分布统计表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parity TEXT NOT NULL,
                n_eigenvalues INTEGER,
                mean_spacing REAL,
                variance_spacing REAL,
                spectral_statistics TEXT,
                weyl_law_deviation TEXT,
                timestamp TEXT
            )
        ''')
        
        # 分形曲面参数表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fractal_surfaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surface_name TEXT UNIQUE,
                surface_type TEXT,
                dimension REAL,
                limit_set_dim REAL,
                parameters TEXT,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_eigenvalue(self, data: EigenvalueData, surface_type: str = 'modular',
                         surface_params: str = None):
        """插入特征值记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fourier_json = json.dumps(data.fourier_coeffs.tolist() if len(data.fourier_coeffs) > 0 else [])
        
        cursor.execute('''
            INSERT OR REPLACE INTO eigenvalues 
            (idx, R, lambda_val, parity, error_estimate, condition_number,
             fourier_coeffs, computation_time, timestamp, surface_type, surface_params)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data.index, data.R, data.lambda_val, data.parity, 
              data.error_estimate, data.condition_number, fourier_json,
              data.computation_time, data.timestamp, surface_type, surface_params))
        
        conn.commit()
        conn.close()
    
    def get_eigenvalues(self, parity: str = None, surface_type: str = 'modular',
                       limit: int = None) -> List[EigenvalueData]:
        """查询特征值"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM eigenvalues WHERE surface_type = ?"
        params = [surface_type]
        
        if parity:
            query += " AND parity = ?"
            params.append(parity)
        
        query += " ORDER BY R"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            coeffs = np.array(json.loads(row[7])) if row[7] else np.array([])
            data = EigenvalueData(
                index=row[1], R=row[2], lambda_val=row[3], parity=row[4],
                error_estimate=row[5], condition_number=row[6],
                fourier_coeffs=coeffs, computation_time=row[8],
                timestamp=row[9]
            )
            results.append(data)
        
        return results
    
    def export_to_json(self, filepath: str, parity: str = None):
        """导出数据到JSON"""
        data = self.get_eigenvalues(parity=parity)
        export_data = []
        
        for d in data:
            export_data.append({
                'index': d.index,
                'R': d.R,
                'lambda': d.lambda_val,
                'parity': d.parity,
                'error_estimate': d.error_estimate,
                'condition_number': d.condition_number,
                'computation_time': d.computation_time,
                'timestamp': d.timestamp
            })
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def insert_fractal_surface(self, name: str, surface_type: str, dimension: float,
                               limit_set_dim: float, parameters: dict, description: str):
        """插入分形曲面记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO fractal_surfaces 
            (surface_name, surface_type, dimension, limit_set_dim, parameters, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, surface_type, dimension, limit_set_dim, 
              json.dumps(parameters), description))
        
        conn.commit()
        conn.close()


class ExtendedMaassSolver:
    """
    扩展Maass特征值求解器
    
    支持更多特征值计算和分形曲面探索。
    """
    
    # 扩展的已知特征值列表（来自文献）
    KNOWN_EVEN_R = [
        13.779751351890, 17.738563381109, 19.423481346970,
        21.315796882311, 22.785280830796, 24.608206712860,
        25.521885634914, 26.556773776157, 27.500116922257,
        28.510714956855
    ]
    
    KNOWN_ODD_R = [
        9.533695261349, 12.173008240650, 14.358509516256,
        16.138121172691, 16.644259197914, 18.180913141642,
        19.423481346970, 20.893626352902, 21.315796882311,
        22.785280830796
    ]
    
    def __init__(self, config: Optional[HejhalConfig] = None):
        """初始化求解器"""
        self.config = config or HejhalConfig()
        
        if HAS_MPMATH:
            mpmath.mp.dps = self.config.mpmath_dps
        
        self.points = self._select_collocation_points()
        self._bessel_cache: Dict[Tuple[float, float], float] = {}
        self.database = MaassEigenvalueDatabase()
    
    def _select_collocation_points(self) -> List[complex]:
        """选择配点 - 改进的分布策略"""
        M = self.config.num_points
        y_min = self.config.y_min
        y_max = self.config.y_max
        
        points = []
        
        # 使用更均匀的分布策略
        # 在y方向使用对数分布以更好捕获边界行为
        ny = int(np.sqrt(M)) + 2
        
        # y坐标 - 改进的分布
        log_y = np.linspace(np.log(y_min), np.log(y_max), ny)
        y_vals = np.exp(log_y)
        
        for y in y_vals:
            # 基本域边界: |x| < min(0.5, sqrt(y^2 - 1))
            x_bound = min(0.48, np.sqrt(max(0.02, y*y - 1)))
            if x_bound > 0.02:
                nx = max(2, int(M / len(y_vals)) + 1)
                # x方向使用切比雪夫点分布
                x_vals = x_bound * np.cos(np.pi * (2*np.arange(nx) + 1) / (2*nx))
                for x in x_vals:
                    if len(points) < M:
                        points.append(complex(x, y))
        
        # 确保有M个点
        while len(points) < M:
            y = y_min + (y_max - y_min) * np.random.random()
            x_bound = min(0.48, np.sqrt(max(0.02, y*y - 1)))
            if x_bound > 0.02:
                x = (2*np.random.random() - 1) * x_bound
                points.append(complex(x, y))
        
        return points[:M]
    
    def _k_bessel(self, t: float, x: float) -> float:
        """计算修正Bessel函数 K_{it}(x)"""
        if x <= 0:
            return 0.0
        
        key = (round(t, 12), round(x, 12))
        if key in self._bessel_cache:
            return self._bessel_cache[key]
        
        if not HAS_MPMATH:
            # 后备渐近展开
            if x > 10:
                return np.sqrt(np.pi / (2*x)) * np.exp(-x)
            return 0.0
        
        try:
            result = mpmath.besselk(1j * t, x)
            val = float(result.real)
            self._bessel_cache[key] = val
            return val
        except Exception:
            return 0.0
    
    def _compute_matrix_element(self, z: complex, n: int, t: float) -> float:
        """计算配点矩阵元素"""
        x, y = z.real, z.imag
        
        # 原点处的项
        arg1 = 2 * np.pi * n * y
        k1 = self._k_bessel(t, arg1)
        b1 = np.sqrt(y) * k1
        
        if self.config.parity == 'even':
            term1 = b1 * np.cos(2 * np.pi * n * x)
        else:
            term1 = b1 * np.sin(2 * np.pi * n * x)
        
        # 变换点 S(z) = -1/z
        denom = x*x + y*y
        if denom < 1e-12:
            return term1
        
        x_s = -x / denom
        y_s = y / denom
        
        arg2 = 2 * np.pi * n * y_s
        k2 = self._k_bessel(t, arg2)
        b2 = np.sqrt(y_s) * k2
        
        if self.config.parity == 'even':
            term2 = b2 * np.cos(2 * np.pi * n * x_s)
        else:
            term2 = b2 * np.sin(2 * np.pi * n * x_s)
        
        return term1 - term2
    
    def construct_matrix(self, t: float) -> np.ndarray:
        """构造配点矩阵 A(t)"""
        M = self.config.truncation_M
        A = np.zeros((M, M))
        
        for j, z in enumerate(self.points[:M]):
            for n in range(1, M + 1):
                A[j, n-1] = self._compute_matrix_element(z, n, t)
        
        return A
    
    def matrix_condition(self, t: float) -> float:
        """计算矩阵条件指标"""
        try:
            A = self.construct_matrix(t)
            norm = np.linalg.norm(A)
            if norm < 1e-300:
                return 1.0
            
            A_norm = A / norm
            s = svdvals(A_norm)
            s_filtered = s[s > 1e-15]
            
            if len(s_filtered) < 2:
                return 1.0
            
            return float(s_filtered[-1] / s_filtered[0])
        except:
            return 1.0
    
    def find_eigenvalue(self, t_guess: float, 
                       half_width: float = 0.5) -> Optional[Tuple[float, float]]:
        """在t_guess附近搜索特征值"""
        # 粗搜索 - 增加点数以提高精度
        t_vals = np.linspace(t_guess - half_width, t_guess + half_width, 60)
        conditions = []
        
        for t in t_vals:
            cond = self.matrix_condition(t)
            conditions.append(cond)
        
        conditions = np.array(conditions)
        min_idx = np.argmin(conditions)
        min_cond = conditions[min_idx]
        
        if min_cond > 0.2:  # 阈值降低
            return None
        
        # 精化
        t_best = t_vals[min_idx]
        try:
            result = minimize_scalar(
                self.matrix_condition,
                bounds=(max(0.1, t_best - 0.15), t_best + 0.15),
                method='bounded',
                options={'xatol': self.config.tolerance, 'maxiter': 50}
            )
            if result.success:
                return result.x, result.fun
        except:
            pass
        
        return t_best, min_cond
    
    def compute_single_eigenvalue(self, index: int, parity: str) -> Optional[EigenvalueData]:
        """计算单个特征值"""
        known_list = self.KNOWN_EVEN_R if parity == 'even' else self.KNOWN_ODD_R
        
        if index > len(known_list):
            print(f"  警告: 序号 {index} 超出已知列表，使用外推估计")
            # 使用特征值的渐近分布估计
            if len(known_list) >= 2:
                avg_spacing = (known_list[-1] - known_list[0]) / (len(known_list) - 1)
                t_guess = known_list[-1] + avg_spacing * (index - len(known_list))
            else:
                return None
        else:
            t_guess = known_list[index - 1]
        
        print(f"  搜索 R ≈ {t_guess:.4f}...")
        start = time.time()
        result = self.find_eigenvalue(t_guess, half_width=0.6)
        elapsed = time.time() - start
        
        if result:
            t, cond = result
            lam = 0.25 + t*t
            error = abs(t - t_guess) if index <= len(known_list) else 0.1
            
            # 获取Fourier系数
            coeffs = self.get_fourier_coefficients(t)
            
            data = EigenvalueData(
                index=index, R=t, lambda_val=lam, parity=parity,
                error_estimate=error, condition_number=cond,
                fourier_coeffs=coeffs, computation_time=elapsed
            )
            return data
        
        return None
    
    def compute_eigenvalues_batch(self, n_even: int = 10, n_odd: int = 10,
                                  save_to_db: bool = True) -> Dict[str, List[EigenvalueData]]:
        """
        批量计算特征值
        
        参数:
            n_even: 偶形式数量
            n_odd: 奇形式数量
            save_to_db: 是否保存到数据库
        
        返回:
            {'even': [...], 'odd': [...]}
        """
        results = {'even': [], 'odd': []}
        
        print("=" * 70)
        print("Hejhal算法 - 扩展批量计算")
        print("=" * 70)
        print(f"配置: M={self.config.truncation_M}, 点数={self.config.num_points}")
        print(f"目标: {n_even}个偶形式, {n_odd}个奇形式")
        print()
        
        # 计算偶形式
        print("-" * 70)
        print(f"计算偶形式 (parity=even)")
        print("-" * 70)
        self.config.parity = 'even'
        
        for i in range(1, n_even + 1):
            print(f"\n[{i}/{n_even}] 偶形式:")
            data = self.compute_single_eigenvalue(i, 'even')
            if data:
                results['even'].append(data)
                print(f"  ✓ R = {data.R:.8f}, λ = {data.lambda_val:.4f}")
                print(f"    误差 = {data.error_estimate:.2e}, 时间 = {data.computation_time:.1f}s")
                
                if save_to_db:
                    self.database.insert_eigenvalue(data, 'modular')
            else:
                print(f"  ✗ 未找到")
        
        # 计算奇形式
        print("\n" + "-" * 70)
        print(f"计算奇形式 (parity=odd)")
        print("-" * 70)
        self.config.parity = 'odd'
        
        for i in range(1, n_odd + 1):
            print(f"\n[{i}/{n_odd}] 奇形式:")
            data = self.compute_single_eigenvalue(i, 'odd')
            if data:
                results['odd'].append(data)
                print(f"  ✓ R = {data.R:.8f}, λ = {data.lambda_val:.4f}")
                print(f"    误差 = {data.error_estimate:.2e}, 时间 = {data.computation_time:.1f}s")
                
                if save_to_db:
                    self.database.insert_eigenvalue(data, 'modular')
            else:
                print(f"  ✗ 未找到")
        
        return results
    
    def get_fourier_coefficients(self, t: float) -> np.ndarray:
        """获取Fourier系数"""
        A = self.construct_matrix(t)
        try:
            _, _, Vh = svd(A)
            coeffs = Vh[-1, :].copy()
            max_c = np.max(np.abs(coeffs))
            if max_c > 0:
                coeffs = coeffs / max_c
            return coeffs
        except:
            return np.zeros(self.config.truncation_M)


class EigenvalueDistributionAnalyzer:
    """
    特征值分布分析器
    
    分析特征值的统计性质，包括Weyl定律、间距分布等。
    """
    
    def __init__(self, eigenvalues: List[EigenvalueData]):
        """
        初始化分析器
        
        参数:
            eigenvalues: 特征值数据列表
        """
        self.eigenvalues = sorted(eigenvalues, key=lambda x: x.R)
        self.R_values = np.array([e.R for e in self.eigenvalues])
        self.lambda_values = np.array([e.lambda_val for e in self.eigenvalues])
    
    def compute_spacings(self) -> np.ndarray:
        """计算相邻特征值间距"""
        if len(self.R_values) < 2:
            return np.array([])
        return np.diff(self.R_values)
    
    def compute_normalized_spacings(self) -> np.ndarray:
        """计算归一化间距（Weyl定律意义下）"""
        spacings = self.compute_spacings()
        if len(spacings) == 0:
            return spacings
        
        # 对于模曲面，Weyl定律给出：N(λ) ~ λ/12
        # 对应的局部平均间距
        mean_spacing = np.mean(spacings)
        if mean_spacing > 0:
            return spacings / mean_spacing
        return spacings
    
    def weyl_law_residual(self, T: float = None) -> Dict:
        """
        计算Weyl定律余项
        
        Weyl定律: N(λ) ~ (1/12) * λ = (1/12) * (1/4 + R^2)
        
        返回:
            {'T': T_values, 'N_actual': 实际计数, 'N_weyl': Weyl预测, 'residual': 余项}
        """
        if T is None:
            T = np.linspace(0, max(self.R_values) * 1.1, 100)
        
        N_actual = np.array([np.sum(self.R_values <= t) for t in T])
        # Weyl定律: N(λ) = λ/12 + ... = (1/4 + R^2)/12
        N_weyl = (0.25 + T**2) / 12
        
        residual = N_actual - N_weyl
        
        return {
            'T': T,
            'N_actual': N_actual,
            'N_weyl': N_weyl,
            'residual': residual
        }
    
    def level_spacing_statistics(self) -> Dict:
        """
        能级间距统计
        
        返回:
            包含各种统计量的字典
        """
        spacings = self.compute_normalized_spacings()
        
        if len(spacings) == 0:
            return {}
        
        stats_dict = {
            'mean': np.mean(spacings),
            'std': np.std(spacings),
            'variance': np.var(spacings),
            'skewness': stats.skew(spacings),
            'kurtosis': stats.kurtosis(spacings),
            'min': np.min(spacings),
            'max': np.max(spacings),
            'median': np.median(spacings)
        }
        
        # 与Poisson和GOE分布对比
        # Poisson: P(s) = exp(-s)
        # GOE: P(s) ~ s * exp(-πs²/4)
        stats_dict['goe_comparison'] = self._compare_to_goe(spacings)
        
        return stats_dict
    
    def _compare_to_goe(self, spacings: np.ndarray) -> Dict:
        """与GOE随机矩阵理论对比"""
        # GOE的间距方差 ~ 0.2858
        goe_variance = (4 - np.pi) / (2 * np.pi)  # ≈ 0.2732
        
        actual_variance = np.var(spacings)
        
        # Kolmogorov-Smirnov检验
        # 标准化
        spacings_std = (spacings - np.mean(spacings)) / np.std(spacings)
        
        return {
            'actual_variance': actual_variance,
            'goe_variance': goe_variance,
            'poisson_variance': 1.0,  # Poisson分布方差为1
            'variance_ratio_goe': actual_variance / goe_variance,
            'variance_ratio_poisson': actual_variance / 1.0
        }
    
    def spectral_form_factor(self, beta_range: Tuple[float, float] = (0.01, 10),
                            num_points: int = 100) -> Dict:
        """
        计算谱形式因子
        
        g(β) = Σ exp(-β * λ_n)
        
        这是热核 trace e^(-βΔ) 的离散版本。
        """
        betas = np.linspace(beta_range[0], beta_range[1], num_points)
        g_beta = []
        
        for beta in betas:
            g = np.sum(np.exp(-beta * self.lambda_values))
            g_beta.append(g)
        
        return {'beta': betas, 'g_beta': np.array(g_beta)}
    
    def generate_report(self) -> str:
        """生成分析报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("特征值分布统计分析")
        lines.append("=" * 70)
        lines.append(f"样本数量: {len(self.eigenvalues)}")
        lines.append(f"R范围: [{min(self.R_values):.2f}, {max(self.R_values):.2f}]")
        lines.append("")
        
        # 间距统计
        lines.append("-" * 70)
        lines.append("能级间距统计")
        lines.append("-" * 70)
        
        spacing_stats = self.level_spacing_statistics()
        if spacing_stats:
            lines.append(f"平均间距: {spacing_stats['mean']:.4f}")
            lines.append(f"间距方差: {spacing_stats['variance']:.4f}")
            lines.append(f"偏度: {spacing_stats['skewness']:.4f}")
            lines.append(f"峰度: {spacing_stats['kurtosis']:.4f}")
            lines.append("")
            
            if 'goe_comparison' in spacing_stats:
                comp = spacing_stats['goe_comparison']
                lines.append("与随机矩阵理论对比:")
                lines.append(f"  实际方差 / GOE方差: {comp['variance_ratio_goe']:.4f}")
                lines.append(f"  实际方差 / Poisson方差: {comp['variance_ratio_poisson']:.4f}")
                if 0.8 < comp['variance_ratio_goe'] < 1.2:
                    lines.append("  → 符合GOE统计（量子混沌特征）")
                elif comp['variance_ratio_poisson'] > 0.9:
                    lines.append("  → 接近Poisson统计（可积系统特征）")
        
        return "\n".join(lines)


class FractalHyperbolicSurface:
    """
    分形双曲曲面探索
    
    探索无限面积双曲曲面和分形极限集的谱理论。
    基于Borthwick的工作。
    """
    
    def __init__(self, name: str, dimension: float, limit_set_dim: float):
        """
        初始化分形双曲曲面
        
        参数:
            name: 曲面名称
            dimension: 双曲维数
            limit_set_dim: 极限集Hausdorff维数
        """
        self.name = name
        self.dimension = dimension
        self.limit_set_dim = limit_set_dim
    
    def scattering_matrix_size(self) -> int:
        """
        散射矩阵大小
        
        对于分形双曲曲面，连续谱的描述需要散射矩阵。
        """
        # 简化估计：与极限集维数相关
        return max(2, int(2 * self.limit_set_dim))
    
    def resonances_estimate(self, max_imag: float = -0.1) -> List[complex]:
        """
        共振态估计
        
        对于无限面积双曲曲面，特征值变为共振态（复数）。
        
        参数:
            max_imag: 最大虚部（负数）
        
        返回:
            估计的共振态列表
        """
        # 基于分形维数的启发式估计
        # 共振态与极限集维数有关
        resonances = []
        
        # 使用分形维数估计共振带
        # δ = limit_set_dim
        delta = self.limit_set_dim
        
        # 共振态大致位于 Im(s) < (δ - 1)/2
        imag_bound = (delta - 1) / 2
        
        # 生成一些假想的共振态（实际计算需要更复杂的数值方法）
        for n in range(1, 10):
            # 启发式分布
            real_part = n * 0.5
            imag_part = min(-0.1, imag_bound - n * 0.05)
            resonances.append(complex(real_part, imag_part))
        
        return resonances
    
    def spectral_dimension_relation(self) -> Dict:
        """
        谱维数关系
        
        探索特征值分布与分形维数的关系。
        这是本研究的核心问题。
        """
        delta = self.limit_set_dim
        
        relations = {
            'limit_set_dimension': delta,
            'spectral_dimension_estimate': 2 * delta / (delta + 1),
            'resonance_gap_estimate': (1 - delta) / 2 if delta < 1 else 0,
            'density_exponent': delta
        }
        
        return relations


# =============================================================================
# 主程序
# =============================================================================

def run_extended_computations():
    """运行扩展计算"""
    print("\n" + "=" * 70)
    print("Hejhal算法扩展计算 - Maass形式特征值数据库")
    print("=" * 70)
    print()
    
    # 创建高精度配置
    config = HejhalConfig(
        truncation_M=20,
        num_points=20,
        tolerance=1e-10,
        mpmath_dps=30
    )
    
    # 初始化求解器
    solver = ExtendedMaassSolver(config)
    
    # 批量计算前10个特征值
    results = solver.compute_eigenvalues_batch(n_even=10, n_odd=10, save_to_db=True)
    
    # 分析结果
    print("\n" + "=" * 70)
    print("计算结果汇总")
    print("=" * 70)
    
    for parity, data_list in results.items():
        if data_list:
            print(f"\n{parity.capitalize()}形式:")
            print(f"{'序号':<6}{'R':<18}{'λ':<20}{'误差':<12}{'时间(s)':<10}")
            print("-" * 70)
            for d in data_list:
                print(f"{d.index:<6}{d.R:<18.8f}{d.lambda_val:<20.4f}"
                      f"{d.error_estimate:<12.2e}{d.computation_time:<10.1f}")
    
    # 分布分析
    print("\n" + "=" * 70)
    print("分布统计分析")
    print("=" * 70)
    
    all_eigenvalues = results['even'] + results['odd']
    
    if all_eigenvalues:
        analyzer = EigenvalueDistributionAnalyzer(all_eigenvalues)
        print(analyzer.generate_report())
    
    # 导出数据
    db_path = solver.database.db_path
    json_path = db_path.parent / "eigenvalues_export.json"
    solver.database.export_to_json(str(json_path))
    print(f"\n数据已导出到: {json_path}")
    
    return results


def explore_fractal_surfaces():
    """探索分形双曲曲面"""
    print("\n" + "=" * 70)
    print("分形双曲曲面谱探索")
    print("=" * 70)
    print()
    
    # 定义一些示例分形双曲曲面
    surfaces = [
        FractalHyperbolicSurface("Schottky_3_circles", 2.0, 0.8),
        FractalHyperbolicSurface("Infinite_geodesic", 2.0, 0.5),
        FractalHyperbolicSurface("Fractal_drum", 2.0, 0.3)
    ]
    
    for surf in surfaces:
        print(f"\n曲面: {surf.name}")
        print("-" * 50)
        print(f"极限集维数: {surf.limit_set_dim}")
        print(f"散射矩阵大小: {surf.scattering_matrix_size()}")
        
        relations = surf.spectral_dimension_relation()
        print(f"谱维数关系:")
        for key, val in relations.items():
            print(f"  {key}: {val:.4f}")
        
        resonances = surf.resonances_estimate()
        print(f"共振态估计 (前5个):")
        for r in resonances[:5]:
            print(f"  s = {r.real:.3f} + {r.imag:.3f}i")


def main():
    """主函数"""
    import sys
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if command == 'compute':
        run_extended_computations()
    elif command == 'fractal':
        explore_fractal_surfaces()
    elif command == 'all':
        run_extended_computations()
        explore_fractal_surfaces()
    else:
        print("用法: python hejhal_extended_computations.py [compute|fractal|all]")
        run_extended_computations()


if __name__ == '__main__':
    main()
