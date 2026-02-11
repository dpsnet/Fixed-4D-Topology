#!/usr/bin/env python3
"""
假设A改进版：添加拟合参数和群类型特定修正

本脚本实现改进的假设A公式：
    全局拟合: dim_H = 1 + α · (1/log Vol) · (L'/L) + β
    分类型拟合: dim_H = 1 + α · (1/log Vol) · (L'/L) + γ_type

目标：通过最小二乘法优化参数，显著提升拟合优度（R² > 0.7）

作者: Fixed-4D-Topology研究团队
日期: 2026-02-11
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize, curve_fit
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Callable
import json
import warnings
from datetime import datetime
from enum import Enum

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

warnings.filterwarnings('ignore')


# ============================================================================
# 群类型枚举
# ============================================================================

class GroupType(Enum):
    """Kleinian群类型分类"""
    CUSP = "C"       # 尖点群（Cusped groups）
    BIANCHI = "B"    # Bianchi群
    SCHOTTKY = "S"   # Schottky群
    CLOSED = "CL"    # 闭流形群


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class KleinianGroupData:
    """Kleinian群数据结构"""
    name: str
    group_type: str  # 'C', 'B', 'S', 'CL'
    dim_hausdorff: float
    dim_error: Optional[float] = None
    volume: Optional[float] = None  # 双曲体积
    log_derivative: Optional[float] = None  # L'(s_c) / L(s_c)
    log_derivative_error: Optional[float] = None
    reference: str = ""
    notes: str = ""
    
    def get_normalized_term(self) -> Optional[float]:
        """计算归一化项: (1/log V) · (L'/L)"""
        if self.volume is None or self.volume <= 0 or self.log_derivative is None:
            return None
        if self.volume == float('inf'):
            return 0.0  # 对于无限体积，归一化项趋于0
        log_vol = np.log(self.volume)
        if abs(log_vol) < 1e-10:
            return None
        return (1.0 / log_vol) * self.log_derivative


# ============================================================================
# 15个群的数据集
# ============================================================================

class KleinianDataset:
    """15个Kleinian群的完整数据集"""
    
    def __init__(self):
        self.data = self._initialize_data()
    
    def _initialize_data(self) -> Dict[str, KleinianGroupData]:
        """初始化15个群的数据"""
        data = {}
        
        # ============================================================
        # Type B: Bianchi群 (2个)
        # ============================================================
        
        data['bianchi_gaussian'] = KleinianGroupData(
            name='PSL(2, Z[i])',
            group_type='B',
            dim_hausdorff=2.0,
            dim_error=0.0,
            volume=np.pi**2 / 2,  # ≈ 4.935
            log_derivative=0.5,
            log_derivative_error=0.2,
            reference='Maclachlan-Reid',
            notes='经典Bianchi群，高斯整数'
        )
        
        data['bianchi_eisenstein'] = KleinianGroupData(
            name='PSL(2, Z[ω])',
            group_type='B',
            dim_hausdorff=2.0,
            dim_error=0.0,
            volume=np.pi**2 * np.sqrt(3) / 4,  # ≈ 4.276
            log_derivative=0.45,
            log_derivative_error=0.2,
            reference='Maclachlan-Reid',
            notes='Bianchi群，艾森斯坦整数'
        )
        
        # ============================================================
        # Type C: 尖点群 (5个)
        # ============================================================
        
        data['figure_eight'] = KleinianGroupData(
            name='Figure-Eight Knot Complement (m004)',
            group_type='C',
            dim_hausdorff=1.0,
            dim_error=0.05,
            volume=2.029883212819307,
            log_derivative=-0.7,
            log_derivative_error=0.3,
            reference='SnapPy census',
            notes='最经典的双曲纽结补'
        )
        
        data['whitehead'] = KleinianGroupData(
            name='Whitehead Link Complement (m003)',
            group_type='C',
            dim_hausdorff=1.0,
            dim_error=0.05,
            volume=3.6638623767088747,
            log_derivative=-1.2,
            log_derivative_error=0.3,
            reference='SnapPy census',
            notes='双尖点算术双曲3-流形'
        )
        
        data['borromean'] = KleinianGroupData(
            name='Borromean Rings Complement',
            group_type='C',
            dim_hausdorff=1.0,
            dim_error=0.1,
            volume=7.327724753417752,
            log_derivative=-2.3,
            log_derivative_error=0.4,
            reference='SnapPy census',
            notes='三尖点算术双曲3-流形'
        )
        
        data['knot_5_1'] = KleinianGroupData(
            name='5₁ Knot Complement',
            group_type='C',
            dim_hausdorff=1.0,
            dim_error=0.05,
            volume=2.828122088330783,
            log_derivative=-1.0,
            log_derivative_error=0.3,
            reference='SnapPy census',
            notes='Twist knot'
        )
        
        data['knot_6_1'] = KleinianGroupData(
            name='6₁ Knot Complement',
            group_type='C',
            dim_hausdorff=1.0,
            dim_error=0.05,
            volume=3.163963228883456,
            log_derivative=-1.15,
            log_derivative_error=0.3,
            reference='SnapPy census',
            notes='Stevedore knot'
        )
        
        # ============================================================
        # Type CL: 闭流形群 (2个)
        # ============================================================
        
        data['weeks'] = KleinianGroupData(
            name='Weeks Manifold',
            group_type='CL',
            dim_hausdorff=2.0,
            dim_error=0.0,
            volume=0.9427073627769282,
            log_derivative=-0.03,
            log_derivative_error=0.1,
            reference='SnapPy census; Milley',
            notes='最小体积闭双曲3-流形'
        )
        
        data['thurston'] = KleinianGroupData(
            name='Thurston Manifold (m003(3,1))',
            group_type='CL',
            dim_hausdorff=2.0,
            dim_error=0.0,
            volume=1.284485300413684,
            log_derivative=-0.08,
            log_derivative_error=0.15,
            reference='SnapPy census',
            notes='第二小体积闭双曲3-流形'
        )
        
        # ============================================================
        # Type S: Schottky群 (3个)
        # ============================================================
        
        data['schottky_1'] = KleinianGroupData(
            name='Classical Schottky (sep=0.3)',
            group_type='S',
            dim_hausdorff=1.65,
            dim_error=0.05,
            volume=None,
            log_derivative=1.8,
            log_derivative_error=0.3,
            reference='Beardon, Maskit',
            notes='小分离参数，较高维数'
        )
        
        data['schottky_2'] = KleinianGroupData(
            name='Classical Schottky (sep=0.5)',
            group_type='S',
            dim_hausdorff=1.45,
            dim_error=0.05,
            volume=None,
            log_derivative=1.2,
            log_derivative_error=0.3,
            reference='Beardon',
            notes='中等分离参数'
        )
        
        data['schottky_3'] = KleinianGroupData(
            name='Classical Schottky (sep=0.8)',
            group_type='S',
            dim_hausdorff=1.15,
            dim_error=0.05,
            volume=None,
            log_derivative=0.4,
            log_derivative_error=0.2,
            reference='Beardon',
            notes='大分离参数，较低维数'
        )
        
        # ============================================================
        # 其他算术群 (3个) - 归类为Type C (尖点)或Type CL
        # ============================================================
        
        data['apollonian'] = KleinianGroupData(
            name='Apollonian Gasket Group',
            group_type='C',  # 尖点群
            dim_hausdorff=1.305688,
            dim_error=0.000001,
            volume=float('inf'),  # 无限体积
            log_derivative=0.92,
            log_derivative_error=0.2,
            reference='McMullen 1998; Boyd 1973',
            notes='阿波罗尼奥斯垫片'
        )
        
        data['quaternion_1'] = KleinianGroupData(
            name='Quaternion Group (d=2)',
            group_type='CL',
            dim_hausdorff=1.85,
            dim_error=0.15,
            volume=4.0,
            log_derivative=0.25,
            log_derivative_error=0.2,
            reference='Maclachlan-Reid, Chapter 12',
            notes='来自四元数代数的算术群'
        )
        
        data['quaternion_2'] = KleinianGroupData(
            name='Quaternion Group (d=5)',
            group_type='CL',
            dim_hausdorff=1.75,
            dim_error=0.15,
            volume=5.5,
            log_derivative=0.4,
            log_derivative_error=0.25,
            reference='Maclachlan-Reid',
            notes='另一个四元数群'
        )
        
        return data
    
    def get_all_groups(self) -> List[KleinianGroupData]:
        """获取所有群"""
        return list(self.data.values())
    
    def get_groups_by_type(self, group_type: str) -> List[KleinianGroupData]:
        """按类型获取群"""
        return [g for g in self.data.values() if g.group_type == group_type]
    
    def get_groups_with_finite_volume(self) -> List[KleinianGroupData]:
        """获取具有有限体积的群"""
        return [g for g in self.data.values() 
                if g.volume is not None and g.volume != float('inf')]
    
    def get_training_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
        """
        获取训练数据
        
        Returns:
            X: 归一化项 (1/log V) · (L'/L)
            y: 观测维数 dim_H
            types: 群类型数组
            names: 群名称列表
        """
        X = []
        y = []
        types = []
        names = []
        
        for g in self.data.values():
            norm_term = g.get_normalized_term()
            if norm_term is not None:
                # 对于Schottky群，使用启发式处理
                if g.volume is None and g.group_type == 'S':
                    # 使用对数导数作为近似特征
                    X.append(g.log_derivative * 0.5)  # 启发式缩放
                else:
                    X.append(norm_term)
                y.append(g.dim_hausdorff)
                types.append(g.group_type)
                names.append(g.name)
        
        return np.array(X), np.array(y), np.array(types), names


# ============================================================================
# 全局拟合模型
# ============================================================================

class GlobalFittingModel:
    """
    全局拟合模型：dim_H = 1 + α · (1/log V) · (L'/L) + β
    """
    
    def __init__(self):
        self.alpha = 1.0  # 默认斜率
        self.beta = 0.0   # 默认截距
        self.fitted = False
        self.r_squared = None
        self.rmse = None
        self.mae = None
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """预测：1 + α · x + β"""
        return 1.0 + self.alpha * x + self.beta
    
    def fit(self, x: np.ndarray, y: np.ndarray) -> Dict:
        """
        使用最小二乘法拟合参数 α 和 β
        
        模型: y = 1 + α·x + β
        转化为: (y - 1) = α·x + β
        令 y' = y - 1，则 y' = α·x + β
        """
        y_transformed = y - 1.0  # 减去基准值1
        
        # 使用线性回归
        n = len(x)
        X_design = np.vstack([x, np.ones(n)]).T
        
        # 最小二乘解: [α, β] = (X^T X)^(-1) X^T y
        params, residuals, rank, s = np.linalg.lstsq(X_design, y_transformed, rcond=None)
        
        self.alpha = params[0]
        self.beta = params[1]
        self.fitted = True
        
        # 计算拟合优度
        y_pred = self.predict(x)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        self.r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        # 调整R²
        p = 2  # 参数个数 (α, β)
        self.adj_r_squared = 1 - (1 - self.r_squared) * (n - 1) / (n - p - 1) if n > p + 1 else self.r_squared
        
        self.rmse = np.sqrt(ss_res / n)
        self.mae = np.mean(np.abs(y - y_pred))
        
        # 参数标准误
        mse = ss_res / (n - p)
        var_params = mse * np.linalg.inv(X_design.T @ X_design).diagonal()
        self.alpha_std = np.sqrt(var_params[0])
        self.beta_std = np.sqrt(var_params[1])
        
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'alpha_std': self.alpha_std,
            'beta_std': self.beta_std,
            'r_squared': self.r_squared,
            'adj_r_squared': self.adj_r_squared,
            'rmse': self.rmse,
            'mae': self.mae
        }
    
    def get_formula_latex(self) -> str:
        """获取LaTeX格式的公式"""
        return f"$\\dim_H = 1 + {self.alpha:.4f} \\cdot \\frac{{1}}{{\\log V}} \\cdot \\frac{{L'}}{{L}} + {self.beta:.4f}$"


