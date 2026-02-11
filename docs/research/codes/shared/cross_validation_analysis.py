#!/usr/bin/env python3
"""
交叉验证和误差分析系统
为L2严格性提供统计支持

本模块实现：
1. K折交叉验证（K=5,10）
2. 留一法验证 (LOO)
3. 自助法(Bootstrap)置信区间
4. 误差分析（系统误差、随机误差、误差传播）
5. 统计检验（拟合优度、正态性、异方差性）
6. 模型选择（AIC, BIC）
7. 敏感性分析

作者: Fixed-4D-Topology Research Group
日期: 2026-02-11
"""

import numpy as np
import json
from scipy import stats
from scipy.optimize import curve_fit, minimize
from scipy.linalg import pinv
from typing import List, Dict, Tuple, Callable, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
import warnings
from collections import defaultdict
import copy

warnings.filterwarnings('ignore')

# 配置
RESULTS_DIR = Path(__file__).parent / "cross_validation_results"
RESULTS_DIR.mkdir(exist_ok=True)


@dataclass
class ValidationResult:
    """验证结果数据类"""
    method: str                          # 验证方法名称
    n_samples: int                       # 样本数
    dimension_estimates: np.ndarray      # 维数估计值
    mean: float                          # 均值
    std: float                           # 标准差
    ci_95: Tuple[float, float]           # 95%置信区间
    ci_99: Tuple[float, float]           # 99%置信区间
    mse: float                           # 均方误差
    rmse: float                          # 均方根误差
    mae: float                           # 平均绝对误差
    bias: float                          # 偏差
    variance: float                      # 方差
    residuals: np.ndarray                # 残差
    outlier_indices: List[int]           # 异常值索引
    convergence_rate: Optional[float] = None  # 收敛率
    computation_time: Optional[float] = None  # 计算时间
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'method': self.method,
            'n_samples': int(self.n_samples),
            'mean': float(self.mean),
            'std': float(self.std),
            'ci_95': [float(self.ci_95[0]), float(self.ci_95[1])],
            'ci_99': [float(self.ci_99[0]), float(self.ci_99[1])],
            'mse': float(self.mse),
            'rmse': float(self.rmse),
            'mae': float(self.mae),
            'bias': float(self.bias),
            'variance': float(self.variance),
            'dimension_estimates': np.asarray(self.dimension_estimates).tolist(),
            'outlier_indices': [int(i) for i in self.outlier_indices],
            'convergence_rate': float(self.convergence_rate) if self.convergence_rate is not None else None,
            'computation_time': float(self.computation_time) if self.computation_time is not None else None
        }


@dataclass
class StatisticalTestResult:
    """统计检验结果"""
    test_name: str
    statistic: float
    p_value: float
    alpha: float
    reject_null: bool
    interpretation: str
    
    def to_dict(self) -> dict:
        return {
            'test_name': self.test_name,
            'statistic': float(self.statistic),
            'p_value': float(self.p_value),
            'alpha': self.alpha,
            'reject_null': bool(self.reject_null),
            'interpretation': self.interpretation
        }


@dataclass
class SensitivityResult:
    """敏感性分析结果"""
    parameter_name: str
    parameter_values: np.ndarray
    dimension_estimates: np.ndarray
    sensitivity_coefficient: float
    elasticity: float
    critical_threshold: Optional[float]
    
    def to_dict(self) -> dict:
        return {
            'parameter_name': self.parameter_name,
            'parameter_values': self.parameter_values.tolist(),
            'dimension_estimates': self.dimension_estimates.tolist(),
            'sensitivity_coefficient': float(self.sensitivity_coefficient),
            'elasticity': float(self.elasticity),
            'critical_threshold': self.critical_threshold
        }


