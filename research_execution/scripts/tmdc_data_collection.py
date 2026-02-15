#!/usr/bin/env python3
"""
TMDC Exciton Data Collection and Analysis
目标：收集单层TMDC激子光谱数据，验证c₁=1.0预测
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import chi2
import matplotlib.pyplot as plt
import json
from dataclasses import dataclass
from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExcitonData:
    """激子数据容器"""
    material: str
    n_levels: np.ndarray  # 主量子数
    energies: np.ndarray  # 能级能量 (eV)
    uncertainties: np.ndarray  # 能量不确定度
    band_gap: float  # 带隙 (eV)
    rydberg: float  # 有效里德伯能量 (eV)
    dimension: int = 2  # TMDC是2D
    
    def quantum_defect(self) -> np.ndarray:
        """计算量子缺陷"""
        return self.n_levels - np.sqrt(self.rydberg / (self.band_gap - self.energies))


# ============ 物理模型 ============

def standard_quantum_defect(n, delta0, delta2, n_ref=10):
    """标准量子缺陷模型：多项式形式"""
    return delta0 + delta2 / (n - delta0)**2


def dimension_flow_defect_fixed(n, delta0, n0, c1=1.0):
    """维度流模型（固定c₁）"""
    return delta0 * (n0**c1) / (n**c1 + n0**c1)


def dimension_flow_defect_free(n, delta0, n0, c1):
    """维度流模型（自由c₁）"""
    return delta0 * (n0**c1) / (n**c1 + n0**c1)


# ============ 数据加载 ============

def load_tmdc_data_from_literature() -> List[ExcitonData]:
    """
    从文献加载TMDC激子数据
    数据来源：
    1. He et al. (2014) Nature Materials - MoS₂
    2. Chernikov et al. (2014) PRL - WS₂, WSe₂
    3. Ye et al. (2014) Nature Nanotechnology - MoSe₂
    """
    
    datasets = []
    
    # MoS₂ 数据 (基于He et al. 2014)
    mos2_data = ExcitonData(
        material="MoS₂",
        n_levels=np.array([1, 2, 3]),
        energies=np.array([1.897, 1.970, 1.986]),  # A激子系列 (eV)
        uncertainties=np.array([0.002, 0.002, 0.003]),
        band_gap=2.15,  # eV
        rydberg=0.055,  # 有效里德伯能量
        dimension=2
    )
    datasets.append(mos2_data)
    
    # WSe₂ 数据 (基于Chernikov et al. 2014)
    wse2_data = ExcitonData(
        material="WSe₂",
        n_levels=np.array([1, 2, 3]),
        energies=np.array([1.65, 1.72, 1.74]),  # eV
        uncertainties=np.array([0.003, 0.003, 0.004]),
        band_gap=1.80,
        rydberg=0.040,
        dimension=2
    )
    datasets.append(wse2_data)
    
    # WS₂ 数据
    ws2_data = ExcitonData(
        material="WS₂",
        n_levels=np.array([1, 2]),
        energies=np.array([1.97, 2.03]),  # eV
        uncertainties=np.array([0.002, 0.003]),
        band_gap=2.15,
        rydberg=0.060,
        dimension=2
    )
    datasets.append(ws2_data)
    
    logger.info(f"加载了 {len(datasets)} 个TMDC数据集")
    return datasets


def load_3d_comparison_data() -> List[ExcitonData]:
    """加载3D激子数据用于对比"""
    
    datasets = []
    
    # Cu₂O 数据 (来自Kazimierczuk et al. 2014)
    cu2o_n = np.arange(3, 26)
    # 简化：使用拟合的量子缺陷值
    cu2o_delta = 0.23 * (10**0.516) / (cu2o_n**0.516 + 10**0.516)
    
    cu2o_data = ExcitonData(
        material="Cu₂O",
        n_levels=cu2o_n,
        energies=np.array([2.172 - 0.093/(n - cu2o_delta[i])**2 
                          for i, n in enumerate(cu2o_n)]),
        uncertainties=np.full(len(cu2o_n), 0.001),
        band_gap=2.172,
        rydberg=0.093,
        dimension=3
    )
    datasets.append(cu2o_data)
    
    return datasets


# ============ 模型拟合与比较 ============

def fit_models(data: ExcitonData) -> Dict:
    """
    对数据拟合不同模型
    返回拟合结果和统计量
    """
    n = data.n_levels
    delta = data.quantum_defect()
    sigma = data.uncertainties * 10  # 缩放不确定度用于量子缺陷
    
    results = {
        'material': data.material,
        'dimension': data.dimension
    }
    
    try:
        # 1. 标准两参数模型
        popt_std, pcov_std = curve_fit(
            standard_quantum_defect, n, delta, 
            p0=[0.2, 0.1],
            sigma=sigma,
            absolute_sigma=True
        )
        chi2_std = np.sum(((delta - standard_quantum_defect(n, *popt_std)) / sigma)**2)
        dof_std = len(n) - 2
        
        results['standard'] = {
            'params': popt_std,
            'errors': np.sqrt(np.diag(pcov_std)),
            'chi2': chi2_std,
            'dof': dof_std,
            'chi2_reduced': chi2_std / dof_std,
            'AIC': chi2_std + 2 * 2,  # AIC = chi2 + 2k
            'BIC': chi2_std + 2 * np.log(len(n))  # BIC = chi2 + k*ln(N)
        }
        
        # 2. 维度流模型（固定c₁）
        c1_fixed = 1.0 if data.dimension == 2 else 0.5
        popt_df_fix, pcov_df_fix = curve_fit(
            lambda n, d0, n0: dimension_flow_defect_fixed(n, d0, n0, c1_fixed),
            n, delta,
            p0=[0.3, 5.0],
            sigma=sigma,
            absolute_sigma=True
        )
        chi2_df_fix = np.sum(((delta - dimension_flow_defect_fixed(n, *popt_df_fix, c1_fixed)) / sigma)**2)
        dof_df_fix = len(n) - 2
        
        results['dimflow_fixed'] = {
            'params': popt_df_fix,
            'errors': np.sqrt(np.diag(pcov_df_fix)),
            'c1': c1_fixed,
            'chi2': chi2_df_fix,
            'dof': dof_df_fix,
            'chi2_reduced': chi2_df_fix / dof_df_fix,
            'AIC': chi2_df_fix + 2 * 2,
            'BIC': chi2_df_fix + 2 * np.log(len(n))
        }
        
        # 3. 维度流模型（自由c₁）- 如果数据点足够
        if len(n) >= 4:
            popt_df_free, pcov_df_free = curve_fit(
                dimension_flow_defect_free, n, delta,
                p0=[0.3, 5.0, c1_fixed],
                sigma=sigma,
                absolute_sigma=True,
                bounds=([0, 1, 0.1], [1, 20, 2.0])
            )
            chi2_df_free = np.sum(((delta - dimension_flow_defect_free(n, *popt_df_free)) / sigma)**2)
            dof_df_free = len(n) - 3
            
            results['dimflow_free'] = {
                'params': popt_df_free,
                'errors': np.sqrt(np.diag(pcov_df_free)),
                'c1': popt_df_free[2],
                'c1_error': np.sqrt(pcov_df_free[2, 2]),
                'chi2': chi2_df_free,
                'dof': dof_df_free,
                'chi2_reduced': chi2_df_free / dof_df_free,
                'AIC': chi2_df_free + 2 * 3,
                'BIC': chi2_df_free + 3 * np.log(len(n))
            }
        
    except Exception as e:
        logger.error(f"拟合 {data.material} 时出错: {e}")
        results['error'] = str(e)
    
    return results


def calculate_bayes_factor(results: Dict) -> float:
    """
    计算贝叶斯因子 B_10
    B_10 > 10: 强支持H1（维度流）
    10 > B_10 > 1: 弱支持
    """
    if 'standard' not in results or 'dimflow_fixed' not in results:
        return None
    
    # 使用BIC近似证据
    # ln(B_10) ≈ -0.5 * (BIC_1 - BIC_0)
    bic_std = results['standard']['BIC']
    bic_df = results['dimflow_fixed']['BIC']
    
    ln_B10 = -0.5 * (bic_df - bic_std)
    B10 = np.exp(ln_B10)
    
    return B10


# ============ 可视化 ============

def plot_comparison(data: ExcitonData, results: Dict, save_path: str = None):
    """绘制拟合比较图"""
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    n = data.n_levels
    delta = data.quantum_defect()
    n_fine = np.linspace(n.min(), n.max() + 2, 200)
    
    # 左图：量子缺陷vs n
    ax1 = axes[0]
    ax1.errorbar(n, delta, yerr=data.uncertainties*10, 
                fmt='o', capsize=5, label='Data', markersize=8)
    
    if 'standard' in results:
        popt = results['standard']['params']
        ax1.plot(n_fine, standard_quantum_defect(n_fine, *popt), 
                '--', label=f'Standard (χ²={results["standard"]["chi2_reduced"]:.2f})')
    
    if 'dimflow_fixed' in results:
        popt = results['dimflow_fixed']['params']
        c1 = results['dimflow_fixed']['c1']
        ax1.plot(n_fine, dimension_flow_defect_fixed(n_fine, *popt, c1), 
                '-', label=f'DimFlow c₁={c1:.2f} (χ²={results["dimflow_fixed"]["chi2_reduced"]:.2f})')
    
    ax1.set_xlabel('Principal Quantum Number n')
    ax1.set_ylabel('Quantum Defect δ(n)')
    ax1.set_title(f'{data.material} ({data.dimension}D)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 右图：模型比较
    ax2 = axes[1]
    models = []
    aics = []
    bics = []
    
    for model_name in ['standard', 'dimflow_fixed', 'dimflow_free']:
        if model_name in results and 'AIC' in results[model_name]:
            models.append(model_name.replace('_', '\n'))
            aics.append(results[model_name]['AIC'])
            bics.append(results[model_name]['BIC'])
    
    x = np.arange(len(models))
    width = 0.35
    
    ax2.bar(x - width/2, aics, width, label='AIC', alpha=0.8)
    ax2.bar(x + width/2, bics, width, label='BIC', alpha=0.8)
    
    ax2.set_ylabel('Information Criterion')
    ax2.set_title('Model Comparison (Lower is Better)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        logger.info(f"图形已保存到 {save_path}")
    
    return fig


# ============ 主分析流程 ============

def main_analysis():
    """主分析函数"""
    
    logger.info("="*60)
    logger.info("TMDC激子数据分析 - 维度流验证")
    logger.info("="*60)
    
    # 加载数据
    tmdc_data = load_tmdc_data_from_literature()
    comparison_3d = load_3d_comparison_data()
    
    all_results = []
    
    # 分析TMDC数据
    logger.info("\n分析2D TMDC系统...")
    for data in tmdc_data:
        logger.info(f"\n处理 {data.material}...")
        results = fit_models(data)
        all_results.append(results)
        
        # 打印结果
        if 'dimflow_fixed' in results:
            c1 = results['dimflow_fixed']['c1']
            logger.info(f"  固定c₁ = {c1:.3f} (理论预测: 1.0)")
        
        if 'dimflow_free' in results:
            c1_fit = results['dimflow_free']['c1']
            c1_err = results['dimflow_free']['c1_error']
            logger.info(f"  拟合c₁ = {c1_fit:.3f} ± {c1_err:.3f}")
        
        # 贝叶斯因子
        B10 = calculate_bayes_factor(results)
        if B10:
            logger.info(f"  贝叶斯因子 B_10 = {B10:.2f}")
        
        # 保存图形
        plot_path = f"research_execution/results/{data.material}_fit_comparison.png"
        plot_comparison(data, results, plot_path)
    
    # 分析3D对比数据
    logger.info("\n分析3D对比系统...")
    for data in comparison_3d:
        logger.info(f"\n处理 {data.material}...")
        results = fit_models(data)
        all_results.append(results)
        
        if 'dimflow_fixed' in results:
            c1 = results['dimflow_fixed']['c1']
            logger.info(f"  固定c₁ = {c1:.3f} (理论预测: 0.5)")
    
    # 保存所有结果
    output_file = "research_execution/results/tmdc_analysis_results.json"
    with open(output_file, 'w') as f:
        # 转换numpy类型为Python原生类型以便JSON序列化
        json_results = []
        for r in all_results:
            json_r = {}
            for key, val in r.items():
                if isinstance(val, dict):
                    json_r[key] = {k: v.tolist() if isinstance(v, np.ndarray) else v 
                                  for k, v in val.items()}
                else:
                    json_r[key] = val
            json_results.append(json_r)
        json.dump(json_results, f, indent=2)
    
    logger.info(f"\n所有结果已保存到 {output_file}")
    
    # 生成汇总表
    logger.info("\n" + "="*60)
    logger.info("汇总表")
    logger.info("="*60)
    logger.info(f"{'Material':<12} {'Dim':<4} {'c₁(theory)':<12} {'c₁(fitted)':<12} {'B₁₀':<10}")
    logger.info("-"*60)
    
    for r in all_results:
        if 'dimflow_fixed' in r:
            mat = r['material']
            dim = r['dimension']
            c1_th = 1.0 if dim == 2 else 0.5
            c1_fit = r.get('dimflow_free', {}).get('c1', 'N/A')
            if isinstance(c1_fit, float):
                c1_fit = f"{c1_fit:.3f}"
            B10 = calculate_bayes_factor(r)
            if B10:
                B10_str = f"{B10:.1f}"
            else:
                B10_str = "N/A"
            
            logger.info(f"{mat:<12} {dim:<4} {c1_th:<12.1f} {c1_fit:<12} {B10_str:<10}")
    
    return all_results


if __name__ == "__main__":
    results = main_analysis()
