"""
重新设计的c1提取器
Revamped C1 Extractor

配合新的分形生成器
关键改进:
1. 针对新的谱维度公式优化
2. 使用正确的拟合函数
3. 更好的错误处理
"""

import numpy as np
from typing import Dict, Tuple
from scipy.optimize import curve_fit


class RevampedExtractor:
    """
    重新设计的c1提取器
    
    针对新的安全谱维度公式:
    d_s(ℓ) = d_min + (d_max - d_min) / (1 + (ℓ_0/ℓ)^(1/c1))
    """
    
    def __init__(self, dimension: int):
        self.d = dimension
        self.d_min = 2.0
        self.d_max = float(dimension)
        self.c1_theory = 1.0 / dimension
    
    def extract_c1(self, points: np.ndarray, ell_0: float = 1.0) -> Dict:
        """
        提取c1
        
        步骤:
        1. 构建图拉普拉斯
        2. 计算谱维度
        3. 拟合提取c1和d_max
        """
        try:
            from fractal_laplacian import FractalLaplacian
            
            # 构建拉普拉斯
            fl = FractalLaplacian(dimension=self.d)
            L = fl.construct_graph_laplacian(points, epsilon=None)
            
            # 计算谱维度
            # 使用较宽的t范围
            t_range = np.logspace(-2, 2, 60)
            t_vals, d_s = fl.compute_spectral_dimension(
                L, 
                t_range=t_range,
                n_eigenvalues=min(50, len(points)//4)
            )
            
            # 转换为长度尺度
            ell_vals = np.sqrt(t_vals)
            
            # 过滤有效值
            valid = (ell_vals > 0) & (d_s > 0.5) & (d_s < self.d + 1) & \
                    (~np.isnan(ell_vals)) & (~np.isnan(d_s))
            
            if np.sum(valid) < 10:
                return {
                    'error': f'Insufficient valid points: {np.sum(valid)}',
                    'd_s_range': (float(d_s.min()), float(d_s.max()))
                }
            
            ell = ell_vals[valid]
            d_s_valid = d_s[valid]
            
            # 方法1: 非线性拟合完整公式
            result_fit = self._fit_full_formula(ell, d_s_valid, ell_0)
            
            # 方法2: 线性化拟合
            result_linear = self._fit_linearized(ell, d_s_valid, ell_0)
            
            # 选择更好的结果
            if result_fit.get('quality', 0) > result_linear.get('quality', 0):
                result = result_fit
                result['method_used'] = 'nonlinear'
            else:
                result = result_linear
                result['method_used'] = 'linearized'
            
            # 添加额外信息
            result['d_s_range'] = (float(d_s.min()), float(d_s.max()))
            result['ell_range'] = (float(ell.min()), float(ell.max()))
            result['n_points_used'] = int(np.sum(valid))
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def _fit_full_formula(self, ell: np.ndarray, d_s: np.ndarray, 
                          ell_0: float) -> Dict:
        """
        非线性拟合完整公式
        
        d_s = d_min + (d_max - d_min) / (1 + (ell_0/ell)^(1/c1))
        
        拟合参数: d_max, c1
        """
        def model(ell, d_max, c1):
            if c1 <= 0:
                return np.full_like(ell, np.nan)
            ratio = ell_0 / ell
            exponent = 1.0 / c1
            transition = 1.0 / (1.0 + ratio ** exponent)
            return self.d_min + (d_max - self.d_min) * transition
        
        # 初始猜测
        p0 = [self.d_max, self.c1_theory]
        
        try:
            # 边界约束
            bounds = ([self.d_min, 0.01], [self.d_max + 2, 2.0])
            
            popt, pcov = curve_fit(model, ell, d_s, p0=p0, bounds=bounds, maxfev=5000)
            
            d_max_fit, c1_fit = popt
            
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
                'c1_theory': self.c1_theory,
                'd_max': float(d_max_fit),
                'd_max_error': float(perr[0]),
                'd_max_theory': self.d_max,
                'quality': float(r_squared),
                'bias': float(c1_fit - self.c1_theory),
                'bias_percent': float(abs(c1_fit - self.c1_theory) / self.c1_theory * 100),
            }
            
        except Exception as e:
            return {'error': f'Nonlinear fit failed: {e}'}
    
    def _fit_linearized(self, ell: np.ndarray, d_s: np.ndarray, 
                        ell_0: float) -> Dict:
        """
        线性化拟合
        
        从公式:
        d_s = d_min + (d_max - d_min) / (1 + (ell_0/ell)^(1/c1))
        
        变形:
        (d_max - d_min) / (d_s - d_min) = 1 + (ell_0/ell)^(1/c1)
        (d_max - d_min) / (d_s - d_min) - 1 = (ell_0/ell)^(1/c1)
        
        取对数:
        ln[(d_max - d_min)/(d_s - d_min) - 1] = (1/c1) * ln(ell_0/ell)
        
        这关于 1/c1 是线性的！
        """
        try:
            # 需要d_max的估计
            # 使用d_s的最大值作为初始估计
            d_max_init = min(np.max(d_s) * 1.1, self.d_max + 1)
            
            # 迭代优化
            best_result = None
            best_quality = -1
            
            for d_max_try in np.linspace(max(np.max(d_s), self.d_min + 0.5), 
                                          self.d_max + 1, 10):
                y = (d_max_try - self.d_min) / (d_s - self.d_min) - 1
                
                # 过滤正值
                valid_y = y > 0
                if np.sum(valid_y) < 5:
                    continue
                
                ell_valid = ell[valid_y]
                y_valid = y[valid_y]
                
                # 计算对数
                log_y = np.log(y_valid)
                log_ratio = np.log(ell_0 / ell_valid)
                
                # 线性拟合: log_y = (1/c1) * log_ratio
                # 即: y = slope * x, 其中 slope = 1/c1
                
                slope = np.sum(log_y * log_ratio) / np.sum(log_ratio ** 2)
                
                if slope > 0:
                    c1_fit = 1.0 / slope
                    
                    # 计算预测值
                    y_pred = slope * log_ratio
                    ss_res = np.sum((log_y - y_pred)**2)
                    ss_tot = np.sum((log_y - np.mean(log_y))**2)
                    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
                    
                    if r_squared > best_quality:
                        best_quality = r_squared
                        best_result = {
                            'c1': float(c1_fit),
                            'c1_theory': self.c1_theory,
                            'd_max': float(d_max_try),
                            'd_max_theory': self.d_max,
                            'quality': float(r_squared),
                            'bias': float(c1_fit - self.c1_theory),
                            'bias_percent': float(abs(c1_fit - self.c1_theory) / self.c1_theory * 100),
                        }
            
            return best_result if best_result else {'error': 'Linearized fit failed'}
            
        except Exception as e:
            return {'error': f'Linearized fit failed: {e}'}


