# K方向: 机器学习维度
## K Direction: Machine Learning Dimension

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.10+-red.svg)](https://pytorch.org/)

**基于Fisher信息的神经网络有效维度理论框架**

---

## 🎯 核心思想

神经网络的有效维度(effective dimension) $d_{\text{eff}}$ 衡量模型的"真实"复杂度，远小于参数数量 $D$。本框架提供：

- **严格数学定义**: 基于Fisher信息矩阵
- **动态演化方程**: 描述训练过程中的维度变化
- **泛化误差界**: $O(\sqrt{d_{\text{eff}}/n})$ 样本复杂度
- **Dimensionics统一**: 与物理维度理论的跨学科连接

---

## 📁 项目结构

```
K_machine_learning_dimension/
├── theory/                          # 理论文档
│   ├── K1.1_Fisher_Information.md   # Fisher信息基础
│   ├── K1.2_Effective_Dimension.md  # 有效维度定义
│   ├── K1.3_Training_Dynamics.md    # 训练动态方程
│   ├── K1.4_Generalization_Bounds.md # 泛化界证明
│   ├── K1.5_Dimensionics_Connection.md # Dimensionics连接
│   └── K_DIRECTION_PAPER.md         # 整合论文框架
│
├── code/                            # Python工具包
│   ├── neural_dimension/            # 主包
│   │   ├── core/                    # 核心模块
│   │   │   ├── fisher_information.py
│   │   │   ├── effective_dimension.py
│   │   │   └── dimension_dynamics.py
│   │   ├── models/                  # 模型架构
│   │   │   ├── standard_architectures.py
│   │   │   └── lottery_ticket.py
│   │   ├── visualization/           # 可视化
│   │   │   └── dimension_plots.py
│   │   └── experiments/             # 实验实现
│   │       ├── double_descent.py
│   │       └── neural_collapse.py
│   └── setup.py                     # 安装配置
│
├── experiments/                     # 实验脚本
│   ├── protocols/                   # 实验协议
│   │   └── EXPERIMENTS_PROTOCOL.md
│   └── scripts/                     # 可运行脚本
│       ├── E1_effective_dim_baseline.py
│       ├── E2_training_dynamics.py
│       ├── E3_double_descent.py
│       ├── E4_neural_collapse.py
│       ├── E5_lottery_ticket.py
│       └── E6_generalization_bound.py
│
├── integration/                     # 跨方向连接
│   ├── KH_QUANTUM_NN.md             # K-H连接
│   ├── KI_NETWORK_NN.md             # K-I连接
│   ├── KJ_RANDOM_INIT.md            # K-J连接
│   ├── K_CROSS_DIRECTION_FRAMEWORK.md # 统一框架
│   └── JOINT_EXPERIMENTS.md         # 联合实验设计
│
├── notebooks/                       # Jupyter演示
│   └── (待创建)
│
├── tests/                           # 单元测试
│   └── (待创建)
│
├── PLAN.md                          # 并行开发计划
├── PROGRESS.md                      # 进度追踪
└── README.md                        # 本文件
```

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
cd Fixed-4D-Topology/extended_research/K_machine_learning_dimension

# 安装包
pip install code/

# 或开发模式
pip install -e code/
```

### 基础用法

```python
import torch
from neural_dimension import FisherInformationMatrix, EffectiveDimensionCalculator
from neural_dimension.models import TwoLayerMLP

# 创建模型
model = TwoLayerMLP(hidden_dim=128)

# 准备数据
train_loader = ...  # PyTorch DataLoader

# 计算Fisher信息矩阵
fisher_calc = FisherInformationMatrix(model, sigma=1.0)
fisher_matrix = fisher_calc.compute_diagonal_fisher(train_loader)

# 计算有效维度
dim_calc = EffectiveDimensionCalculator(fisher_calc)
dimensions = dim_calc.compute_all_dimensions(n_samples=1000)

print(f"有效维度: {dimensions['fisher_effective_dimension']:.2f}")
print(f"总参数: {dimensions['total_parameters']}")
print(f"维度压缩比: {dimensions['reduction_ratio']:.4f}")
```

### 运行实验

```bash
# E1: 有效维度基准测量
python experiments/scripts/E1_effective_dim_baseline.py

# E2: 训练动态追踪
python experiments/scripts/E2_training_dynamics.py

# E3: 双下降验证
python experiments/scripts/E3_double_descent.py

# E4: 神经崩塌分析
python experiments/scripts/E4_neural_collapse.py

# E5: 彩票票假设
python experiments/scripts/E5_lottery_ticket.py

# E6: 泛化界验证
python experiments/scripts/E6_generalization_bound.py
```

---

## 📊 核心理论

### 有效维度定义

基于Fisher信息矩阵 $F$:

$$d_{\text{eff}} = \frac{(\text{tr} F)^2}{\text{tr}(F^2)} = \frac{(\sum_i \lambda_i)^2}{\sum_i \lambda_i^2}$$

### 关键性质

- **范围**: $1 \leq d_{\text{eff}} \leq D$ (总参数)
- **尺度不变性**: 对 $F$ 的缩放不变
- **单调性**: $F_1 \preceq F_2 \Rightarrow d_{\text{eff}}^{(1)} \leq d_{\text{eff}}^{(2)}$

### 泛化界

以高概率:

$$R \leq \hat{R} + \mathcal{O}\left(\sqrt{\frac{d_{\text{eff}} \ln(n/d_{\text{eff}})}{n}}\right)$$

### 维度演化方程

$$\frac{\partial d_{\text{eff}}}{\partial t} = \alpha \mathcal{L}(d_{\text{data}} - d_{\text{eff}}) - \beta d_{\text{eff}} R$$

---

## 🔬 实验概览

| 实验 | 目标 | 关键结果 |
|------|------|----------|
| **E1** | 基准测量 | 不同架构的 $d_{\text{eff}}$ 比较 |
| **E2** | 训练动态 | $d_{\text{eff}}(t)$ 演化曲线 |
| **E3** | 双下降 | 维度解释的双下降验证 |
| **E4** | 神经崩塌 | NC1/NC2/NC3 与维度关系 |
| **E5** | 彩票票 | 获胜票券的维度特性 |
| **E6** | 泛化界 | 理论界的经验验证 |

---

## 🔗 跨方向连接

K方向与以下方向建立连接:

- **H方向 (量子维度)**: 量子神经网络的有效维度
- **I方向 (网络几何)**: 神经网络作为复杂网络
- **J方向 (随机分形)**: 渗流理论与初始化

详见 `integration/` 目录。

---

## 📖 文档

- **理论**: 见 `theory/` 目录
- **实验协议**: 见 `experiments/protocols/`
- **API文档**: (待生成)

---

## 🙏 致谢

### 研究起源

K方向（机器学习维度）是 **Fixed-4D-Topology统一框架** 的扩展研究，
由同一研究者发起。该方向将维度理论从物理-数学领域扩展到机器学习领域，
形成K-H-I-J跨方向研究体系的一部分。

**研究演进** (根据Git提交历史):
- **2026-01-27**: 基础框架建立 (Fundamental-Mathematics, Physical-Applications等)
- **2026-02-03**: 扩展框架建立 (Advanced-Physics-Framework, Computational-Framework等)
- **2026-02-07**: Fixed-4D-Topology v1.0.0发布，A~G方向深度研究启动
- **2026-02-07**: H-J扩展研究启动 (量子维度、网络几何、随机分形)
- **2026-02-09**: **K方向启动**: 机器学习维度理论

### 方法论

- **人类研究员**: 研究愿景、概念指导、质量把控
- **Kimi 2.5 Agent**: 数学推导、代码实现、文档编写
- 采用人机协作范式，诚实披露AI贡献

---

## 🤝 贡献

欢迎贡献！请查看主仓库的 CONTRIBUTING.md。

---

## 📄 引用

```bibtex
@article{k_direction_2026,
  title={Neural Network Effective Dimension: A Dimensionics Framework},
  author={Human Researcher and Kimi 2.5 Agent},
  year={2026},
  url={https://github.com/dpsnet/Fixed-4D-Topology}
}
```

---

## 📝 许可证

MIT License - 见主仓库 LICENSE 文件。

---

**研究方法论**: 本研究采用人机协作范式。Kimi 2.5 Agent 生成所有内容，人类提供方向指导。

**状态**: 开发阶段基本完成，进入实验验证阶段。

**最后更新**: 2026-02-09
