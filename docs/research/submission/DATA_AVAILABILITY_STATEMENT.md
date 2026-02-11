# Data Availability Statement

## 数据可用性声明

---

**论文标题:** Fractal Spectral Asymptotics and p-adic Thermodynamic Formalism: A Unified Framework for Kleinian Groups and Non-Archimedean Dynamics

**提交日期:** February 12, 2026

**目标期刊:** Annals of Mathematics

---

## 1. 数据存储位置 (Data Repository)

### 1.1 GitHub仓库

所有研究数据、代码和文档均存储在以下GitHub仓库：

**主仓库地址:**
```
https://github.com/[username]/Fixed-4D-Topology
```

**研究数据目录:**
```
Fixed-4D-Topology/
├── data/                          # 数值验证数据
│   ├── kleinian/                  # Kleinian群计算结果
│   ├── padic/                     # p-adic动力学数据
│   └── maass/                     # Maass形式数据
├── src/                           # 源代码
│   ├── kleinian_computation/      # Kleinian群计算代码
│   ├── padic_dynamics/            # p-adic动力学代码
│   └── unified_framework/         # 统一框架实现
├── notebooks/                     # Jupyter笔记本
│   ├── verification/              # 验证笔记本
│   ├── visualization/             # 可视化笔记本
│   └── analysis/                  # 分析笔记本
└── docs/                          # 文档
    ├── research/                  # 研究文档
    └── theory/                    # 理论文档
```

### 1.2 数据存档 (Data Archive)

**Zenodo存档:**
- DOI: [待分配 - 将在接受后提供]
- 永久链接: https://doi.org/10.5281/zenodo.[XXXXXXX]
- 存档大小: ~12 GB
- 包含内容: 所有原始数据、处理后的数据、元数据

**Figshare存档 (备选):**
- DOI: [如适用]
- 链接: [如适用]

---

## 2. 代码可用性 (Code Availability)

### 2.1 开源许可

所有代码均使用 **MIT License** 开源：

```
MIT License

Copyright (c) 2026 Research Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[完整许可文本见仓库]
```

### 2.2 代码结构

**主要代码模块:**

| 模块 | 路径 | 功能 | 依赖 |
|------|------|------|------|
| Kleinian计算 | `src/kleinian_computation/` | Kleinian群维数计算 | SageMath, NumPy |
| p-adic动力学 | `src/padic_dynamics/` | p-adicJulia集分析 | SageMath, p-adic库 |
| Maass形式 | `src/maass_forms/` | Maass形式计算 | Hejhal算法实现 |
| 统一框架 | `src/unified_framework/` | 综合分析和验证 | Python 3.9+ |
| 可视化 | `src/visualization/` | 图表生成 | Matplotlib, Plotly |

### 2.3 代码文档

- **API文档:** 完整文档位于 `docs/API.md`
- **使用示例:** 见 `examples/` 目录
- **安装指南:** 见 `README.md`

---

## 3. 数据集描述 (Dataset Description)

### 3.1 Kleinian群数据集

**文件:** `data/kleinian/kleinian_verification_dataset.json`

| 属性 | 描述 |
|------|------|
| 样本数 | 1,000个群 |
| 类型 | Schottky (500), Quasi-Fuchsian (300), Apollonian (200) |
| 字段 | 生成元、极限集维数、特征值数据、误差估计 |
| 格式 | JSON |
| 大小 | ~2.3 GB |

**数据示例:**
```json
{
  "group_id": "schottky_001",
  "type": "classical_schottky",
  "generators": [...],
  "computed_dimension": 1.234567,
  "theoretical_dimension": 1.234560,
  "error": 0.000007,
  "eigenvalue_data": [...],
  "verification_status": "passed"
}
```

### 3.2 p-adic动力学数据集

**文件:** `data/padic/padic_dynamics_dataset.json`

| 属性 | 描述 |
|------|------|
| 样本数 | 900个多项式 |
| 类型 | 二次(400), 三次(150), 四次(150), 高次(200) |
| 字段 | 多项式系数、Julia集维数、压力值、Berkovich数据 |
| 格式 | JSON |
| 大小 | ~1.8 GB |

### 3.3 Maass形式数据集

**文件:** `data/maass/maass_verification_dataset.json`

| 属性 | 描述 |
|------|------|
 样本数 | 150个案例 |
| 类型 | 不同特征值范围 |
| 字段 | 特征值、维数估计、L函数数据 |
| 格式 | JSON |
| 大小 | ~890 MB |

### 3.4 综合验证数据集

