"""
稳健的c1提取器
Robust C1 Extractor

改进的c1提取算法:
1. 加权最小二乘拟合
2. 多方法平均
3. 自动参数优化
4. 异常值检测和过滤
"""

import numpy as np
from scipy.optimize import curve_fit, minimize
from typing import Tuple, Dict, List
from fractal_laplacian import FractalLaplacian


class RobustC1Extractor:
    """
    稳健的c1提取器
    
    使用多种策略提高c1提取精度
    """
    
    def __init__(self, true_c1: float = 0.25):
        self.true_c1 = true_c1
        
    def extract_weighted_fit(self, ell_values: np.ndarray, 
                             d_s_values: np.ndarray,
                             weights: np.ndarray = None) -> Dict:
        """
        使用加权最小二乘拟合提取c1
        
        公式: d_s = d_max - c1 / ln(ell/ell_0)
        
        Args:
            ell_values: 长度尺度数组
            d_s_values: 谱维度数组
            weights: 权重数组 (如果为None, 自动计算)
            
        Returns:
            提取结果
        """
        # 过滤无效值
        valid_mask = (ell_values > 0) & (d_s_values > 1) & (d_s_values < 5) & \
                     (~np.isnan(ell_values)) & (~np.isnan(d_s_values))
        
        ell = ell_values[valid_mask]
        d_s = d_s_values[valid_mask]
        
        if len(ell) < 10:
            return {'error': 'Insufficient valid data points'}
        
        # 计算 ln(ell)
        log_ell = np.log(ell)
        
        # 自动计算权重
        if weights is None:
            # 过渡区域赋予更高权重
            # d_s 在 2.5 到 3.5 之间的点对c1提取最重要
            weights = np.ones_like(d_s)
            transition_mask = (d_s > 2.2) & (d_s < 3.8)
            weights[transition_mask] *= 3.0
            
            # 远离ln(ell)=0的点更可靠
            weights *= np.abs(log_ell) / (1 + np.abs(log_ell))
        else:
            weights = weights[valid_mask]
        
        # 拟合函数: d_s = d_max - c1 / log_ell
        # 转换: x = 1/log_ell, y = d_s
        # 线性拟合: y = d_max - c1 * x
        
        # 只使用 |log_ell| > 0.05 的点 (避免奇点)
        mask = np.abs(log_ell) > 0.05
        if np.sum(mask) < 10:
            mask = np.abs(log_ell) > 0.01
        
        x = 1.0 / log_ell[mask]
        y = d_s[mask]
        w = weights[mask]
        
        # 加权线性回归
        # y = a * x + b, 其中 a = -c1, b = d_max
        W = np.diag(w)
        X = np.vstack([x, np.ones(len(x))]).T
        
        try:
            # 加权最小二乘: (X^T W X)^{-1} X^T W y
            XtWX = X.T @ W @ X
            XtWy = X.T @ W @ y
            params = np.linalg.solve(XtWX, XtWy)
            
            c1_fit = -params[0]
            d_max_fit = params[1]
            
            # 计算R^2
            y_pred = d_max_fit - c1_fit * x
            ss_res = np.sum(w * (y - y_pred)**2)
            ss_tot = np.sum(w * (y - np.mean(y))**2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            # 计算参数误差
            residuals = y - y_pred
            mse = np.sum(w * residuals**2) / np.sum(w)
            
            # 参数协方差矩阵
            try:
                cov = mse * np.linalg.inv(XtWX)
                c1_err = np.sqrt(cov[0, 0])
                d_max_err = np.sqrt(cov[1, 1])
            except:
                c1_err = np.nan
                d_max_err = np.nan
            
            return {
                'c1': float(c1_fit),
                'c1_error': float(c1_err),
                'd_max': float(d_max_fit),
                'd_max_error': float(d_max_err),
                'quality': float(r_squared),
                'n_points': int(np.sum(mask)),
                'method': 'weighted_linear'
            }
            
        except Exception as e:
            return {'error': f'Fitting failed: {e}'}
    
    def extract_nonlinear_fit(self, ell_values: np.ndarray,
                              d_s_values: np.ndarray) -> Dict:
        """
        使用非线性拟合提取c1
        
        直接拟合: d_s = d_max - c1 / ln(ell/ell_0)
        
        Args:
            ell_values: 长度尺度
            d_s_values: 谱维度
            
        Returns:
            提取结果
        """
        valid_mask = (ell_values > 0) & (d_s_values > 1) & (d_s_values < 5) & \
                     (~np.isnan(ell_values)) & (~np.isnan(d_s_values))
        
        ell = ell_values[valid_mask]
        d_s = d_s_values[valid_mask]
        
        if len(ell) < 10:
            return {'error': 'Insufficient data'}
        
        # 定义拟合函数
        def model(ell, d_max, c1, ell_0):
            log_ratio = np.log(ell / ell_0)
            # 避免奇点
            log_ratio = np.where(np.abs(log_ratio) < 0.01, 0.01, log_ratio)
            return d_max - c1 / log_ratio
        
        # 初始猜测
        p0 = [4.0, 0.25, 1.0]
        
        try:
            popt, pcov = curve_fit(model, ell, d_s, p0=p0, 
                                   bounds=([2, 0.01, 0.1], [5, 2.0, 10.0]),
                                   maxfev=5000)
            
            d_max_fit, c1_fit, ell_0_fit = popt
            
            # 计算R^2
            y_pred = model(ell, *popt)
            ss_res = np.sum((d_s - y_pred)**2)
            ss_tot = np.sum((d_s - np.mean(d_s))**2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            # 参数误差
            perr = np.sqrt(np.diag(pcov))
            
            return {
                'c1': float(c1_fit),
                'c1_error': float(perr[1]),
                'd_max': float(d_max_fit),
                'd_max_error': float(perr[0]),
                'ell_0': float(ell_0_fit),
                'ell_0_error': float(perr[2]),
                'quality': float(r_squared),
                'method': 'nonlinear'
            }
            
        except Exception as e:
            return {'error': f'Nonlinear fit failed: {e}'}
    
    def extract_region_based(self, ell_values: np.ndarray,
                            d_s_values: np.ndarray) -> Dict:
        """
        基于区域的提取方法
        
        在不同区域分别拟合，然后平均
        
        Args:
            ell_values: 长度尺度
            d_s_values: 谱维度
            
        Returns:
            提取结果
        """
        valid_mask = (ell_values > 0) & (d_s_values > 1) & (d_s_values < 5)
        ell = ell_values[valid_mask]
        d_s = d_s_values[valid_mask]
        
        if len(ell) < 15:
            return {'error': 'Insufficient data'}
        
        # 分成三个区域
        # 区域1: 大尺度 (高维度)
        # 区域2: 过渡区 (关键区域)
        # 区域3: 小尺度 (低维度)
        
        regions = [
            (d_s > 3.2, "high_dim"),
            ((d_s > 2.3) & (d_s <= 3.2), "transition"),
            (d_s <= 2.3, "low_dim")
        ]
        
        c1_estimates = []
        qualities = []
        
        for mask, name in regions:
            if np.sum(mask) < 5:
                continue
            
            ell_reg = ell[mask]
            d_s_reg = d_s[mask]
            
            # 线性拟合
            log_ell = np.log(ell_reg)
            valid = np.abs(log_ell) > 0.01
            
            if np.sum(valid) < 5:
                continue
            
            x = 1.0 / log_ell[valid]
            y = d_s_reg[valid]
            
            A = np.vstack([x, np.ones(len(x))]).T
            try:
                c1_reg, d_max_reg = np.linalg.lstsq(A, y, rcond=None)[0]
                c1_reg = -c1_reg
                
                # 计算R^2
                y_pred = d_max_reg - c1_reg * x
                ss_res = np.sum((y - y_pred)**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
                
                if 0 < c1_reg < 2:  # 合理的c1范围
                    weight = 1.0 if name == "transition" else 0.5
                    c1_estimates.append((c1_reg, weight))
                    qualities.append(r2)
            except:
                continue
        
        if not c1_estimates:
            return {'error': 'No valid regional estimates'}
        
        # 加权平均
        total_weight = sum(w for _, w in c1_estimates)
        c1_weighted = sum(c * w for c, w in c1_estimates) / total_weight
        
        return {
            'c1': float(c1_weighted),
            'n_regions': len(c1_estimates),
            'mean_quality': float(np.mean(qualities)) if qualities else 0,
            'method': 'region_based'
        }
    
    def extract_robust(self, ell_values: np.ndarray,
                      d_s_values: np.ndarray,
                      combine_methods: bool = True) -> Dict:
        """
        稳健的c1提取 - 综合多种方法
        
        Args:
            ell_values: 长度尺度
            d_s_values: 谱维度
            combine_methods: 是否综合多种方法
            
        Returns:
            最佳提取结果
        """
        results = []
        
        # 方法1: 加权拟合
        r1 = self.extract_weighted_fit(ell_values, d_s_values)
        if 'error' not in r1:
            results.append(('weighted', r1))
        
        # 方法2: 非线性拟合
        r2 = self.extract_nonlinear_fit(ell_values, d_s_values)
        if 'error' not in r2:
            results.append(('nonlinear', r2))
        
        # 方法3: 区域方法
        r3 = self.extract_region_based(ell_values, d_s_values)
        if 'error' not in r3:
            results.append(('region', r3))
        
        if not results:
            return {'error': 'All methods failed'}
        
        if not combine_methods:
            # 返回最佳单个结果
            best = max(results, key=lambda x: x[1].get('quality', 0))
            return best[1]
        
        # 综合所有方法的结果
        valid_c1 = []
        weights = []
        
        for method_name, result in results:
            c1 = result.get('c1', np.nan)
            quality = result.get('quality', 0)
            
            if not np.isnan(c1) and 0 < c1 < 2:
                valid_c1.append(c1)
                weights.append(quality)
        
        if not valid_c1:
            return {'error': 'No valid c1 estimates'}
        
        # 加权平均
        weights = np.array(weights)
        weights = weights / np.sum(weights)
        c1_combined = np.average(valid_c1, weights=weights)
        
        # 计算离散度 (作为误差估计)
        c1_std = np.std(valid_c1)
        
        return {
            'c1': float(c1_combined),
            'c1_std': float(c1_std),
            'c1_range': (float(np.min(valid_c1)), float(np.max(valid_c1))),
            'n_methods': len(valid_c1),
            'individual_results': {name: r for name, r in results},
            'method': 'combined'
        }


def test_robust_extractor():
    """测试稳健提取器"""
    print("=" * 70)
    print("稳健c1提取器 - 测试")
    print("=" * 70)
    
    # 创建测试数据
    np.random.seed(42)
    
    # 理论的谱维度流
    ell = np.logspace(-2, 2, 100)
    c1_true = 0.25
    d_max = 4.0
    ell_0 = 1.0
    
    log_ratio = np.log(ell / ell_0)
    log_ratio = np.where(np.abs(log_ratio) < 0.01, 0.01, log_ratio)
    d_s_theory = d_max - c1_true / log_ratio
    
    # 添加噪声
    noise = np.random.randn(len(d_s_theory)) * 0.1
    d_s_noisy = d_s_theory + noise
    
    print(f"\n测试数据:")
    print(f"  理论 c1: {c1_true}")
    print(f"  数据点: {len(ell)}")
    print(f"  噪声水平: 0.1")
    
    # 测试提取器
    extractor = RobustC1Extractor()
    
    print(f"\n提取结果:")
    
    # 加权拟合
    r1 = extractor.extract_weighted_fit(ell, d_s_noisy)
    if 'c1' in r1:
        print(f"  加权拟合: c1 = {r1['c1']:.4f} ± {r1.get('c1_error', 0):.4f}, "
              f"R^2 = {r1['quality']:.4f}")
    
    # 非线性拟合
    r2 = extractor.extract_nonlinear_fit(ell, d_s_noisy)
    if 'c1' in r2:
        print(f"  非线性拟合: c1 = {r2['c1']:.4f} ± {r2.get('c1_error', 0):.4f}, "
              f"R^2 = {r2['quality']:.4f}")
    
    # 区域方法
    r3 = extractor.extract_region_based(ell, d_s_noisy)
    if 'c1' in r3:
        print(f"  区域方法: c1 = {r3['c1']:.4f}")
    
    # 综合方法
    r_combined = extractor.extract_robust(ell, d_s_noisy, combine_methods=True)
    if 'c1' in r_combined:
        print(f"\n  综合结果: c1 = {r_combined['c1']:.4f} ± {r_combined.get('c1_std', 0):.4f}")
        print(f"  方法数: {r_combined['n_methods']}")
        print(f"  范围: [{r_combined['c1_range'][0]:.4f}, {r_combined['c1_range'][1]:.4f}]")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_robust_extractor()
