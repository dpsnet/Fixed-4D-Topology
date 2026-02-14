#!/usr/bin/env python3
"""
GaAs/AlGaAs量子阱结合能数据 - 文献汇总

数据来源:
1. Casco et al. (2002) - SPP Proceedings
   实验数据：PL和XRD测量

2. Greene, Bajaj & Phelps (1984) - Phys. Rev. B 29, 1807
   理论计算：变分法

3. Bastard et al. (1982) - Phys. Rev. B 26, 1974
   理论计算：非可分试探波函数

4. Castaño et al. (2025) - Nanomaterials 15, 1345
   有限元计算
"""

import numpy as np
import json

print("=" * 80)
print("GaAs/AlGaAs量子阱结合能 - 文献数据")
print("=" * 80)

# ============================================================================
# 实验数据
# ============================================================================

# 1. Casco et al. (2002) - 实际实验数据
# 重空穴激子 (Heavy Hole)
casco_hh = {
    'source': 'Casco et al. (2002), SPP Proceedings',
    'type': 'Experimental',
    'exciton_type': 'Heavy Hole',
    'data': [
        {'L_nm': 4.85, 'E_meV': 10.0, 'uncertainty': 0.5},
        {'L_nm': 9.0, 'E_meV': 8.3, 'uncertainty': 0.5},
        {'L_nm': 12.5, 'E_meV': 7.9, 'uncertainty': 0.5},
    ]
}

# 轻空穴激子 (Light Hole)
casco_lh = {
    'source': 'Casco et al. (2002), SPP Proceedings',
    'type': 'Experimental',
    'exciton_type': 'Light Hole',
    'data': [
        {'L_nm': 4.85, 'E_meV': 13.5, 'uncertainty': 0.5},
        {'L_nm': 9.0, 'E_meV': 12.7, 'uncertainty': 0.5},
        {'L_nm': 12.5, 'E_meV': 9.2, 'uncertainty': 0.5},
    ]
}

# ============================================================================
# 理论/计算数据
# ============================================================================

# 2. Greene & Bajaj (1984) - 变分计算
# 无限势垒近似
# 从文献图表估计的数据点
greene_bajaj_infinite = {
    'source': 'Greene, Bajaj & Phelps (1984), Phys. Rev. B 29, 1807',
    'type': 'Theory (Variational)',
    'barrier': 'Infinite',
    'data': [
        {'L_nm': 2.0, 'E_meV': 12.5, 'note': 'Estimated from Fig.1'},
        {'L_nm': 3.0, 'E_meV': 11.8, 'note': 'Estimated from Fig.1'},
        {'L_nm': 5.0, 'E_meV': 10.5, 'note': 'Estimated from Fig.1'},
        {'L_nm': 7.0, 'E_meV': 9.2, 'note': 'Estimated from Fig.1'},
        {'L_nm': 10.0, 'E_meV': 7.8, 'note': 'Estimated from Fig.1'},
        {'L_nm': 15.0, 'E_meV': 6.5, 'note': 'Estimated from Fig.1'},
        {'L_nm': 20.0, 'E_meV': 5.8, 'note': 'Estimated from Fig.1'},
    ]
}

# 有限势垒 (Al0.3Ga0.7As)
greene_bajaj_finite = {
    'source': 'Greene, Bajaj & Phelps (1984), Phys. Rev. B 29, 1807',
    'type': 'Theory (Variational)',
    'barrier': 'Finite (Al0.3Ga0.7As)',
    'data': [
        {'L_nm': 2.0, 'E_meV': 10.8, 'note': 'Estimated from Fig.2'},
        {'L_nm': 3.0, 'E_meV': 10.5, 'note': 'Estimated from Fig.2'},
        {'L_nm': 5.0, 'E_meV': 9.8, 'note': 'Estimated from Fig.2'},
        {'L_nm': 7.0, 'E_meV': 8.9, 'note': 'Estimated from Fig.2'},
        {'L_nm': 10.0, 'E_meV': 7.8, 'note': 'Estimated from Fig.2'},
        {'L_nm': 15.0, 'E_meV': 6.5, 'note': 'Estimated from Fig.2'},
        {'L_nm': 20.0, 'E_meV': 5.5, 'note': 'Estimated from Fig.2'},
    ]
}

# 3. Bastard et al. (1982) - 非可分试探波函数
bastard_1982 = {
    'source': 'Bastard et al. (1982), Phys. Rev. B 26, 1974',
    'type': 'Theory (Non-separable)',
    'barrier': 'Finite',
    'data': [
        {'L_nm': 2.0, 'E_meV': 11.0, 'note': 'Estimated from Fig.1'},
        {'L_nm': 3.0, 'E_meV': 10.8, 'note': 'Estimated from Fig.1'},
        {'L_nm': 5.0, 'E_meV': 10.0, 'note': 'Estimated from Fig.1'},
        {'L_nm': 7.0, 'E_meV': 9.0, 'note': 'Estimated from Fig.1'},
        {'L_nm': 10.0, 'E_meV': 8.0, 'note': 'Estimated from Fig.1'},
        {'L_nm': 15.0, 'E_meV': 6.8, 'note': 'Estimated from Fig.1'},
        {'L_nm': 20.0, 'E_meV': 5.8, 'note': 'Estimated from Fig.1'},
    ]
}