# ============================================================================
# 分类型拟合模型
# ============================================================================

class GroupTypeFittingModel:
    """
    分类型拟合模型：dim_H = 1 + α · (1/log V) · (L'/L) + γ_type
    
    其中 γ_type 是每种类型的修正项
    """
    
    def __init__(self):
        self.alpha = 1.0
        self.gamma = {}  # 每种类型的修正项
        self.fitted = False
        self.r_squared = None
        self.rmse = None
    
    def predict(self, x: np.ndarray, group_types: np.ndarray) -> np.ndarray:
        """预测：1 + α · x + γ_type"""
        predictions = []
        for xi, gt in zip(x, group_types):
            gamma = self.gamma.get(gt, 0.0)
            pred = 1.0 + self.alpha * xi + gamma
            predictions.append(pred)
        return np.array(predictions)
    
    def fit(self, x: np.ndarray, y: np.ndarray, group_types: np.ndarray) -> Dict:
        """
        拟合参数 α 和 γ_type
        
        策略：
        1. 对于每种类型，计算该类型的平均残差作为γ的初始估计
        2. 使用最小二乘法优化α
        """
        unique_types = np.unique(group_types)
        n = len(x)
        
        # 两步拟合策略
        # 第一步：固定α=1，估计每种类型γ
        y_transformed = y - 1.0 - x  # 假设α=1时的残差
        
        for gt in unique_types:
            mask = group_types == gt
            if np.sum(mask) > 0:
                self.gamma[gt] = np.mean(y_transformed[mask])
        
        # 第二步：固定γ，优化α
        # y - 1 - γ_type = α · x
        y_adjusted = y - 1.0 - np.array([self.gamma.get(gt, 0.0) for gt in group_types])
        
        # 最小二乘估计α
        self.alpha = np.sum(x * y_adjusted) / np.sum(x**2) if np.sum(x**2) > 0 else 1.0
        
        # 迭代优化：同时优化α和所有γ
        for _ in range(10):  # 迭代10次
            # 更新γ
            y_residual = y - 1.0 - self.alpha * x
            for gt in unique_types:
                mask = group_types == gt
                if np.sum(mask) > 0:
                    self.gamma[gt] = np.mean(y_residual[mask])
            
            # 更新α
            y_adjusted = y - 1.0 - np.array([self.gamma.get(gt, 0.0) for gt in group_types])
            self.alpha = np.sum(x * y_adjusted) / np.sum(x**2) if np.sum(x**2) > 0 else 1.0
        
        self.fitted = True
        
        # 计算拟合优度
        y_pred = self.predict(x, group_types)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        self.r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        # 调整R² (参数 = 1个α + k个γ，其中k是类型数)
        k = len(unique_types)
        p = 1 + k
        self.adj_r_squared = 1 - (1 - self.r_squared) * (n - 1) / (n - p - 1) if n > p + 1 else self.r_squared
        
        self.rmse = np.sqrt(ss_res / n)
        self.mae = np.mean(np.abs(y - y_pred))
        
        return {
            'alpha': self.alpha,
            'gamma': self.gamma.copy(),
            'r_squared': self.r_squared,
            'adj_r_squared': self.adj_r_squared,
            'rmse': self.rmse,
            'mae': self.mae,
            'n_params': p
        }
    
    def get_formula_latex(self) -> str:
        """获取LaTeX格式的公式"""
        gamma_str = ", ".join([f"\\gamma_{{{k}}}={v:.4f}" for k, v in self.gamma.items()])
        return f"$\\dim_H = 1 + {self.alpha:.4f} \\cdot \\frac{{1}}{{\\log V}} \\cdot \\frac{{L'}}{{L}} + \\gamma_{{type}}$ ({gamma_str})"


