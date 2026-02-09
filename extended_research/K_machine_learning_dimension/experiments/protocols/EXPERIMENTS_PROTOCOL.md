# K方向实验协议
## K Direction Experiments Protocol

**版本**: 1.0  
**制定日期**: 2026-02-09  
**目标**: 验证K方向理论的可复现实验

---

## 1. 实验哲学

### 可复现性保证
- 所有实验使用**固定随机种子**
- 完整的超参数记录
- 代码版本控制
- 原始结果存档

### 严格性等级
- **L1**: 严格控制的基准实验
- **L2**: 统计显著性验证
- **L3**: 探索性实验

---

## 2. 实验矩阵

### E1: 有效维度基准测量

**目标**: 测量标准架构的有效维度

**模型**: 
- MLP: [784-128-64-10] (MNIST)
- CNN: Conv[32-64] + FC[128-10] (CIFAR-10)
- ResNet-18 (CIFAR-10)

**数据集**: MNIST, CIFAR-10

**超参数**:
```yaml
batch_size: 128
epochs: 100
optimizer: SGD
learning_rate: 0.01
momentum: 0.9
weight_decay: 5e-4
random_seed: 42
```

**测量指标**:
- Fisher有效维度
- 参与比
- 条件数
- 特征值谱

**输出**: `results/effective_dim/`

---

### E2: 训练动态追踪

**目标**: 追踪 $d_{\text{eff}}$ 在训练过程中的演化

**设置**:
- 每epoch测量一次 $d_{\text{eff}}$
- 记录损失、准确率、学习率
- 检查点保存

**分析**:
- 早期阶段: $d_{\text{eff}}$ 增长
- 中期阶段: 平台期
- 晚期阶段: 可能下降

**输出**: `results/training_dynamics/`

---

### E3: 双下降验证

**目标**: 验证维度解释的双下降现象

**设置**:
- 固定数据量 $N$
- 变化模型参数量 $D$
- 测量 $d_{\text{eff}}$ 和泛化误差

**预期结果**:
- 欠参数化: $d_{\text{eff}} < d_{\text{data}}$ → 欠拟合
- 插值阈值: 误差峰值
- 过参数化: $d_{\text{eff}} > d_{\text{data}}$ + 正则化 → 良好拟合

**输出**: `results/double_descent/`

---

### E4: 神经崩塌分析

**目标**: 验证神经崩塌的维度解释

**设置**:
- 深度MLP
- 合成数据 (K类)

**测量**:
- NC1 (类内协方差)
- NC2 (类间对齐)
- $d_{\text{eff}}$ vs 类别数K

**假设**: $d_{\text{eff}} \approx K-1$ 时最优

**输出**: `results/neural_collapse/`

---

### E5: 彩票票假设

**目标**: 验证获胜票券的最优维度

**设置**:
- VGG-19 on CIFAR-10
- 迭代幅度剪枝 (IMP)
- 稀疏率: [0%, 20%, 50%, 80%, 95%]

**比较**:
- 获胜票券: $d_{\text{eff}}^{\text{win}}$
- 随机票券: $d_{\text{eff}}^{\text{rand}}$

**假设**: $d_{\text{eff}}^{\text{win}}$ 更接近最优

**输出**: `results/lottery_ticket/`

---

### E6: 泛化界验证

**目标**: 验证基于维度的泛化误差上界

**设置**:
- 不同训练集大小 $N$
- 固定架构

**验证**:
$$
|R - \hat{R}| \lesssim \sqrt{\frac{d_{\text{eff}}}{N}}
$$

**输出**: `results/generalization/`

---

## 3. 实验模板

### Python模板

```python
"""
Experiment Template for K Direction
"""

import torch
import numpy as np
from neural_dimension import FisherInformationMatrix, EffectiveDimensionCalculator

# 1. Set random seed
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# 2. Load model and data
model = load_model()
train_loader, test_loader = load_data()

# 3. Compute Fisher Information
fisher_calc = FisherInformationMatrix(model, sigma=1.0)
fisher_matrix = fisher_calc.compute_diagonal_fisher(train_loader)

# 4. Compute effective dimension
dim_calc = EffectiveDimensionCalculator(fisher_calc)
dimensions = dim_calc.compute_all_dimensions(n_samples=len(train_loader.dataset))

# 5. Save results
save_results(dimensions, path=f"results/experiment_name/seed_{SEED}.json")
```

---

## 4. 评估标准

### 通过标准

| 实验 | 通过标准 | 严格性 |
|------|---------|--------|
| E1 | 成功测量所有模型 $d_{\text{eff}}$ | L1 |
| E2 | 训练曲线平滑，趋势符合预期 | L1 |
| E3 | 双下降曲线与维度解释一致 | L2 |
| E4 | NC1/NC2与$d_{\text{eff}}$相关 | L2 |
| E5 | 获胜票券$d_{\text{eff}}$显著不同 | L2 |
| E6 | 泛化误差与理论界趋势一致 | L3 |

---

## 5. 报告格式

每个实验输出:
- `config.yaml`: 实验配置
- `results.json`: 数值结果
- `plots/`: 可视化
- `model_checkpoints/`: 模型检查点 (可选)
- `README.md`: 实验摘要

---

## 6. 时间线

| 天数 | 实验 | 依赖 |
|------|------|------|
| 1-2 | E1 | 代码路线 C2 |
| 3 | E2 | 代码路线 C3 |
| 4 | E3 | E1, E2 |
| 5 | E4 | E1 |
| 6 | E5 | E1 |
| 7 | E6 | E1, E2 |
| 8 | 整合报告 | 全部 |

---

**协议制定**: Kimi 2.5 Agent  
**审查**: 待人类确认