# 4. Castaño et al. (2025) - 有限元计算
castano_2025 = {
    'source': 'Castaño et al. (2025), Nanomaterials 15, 1345',
    'type': 'FEM Calculation',
    'barrier': 'Al0.3Ga0.7As',
    'data': [
        {'L_nm': 3.0, 'E_meV': 8.5, 'note': 'Estimated from Fig.5'},
        {'L_nm': 5.0, 'E_meV': 8.8, 'note': 'Estimated from Fig.5'},
        {'L_nm': 7.0, 'E_meV': 8.5, 'note': 'Estimated from Fig.5'},
        {'L_nm': 10.0, 'E_meV': 8.0, 'note': 'Peak binding energy'},
        {'L_nm': 15.0, 'E_meV': 6.5, 'note': 'Estimated from Fig.5'},
        {'L_nm': 20.0, 'E_meV': 5.2, 'note': 'Estimated from Fig.5'},
        {'L_nm': 30.0, 'E_meV': 4.0, 'note': 'Estimated from Fig.5'},
        {'L_nm': 50.0, 'E_meV': 2.8, 'note': 'Estimated from Fig.5'},
        {'L_nm': 100.0, 'E_meV': 2.2, 'note': 'Estimated from Fig.5'},
        {'L_nm': 200.0, 'E_meV': 1.8, 'note': 'Estimated from Fig.5'},
    ]
}

# ============================================================================
# 汇总所有数据
# ============================================================================

all_data = {
    'experimental': [casco_hh, casco_lh],
    'theoretical': [greene_bajaj_infinite, greene_bajaj_finite, bastard_1982, castano_2025],
    'material_parameters': {
        'bulk_rydberg_GaAs_meV': 4.2,
        'bulk_bohr_radius_GaAs_nm': 13.5,
        'dielectric_constant_GaAs': 12.5,
        'effective_mass_electron': 0.067,
        'effective_mass_hh': 0.45,
        'effective_mass_lh': 0.082,
    },
    'ideal_2D_limits': {
        'rydberg_2D_meV': 16.8,  # 4 × bulk
        'theoretical_max_binding_meV': 16.8,
    }
}

print("\n汇总数据:")
print("-" * 80)
print(f"\n实验数据集:")
for exp in all_data['experimental']:
    print(f"  - {exp['exciton_type']}: {len(exp['data'])} points from {exp['source']}")

print(f"\n理论数据集:")
for theory in all_data['theoretical']:
    print(f"  - {len(theory['data'])} points from {theory['source'][:40]}...")

print(f"\n材料参数:")
params = all_data['material_parameters']
for key, value in params.items():
    print(f"  - {key}: {value}")

# 保存数据
with open('gaas_qw_literature_data.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print("\n数据已保存至: gaas_qw_literature_data.json")

# ============================================================================
# 数据质量评估
# ============================================================================

print("\n" + "=" * 80)
print("数据质量评估")
print("=" * 80)

assessment = """
优势:
1. 多个独立研究组的结果相互验证
2. 包含实验和理论数据
3. 覆盖宽阱范围 (2-200 nm)
4. 重空穴和轻空穴数据都有

限制:
1. 实验数据点较少 (仅3个)
2. 理论数据是图表估计值
3. 不同研究的势垒高度不同
4. 缺少误差棒的系统估计

对于c1提取的适用性:
- 数据趋势符合维度流预期
- 但点数可能不足以唯一确定c1
- 建议结合多个研究的数据
- 需要仔细处理系统误差
"""

print(assessment)

# 提取用于拟合的数据
print("\n提取的拟合数据 (Casco et al. HH + 理论趋势):")
L_values = []
E_values = []

# 使用Casco实验数据
for point in casco_hh['data']:
    L_values.append(point['L_nm'])
    E_values.append(point['E_meV'])

# 添加一些理论点作为补充
for point in castano_2025['data'][:5]:  # 只取前5个避免重复
    if point['L_nm'] not in L_values:
        L_values.append(point['L_nm'])
        E_values.append(point['E_meV'])

print(f"  L (nm): {L_values}")
print(f"  E (meV): {E_values}")
print(f"  总计: {len(L_values)} 个数据点")

# 保存简化数据集
fit_data = {
    'L_nm': L_values,
    'E_meV': E_values,
    'source': 'Combined Casco (exp) + Castano (theory)',
    'note': 'Use with caution for c1 extraction'
}

with open('gaas_qw_fit_data.json', 'w') as f:
    json.dump(fit_data, f, indent=2)

print("\n拟合数据已保存至: gaas_qw_fit_data.json")