def test_revamped_extraction():
    """测试重新设计的提取器"""
    print("=" * 70)
    print("重新设计的c1提取器 - 测试")
    print("=" * 70)
    
    from revamped_fractal_generator import RevampedFractalGenerator
    
    for dim in [3, 4, 5]:
        print(f"\n{'='*70}")
        print(f"{dim}维空间 (理论c1 = 1/{dim} = {1.0/dim:.4f})")
        print(f"{'='*70}")
        
        gen = RevampedFractalGenerator(dimension=dim)
        extractor = RevampedExtractor(dimension=dim)
        
        c1_values = []
        
        for i in range(5):
            np.random.seed(i * 10 + dim)
            
            # 生成两种类型的分形
            if i % 2 == 0:
                points, _, _ = gen.generate_shell_based_fractal(n_points=400)
            else:
                points, _ = gen.generate_explicit_transition(n_points=400)
            
            # 提取c1
            result = extractor.extract_c1(points)
            
            if 'c1' in result:
                c1_values.append(result['c1'])
                bias = result.get('bias_percent', 0)
                method = result.get('method_used', '?')
                d_max = result.get('d_max', 0)
                quality = result.get('quality', 0)
                
                status = '✓' if bias < 20 else ('~' if bias < 50 else '✗')
                print(f"  样本{i+1}: c1={result['c1']:.4f}, d_max={d_max:.2f}, "
                      f"R²={quality:.3f}, 偏差={bias:.1f}% [{method}] {status}")
            else:
                print(f"  样本{i+1}: 失败 - {result.get('error', 'Unknown')[:40]}")
        
        if c1_values:
            c1_values = np.array(c1_values)
            mean_c1 = np.mean(c1_values)
            theory = 1.0 / dim
            bias_pct = abs(mean_c1 - theory) / theory * 100
            
            print(f"\n  统计:")
            print(f"    理论c1: {theory:.4f}")
            print(f"    提取均值: {mean_c1:.4f} ± {np.std(c1_values):.4f}")
            print(f"    偏差: {bias_pct:.1f}%")
            
            if bias_pct < 20:
                print(f"    ✅ 达到目标 (<20%)")
            elif bias_pct < 50:
                print(f"    🟡 接近目标")
            else:
                print(f"    ⚠️ 需要进一步改进")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_revamped_extraction()