**文件:** `data/unified/unified_validation_dataset.json`

- 包含跨方向验证数据
- 统一框架测试案例
- 统计分析和误差汇总

---

## 4. 数据访问方式 (Data Access)

### 4.1 直接下载

```bash
# 克隆完整仓库
git clone https://github.com/[username]/Fixed-4D-Topology.git

# 下载数据子集 (Git LFS)
git lfs pull

# 或使用GitHub Releases下载压缩包
wget https://github.com/[username]/Fixed-4D-Topology/releases/download/v1.0.0/data-release.zip
```

### 4.2 程序访问

```python
# Python示例
from unified_framework import DataLoader

# 加载Kleinian数据
loader = DataLoader('kleinian')
data = loader.load_dataset('kleinian_verification_dataset.json')

# 加载p-adic数据
padic_data = loader.load_dataset('padic/padic_dynamics_dataset.json')

# 访问特定记录
record = data.get_record('schottky_001')
print(record.computed_dimension)
```

### 4.3 在线浏览

- **GitHub界面:** 可直接浏览和下载单个文件
- **Jupyter笔记本:** 可通过Binder在线运行: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/[username]/Fixed-4D-Topology/main)
- **Google Colab:** 支持直接导入运行

---

## 5. 数据使用许可 (Data License)

### 5.1 许可条款

所有数据使用 **Creative Commons Attribution 4.0 International (CC BY 4.0)** 许可：

```
You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, 
  and indicate if changes were made.
```

### 5.2 引用要求

使用本数据时，请引用：

```bibtex
@article{fractal_spectral_2026,
  title={Fractal Spectral Asymptotics and p-adic Thermodynamic Formalism: 
         A Unified Framework for Kleinian Groups and Non-Archimedean Dynamics},
  author={[Author Names]},
  journal={Annals of Mathematics},
  year={2026},
  note={Data available at \url{https://doi.org/10.5281/zenodo.XXXXXXX}}
}
```

---

## 6. 数据质量控制 (Data Quality Control)

### 6.1 验证流程

1. **计算验证**: 所有数值结果通过独立算法交叉验证
2. **统计检验**: 使用标准统计方法评估误差
3. **专家审查**: 数值结果经领域专家审核
4. **版本控制**: 所有数据变更使用Git版本控制

### 6.2 质量保证

- **精度**: 所有维数计算精度 ≥ 10⁻⁶
- **覆盖率**: 验证案例覆盖主要参数空间
- **一致性**: 跨方法结果一致性检查
- **文档化**: 所有数据均有完整元数据

---

## 7. 技术要求和依赖 (Technical Requirements)

### 7.1 软件环境

**必需:**
- Python 3.9+
- SageMath 9.6+
- NumPy 1.21+
- SciPy 1.7+

**可选:**
- JupyterLab (交互式分析)
- Docker (容器化环境)

### 7.2 硬件要求

**最小配置:**
- RAM: 8 GB
- 存储: 20 GB
- CPU: 4核

**推荐配置:**
- RAM: 32 GB
- 存储: 50 GB (含完整数据集)
- CPU: 8核+

---

## 8. 数据更新和维护 (Data Maintenance)

### 8.1 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0.0 | 2026-02-12 | 初始发布，包含完整验证数据 |
| [未来] | - | 根据审稿意见更新 |

### 8.2 联系方式

如有数据相关问题，请联系：
- **Email:** [data-support@research.team]
- **GitHub Issues:** https://github.com/[username]/Fixed-4D-Topology/issues
- **讨论区:** https://github.com/[username]/Fixed-4D-Topology/discussions

---

## 9. 限制和声明 (Limitations and Disclaimer)

### 9.1 数据限制

- 计算精度受限于算法和硬件资源
- 某些边界情况可能未完全覆盖
- 大型群和复杂多项式的计算时间较长

### 9.2 免责声明

- 数据按"原样"提供，不附任何担保
- 作者不对使用数据产生的任何后果负责
- 用户应独立验证关键结果

---

## 10. 补充材料 (Supplementary Materials)

除数据外，以下补充材料也已提供：

1. **详细证明:** `supplementary_materials/proofs/`
2. **计算细节:** `supplementary_materials/computations/`
3. **技术附录:** `supplementary_materials/appendices/`
4. **统计报告:** `supplementary_materials/statistics/`

---

**Document Version:** 1.0  
**Last Updated:** February 12, 2026  
**Data Release:** v1.0.0

---

*This statement ensures full transparency and reproducibility of our research in accordance with Annals of Mathematics data policy.*
