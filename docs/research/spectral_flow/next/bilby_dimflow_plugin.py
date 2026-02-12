#!/usr/bin/env python3
"""
Bilby + 维度流动 波形插件

使用Bilby进行维度流动的引力波分析
"""

import numpy as np
import bilby
from bilby.gw.source import _base_lal_caller

# 维度流动函数
def dimension_flow_orbital(r_orbit, r_isco=6.0):
    """轨道相关的维度流动"""
    epsilon = r_isco / r_orbit if r_orbit > r_isco else 1.0
    return 2.5 + 1.5 / (1 + (epsilon / 0.8)**1.7)


def dimflow_binary_black_hole(
    frequency_array,
    mass_1,
    mass_2,
    luminosity_distance,
    a_1=0.0,
    a_2=0.0,
    tilt_1=0.0,
    tilt_2=0.0,
    phi_12=0.0,
    phi_jl=0.0,
    theta_jn=0.0,
    phase=0.0,
    d_eff_param=3.5,  # 维度流动参数!
    **kwargs
):
    """
    维度流动修正的双黑洞波形
    
    参数:
    - d_eff_param: 有效维度参数 (2.5-4.0)
    
    其他参数同标准IMRPhenomD
    """
    # 计算修正的啁啾质量
    M_chirp_std = (mass_1 * mass_2)**(3/5) / (mass_1 + mass_2)**(1/5)
    M_chirp_eff = M_chirp_std * (4.0 / d_eff_param)**(3/5)
    
    # 质量比调整 (保持质量比不变)
    mass_ratio = mass_2 / mass_1
    M_total_eff = M_chirp_eff * (1 + mass_ratio)**(1/5) / mass_ratio**(3/5)
    
    mass_1_eff = M_total_eff / (1 + mass_ratio)
    mass_2_eff = M_total_eff * mass_ratio / (1 + mass_ratio)
    
    # 调用标准IMRPhenomD (使用Bilby)
    from bilby.gw.source import lal_binary_black_hole
    
    h = lal_binary_black_hole(
        frequency_array,
        mass_1=mass_1_eff,
        mass_2=mass_2_eff,
        luminosity_distance=luminosity_distance,
        a_1=a_1,
        a_2=a_2,
        tilt_1=tilt_1,
        tilt_2=tilt_2,
        phi_12=phi_12,
        phi_jl=phi_jl,
        theta_jn=theta_jn,
        phase=phase,
        **kwargs
    )
    
    # 应用振幅修正
    amp_correction = (4.0 / d_eff_param)**(5/6)
    h *= amp_correction
    
    return h


# 注册波形
bilby.gw.source.add_source('dimflow_IMRPhenomD', dimflow_binary_black_hole)


class DimFlowAnalysis:
    """维度流动分析类"""
    
    def __init__(self, label='dimflow_analysis'):
        self.label = label
        self.results = {}
    
    def setup_injection(self, injection_parameters):
        """设置注入参数"""
        self.injection_parameters = injection_parameters
    
    def setup_priors(self, include_dimflow=True):
        """设置先验"""
        priors = bilby.gw.prior.BBHPriorDict()
        
        # 标准参数
        priors['mass_1'] = bilby.core.prior.Uniform(20, 50, 'mass_1')
        priors['mass_2'] = bilby.core.prior.Uniform(20, 50, 'mass_2')
        priors['luminosity_distance'] = bilby.core.prior.Uniform(100, 1000, 'luminosity_distance')
        
        if include_dimflow:
            # 维度流动参数
            priors['d_eff_param'] = bilby.core.prior.Uniform(2.5, 4.0, 'd_eff_param')
        
        return priors
    
    def run_analysis(self, ifos, waveform_arguments, priors, duration=4, sampling_rate=2048):
        """运行分析"""
        
        # 创建波形生成器
        waveform_generator = bilby.gw.WaveformGenerator(
            duration=duration,
            sampling_frequency=sampling_rate,
            frequency_domain_source_model=dimflow_binary_black_hole,
            waveform_arguments=waveform_arguments,
        )
        
        # 似然函数
        likelihood = bilby.gw.GravitationalWaveTransient(
            interferometers=ifos,
            waveform_generator=waveform_generator,
        )
        
        # 运行采样
        result = bilby.run_sampler(
            likelihood=likelihood,
            priors=priors,
            sampler='dynesty',
            npoints=500,
            outdir=f'outdir_{self.label}',
            label=self.label,
        )
        
        self.results = result
        return result
    
    def compare_models(self, result_std, result_dimflow):
        """比较标准模型和维度流动模型"""
        
        ln_z_std = result_std.log_evidence
        ln_z_dimflow = result_dimflow.log_evidence
        
        bayes_factor = np.exp(ln_z_dimflow - ln_z_std)
        
        print(f"标准模型证据: {ln_z_std:.2f}")
        print(f"维度流动模型证据: {ln_z_dimflow:.2f}")
        print(f"贝叶斯因子 B_21: {bayes_factor:.2f}")
        
        if bayes_factor > 10:
            conclusion = "强支持维度流动模型"
        elif bayes_factor > 3:
            conclusion = "中等支持维度流动模型"
        elif bayes_factor > 1:
            conclusion = "弱支持维度流动模型"
        elif bayes_factor > 1/3:
            conclusion = "弱支持标准模型"
        elif bayes_factor > 1/10:
            conclusion = "中等支持标准模型"
        else:
            conclusion = "强支持标准模型"
        
        print(f"结论: {conclusion}")
        
        return bayes_factor


if __name__ == "__main__":
    print("Bilby + 维度流动 波形插件")
    print("使用: bilby.gw.source.add_source('dimflow_IMRPhenomD', dimflow_binary_black_hole)")
