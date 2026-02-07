# 复杂网络的有效维度：大规模实证研究

**Effective Dimensions of Complex Networks: A Large-Scale Empirical Study**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Data: 2.1M nodes](https://img.shields.io/badge/data-2.1M%20nodes-green.svg)]()

[English Version](#english-version) | [中文介绍](#中文介绍)

---

## 🎯 项目简介

这是一个关于**复杂网络有效维度**的开源研究项目。我们分析了**7个大规模真实网络数据集**，涵盖210万个节点，揭示了不同网络类型的几何特性。

### 核心发现

```
网络维度层次:

全球基础设施 (Internet AS)     d = 4.4  ████████████████████████████ 最高
学术合作网络 (DBLP)            d = 3.0  ██████████████████░░░░░░░░░░ 高
社交网络 (Facebook)            d = 2.6  ████████████████░░░░░░░░░░░░ 中
生物网络 (Yeast PPI)           d = 2.4  ███████████████░░░░░░░░░░░░░ 中
区域基础设施 (Power Grid)      d = 2.1  ████████████░░░░░░░░░░░░░░░░ 中
社交网络 (Twitter)             d = 2.0  ███████████░░░░░░░░░░░░░░░░░ 低
机构通信网络 (Email)           d = 1.2  ███████░░░░░░░░░░░░░░░░░░░░░ 最低
```

**关键洞察**:
- 🔍 标准网络模型（BA/WS）系统性低估真实网络维度50%-400%
- 🧬 生物网络复杂度被严重低估（维度与社交网络相当）
- 🌍 全球互联网具有超复杂拓扑结构（d=4.4）
- 📐 空间约束决定区域网络维度（电网d≈2.0符合平面图理论）

---

## 📊 数据集

| 网络 | 类型 | 节点数 | 维度 | 来源 |
|-----|------|-------|------|------|
| Internet AS | 基础设施 | 1,696,415 | **4.36** | CAIDA |
| DBLP | 学术合作 | 317,080 | **3.0** | SNAP |
| Yeast PPI | 生物网络 | 7,203 | **2.4** | BioGRID |
| Facebook | 社交网络 | 4,039 | **2.57** | SNAP |
| Twitter | 社交网络 | 81,306 | **~2.0** | SNAP |
| Power Grid | 基础设施 | 101 | **2.11** | IEEE |
| Email | 机构通信 | 1,005 | **1.24** | SNAP |

**总计**: 2,107,149节点, 14,850,609边

### 数据可用性

所有数据均来自公开数据源，可自由获取：
- **SNAP**: https://snap.stanford.edu/data/
- **BioGRID**: https://downloads.thebiogrid.org/ (MIT License)
- **CAIDA**: https://www.caida.org/data/
- **IEEE**: https://www2.ee.washington.edu/research/pstca/

详细数据说明见 [data/README.md](data/README.md)

---

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 无需额外依赖（纯Python标准库）

### 安装

```bash
# 克隆仓库
git clone https://github.com/dpsnet/complex-network-dimensions.git
cd complex-network-dimensions

# 查看代码结构
ls -la code/
```

### 运行分析

```bash
# 分析酵母PPI网络维度
python code/parse_biogrid_yeast.py

# 分析电网维度
python code/parse_power_grid.py

# 大规模网络抽样分析
python code/analyze_large_network.py
```

---

## 📁 项目结构

```
.
├── papers/              # 研究论文
│   ├── manuscript.md   # 主论文
│   └── supplementary/  # 补充材料
│
├── data/               # 数据集
│   ├── raw/           # 原始数据
│   └── processed/     # 处理后的数据
│
├── code/              # 分析代码
│   ├── parse_biogrid_yeast.py
│   ├── parse_power_grid.py
│   ├── analyze_large_network.py
│   └── download_and_validate.py
│
├── results/           # 分析结果
│   └── dimension_results.csv
│
└── docs/             # 文档
    ├── methodology.md
    └── data_sources.md
```

---

## 📖 研究论文

完整研究论文见 [papers/manuscript.md](papers/manuscript.md)

### 核心结论

1. **维度层次**: 基础设施 > 学术合作 > 社交/生物 > 机构通信
2. **模型局限**: 标准BA/WS模型无法捕捉真实网络复杂性
3. **生物网络**: 蛋白质相互作用网络的维度被传统理论低估
4. **尺度效应**: 网络维度与规模/功能强相关

---

## 🔬 方法论

### 盒计数法 (Box-Counting)

用于测量网络的有效维度：

```
d_B = -Δlog(N_B) / Δlog(l_B)
```

其中 N_B 是覆盖网络所需的盒子数，l_B 是盒子大小。

### 算法特点

- ✅ 纯Python实现，无需外部依赖
- ✅ 支持大规模网络（百万级节点）
- ✅ 智能抽样算法，高效处理密集网络
- ✅ 完整注释，易于理解

---

## 📈 结果可视化

![维度层次图](docs/figures/dimension_hierarchy.png)

详细可视化图表见 `docs/figures/`

---

## 🤝 如何贡献

欢迎社区贡献！您可以：

- 🐛 报告bug
- 💡 提出改进建议
- 📊 添加新的网络数据集
- 🔧 优化算法
- 📝 完善文档

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📚 引用

如果您使用了本项目的数据或代码，请引用：

```bibtex
@misc{wang2026networkdimensions,
  title={Effective Dimensions of Complex Networks: A Large-Scale Empirical Study},
  author={Wang Bin},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/dpsnet/complex-network-dimensions}}
}
```

同时请引用原始数据源：
- **BioGRID**: Stark et al. (2006), Nucleic Acids Res. 34:D535-9
- **SNAP**: 各数据集原始论文
- **CAIDA**: 数据源说明

---

## 📜 许可证

### 代码
[MIT License](LICENSE) - 自由使用、修改、分发

### 数据
- BioGRID: MIT License
- SNAP/CAIDA/IEEE: 公开学术使用

详见数据目录中的README

---

## 🙏 致谢

感谢以下组织提供公开数据：
- [SNAP Stanford](https://snap.stanford.edu/) - 社交网络数据
- [BioGRID](https://thebiogrid.org/) - 蛋白质相互作用数据
- [CAIDA](https://www.caida.org/) - 互联网拓扑数据
- [IEEE](https://www.ieee.org/) - 电力系统测试案例

---

## 📧 联系方式

- 项目主页: https://github.com/dpsnet/Fixed-4D-Topology
- 问题反馈: [GitHub Issues](https://github.com/dpsnet/Fixed-4D-Topology/issues)

---

## English Version

### Overview

This is an open-source research project on **effective dimensions of complex networks**. We analyzed **7 large-scale real-world networks** covering 2.1 million nodes, revealing the geometric properties of different network types.

### Key Findings

- Standard network models (BA/WS) underestimate real network dimensions by 50-400%
- Biological networks have unexpectedly high dimensions (comparable to social networks)
- Global internet infrastructure has super-complex topology (d=4.4)
- Spatial constraints determine regional network dimensions

### Datasets

7 real-world networks: Internet AS, DBLP, Yeast PPI, Facebook, Twitter, Power Grid, Email

### Quick Start

```bash
git clone https://github.com/dpsnet/complex-network-dimensions.git
cd complex-network-dimensions
python code/parse_biogrid_yeast.py
```

### License

Code: MIT License  
Data: Original licenses (BioGRID MIT, others academic use)

---

**Last Updated**: 2026-02-07  
**Status**: ✅ Research Complete, Open Source Release Ready
