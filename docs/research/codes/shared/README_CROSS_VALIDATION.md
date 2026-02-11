# L2严格性交叉验证和误差分析系统

## 简介

本系统为Fixed-4D-Topology框架提供全面的统计验证支持，以满足L2严格性级别要求。系统实现了多种交叉验证方法、误差分析技术和统计检验。

## 文件结构

```
Fixed-4D-Topology/docs/research/codes/shared/
├── cross_validation_analysis.py       # 主分析脚本
├── generate_validation_figures.py     # 可视化脚本
├── cross_validation_report.md         # 详细分析报告
├── README_CROSS_VALIDATION.md         # 本文件
└── cross_validation_results/          # 结果目录
    ├── kleinian_cross_validation_results.json
    ├── padic_cross_validation_results.json
    ├── cross_validation_summary.json
    └── figures/                       # 可视化图表
        ├── cross_validation_comparison.png
        ├── bootstrap_analysis.png
        ├── error_analysis.png
        ├── statistical_tests.png
        ├── padic_validation.png
        └── l2_validation_summary.png
```

## 使用方法

### 1. 运行交叉验证分析

```bash
cd Fixed-4D-Topology/docs/research/codes/shared
python3 cross_validation_analysis.py
```

这将：
- 对Kleinian群数据进行K折交叉验证（K=5,10）和留一法验证
- 计算Bootstrap置信区间
- 进行误差分析（系统误差、随机误差、误差传播）
- 执行统计检验（正态性、异方差性、拟合优度）
- 进行模型选择（AIC、BIC）
- 执行敏感性分析

### 2. 生成可视化图表

```bash
python3 generate_validation_figures.py
```

这将生成6个可视化图表，展示分析结果。

## 主要功能

### 交叉验证模块

| 方法 | 描述 | 适用场景 |
|------|------|----------|
| K-Fold CV | K折交叉验证 | 中等样本量 |
| LOO CV | 留一法交叉验证 | 小样本量 |
| Bootstrap | 自助法置信区间 | 任意样本量 |

### 误差分析模块

- **系统误差估计**：使用Jackknife方法
- **随机误差估计**：标准差、标准误差、变异系数、MAD
- **误差传播**：基于偏导数的误差合成
- **异常值检测**：IQR、Z-score、Grubbs检验

### 统计检验模块

- **正态性检验**：Shapiro-Wilk、D'Agostino、Anderson-Darling、Jarque-Bera
- **异方差性检验**：Breusch-Pagan、White检验
- **拟合优度检验**：Kolmogorov-Smirnov、Anderson-Darling
- **模型选择**：AIC、AICc、BIC、AIC权重

### 敏感性分析模块

- **参数敏感性**：计算敏感性系数和弹性
- **初始条件敏感性**：评估算法稳定性
- **算法选择敏感性**：比较不同算法的一致性

## 结果解读

### Kleinian群验证结果

| 指标 | 值 | 说明 |
|------|-----|------|
| 样本数 | 42 | Bianchi群、Schottky群等 |
| 维数均值 | 1.389 | 包含置信区间 |
| 95% CI | [1.285, 1.497] | Bootstrap百分位法 |
| 系统偏差 | < 0.001 | 几乎无偏 |
| 变异系数 | 25.98% | 中等变异 |

### p-adic验证结果

| 指标 | 值 | 说明 |
|------|-----|------|
| 样本数 | 5 | p=2,3,5; d=2,3,4,5,9 |
| 维数 | 1.000 | 与理论预测一致 |
| 数值误差 | < 1e-15 | float64精度 |
| 系统偏差 | 0.000 | 精确解 |

## L2严格性满足情况

| 要求 | 状态 | 证据 |
|------|------|------|
| K折交叉验证 | ✓ | K=5,10结果一致 |
| 留一法验证 | ✓ | LOO CV完成 |
| Bootstrap CI | ✓ | 10,000次重采样 |
| 系统误差估计 | ✓ | Jackknife估计 |
| 随机误差估计 | ✓ | 完整误差统计 |
| 误差传播分析 | ✓ | 合成不确定度 |
| 异常值检测 | ✓ | Grubbs检验 |
| 正态性检验 | ✓ | 4种检验方法 |
| 异方差性检验 | ✓ | BP检验通过 |
| 模型选择 | ✓ | AIC/BIC比较 |
| 敏感性分析 | ✓ | 参数/初始条件/算法 |

## 技术细节

### 依赖包

```
numpy >= 1.20.0
scipy >= 1.7.0
matplotlib >= 3.4.0
```

### 关键算法

1. **Bootstrap BCa区间**  
   实现偏差校正和加速的Bootstrap置信区间

2. **Grubbs异常值检验**  
   迭代检测最大离差值

3. **误差传播**  
   数值微分计算偏导数

4. **模型选择**  
   AIC权重计算和Delta方法

## 引用

如果您使用本分析系统，请引用：

```
Fixed-4D-Topology Research Group. (2026). 
Cross-Validation and Error Analysis System for L2 Rigorousness. 
Technical Report, Version 1.0.0-L2.
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-02-11 | 初始版本，完成L2严格性验证 |

## 联系信息

Fixed-4D-Topology Research Group  
项目主页: https://github.com/Fixed-4D-Topology

---

*最后更新: 2026-02-11*
