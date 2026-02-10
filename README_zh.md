# Dimensionics: 数学核心 (T1-T4)

**[English](README.md) | 中文**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18511249.svg)](https://doi.org/10.5281/zenodo.18511249)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-核心基础-blue.svg)]()

> **L1/L2 严格数学基础**: Cantor理论、Master方程、凸性分析、谱几何。

---

## ⚠️ 撤销声明

**v3.0.0 已被撤销** (2026年2月11日)

之前的版本声称：
- ❌ "三座桥消除唯象参数" — **虚假**
- ❌ "C* = (Δλ/λ₁)·d_c·(1-d_c)·π/4" — **错误** (理论值~1.46，经验值~0.21)
- ❌ "三座桥的L1严格证明" — **未证明**
- ❌ "100%第一性原理统一" — **未实现**

**本版本 (v3.0.0-core)** 仅包含数学严格的核心内容 (T1-T4)。

---

## 当前范围 (L1/L2 严格)

### 数学核心 (T1-T4)

| 模块 | 方向 | 严格性 | 状态 |
|------|------|--------|------|
| **T1** | Cantor维数逼近 | L1-L2 | ✅ 完成 |
| **T2** | Master方程与谱PDE | L2 | ✅ 完成 |
| **T3** | 凸性分析 | L1 | ✅ 完成 |
| **T4** | 代数拓扑与谱几何 | L2 | ✅ 完成 |

### 物理应用 (A-G)

| 论文 | 主题 | 严格性 | 状态 |
|------|------|--------|------|
| **A** | 谱Zeta函数 | L2 | ✅ 可用 |
| **B** | 维度流动力学 | L2 | ✅ 可用 |
| **C** | 模对应 | L2 | ✅ 可用 |
| **D** | P-adic算术 | L2 | ✅ 可用 |
| **E** | 分形上的Sobolev空间 | L2 | ✅ 可用 |
| **F** | 复杂度理论 | L2 | ✅ 可用 |
| **G** | 变分原理 | L2 | ✅ 可用 |

**总计**: 11篇论文 (T1-T4核心 + A-G应用)，全部有tex+pdf。

---

## 删除内容 (未达L1/L2)

| 内容 | 原因 | 当前位置 |
|------|------|----------|
| **三座桥 (A,B,C)** | 公式未证明，声明虚假 | 已删除 |
| **H (量子维度)** | 仅数值模拟 (L3) | 仅研究计划 |
| **I (网络几何)** | 仅实证分析 (L3) | 仅研究计划 |
| **J (随机分形)** | 仅模拟 (L3) | 仅研究计划 |
| **K (机器学习维度)** | 仅实验性质 (L3) | 仅研究计划 |

**标准**: L1/L2 或没有。

---

## 安装

```bash
pip install dimensionics
```

## 使用

```python
from dimensionics import MasterEquation, CantorApproximation

# T2: Master方程
me = MasterEquation(alpha=0.5, beta=0.3)

# T1: Cantor逼近
cantor = CantorApproximation()
```

---

## 仓库结构

```
Fixed-4D-Topology/
├── src/dimensionics/           # 严格核心 (T1-T4)
│   ├── core/                   # T2-T3: Master方程、凸性
│   ├── number_theory/          # T1: Cantor理论
│   └── topology/               # T4: 谱几何
├── papers/                     # 核心论文 (T1-T10, A-G)
├── docs/theory/core/           # T1-T4 文档
└── extended_research/          # H-K (研究计划，不做理论发布)
```

---

## 版本历史

| 版本 | 日期 | 状态 | 内容 |
|------|------|------|------|
| v2.1.0 | 2月9日 | ✅ 有效 | 5篇论文，T1-T10 + A-G 基础 |
| **v3.0.0-core** | **2月11日** | **✅ 当前** | **仅T1-T4严格核心** |
| v3.0.0 | 2月10日 | ❌ **已撤销** | 关于桥梁的虚假声明 |

---

## 研究状态

**已完成 (L1/L2)**：
- ✅ T1: Cantor逼近理论
- ✅ T2: Master方程框架
- ✅ T3: 凸性分析
- ✅ T4: 谱几何

**进行中 (研究计划)**：
- 🟡 H-K: 扩展方向 (需要达到L1/L2)
- 🟡 三座桥: 研究假说 (需要严格证明或证伪)

---

## 引用

```bibtex
@misc{dimensionics2026core,
  title={Dimensionics: Mathematical Core (T1-T4)},
  year={2026},
  version={3.0.0-core},
  doi={10.5281/zenodo.18511249},
  url={https://github.com/dpsnet/Fixed-4D-Topology}
}
```

---

**标准**: 仅包含完整数学证明的内容 (L1/L2)。