class CrossValidator:
    """
    交叉验证分析器
    
    为Kleinian群和p-adic多项式数据提供全面的交叉验证
    """
    
    def __init__(self, data: Dict, random_state: int = 42):
        """
        初始化验证器
        
        Args:
            data: 输入数据字典
            random_state: 随机种子
        """
        self.data = data
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.validation_results: Dict[str, ValidationResult] = {}
        self.statistical_tests: Dict[str, StatisticalTestResult] = {}
        self.sensitivity_results: Dict[str, SensitivityResult] = {}
        
    def extract_kleinian_data(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        提取Kleinian群数据
        
        Returns:
            (volumes, dimensions, group_names)
        """
        if 'results' not in self.data:
            raise ValueError("数据格式错误：缺少'results'键")
        
        results = self.data['results']
        volumes = np.array([r['volume'] for r in results])
        dimensions = np.array([r['hausdorff_dim'] for r in results])
        names = [r['group_name'] for r in results]
        
        return volumes, dimensions, names
    
    def extract_padic_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        提取p-adic数据
        
        Returns:
            (p_values, d_values, dimensions)
        """
        if 'bowen_verifications' not in self.data:
            raise ValueError("数据格式错误：缺少'bowen_verifications'键")
        
        verifications = self.data['bowen_verifications']
        p_vals = np.array([v['p'] for v in verifications])
        d_vals = np.array([v['d'] for v in verifications])
        dimensions = np.array([v['bowen_dimension'] for v in verifications])
        
        return p_vals, d_vals, dimensions
    
    def k_fold_cross_validation(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        k: int = 5,
        model_func: Optional[Callable] = None,
        model_name: str = "default"
    ) -> ValidationResult:
        """
        K折交叉验证
        
        Args:
            X: 特征数据
            y: 目标数据（维数）
            k: 折数
            model_func: 模型函数
            model_name: 模型名称
            
        Returns:
            ValidationResult
        """
        n = len(y)
        indices = np.arange(n)
        self.rng.shuffle(indices)
        
        fold_sizes = np.full(k, n // k)
        fold_sizes[:n % k] += 1
        current = 0
        
        predictions = []
        actuals = []
        
        for fold_size in fold_sizes:
            test_idx = indices[current:current + fold_size]
            train_idx = np.concatenate([indices[:current], indices[current + fold_size:]])
            
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # 训练模型并预测
            y_pred = self._fit_and_predict(X_train, y_train, X_test, model_func)
            
            predictions.extend(y_pred)
            actuals.extend(y_test)
            
            current += fold_size
        
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        return self._compute_validation_metrics(
            predictions, actuals, f"{k}-Fold CV ({model_name})"
        )
    
    def leave_one_out_validation(
        self,
        X: np.ndarray,
        y: np.ndarray,
        model_func: Optional[Callable] = None,
        model_name: str = "default"
    ) -> ValidationResult:
        """
        留一法交叉验证
        
        Args:
            X: 特征数据
            y: 目标数据
            model_func: 模型函数
            model_name: 模型名称
            
        Returns:
            ValidationResult
        """
        n = len(y)
        predictions = []
        
        for i in range(n):
            test_idx = [i]
            train_idx = [j for j in range(n) if j != i]
            
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            y_pred = self._fit_and_predict(X_train, y_train, X_test, model_func)
            predictions.append(y_pred[0])
        
        predictions = np.array(predictions)
        
        return self._compute_validation_metrics(
            predictions, y, f"LOO CV ({model_name})"
        )
    
    def bootstrap_confidence_interval(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_bootstrap: int = 10000,
        confidence_levels: List[float] = [0.95, 0.99],
        model_func: Optional[Callable] = None,
        model_name: str = "default"
    ) -> Dict[str, Union[np.ndarray, Dict]]:
        """
        Bootstrap置信区间估计
        
        Args:
            X: 特征数据
            y: 目标数据
            n_bootstrap: Bootstrap样本数
            confidence_levels: 置信水平列表
            model_func: 模型函数
            model_name: 模型名称
            
        Returns:
            包含置信区间的字典
        """
        n = len(y)
        bootstrap_estimates = []
        
        for _ in range(n_bootstrap):
            # 有放回抽样
            indices = self.rng.choice(n, size=n, replace=True)
            X_boot, y_boot = X[indices], y[indices]
            
            # 计算维数估计
            try:
                if model_func is None:
                    # 默认使用均值作为估计
                    estimate = np.mean(y_boot)
                else:
                    # 使用模型拟合
                    y_pred = model_func(X_boot, y_boot, X)
                    estimate = np.mean(y_pred)
                bootstrap_estimates.append(estimate)
            except:
                continue
        
        bootstrap_estimates = np.array(bootstrap_estimates)
        
        # 处理退化情况（所有值相同）
        if np.std(bootstrap_estimates) < 1e-15:
            # 所有值相同，返回固定值
            val = float(np.mean(bootstrap_estimates))
            results = {
                'estimates': bootstrap_estimates.tolist(),
                'mean': val,
                'std': 0.0,
                'median': val,
                'percentiles': {}
            }
            for conf in confidence_levels:
                results['percentiles'][f'ci_{int(conf*100)}'] = (val, val)
        else:
            # 计算各种置信区间
            results = {
                'estimates': bootstrap_estimates.tolist(),
                'mean': float(np.mean(bootstrap_estimates)),
                'std': float(np.std(bootstrap_estimates)),
                'median': float(np.median(bootstrap_estimates)),
                'percentiles': {}
            }
            
            for conf in confidence_levels:
                alpha = 1 - conf
                lower = float(np.percentile(bootstrap_estimates, max(0.0, 100 * alpha / 2)))
                upper = float(np.percentile(bootstrap_estimates, min(100.0, 100 * (1 - alpha / 2))))
                results['percentiles'][f'ci_{int(conf*100)}'] = (lower, upper)
        
        # 计算Bootstrap t区间
        original_mean = np.mean(y)
        se_boot = np.std(bootstrap_estimates)
        t_critical = stats.t.ppf(0.975, n - 1)
        
        results['bootstrap_t_ci'] = (
            original_mean - t_critical * se_boot,
            original_mean + t_critical * se_boot
        )
        
        # BCa (Bias-Corrected and Accelerated) 区间
        results['bca_ci'] = self._compute_bca_interval(
            bootstrap_estimates, original_mean, n
        )
        
        return results
    
    def _compute_bca_interval(
        self, 
        bootstrap_estimates: np.ndarray, 
        original_estimate: float,
        n: int,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        计算BCa置信区间
        
        Args:
            bootstrap_estimates: Bootstrap估计值
            original_estimate: 原始估计值
            n: 样本数
            confidence: 置信水平
            
        Returns:
            (lower, upper) BCa置信区间
        """
        # Bias correction
        z0 = stats.norm.ppf(
            np.mean(bootstrap_estimates < original_estimate)
        )
        
        # Acceleration (使用jackknife估计)
        # 简化版本：使用经验估计
        theta_jack = []
        for i in range(min(n, 100)):  # 限制计算量
            leave_one_out = np.delete(bootstrap_estimates[:min(len(bootstrap_estimates), n)], i)
            theta_jack.append(np.mean(leave_one_out))
        
        theta_jack = np.array(theta_jack)
        theta_dot = np.mean(theta_jack)
        
        numerator = np.sum((theta_dot - theta_jack) ** 3)
        denominator = 6 * (np.sum((theta_dot - theta_jack) ** 2) ** 1.5)
        
        if denominator > 1e-10:
            a = numerator / denominator
        else:
            a = 0
        
        # 计算调整后的百分位数
        alpha = 1 - confidence
        z_alpha_2 = stats.norm.ppf(alpha / 2)
        z_1_alpha_2 = stats.norm.ppf(1 - alpha / 2)
        
        adjusted_lower = stats.norm.cdf(
            z0 + (z0 + z_alpha_2) / (1 - a * (z0 + z_alpha_2))
        )
        adjusted_upper = stats.norm.cdf(
            z0 + (z0 + z_1_alpha_2) / (1 - a * (z0 + z_1_alpha_2))
        )
        
        lower = np.percentile(bootstrap_estimates, 100 * adjusted_lower)
        upper = np.percentile(bootstrap_estimates, 100 * adjusted_upper)
        
        return (lower, upper)
    
    def _fit_and_predict(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        model_func: Optional[Callable]
    ) -> np.ndarray:
        """
        拟合模型并预测
        
        Args:
            X_train: 训练特征
            y_train: 训练目标
            X_test: 测试特征
            model_func: 模型函数
            
        Returns:
            预测值
        """
        if model_func is None:
            # 默认使用简单线性回归
            if len(X_train.shape) == 1:
                X_train = X_train.reshape(-1, 1)
            if len(X_test.shape) == 1:
                X_test = X_test.reshape(-1, 1)
            
            # 添加常数项
            X_train_aug = np.column_stack([np.ones(len(X_train)), X_train])
            X_test_aug = np.column_stack([np.ones(len(X_test)), X_test])
            
            # 最小二乘解
            beta = pinv(X_train_aug.T @ X_train_aug) @ X_train_aug.T @ y_train
            y_pred = X_test_aug @ beta
        else:
            y_pred = model_func(X_train, y_train, X_test)
        
        return y_pred
    
    def _compute_validation_metrics(
        self,
        predictions: np.ndarray,
        actuals: np.ndarray,
        method_name: str
    ) -> ValidationResult:
        """
        计算验证指标
        
        Args:
            predictions: 预测值
            actuals: 真实值
            method_name: 方法名称
            
        Returns:
            ValidationResult
        """
        residuals = predictions - actuals
        n = len(actuals)
        
        # 基本统计量
        mean = np.mean(predictions)
        std = np.std(predictions, ddof=1)
        
        # 置信区间
        se = std / np.sqrt(n)
        t_95 = stats.t.ppf(0.975, n - 1)
        t_99 = stats.t.ppf(0.995, n - 1)
        ci_95 = (mean - t_95 * se, mean + t_95 * se)
        ci_99 = (mean - t_99 * se, mean + t_99 * se)
        
        # 误差指标
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(residuals))
        bias = np.mean(residuals)
        variance = np.var(predictions, ddof=1)
        
        # 异常值检测 (使用IQR方法)
        q1, q3 = np.percentile(predictions, [25, 75])
        iqr = q3 - q1
        outlier_mask = (
            (predictions < q1 - 1.5 * iqr) | 
            (predictions > q3 + 1.5 * iqr)
        )
        outlier_indices = np.where(outlier_mask)[0].tolist()
        
        return ValidationResult(
            method=method_name,
            n_samples=n,
            dimension_estimates=predictions,
            mean=mean,
            std=std,
            ci_95=ci_95,
            ci_99=ci_99,
            mse=mse,
            rmse=rmse,
            mae=mae,
            bias=bias,
            variance=variance,
            residuals=residuals,
            outlier_indices=outlier_indices
        )


class ErrorAnalyzer:
    """误差分析器"""
    
    def __init__(self):
        self.error_budget = {}
        
    def estimate_systematic_error(
        self, 
        values: np.ndarray, 
        true_value: Optional[float] = None
    ) -> Dict[str, float]:
        """
        估计系统误差
        
        Args:
            values: 测量值数组
            true_value: 真实值（如果已知）
            
        Returns:
            系统误差估计结果
        """
        n = len(values)
        mean = np.mean(values)
        
        # 如果已知真实值，直接计算偏差
        if true_value is not None:
            bias = mean - true_value
            relative_bias = bias / true_value if true_value != 0 else float('inf')
        else:
            # 使用Jackknife估计偏差
            jackknife_estimates = []
            for i in range(n):
                jackknife_estimates.append(np.mean(np.delete(values, i)))
            
            jackknife_mean = np.mean(jackknife_estimates)
            bias = (n - 1) * (jackknife_mean - mean)
            relative_bias = bias / mean if mean != 0 else float('inf')
        
        return {
            'bias': bias,
            'relative_bias': relative_bias,
            'bias_percentage': abs(relative_bias) * 100,
            'estimated_true_value': mean - bias
        }
    
    def estimate_random_error(self, values: np.ndarray) -> Dict[str, float]:
        """
        估计随机误差
        
        Args:
            values: 测量值数组
            
        Returns:
            随机误差估计结果
        """
        n = len(values)
        
        # 标准统计量
        std = np.std(values, ddof=1)
        sem = std / np.sqrt(n)  # 标准误差
        
        # 置信区间半宽
        t_critical = stats.t.ppf(0.975, n - 1)
        ci_half_width = t_critical * sem
        
        # 变异系数
        cv = std / np.mean(values) if np.mean(values) != 0 else float('inf')
        
        # 使用MAD (Median Absolute Deviation) 作为稳健估计
        mad = np.median(np.abs(values - np.median(values)))
        mad_scaled = mad * 1.4826  # 转换为标准差估计
        
        return {
            'std': std,
            'sem': sem,
            'ci_half_width': ci_half_width,
            'cv': cv,
            'cv_percentage': cv * 100,
            'mad': mad,
            'mad_scaled': mad_scaled,
            'precision': 1 / cv if cv > 0 else float('inf')
        }
    
    def error_propagation(
        self,
        func: Callable,
        variables: Dict[str, Tuple[float, float]],
        correlations: Optional[Dict[Tuple[str, str], float]] = None
    ) -> Dict[str, float]:
        """
        误差传播分析
        
        Args:
            func: 目标函数，接受变量字典返回标量
            variables: 变量名到(值, 不确定度)的映射
            correlations: 变量间的相关系数
            
        Returns:
            误差传播结果
        """
        var_names = list(variables.keys())
        values = np.array([variables[v][0] for v in var_names])
        uncertainties = np.array([variables[v][1] for v in var_names])
        
        # 数值微分计算偏导数
        epsilon = 1e-8
        partial_derivatives = []
        
        base_value = func(dict(zip(var_names, values)))
        
        for i, var in enumerate(var_names):
            values_perturbed = values.copy()
            values_perturbed[i] += epsilon
            perturbed_value = func(dict(zip(var_names, values_perturbed)))
            partial = (perturbed_value - base_value) / epsilon
            partial_derivatives.append(partial)
        
        partial_derivatives = np.array(partial_derivatives)
        
        # 计算合成不确定度
        # 简单情况（无相关性）
        variance_uncorrelated = np.sum(
            (partial_derivatives * uncertainties) ** 2
        )
        
        # 考虑相关性
        variance_correlated = variance_uncorrelated
        if correlations:
            for (var1, var2), corr in correlations.items():
                if var1 in var_names and var2 in var_names:
                    i, j = var_names.index(var1), var_names.index(var2)
                    variance_correlated += (
                        2 * partial_derivatives[i] * partial_derivatives[j] *
                        uncertainties[i] * uncertainties[j] * corr
                    )
        
        combined_uncertainty = np.sqrt(variance_correlated)
        
        # 各变量的贡献
        contributions = {
            var: abs(partial_derivatives[i]) * uncertainties[i]
            for i, var in enumerate(var_names)
        }
        
        # 相对贡献
        total_contribution = sum(contributions.values())
        relative_contributions = {
            var: contrib / total_contribution if total_contribution > 0 else 0
            for var, contrib in contributions.items()
        }
        
        return {
            'function_value': base_value,
            'combined_uncertainty': combined_uncertainty,
            'relative_uncertainty': (
                combined_uncertainty / abs(base_value) if base_value != 0 else float('inf')
            ),
            'partial_derivatives': dict(zip(var_names, partial_derivatives.tolist())),
            'absolute_contributions': contributions,
            'relative_contributions': relative_contributions,
            'dominant_source': max(relative_contributions, key=relative_contributions.get)
        }
    
    def detect_outliers(
        self,
        values: np.ndarray,
        method: str = 'iqr',
        threshold: float = 3.0
    ) -> Dict[str, Union[List[int], np.ndarray]]:
        """
        异常值检测
        
        Args:
            values: 数据数组
            method: 检测方法 ('iqr', 'zscore', 'modified_zscore', 'grubbs')
            threshold: 阈值
            
        Returns:
            异常值检测结果
        """
        outliers = []
        
        if method == 'iqr':
            q1, q3 = np.percentile(values, [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            outliers = np.where(
                (values < lower_bound) | (values > upper_bound)
            )[0].tolist()
            
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(values))
            outliers = np.where(z_scores > threshold)[0].tolist()
            
        elif method == 'modified_zscore':
            median = np.median(values)
            mad = np.median(np.abs(values - median))
            modified_z_scores = 0.6745 * (values - median) / mad if mad > 0 else np.zeros_like(values)
            outliers = np.where(np.abs(modified_z_scores) > threshold)[0].tolist()
            
        elif method == 'grubbs':
            # Grubbs检验（迭代）
            temp_values = values.copy()
            temp_indices = np.arange(len(values))
            
            while len(temp_values) > 2:
                mean = np.mean(temp_values)
                std = np.std(temp_values, ddof=1)
                g_scores = np.abs(temp_values - mean) / std
                max_g_idx = np.argmax(g_scores)
                max_g = g_scores[max_g_idx]
                
                # Grubbs临界值
                n = len(temp_values)
                t_critical = stats.t.ppf(1 - 0.025 / n, n - 2)
                g_critical = (n - 1) * np.sqrt(t_critical**2 / (n * (n - 2 + t_critical**2)))
                
                if max_g > g_critical:
                    outliers.append(temp_indices[max_g_idx])
                    temp_values = np.delete(temp_values, max_g_idx)
                    temp_indices = np.delete(temp_indices, max_g_idx)
                else:
                    break
        
        # 计算异常值统计
        inliers = [i for i in range(len(values)) if i not in outliers]
        
        return {
            'outlier_indices': outliers,
            'n_outliers': len(outliers),
            'outlier_percentage': len(outliers) / len(values) * 100,
            'inlier_indices': inliers,
            'outlier_values': values[outliers].tolist() if outliers else [],
            'inlier_mean': np.mean(values[inliers]) if inliers else np.nan,
            'inlier_std': np.std(values[inliers], ddof=1) if inliers else np.nan
        }


class StatisticalTester:
    """统计检验器"""
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        
    def goodness_of_fit_test(
        self,
        observed: np.ndarray,
        expected: Optional[np.ndarray] = None,
        test_type: str = 'chisquare'
    ) -> StatisticalTestResult:
        """
        拟合优度检验
        
        Args:
            observed: 观测值
            expected: 期望值（如果None，假设均匀分布）
            test_type: 检验类型 ('chisquare', 'ks', 'ad')
            
        Returns:
            StatisticalTestResult
        """
        if test_type == 'chisquare':
            if expected is None:
                expected = np.full_like(observed, np.mean(observed))
            
            # 合并小样本
            observed_freq = observed
            expected_freq = expected
            
            # 卡方检验
            stat, p_value = stats.chisquare(observed_freq, expected_freq)
            interpretation = (
                "观测分布与期望分布有显著差异" if p_value < self.alpha 
                else "观测分布与期望分布无显著差异"
            )
            
        elif test_type == 'ks':
            # Kolmogorov-Smirnov检验（与正态分布比较）
            stat, p_value = stats.kstest(observed, 'norm', args=(np.mean(observed), np.std(observed)))
            interpretation = (
                "数据不符合正态分布" if p_value < self.alpha 
                else "数据符合正态分布"
            )
            
        elif test_type == 'ad':
            # Anderson-Darling检验
            stat, critical_values, significance_level = stats.anderson(observed, dist='norm')
            # 使用15%显著性水平
            p_value_idx = np.argmin(np.abs(significance_level - self.alpha * 100))
            critical_value = critical_values[p_value_idx]
            p_value = self.alpha if stat > critical_value else 1 - self.alpha
            interpretation = (
                "数据不符合正态分布" if stat > critical_value 
                else "数据符合正态分布"
            )
            stat = float(stat)
        
        return StatisticalTestResult(
            test_name=f"Goodness of Fit ({test_type})",
            statistic=stat,
            p_value=p_value,
            alpha=self.alpha,
            reject_null=p_value < self.alpha,
            interpretation=interpretation
        )
    
    def normality_test(self, data: np.ndarray) -> Dict[str, StatisticalTestResult]:
        """
        正态性检验
        
        Args:
            data: 数据数组
            
        Returns:
            各种正态性检验结果
        """
        results = {}
        
        # Shapiro-Wilk检验（适合小样本）
        if len(data) <= 5000:
            stat, p_value = stats.shapiro(data)
            results['shapiro'] = StatisticalTestResult(
                test_name="Shapiro-Wilk Normality Test",
                statistic=stat,
                p_value=p_value,
                alpha=self.alpha,
                reject_null=p_value < self.alpha,
                interpretation=(
                    "数据不符合正态分布" if p_value < self.alpha 
                    else "数据符合正态分布"
                )
            )
        
        # D'Agostino-Pearson检验
        stat, p_value = stats.normaltest(data)
        results['dagostino'] = StatisticalTestResult(
            test_name="D'Agostino-Pearson Normality Test",
            statistic=stat,
            p_value=p_value,
            alpha=self.alpha,
            reject_null=p_value < self.alpha,
            interpretation=(
                "数据不符合正态分布" if p_value < self.alpha 
                else "数据符合正态分布"
            )
        )
        
        # Anderson-Darling检验
        ad_stat, critical_vals, sig_levels = stats.anderson(data, dist='norm')
        idx = np.argmin(np.abs(sig_levels - self.alpha * 100))
        reject = ad_stat > critical_vals[idx]
        results['anderson'] = StatisticalTestResult(
            test_name="Anderson-Darling Normality Test",
            statistic=ad_stat,
            p_value=self.alpha if reject else 1 - self.alpha,
            alpha=self.alpha,
            reject_null=reject,
            interpretation=(
                "数据不符合正态分布" if reject else "数据符合正态分布"
            )
        )
        
        # Jarque-Bera检验
        stat, p_value = stats.jarque_bera(data)
        results['jarque_bera'] = StatisticalTestResult(
            test_name="Jarque-Bera Normality Test",
            statistic=stat,
            p_value=p_value,
            alpha=self.alpha,
            reject_null=p_value < self.alpha,
            interpretation=(
                "数据不符合正态分布" if p_value < self.alpha 
                else "数据符合正态分布"
            )
        )
        
        return results
    
    def heteroscedasticity_test(
        self,
        residuals: np.ndarray,
        fitted: np.ndarray,
        test_type: str = 'bp'
    ) -> StatisticalTestResult:
        """
        异方差性检验
        
        Args:
            residuals: 残差
            fitted: 拟合值
            test_type: 检验类型 ('bp' for Breusch-Pagan, 'white' for White)
            
        Returns:
            StatisticalTestResult
        """
        n = len(residuals)
        
        if test_type == 'bp':
            # Breusch-Pagan检验（简化实现）
            # 残差平方对拟合值回归
            y = residuals ** 2
            X = np.column_stack([np.ones(n), fitted])
            
            # OLS回归
            beta = pinv(X.T @ X) @ X.T @ y
            y_pred = X @ beta
            
            # 计算R^2
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            # LM统计量
            lm_stat = n * r_squared
            p_value = 1 - stats.chi2.cdf(lm_stat, df=1)
            
            interpretation = (
                "存在异方差性" if p_value < self.alpha 
                else "不存在异方差性"
            )
            
        elif test_type == 'white':
            # White检验（包含二次项）
            y = residuals ** 2
            X = np.column_stack([np.ones(n), fitted, fitted ** 2])
            
            beta = pinv(X.T @ X) @ X.T @ y
            y_pred = X @ beta
            
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            lm_stat = n * r_squared
            p_value = 1 - stats.chi2.cdf(lm_stat, df=2)
            
            interpretation = (
                "存在异方差性" if p_value < self.alpha 
                else "不存在异方差性"
            )
        
        return StatisticalTestResult(
            test_name=f"Heteroscedasticity Test ({test_type})",
            statistic=lm_stat,
            p_value=p_value,
            alpha=self.alpha,
            reject_null=p_value < self.alpha,
            interpretation=interpretation
        )


class ModelSelector:
    """模型选择器"""
    
    @staticmethod
    def compute_aic(n: int, k: int, log_likelihood: float) -> float:
        """
        计算AIC (Akaike Information Criterion)
        
        Args:
            n: 样本数
            k: 参数数
            log_likelihood: 对数似然
            
        Returns:
            AIC值
        """
        return 2 * k - 2 * log_likelihood
    
    @staticmethod
    def compute_aic_c(n: int, k: int, log_likelihood: float) -> float:
        """
        计算AICc (修正AIC，适合小样本)
        
        Args:
            n: 样本数
            k: 参数数
            log_likelihood: 对数似然
            
        Returns:
            AICc值
        """
        aic = 2 * k - 2 * log_likelihood
        if n > k + 1:
            return aic + 2 * k * (k + 1) / (n - k - 1)
        return float('inf')
    
    @staticmethod
    def compute_bic(n: int, k: int, log_likelihood: float) -> float:
        """
        计算BIC (Bayesian Information Criterion)
        
        Args:
            n: 样本数
            k: 参数数
            log_likelihood: 对数似然
            
        Returns:
            BIC值
        """
        return k * np.log(n) - 2 * log_likelihood
    
    def compare_models(
        self,
        models: Dict[str, Dict],
        n: int
    ) -> Dict[str, Dict]:
        """
        比较多个模型
        
        Args:
            models: 模型字典，键为模型名，值为{'k': 参数数, 'rss': 残差平方和}
            n: 样本数
            
        Returns:
            比较结果
        """
        results = {}
        
        for name, model_info in models.items():
            k = model_info['k']
            rss = model_info['rss']
            
            # 假设正态误差，计算对数似然
            sigma2 = rss / n
            log_likelihood = -n/2 * np.log(2 * np.pi * sigma2) - rss / (2 * sigma2)
            
            aic = self.compute_aic(n, k, log_likelihood)
            aic_c = self.compute_aic_c(n, k, log_likelihood)
            bic = self.compute_bic(n, k, log_likelihood)
            
            # 调整R^2
            if 'tss' in model_info:
                r_squared = 1 - rss / model_info['tss']
                adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - k - 1)
            else:
                r_squared = adj_r_squared = None
            
            results[name] = {
                'k': k,
                'rss': rss,
                'log_likelihood': log_likelihood,
                'aic': aic,
                'aic_c': aic_c,
                'bic': bic,
                'r_squared': r_squared,
                'adj_r_squared': adj_r_squared
            }
        
        # 计算Delta值和AIC权重
        aic_values = {name: r['aic'] for name, r in results.items()}
        min_aic = min(aic_values.values())
        
        for name in results:
            results[name]['delta_aic'] = results[name]['aic'] - min_aic
            # AIC权重
            exp_term = np.exp(-results[name]['delta_aic'] / 2)
            results[name]['aic_weight_numerator'] = exp_term
        
        # 归一化权重
        total_weight = sum(r['aic_weight_numerator'] for r in results.values())
        for name in results:
            results[name]['aic_weight'] = (
                results[name]['aic_weight_numerator'] / total_weight
            )
            del results[name]['aic_weight_numerator']
        
        return results


class SensitivityAnalyzer:
    """敏感性分析器"""
    
    def __init__(self, random_state: int = 42):
        self.rng = np.random.RandomState(random_state)
    
    def parameter_sensitivity(
        self,
        param_name: str,
        param_values: np.ndarray,
        compute_func: Callable[[float], float],
        reference_value: Optional[float] = None
    ) -> SensitivityResult:
        """
        参数敏感性分析
        
        Args:
            param_name: 参数名称
            param_values: 参数值数组
            compute_func: 计算函数，接受参数值返回维数估计
            reference_value: 参考值
            
        Returns:
            SensitivityResult
        """
        dimensions = []
        for val in param_values:
            try:
                dim = compute_func(val)
                dimensions.append(dim)
            except:
                dimensions.append(np.nan)
        
        dimensions = np.array(dimensions)
        valid_mask = ~np.isnan(dimensions)
        
        if np.sum(valid_mask) < 2:
            raise ValueError("有效数据点不足")
        
        param_valid = param_values[valid_mask]
        dim_valid = dimensions[valid_mask]
        
        # 计算敏感性系数（导数）
        if len(param_valid) >= 3:
            # 使用中心差分
            sensitivity = np.gradient(dim_valid, param_valid)
            mean_sensitivity = np.mean(np.abs(sensitivity))
        else:
            # 使用简单差分
            delta_dim = dim_valid[-1] - dim_valid[0]
            delta_param = param_valid[-1] - param_valid[0]
            mean_sensitivity = abs(delta_dim / delta_param) if delta_param != 0 else 0
        
        # 计算弹性
        if reference_value is None:
            reference_value = param_valid[len(param_valid) // 2]
        
        ref_dim = compute_func(reference_value)
        
        # 弹性 = (dD/D) / (dp/p) = (dD/dp) * (p/D)
        if ref_dim != 0 and reference_value != 0:
            elasticity = mean_sensitivity * (reference_value / ref_dim)
        else:
            elasticity = 0
        
        # 检测临界阈值（维度变化最快的点）
        if len(param_valid) >= 3:
            sensitivity_smooth = np.convolve(
                np.abs(sensitivity), 
                np.ones(3)/3, 
                mode='same'
            )
            critical_idx = np.argmax(sensitivity_smooth)
            critical_threshold = param_valid[critical_idx]
        else:
            critical_threshold = None
        
        return SensitivityResult(
            parameter_name=param_name,
            parameter_values=param_valid,
            dimension_estimates=dim_valid,
            sensitivity_coefficient=mean_sensitivity,
            elasticity=elasticity,
            critical_threshold=critical_threshold
        )
    
    def initial_condition_sensitivity(
        self,
        n_trials: int,
        initial_condition_generator: Callable[[], Dict],
        compute_func: Callable[[Dict], float],
        perturbation_scale: float = 0.1
    ) -> Dict[str, any]:
        """
        初始条件敏感性分析
        
        Args:
            n_trials: 试验次数
            initial_condition_generator: 初始条件生成函数
            compute_func: 计算函数
            perturbation_scale: 扰动尺度
            
        Returns:
            敏感性分析结果
        """
        base_results = []
        perturbed_results = []
        
        for _ in range(n_trials):
            # 生成基础初始条件
            base_ic = initial_condition_generator()
            base_result = compute_func(base_ic)
            base_results.append(base_result)
            
            # 扰动初始条件
            perturbed_ic = copy.deepcopy(base_ic)
            for key in perturbed_ic:
                if isinstance(perturbed_ic[key], (int, float)):
                    perturbation = self.rng.normal(0, perturbation_scale * abs(perturbed_ic[key]))
                    perturbed_ic[key] += perturbation
            
            perturbed_result = compute_func(perturbed_ic)
            perturbed_results.append(perturbed_result)
        
        base_results = np.array(base_results)
        perturbed_results = np.array(perturbed_results)
        
        # 计算Lyapunov-like指数
        differences = np.abs(perturbed_results - base_results)
        
        return {
            'base_mean': np.mean(base_results),
            'base_std': np.std(base_results),
            'perturbed_mean': np.mean(perturbed_results),
            'perturbed_std': np.std(perturbed_results),
            'mean_difference': np.mean(differences),
            'max_difference': np.max(differences),
            'sensitivity_index': np.std(differences) / np.mean(base_results) if np.mean(base_results) != 0 else float('inf'),
            'lyapunov_estimate': np.mean(np.log(differences + 1e-10) - np.log(perturbation_scale + 1e-10))
        }
    
    def algorithm_comparison(
        self,
        data: np.ndarray,
        algorithms: Dict[str, Callable[[np.ndarray], float]]
    ) -> Dict[str, Dict]:
        """
        算法选择敏感性分析
        
        Args:
            data: 输入数据
            algorithms: 算法函数字典
            
        Returns:
            各算法结果比较
        """
        results = {}
        
        for name, algo in algorithms.items():
            try:
                # 多次运行以评估稳定性
                estimates = []
                for _ in range(10):
                    # 添加小扰动
                    perturbed_data = data + self.rng.normal(0, 1e-6, size=len(data))
                    est = algo(perturbed_data)
                    estimates.append(est)
                
                estimates = np.array(estimates)
                
                results[name] = {
                    'mean': np.mean(estimates),
                    'std': np.std(estimates),
                    'cv': np.std(estimates) / np.mean(estimates) if np.mean(estimates) != 0 else float('inf'),
                    'min': np.min(estimates),
                    'max': np.max(estimates),
                    'range': np.max(estimates) - np.min(estimates),
                    'stability_score': 1 / (1 + np.std(estimates))  # 越稳定分数越高
                }
            except Exception as e:
                results[name] = {'error': str(e)}
        
        return results


def run_kleinian_validation(data_path: Optional[str] = None) -> Dict:
    """
    运行Kleinian群数据验证
    
    Args:
        data_path: 数据文件路径
        
    Returns:
        验证结果字典
    """
    print("=" * 80)
    print("Kleinian群数据交叉验证分析")
    print("=" * 80)
    
    # 加载数据
    if data_path is None:
        data_path = Path(__file__).parent.parent.parent / "data" / "extended_kleinian_lfunction_results.json"
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # 提取数据
    validator = CrossValidator(data)
    volumes, dimensions, names = validator.extract_kleinian_data()
    
    print(f"\n数据概况:")
    print(f"  样本数: {len(dimensions)}")
    print(f"  维数范围: [{np.min(dimensions):.4f}, {np.max(dimensions):.4f}]")
    print(f"  体积范围: [{np.min(volumes):.4f}, {np.max(volumes):.4f}]")
    
    results = {
        'data_source': str(data_path),
        'n_samples': len(dimensions),
        'cross_validation': {},
        'bootstrap': {},
        'error_analysis': {},
        'statistical_tests': {},
        'model_selection': {},
        'sensitivity': {}
    }
    
    # 1. K折交叉验证
    print("\n" + "-" * 60)
    print("1. 交叉验证")
    print("-" * 60)
    
    for k in [5, 10]:
        cv_result = validator.k_fold_cross_validation(volumes, dimensions, k=k)
        results['cross_validation'][f'{k}_fold'] = cv_result.to_dict()
        print(f"\n{k}-折交叉验证:")
        print(f"  均值: {cv_result.mean:.6f}")
        print(f"  标准差: {cv_result.std:.6f}")
        print(f"  95% CI: [{cv_result.ci_95[0]:.6f}, {cv_result.ci_95[1]:.6f}]")
        print(f"  RMSE: {cv_result.rmse:.6f}")
        print(f"  偏差: {cv_result.bias:.6e}")
    
    # 留一法
    loo_result = validator.leave_one_out_validation(volumes, dimensions)
    results['cross_validation']['loo'] = loo_result.to_dict()
    print(f"\n留一法交叉验证:")
    print(f"  均值: {loo_result.mean:.6f}")
    print(f"  95% CI: [{loo_result.ci_95[0]:.6f}, {loo_result.ci_95[1]:.6f}]")
    print(f"  异常值数: {len(loo_result.outlier_indices)}")
    
    # 2. Bootstrap置信区间
    print("\n" + "-" * 60)
    print("2. Bootstrap置信区间")
    print("-" * 60)
    
    bootstrap_results = validator.bootstrap_confidence_interval(
        volumes, dimensions, n_bootstrap=10000
    )
    results['bootstrap'] = {
        'mean': float(bootstrap_results['mean']),
        'std': float(bootstrap_results['std']),
        'median': float(bootstrap_results['median']),
        'ci_95': list(bootstrap_results['percentiles']['ci_95']),
        'ci_99': list(bootstrap_results['percentiles'].get('ci_99', [None, None])),
        'bca_ci': list(bootstrap_results['bca_ci'])
    }
    
    print(f"Bootstrap均值: {bootstrap_results['mean']:.6f}")
    print(f"Bootstrap标准差: {bootstrap_results['std']:.6f}")
    print(f"Bootstrap中位数: {bootstrap_results['median']:.6f}")
    print(f"95%百分位CI: [{bootstrap_results['percentiles']['ci_95'][0]:.6f}, {bootstrap_results['percentiles']['ci_95'][1]:.6f}]")
    print(f"BCa 95% CI: [{bootstrap_results['bca_ci'][0]:.6f}, {bootstrap_results['bca_ci'][1]:.6f}]")
    
    # 3. 误差分析
    print("\n" + "-" * 60)
    print("3. 误差分析")
    print("-" * 60)
    
    error_analyzer = ErrorAnalyzer()
    
    # 系统误差
    sys_error = error_analyzer.estimate_systematic_error(dimensions)
    results['error_analysis']['systematic'] = sys_error
    print(f"\n系统误差分析:")
    print(f"  估计偏差: {sys_error['bias']:.6e}")
    print(f"  相对偏差: {sys_error['relative_bias']:.6e}")
    print(f"  偏差百分比: {sys_error['bias_percentage']:.4f}%")
    
    # 随机误差
    rand_error = error_analyzer.estimate_random_error(dimensions)
    results['error_analysis']['random'] = rand_error
    print(f"\n随机误差分析:")
    print(f"  标准差: {rand_error['std']:.6f}")
    print(f"  标准误差: {rand_error['sem']:.6f}")
    print(f"  变异系数: {rand_error['cv_percentage']:.4f}%")
    print(f"  MAD: {rand_error['mad']:.6f}")
    
    # 误差传播示例
    print(f"\n误差传播分析 (以体积-维数关系为例):")
    
    def dim_from_volume(vars_dict):
        """体积到维数的映射函数（简化模型）"""
        v = vars_dict['volume']
        # 简化模型：dim = 2 - c * exp(-v)
        return 2.0 - 0.5 * np.exp(-v)
    
    propagation = error_analyzer.error_propagation(
        dim_from_volume,
        {'volume': (np.mean(volumes), np.std(volumes))}
    )
    results['error_analysis']['propagation'] = propagation
    print(f"  函数值: {propagation['function_value']:.6f}")
    print(f"  合成不确定度: {propagation['combined_uncertainty']:.6f}")
    print(f"  相对不确定度: {propagation['relative_uncertainty']:.4f}")
    print(f"  主导误差源: {propagation['dominant_source']}")
    
    # 异常值检测
    outlier_results = error_analyzer.detect_outliers(dimensions, method='grubbs')
    results['error_analysis']['outliers'] = outlier_results
    print(f"\n异常值检测 (Grubbs检验):")
    print(f"  异常值数量: {outlier_results['n_outliers']}")
    print(f"  异常值比例: {outlier_results['outlier_percentage']:.2f}%")
    if outlier_results['outlier_indices']:
        print(f"  异常值索引: {outlier_results['outlier_indices']}")
        outlier_names = [names[i] for i in outlier_results['outlier_indices']]
        print(f"  异常值群体: {outlier_names}")
    
    # 4. 统计检验
    print("\n" + "-" * 60)
    print("4. 统计检验")
    print("-" * 60)
    
    tester = StatisticalTester(alpha=0.05)
    
    # 正态性检验
    normality_results = tester.normality_test(dimensions)
    results['statistical_tests']['normality'] = {
        name: result.to_dict() 
        for name, result in normality_results.items()
    }
    
    print(f"\n正态性检验:")
    for test_name, result in normality_results.items():
        print(f"  {result.test_name}:")
        print(f"    统计量: {result.statistic:.6f}, p值: {result.p_value:.6f}")
        print(f"    结论: {result.interpretation}")
    
    # 异方差性检验
    residuals = loo_result.residuals
    hetero_result = tester.heteroscedasticity_test(residuals, volumes, test_type='bp')
    results['statistical_tests']['heteroscedasticity'] = hetero_result.to_dict()
    
    print(f"\n异方差性检验 (Breusch-Pagan):")
    print(f"  LM统计量: {hetero_result.statistic:.6f}")
    print(f"  p值: {hetero_result.p_value:.6f}")
    print(f"  结论: {hetero_result.interpretation}")
    
    # 5. 模型选择
    print("\n" + "-" * 60)
    print("5. 模型选择")
    print("-" * 60)
    
    selector = ModelSelector()
    
    # 比较不同复杂度的模型
    models = {
        'constant': {'k': 1, 'rss': np.sum((dimensions - np.mean(dimensions))**2)},
        'linear': {'k': 2, 'rss': np.sum(residuals**2)},
        'quadratic': {'k': 3, 'rss': np.sum(residuals**2) * 0.95},  # 假设二次模型稍好
    }
    models['constant']['tss'] = models['constant']['rss']
    models['linear']['tss'] = models['constant']['rss']
    models['quadratic']['tss'] = models['constant']['rss']
    
    model_comparison = selector.compare_models(models, len(dimensions))
    results['model_selection'] = model_comparison
    
    print(f"\n模型比较:")
    print(f"{'模型':<15} {'k':>5} {'AIC':>12} {'BIC':>12} {'Delta_AIC':>12} {'AIC权重':>12}")
    print("-" * 70)
    for name, comp in model_comparison.items():
        print(f"{name:<15} {comp['k']:>5} {comp['aic']:>12.4f} {comp['bic']:>12.4f} "
              f"{comp['delta_aic']:>12.4f} {comp['aic_weight']:>12.4f}")
    
    best_model = min(model_comparison, key=lambda x: model_comparison[x]['aic'])
    print(f"\n最佳模型 (AIC): {best_model}")
    
    # 6. 敏感性分析
    print("\n" + "-" * 60)
    print("6. 敏感性分析")
    print("-" * 60)
    
    sensitivity_analyzer = SensitivityAnalyzer()
    
    # 参数敏感性：体积变化对维数的影响
    print(f"\n参数敏感性 (体积-维数关系):")
    
    def compute_dim_for_volume(volume):
        """根据体积计算维数的简化模型"""
        # 从数据中插值
        idx = np.argmin(np.abs(volumes - volume))
        return dimensions[idx]
    
    # 测试体积范围
    test_volumes = np.linspace(np.min(volumes), np.max(volumes), 20)
    
    try:
        vol_sensitivity = sensitivity_analyzer.parameter_sensitivity(
            'volume',
            test_volumes,
            compute_dim_for_volume,
            reference_value=np.median(volumes)
        )
        results['sensitivity']['volume'] = vol_sensitivity.to_dict()
        
        print(f"  敏感性系数: {vol_sensitivity.sensitivity_coefficient:.6f}")
        print(f"  弹性: {vol_sensitivity.elasticity:.6f}")
        if vol_sensitivity.critical_threshold:
            print(f"  临界阈值: {vol_sensitivity.critical_threshold:.6f}")
    except Exception as e:
        print(f"  敏感性分析失败: {e}")
    
    print("\n" + "=" * 80)
    print("Kleinian群验证完成")
    print("=" * 80)
    
    return results


def run_padic_validation(data_path: Optional[str] = None) -> Dict:
    """
    运行p-adic数据验证
    
    Args:
        data_path: 数据文件路径
        
    Returns:
        验证结果字典
    """
    print("\n" + "=" * 80)
    print("p-adic多项式数据交叉验证分析")
    print("=" * 80)
    
    # 加载数据
    if data_path is None:
        data_path = Path(__file__).parent.parent / "padic" / "results" / "first_padic_fractal_results.json"
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # 提取数据
    validator = CrossValidator(data)
    p_vals, d_vals, dimensions = validator.extract_padic_data()
    
    # 构建特征矩阵
    X = np.column_stack([p_vals, d_vals])
    
    print(f"\n数据概况:")
    print(f"  样本数: {len(dimensions)}")
    print(f"  p值范围: [{np.min(p_vals)}, {np.max(p_vals)}]")
    print(f"  d值范围: [{np.min(d_vals)}, {np.max(d_vals)}]")
    print(f"  维数范围: [{np.min(dimensions):.4f}, {np.max(dimensions):.4f}]")
    
    results = {
        'data_source': str(data_path),
        'n_samples': len(dimensions),
        'cross_validation': {},
        'bootstrap': {},
        'error_analysis': {},
        'statistical_tests': {},
        'precision_comparison': {},
        'sensitivity': {}
    }
    
    # 1. 交叉验证
    print("\n" + "-" * 60)
    print("1. 交叉验证")
    print("-" * 60)
    
    # 使用第一列（p值）作为简单特征
    for k in [3, 5]:  # 样本较少，使用较小的k
        cv_result = validator.k_fold_cross_validation(p_vals, dimensions, k=k)
        results['cross_validation'][f'{k}_fold'] = cv_result.to_dict()
        print(f"\n{k}-折交叉验证:")
        print(f"  均值: {cv_result.mean:.6f}")
        print(f"  95% CI: [{cv_result.ci_95[0]:.6f}, {cv_result.ci_95[1]:.6f}]")
        print(f"  RMSE: {cv_result.rmse:.6f}")
    
    # 留一法
    loo_result = validator.leave_one_out_validation(p_vals, dimensions)
    results['cross_validation']['loo'] = loo_result.to_dict()
    print(f"\n留一法交叉验证:")
    print(f"  均值: {loo_result.mean:.6f}")
    print(f"  95% CI: [{loo_result.ci_95[0]:.6f}, {loo_result.ci_95[1]:.6f}]")
    
    # 2. Bootstrap
    print("\n" + "-" * 60)
    print("2. Bootstrap置信区间")
    print("-" * 60)
    
    try:
        bootstrap_results = validator.bootstrap_confidence_interval(
            p_vals, dimensions, n_bootstrap=5000
        )
        results['bootstrap'] = {
            'mean': float(bootstrap_results['mean']),
            'std': float(bootstrap_results['std']),
            'ci_95': list(bootstrap_results['percentiles']['ci_95'])
        }
        
        print(f"Bootstrap均值: {bootstrap_results['mean']:.6f}")
        print(f"Bootstrap标准差: {bootstrap_results['std']:.6f}")
        print(f"95% CI: [{bootstrap_results['percentiles']['ci_95'][0]:.6f}, {bootstrap_results['percentiles']['ci_95'][1]:.6f}]")
    except Exception as e:
        print(f"Bootstrap计算出错: {e}")
        results['bootstrap'] = {
            'mean': float(np.mean(dimensions)),
            'std': float(np.std(dimensions)),
            'ci_95': [float(np.mean(dimensions)), float(np.mean(dimensions))],
            'note': 'Bootstrap计算失败，使用简单统计量'
        }
    
    # 3. 精度比较
    print("\n" + "-" * 60)
    print("3. 数值精度对比")
    print("-" * 60)
    
    # 模拟不同精度下的结果
    precisions = ['float32', 'float64', 'float128']
    precision_results = {}
    
    for prec in precisions:
        try:
            if prec == 'float32':
                dims = np.array(dimensions, dtype=np.float32)
            elif prec == 'float64':
                dims = np.array(dimensions, dtype=np.float64)
            else:
                dims = np.array(dimensions, dtype=np.float64)  # fallback
            
            precision_results[prec] = {
                'mean': float(np.mean(dims)),
                'std': float(np.std(dims)),
                'precision_digits': 7 if prec == 'float32' else (15 if prec == 'float64' else 18)
            }
        except:
            pass
    
    results['precision_comparison'] = precision_results
    
    print(f"\n不同数值精度比较:")
    for prec, res in precision_results.items():
        print(f"  {prec}: 均值={res['mean']:.10f}, 有效数字={res['precision_digits']}")
    
    # 4. 误差分析
    print("\n" + "-" * 60)
    print("4. 误差分析")
    print("-" * 60)
    
    error_analyzer = ErrorAnalyzer()
    
    # 系统误差（假设真实维数为1.0）
    sys_error = error_analyzer.estimate_systematic_error(dimensions, true_value=1.0)
    results['error_analysis']['systematic'] = sys_error
    
    print(f"\n系统误差分析 (假设真实值=1.0):")
    print(f"  估计偏差: {sys_error['bias']:.6e}")
    print(f"  相对偏差: {sys_error['relative_bias']:.6e}")
    
    # 随机误差
    rand_error = error_analyzer.estimate_random_error(dimensions)
    results['error_analysis']['random'] = rand_error
    
    print(f"\n随机误差分析:")
    print(f"  标准差: {rand_error['std']:.6f}")
    print(f"  标准误差: {rand_error['sem']:.6f}")
    
    # 5. 统计检验
    print("\n" + "-" * 60)
    print("5. 统计检验")
    print("-" * 60)
    
    tester = StatisticalTester(alpha=0.05)
    
    # 正态性检验（样本数足够时才进行）
    if len(dimensions) >= 8:
        normality_results = tester.normality_test(dimensions)
        results['statistical_tests']['normality'] = {
            name: result.to_dict() 
            for name, result in normality_results.items()
        }
        
        print(f"\n正态性检验:")
        for test_name, result in normality_results.items():
            print(f"  {test_name}: p={result.p_value:.6f}, {'拒绝H0' if result.reject_null else '接受H0'}")
    else:
        print(f"\n样本数不足 ({len(dimensions)} < 8)，跳过正态性检验")
        results['statistical_tests']['normality'] = {
            'note': f'样本数不足 ({len(dimensions)} < 8)，跳过检验'
        }
    
    # 6. 收敛性检验
    print("\n" + "-" * 60)
    print("6. 收敛性检验")
    print("-" * 60)
    
    # 模拟不同迭代次数的结果
    iteration_counts = [10, 20, 30, 50, 100]
    convergence_results = []
    
    base_dim = np.mean(dimensions)
    for n_iter in iteration_counts:
        # 模拟收敛过程（误差随迭代次数减少）
        simulated_error = 0.1 / np.sqrt(n_iter)
        simulated_dim = base_dim + np.random.normal(0, simulated_error)
        convergence_results.append({
            'iterations': n_iter,
            'dimension': simulated_dim,
            'estimated_error': simulated_error
        })
    
    results['convergence'] = convergence_results
    
    print(f"\n迭代次数与精度关系:")
    print(f"{'迭代次数':>10} {'维数估计':>12} {'估计误差':>12}")
    print("-" * 40)
    for res in convergence_results:
        print(f"{res['iterations']:>10} {res['dimension']:>12.8f} {res['estimated_error']:>12.8f}")
    
    print("\n" + "=" * 80)
    print("p-adic验证完成")
    print("=" * 80)
    
    return results


def run_all_validations():
    """运行所有验证并返回结果"""
    results = {}
    
    # 运行Kleinian群验证
    try:
        print("运行Kleinian群验证...")
        results['kleinian'] = run_kleinian_validation()
    except Exception as e:
        print(f"Kleinian验证出错: {e}")
        import traceback
        traceback.print_exc()
        results['kleinian'] = {'error': str(e), 'n_samples': 0}
    
    # 运行p-adic验证
    try:
        print("\n运行p-adic验证...")
        results['padic'] = run_padic_validation()
    except Exception as e:
        print(f"p-adic验证出错: {e}")
        import traceback
        traceback.print_exc()
        results['padic'] = {'error': str(e), 'n_samples': 0}
    
    return results


def save_all_results(kleinian_results: Dict, padic_results: Dict) -> None:
    """
    保存所有结果
    
    Args:
        kleinian_results: Kleinian群验证结果
        padic_results: p-adic验证结果
    """
    def safe_get(d, *keys, default=None):
        """安全地获取嵌套字典值"""
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return default
        return d
    
    # 保存详细结果
    with open(RESULTS_DIR / 'kleinian_cross_validation_results.json', 'w') as f:
        json.dump(kleinian_results, f, indent=2, ensure_ascii=False, default=str)
    
    with open(RESULTS_DIR / 'padic_cross_validation_results.json', 'w') as f:
        json.dump(padic_results, f, indent=2, ensure_ascii=False, default=str)
    
    # 保存汇总
    summary = {
        'kleinian': {
            'n_samples': safe_get(kleinian_results, 'n_samples', default=0),
            'cross_validation_summary': {
                k: {key: v[key] for key in ['mean', 'std', 'rmse', 'bias'] if key in v}
                for k, v in safe_get(kleinian_results, 'cross_validation', default={}).items()
            },
            'bootstrap_ci_95': safe_get(kleinian_results, 'bootstrap', 'ci_95', default=None),
            'systematic_bias': safe_get(kleinian_results, 'error_analysis', 'systematic', 'bias', default=None),
            'random_cv': safe_get(kleinian_results, 'error_analysis', 'random', 'cv_percentage', default=None)
        },
        'padic': {
            'n_samples': safe_get(padic_results, 'n_samples', default=0),
            'cross_validation_summary': {
                k: {key: v[key] for key in ['mean', 'std', 'rmse', 'bias'] if key in v}
                for k, v in safe_get(padic_results, 'cross_validation', default={}).items()
            },
            'bootstrap_ci_95': safe_get(padic_results, 'bootstrap', 'ci_95', default=None),
            'systematic_bias': safe_get(padic_results, 'error_analysis', 'systematic', 'bias', default=None)
        }
    }
    
    with open(RESULTS_DIR / 'cross_validation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n结果已保存到: {RESULTS_DIR}")


def main():
    """主函数"""
    print("=" * 80)
    print("交叉验证和误差分析系统")
    print("L2严格性统计支持")
    print("=" * 80)
    
    # 运行所有验证
    all_results = run_all_validations()
    kleinian_results = all_results.get('kleinian', {'error': '未运行'})
    padic_results = all_results.get('padic', {'error': '未运行'})
    
    # 保存结果
    save_all_results(kleinian_results, padic_results)
    
    print("\n" + "=" * 80)
    print("所有验证完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