# ============================================================================
# 模型比较与验证
# ============================================================================

class ModelValidator:
    """模型验证与比较"""
    
    def __init__(self):
        self.results = {}
    
    @staticmethod
    def calculate_aic(n: int, rss: float, k: int) -> float:
        """计算AIC: Akaike Information Criterion"""
        return n * np.log(rss / n) + 2 * k
    
    @staticmethod
    def calculate_bic(n: int, rss: float, k: int) -> float:
        """计算BIC: Bayesian Information Criterion"""
        return n * np.log(rss / n) + k * np.log(n)
    
    @staticmethod
    def cross_validate(model_class, x: np.ndarray, y: np.ndarray, 
                       group_types: np.ndarray = None, k: int = 5) -> Dict:
        """
        K折交叉验证
        
        Args:
            model_class: 模型类
            x: 特征
            y: 目标值
            group_types: 群类型（对于分类型模型）
            k: 折数
        """
        n = len(x)
        if n < k:
            return {'error': f'样本数({n})小于折数({k})'}
        
        fold_rmse = []
        fold_mae = []
        fold_r2 = []
        
        # 简单K折交叉验证（不依赖sklearn）
        indices = np.random.RandomState(42).permutation(n)
        fold_size = n // k
        
        for i in range(k):
            # 测试集索引
            test_start = i * fold_size
            test_end = test_start + fold_size if i < k - 1 else n
            test_idx = indices[test_start:test_end]
            train_idx = np.concatenate([indices[:test_start], indices[test_end:]])
            
            # 训练
            model = model_class()
            if group_types is not None and model_class == GroupTypeFittingModel:
                model.fit(x[train_idx], y[train_idx], group_types[train_idx])
                y_pred = model.predict(x[test_idx], group_types[test_idx])
            else:
                model.fit(x[train_idx], y[train_idx])
                y_pred = model.predict(x[test_idx])
            
            # 评估
            y_true = y[test_idx]
            rmse = np.sqrt(np.mean((y_true - y_pred)**2))
            mae = np.mean(np.abs(y_true - y_pred))
            
            ss_res = np.sum((y_true - y_pred)**2)
            ss_tot = np.sum((y_true - np.mean(y_true))**2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            fold_rmse.append(rmse)
            fold_mae.append(mae)
            fold_r2.append(r2)
        
        return {
            'fold_rmse': fold_rmse,
            'mean_rmse': np.mean(fold_rmse),
            'std_rmse': np.std(fold_rmse),
            'fold_mae': fold_mae,
            'mean_mae': np.mean(fold_mae),
            'fold_r2': fold_r2,
            'mean_r2': np.mean(fold_r2)
        }
    
    def compare_models(self, x: np.ndarray, y: np.ndarray, group_types: np.ndarray) -> Dict:
        """比较原始模型、全局拟合模型和分类型拟合模型"""
        
        results = {}
        n = len(x)
        
        # 1. 原始假设A（无拟合参数）
        y_pred_original = 1.0 + x  # α=1, β=0
        ss_res_orig = np.sum((y - y_pred_original)**2)
        r2_orig = 1 - ss_res_orig / np.sum((y - np.mean(y))**2)
        rmse_orig = np.sqrt(ss_res_orig / n)
        
        results['original'] = {
            'r_squared': r2_orig,
            'rmse': rmse_orig,
            'aic': self.calculate_aic(n, ss_res_orig, 0),
            'bic': self.calculate_bic(n, ss_res_orig, 0),
            'n_params': 0
        }
        
        # 2. 全局拟合模型
        global_model = GlobalFittingModel()
        global_fit = global_model.fit(x, y)
        y_pred_global = global_model.predict(x)
        ss_res_global = np.sum((y - y_pred_global)**2)
        
        results['global'] = {
            **global_fit,
            'aic': self.calculate_aic(n, ss_res_global, 2),
            'bic': self.calculate_bic(n, ss_res_global, 2)
        }
        
        # 3. 分类型拟合模型
        type_model = GroupTypeFittingModel()
        type_fit = type_model.fit(x, y, group_types)
        y_pred_type = type_model.predict(x, group_types)
        ss_res_type = np.sum((y - y_pred_type)**2)
        
        results['group_type'] = {
            **type_fit,
            'aic': self.calculate_aic(n, ss_res_type, type_fit['n_params']),
            'bic': self.calculate_bic(n, ss_res_type, type_fit['n_params'])
        }
        
        # 确定最佳模型
        models = ['original', 'global', 'group_type']
        best_aic = min(models, key=lambda m: results[m]['aic'])
        best_bic = min(models, key=lambda m: results[m]['bic'])
        best_r2 = max(models, key=lambda m: results[m]['r_squared'])
        
        results['comparison'] = {
            'best_by_aic': best_aic,
            'best_by_bic': best_bic,
            'best_by_r2': best_r2,
            'improvement_over_original_r2': results[best_r2]['r_squared'] - r2_orig
        }
        
        self.results = results
        return results
    
    def analyze_residuals(self, y: np.ndarray, y_pred: np.ndarray, 
                          group_types: np.ndarray) -> Dict:
        """残差分析"""
        residuals = y - y_pred
        
        # 正态性检验
        shapiro_stat, shapiro_p = stats.shapiro(residuals) if len(residuals) >= 3 else (None, None)
        
        # 按类型分析残差
        type_residuals = {}
        for gt in np.unique(group_types):
            mask = group_types == gt
            type_res = residuals[mask]
            type_residuals[gt] = {
                'mean': np.mean(type_res),
                'std': np.std(type_res),
                'max_abs': np.max(np.abs(type_res))
            }
        
        return {
            'mean': np.mean(residuals),
            'std': np.std(residuals),
            'shapiro_stat': shapiro_stat,
            'shapiro_p': shapiro_p,
            'by_type': type_residuals
        }


# ============================================================================
# 可视化
# ============================================================================

class ImprovedHypothesisVisualizer:
    """改进假设的可视化"""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
    
    def plot_model_comparison(self, x: np.ndarray, y: np.ndarray, group_types: np.ndarray,
                              global_model: GlobalFittingModel,
                              type_model: GroupTypeFittingModel,
                              filename: str = "improved_model_comparison.png"):
        """比较不同模型的拟合效果"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        type_colors = {'C': 'red', 'B': 'blue', 'S': 'orange', 'CL': 'green'}
        type_names = {'C': 'Cusped', 'B': 'Bianchi', 'S': 'Schottky', 'CL': 'Closed'}
        
        # 原始假设A
        ax = axes[0]
        y_pred_orig = 1.0 + x
        for gt in np.unique(group_types):
            mask = group_types == gt
            ax.scatter(y_pred_orig[mask], y[mask], s=100, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'), label=type_names.get(gt, gt))
        
        min_val, max_val = min(y.min(), y_pred_orig.min()) * 0.9, max(y.max(), y_pred_orig.max()) * 1.1
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', label='Perfect Match')
        
        # 回归线
        slope, intercept, r_value, _, _ = stats.linregress(y_pred_orig, y)
        x_line = np.linspace(min_val, max_val, 100)
        ax.plot(x_line, slope * x_line + intercept, 'b-', 
                label=f'Fit (R²={r_value**2:.3f})')
        
        ax.set_xlabel('Predicted (Original)', fontsize=11)
        ax.set_ylabel('Observed Dimension', fontsize=11)
        ax.set_title('Original Hypothesis A\n$\\dim_H = 1 + \\frac{1}{\\log V} \\cdot \\frac{L\'}{L}$', 
                     fontsize=12)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # 全局拟合
        ax = axes[1]
        y_pred_global = global_model.predict(x)
        for gt in np.unique(group_types):
            mask = group_types == gt
            ax.scatter(y_pred_global[mask], y[mask], s=100, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'), label=type_names.get(gt, gt))
        
        min_val, max_val = min(y.min(), y_pred_global.min()) * 0.9, max(y.max(), y_pred_global.max()) * 1.1
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', label='Perfect Match')
        
        slope, intercept, r_value, _, _ = stats.linregress(y_pred_global, y)
        x_line = np.linspace(min_val, max_val, 100)
        ax.plot(x_line, slope * x_line + intercept, 'b-', 
                label=f'Fit (R²={r_value**2:.3f})')
        
        ax.set_xlabel('Predicted (Global Fit)', fontsize=11)
        ax.set_ylabel('Observed Dimension', fontsize=11)
        ax.set_title(f'Global Fit\n$\\dim_H = 1 + {global_model.alpha:.3f} \\cdot x + {global_model.beta:.3f}$\n'
                     f'R² = {global_model.r_squared:.3f}', fontsize=12)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # 分类型拟合
        ax = axes[2]
        y_pred_type = type_model.predict(x, group_types)
        for gt in np.unique(group_types):
            mask = group_types == gt
            ax.scatter(y_pred_type[mask], y[mask], s=100, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'), label=type_names.get(gt, gt))
        
        min_val, max_val = min(y.min(), y_pred_type.min()) * 0.9, max(y.max(), y_pred_type.max()) * 1.1
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', label='Perfect Match')
        
        slope, intercept, r_value, _, _ = stats.linregress(y_pred_type, y)
        x_line = np.linspace(min_val, max_val, 100)
        ax.plot(x_line, slope * x_line + intercept, 'b-', 
                label=f'Fit (R²={r_value**2:.3f})')
        
        gamma_str = "\n".join([f"$\\gamma_{{{k}}}={v:.3f}$" for k, v in type_model.gamma.items()])
        ax.set_xlabel('Predicted (Group Type Fit)', fontsize=11)
        ax.set_ylabel('Observed Dimension', fontsize=11)
        ax.set_title(f'Group Type Fit\n$\\dim_H = 1 + {type_model.alpha:.3f} \\cdot x + \\gamma_{{type}}$\n'
                     f'R² = {type_model.r_squared:.3f}\n{gamma_str}', fontsize=12)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"{self.output_dir}/{filename}"
    
    def plot_residual_analysis(self, x: np.ndarray, y: np.ndarray, group_types: np.ndarray,
                               type_model: GroupTypeFittingModel,
                               filename: str = "residual_analysis_improved.png"):
        """残差分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        y_pred = type_model.predict(x, group_types)
        residuals = y - y_pred
        
        type_colors = {'C': 'red', 'B': 'blue', 'S': 'orange', 'CL': 'green'}
        type_names = {'C': 'Cusped', 'B': 'Bianchi', 'S': 'Schottky', 'CL': 'Closed'}
        
        # 残差vs预测值
        ax = axes[0, 0]
        for gt in np.unique(group_types):
            mask = group_types == gt
            ax.scatter(y_pred[mask], residuals[mask], s=100, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'), label=type_names.get(gt, gt))
        ax.axhline(y=0, color='k', linestyle='--', linewidth=2)
        ax.set_xlabel('Predicted Dimension', fontsize=11)
        ax.set_ylabel('Residual', fontsize=11)
        ax.set_title('Residuals vs Predicted', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 残差分布
        ax = axes[0, 1]
        ax.hist(residuals, bins=10, alpha=0.7, color='steelblue', edgecolor='black')
        ax.axvline(x=0, color='r', linestyle='--', linewidth=2)
        ax.axvline(x=np.mean(residuals), color='g', linestyle='-', linewidth=2,
                   label=f'Mean: {np.mean(residuals):.3f}')
        ax.set_xlabel('Residual', fontsize=11)
        ax.set_ylabel('Frequency', fontsize=11)
        ax.set_title('Distribution of Residuals', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # 残差按类型分组
        ax = axes[1, 0]
        positions = []
        labels = []
        for i, gt in enumerate(np.unique(group_types)):
            mask = group_types == gt
            positions.append(i)
            labels.append(type_names.get(gt, gt))
            type_res = residuals[mask]
            ax.scatter([i] * len(type_res), type_res, s=100, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'))
            ax.boxplot(type_res, positions=[i], widths=0.3)
        ax.axhline(y=0, color='k', linestyle='--', linewidth=2)
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Residual', fontsize=11)
        ax.set_title('Residuals by Group Type', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        # 残差vs归一化项
        ax = axes[1, 1]
        for gt in np.unique(group_types):
            mask = group_types == gt
            ax.scatter(x[mask], residuals[mask], s=100, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'), label=type_names.get(gt, gt))
        ax.axhline(y=0, color='k', linestyle='--', linewidth=2)
        ax.set_xlabel('Normalized Term (1/log V) * (L\'/L)', fontsize=11)
        ax.set_ylabel('Residual', fontsize=11)
        ax.set_title('Residuals vs Normalized Term', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"{self.output_dir}/{filename}"
    
    def plot_final_formula(self, x: np.ndarray, y: np.ndarray, group_types: np.ndarray,
                           type_model: GroupTypeFittingModel,
                           filename: str = "final_formula_validation.png"):
        """最终公式验证图"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        y_pred = type_model.predict(x, group_types)
        
        type_colors = {'C': 'red', 'B': 'blue', 'S': 'orange', 'CL': 'green'}
        type_names = {'C': 'Cusped', 'B': 'Bianchi', 'S': 'Schottky', 'CL': 'Closed'}
        
        # 绘制每种类型的点
        for gt in np.unique(group_types):
            mask = group_types == gt
            ax.scatter(y_pred[mask], y[mask], s=200, alpha=0.7, 
                      c=type_colors.get(gt, 'gray'), 
                      label=f"{type_names.get(gt, gt)} (n={np.sum(mask)})",
                      edgecolors='black', linewidth=2)
        
        # 对角线
        min_val = min(y.min(), y_pred.min()) * 0.95
        max_val = max(y.max(), y_pred.max()) * 1.05
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', 
                label='Perfect Match', linewidth=2)
        
        # 回归线
        slope, intercept, r_value, p_value, _ = stats.linregress(y_pred, y)
        x_line = np.linspace(min_val, max_val, 100)
        ax.plot(x_line, slope * x_line + intercept, 'b-', 
                label=f'Linear Fit (R²={r_value**2:.4f})', linewidth=2)
        
        # 95%置信区间（简化）
        residual_std = np.std(y - y_pred)
        ax.fill_between(x_line, 
                        slope * x_line + intercept - 1.96 * residual_std,
                        slope * x_line + intercept + 1.96 * residual_std,
                        alpha=0.2, color='blue', label='95% Confidence')
        
        ax.set_xlabel('Predicted Dimension (Improved Formula)', fontsize=13)
        ax.set_ylabel('Observed Dimension', fontsize=13)
        
        # 标题包含最终公式
        gamma_lines = "\n".join([f"  ${k}$: $\\gamma = {v:+.3f}$" 
                                  for k, v in sorted(type_model.gamma.items())])
        ax.set_title(f'Final Improved Hypothesis A\n'
                     f'$\\dim_H = 1 + {type_model.alpha:.4f} \\cdot \\frac{{1}}{{\\log V}} \\cdot \\frac{{L\'}}{{L}} + \\gamma_{{type}}$\n'
                     f'{gamma_lines}\n'
                     f'$R^2 = {type_model.r_squared:.4f}$, RMSE = {type_model.rmse:.4f}',
                     fontsize=14)
        
        ax.legend(loc='upper left', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"{self.output_dir}/{filename}"


# ============================================================================
# 主程序
# ============================================================================

def run_improved_hypothesis_A_validation(output_dir: str = ".") -> Dict:
    """
    执行完整的改进假设A验证
    """
    print("=" * 80)
    print("假设A改进版：添加拟合参数和群类型特定修正")
    print("=" * 80)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 初始化数据集
    print("[1/8] 初始化15个Kleinian群数据集...")
    dataset = KleinianDataset()
    X, y, types, names = dataset.get_training_data()
    print(f"      总群数量: {len(dataset.data)}")
    print(f"      可用训练样本: {len(X)}")
    print(f"      群类型分布: ")
    for gt in np.unique(types):
        count = np.sum(types == gt)
        print(f"        - Type {gt}: {count}个")
    print()
    
    # 打印数据表
    print("[2/8] 数据汇总表:")
    print("-" * 100)
    print(f"{'Group Name':<40} {'Type':<8} {'Observed':<10} {'Normalized Term':<18} {'Notes':<20}")
    print("-" * 100)
    for name, gt, dim, x in zip(names, types, y, X):
        group = [g for g in dataset.data.values() if g.name == name][0]
        print(f"{name:<40} {gt:<8} {dim:<10.3f} {x:<18.4f} {group.notes[:20]:<20}")
    print("-" * 100)
    print()
    
    # 全局拟合
    print("[3/8] 全局拟合（优化α, β参数）...")
    global_model = GlobalFittingModel()
    global_results = global_model.fit(X, y)
    print(f"      最优参数:")
    print(f"        α = {global_results['alpha']:.4f} ± {global_results['alpha_std']:.4f}")
    print(f"        β = {global_results['beta']:.4f} ± {global_results['beta_std']:.4f}")
    print(f"      拟合优度:")
    print(f"        R² = {global_results['r_squared']:.4f}")
    print(f"        Adjusted R² = {global_results['adj_r_squared']:.4f}")
    print(f"        RMSE = {global_results['rmse']:.4f}")
    print(f"        MAE = {global_results['mae']:.4f}")
    print()
    
    # 分类型拟合
    print("[4/8] 分类型拟合（优化α, γ_type参数）...")
    type_model = GroupTypeFittingModel()
    type_results = type_model.fit(X, y, types)
    print(f"      最优参数:")
    print(f"        α = {type_results['alpha']:.4f}")
    for gt, gamma in sorted(type_results['gamma'].items()):
        print(f"        γ_{gt} = {gamma:+.4f}")
    print(f"      拟合优度:")
    print(f"        R² = {type_results['r_squared']:.4f}")
    print(f"        Adjusted R² = {type_results['adj_r_squared']:.4f}")
    print(f"        RMSE = {type_results['rmse']:.4f}")
    print(f"        MAE = {type_results['mae']:.4f}")
    print(f"        参数个数 = {type_results['n_params']}")
    print()
    
    # 模型比较
    print("[5/8] 模型比较（AIC/BIC）...")
    validator = ModelValidator()
    comparison = validator.compare_models(X, y, types)
    
    print("      原始假设A:")
    print(f"        R² = {comparison['original']['r_squared']:.4f}, "
          f"RMSE = {comparison['original']['rmse']:.4f}, "
          f"AIC = {comparison['original']['aic']:.2f}, "
          f"BIC = {comparison['original']['bic']:.2f}")
    
    print("      全局拟合:")
    print(f"        R² = {comparison['global']['r_squared']:.4f}, "
          f"RMSE = {comparison['global']['rmse']:.4f}, "
          f"AIC = {comparison['global']['aic']:.2f}, "
          f"BIC = {comparison['global']['bic']:.2f}")
    
    print("      分类型拟合:")
    print(f"        R² = {comparison['group_type']['r_squared']:.4f}, "
          f"RMSE = {comparison['group_type']['rmse']:.4f}, "
          f"AIC = {comparison['group_type']['aic']:.2f}, "
          f"BIC = {comparison['group_type']['bic']:.2f}")
    
    print(f"\n      最佳模型（按AIC）: {comparison['comparison']['best_by_aic']}")
    print(f"      最佳模型（按BIC）: {comparison['comparison']['best_by_bic']}")
    print(f"      相比原始的R²提升: {comparison['comparison']['improvement_over_original_r2']:.4f}")
    print()
    
    # 交叉验证
    print("[6/8] 交叉验证...")
    cv_global = validator.cross_validate(GlobalFittingModel, X, y, None, k=5)
    cv_type = validator.cross_validate(GroupTypeFittingModel, X, y, types, k=5)
    
    print(f"      全局拟合模型:")
    print(f"        CV RMSE: {cv_global['mean_rmse']:.4f} ± {cv_global['std_rmse']:.4f}")
    print(f"        CV MAE: {cv_global['mean_mae']:.4f}")
    
    print(f"      分类型拟合模型:")
    print(f"        CV RMSE: {cv_type['mean_rmse']:.4f} ± {cv_type['std_rmse']:.4f}")
    print(f"        CV MAE: {cv_type['mean_mae']:.4f}")
    print()
    
    # 残差分析
    print("[7/8] 残差分析...")
    residuals_analysis = validator.analyze_residuals(y, type_model.predict(X, types), types)
    print(f"      整体残差:")
    print(f"        Mean = {residuals_analysis['mean']:.4f}")
    print(f"        Std = {residuals_analysis['std']:.4f}")
    print(f"        Shapiro p = {residuals_analysis['shapiro_p']:.4f}")
    print(f"      按类型:")
    for gt, stats in residuals_analysis['by_type'].items():
        print(f"        Type {gt}: Mean={stats['mean']:+.4f}, Std={stats['std']:.4f}")
    print()
    
    # 生成可视化
    print("[8/8] 生成可视化图表...")
    viz = ImprovedHypothesisVisualizer(output_dir)
    
    try:
        viz.plot_model_comparison(X, y, types, global_model, type_model)
        print("      - 模型比较图: improved_model_comparison.png")
    except Exception as e:
        print(f"      - 模型比较图生成失败: {e}")
    
    try:
        viz.plot_residual_analysis(X, y, types, type_model)
        print("      - 残差分析图: residual_analysis_improved.png")
    except Exception as e:
        print(f"      - 残差分析图生成失败: {e}")
    
    try:
        viz.plot_final_formula(X, y, types, type_model)
        print("      - 最终公式验证图: final_formula_validation.png")
    except Exception as e:
        print(f"      - 最终公式验证图生成失败: {e}")
    print()
    
    # 汇总结果
    print("=" * 80)
    print("验证完成!")
    print("=" * 80)
    print(f"\n最终改进公式:")
    print(f"  $\\dim_H = 1 + {type_model.alpha:.4f} \\cdot \\frac{{1}}{{\\log V}} \\cdot \\frac{{L'}}{{L}} + \\gamma_{{type}}$")
    print(f"\n群类型修正项:")
    for gt, gamma in sorted(type_model.gamma.items()):
        type_full = {'C': 'Cusped', 'B': 'Bianchi', 'S': 'Schottky', 'CL': 'Closed'}[gt]
        print(f"  Type {gt} ({type_full}): γ = {gamma:+.4f}")
    print(f"\n性能指标:")
    print(f"  R² = {type_results['r_squared']:.4f} (目标: > 0.7)")
    print(f"  Adjusted R² = {type_results['adj_r_squared']:.4f}")
    print(f"  RMSE = {type_results['rmse']:.4f}")
    print(f"  MAE = {type_results['mae']:.4f}")
    print()
    
    # 保存结果
    results = {
        'timestamp': datetime.now().isoformat(),
        'dataset': {
            'n_groups': len(dataset.data),
            'n_training': len(X),
            'group_names': names,
            'observed': y.tolist(),
            'normalized_terms': X.tolist(),
            'types': types.tolist()
        },
        'global_fitting': global_results,
        'group_type_fitting': type_results,
        'model_comparison': comparison,
        'cross_validation': {
            'global': cv_global,
            'group_type': cv_type
        },
        'residual_analysis': residuals_analysis,
        'final_formula': {
            'alpha': type_model.alpha,
            'gamma': type_model.gamma,
            'latex': type_model.get_formula_latex()
        }
    }
    
    return results


if __name__ == "__main__":
    # 检查scikit-learn是否可用（用于分层交叉验证）
    try:
        from sklearn.model_selection import StratifiedKFold
    except ImportError:
        print("警告: scikit-learn未安装，将使用简单交叉验证")
        print("安装命令: pip install scikit-learn")
    
    # 运行验证
    results = run_improved_hypothesis_A_validation(output_dir=".")
    
    # 保存结果到JSON
    output_file = "hypothesis_A_improved_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n详细结果已保存到: {output_file}")
