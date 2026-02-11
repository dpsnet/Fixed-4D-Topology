# Kleinian群与算术分形 - 详细研究计划

## 研究目标

建立算术Kleinian群极限集维数与四元代数模形式L-函数的严格联系。

**核心假设**：
$$\dim_H(\Lambda_G) = 1 + \frac{L(\pi_G, 1/2)}{L(\pi_G, 3/2)} + O(\delta)$$

其中$G$是算术Kleinian群，$\pi_G$是相关联的四元代数模形式。

---

## 第一阶段：基础构建（第1-3个月）

### Week 1-4: 双曲3空间与Kleinian群基础

#### 学习目标
- [ ] 掌握双曲3空间$\mathbb{H}^3$的多种模型
- [ ] 理解PSL(2, **C**)作为等距群的作用
- [ ] 学习极限集的定义和基本性质

#### 关键概念清单
1. **上半空间模型**：$\mathbb{H}^3 = \{(z, t) : z \in \mathbb{C}, t > 0\}$
   - 度量：$ds^2 = (|dz|^2 + dt^2)/t^2$
   
2. **球模型**：$\mathbb{H}^3$作为单位球内部
   
3. **等距群作用**：
   $$\begin{pmatrix} a & b \\ c & d \end{pmatrix} \cdot (z, t) = \frac{(a(z,t) + b, t)}{(c(z,t) + d, t)}$$
   
4. **极限集**：$\Lambda(G) = \overline{G \cdot x} \cap \partial \mathbb{H}^3$

#### 阅读材料
- [ ] Beardon "The Geometry of Discrete Groups", Chapters 1-4
- [ ] Maskit "Kleinian Groups", Chapter 1-2
- [ ] 笔记：docs/research/kleinian_arithmetic/notes/week1-4_hyperbolic_geometry.md

#### 里程碑检查
- [ ] 能计算简单等距变换的极限集
- [ ] 理解Schottky群的构造

---

### Week 5-8: Kleinian群结构与离散性

#### 学习目标
- [ ] Poincaré多面体定理
- [ ] 几何有限性
- [ ] 极限集的拓扑结构

#### 关键概念
1. **离散群**：在$\mathbb{H}^3$上真不连续作用
2. **基本域**：Poincaré多面体
3. **几何有限性**：
   - 凸包体积有限
   - 极限集结构控制
4. **极限集性质**：紧致、完美、无处稠密（对非初等群）

#### 计算实验
- [ ] 使用SnapPy计算基本域
- [ ] 可视化简单Kleinian群的极限集

```python
# 示例代码框架
import snappy

# 创建三角群
M = snappy.Manifold('m004')  # 八字结补空间
print(M.volume())
print(M.symmetry_group())
```

#### 阅读材料
- [ ] Maskit, Chapter 3-4
- [ ] Mumford et al. "Indra's Pearls", 前三章

---

### Week 9-12: 四元代数与算术Kleinian群

#### 学习目标
- [ ] 四元代数基础
- [ ] 算术群的定义
- [ ] 不变量迹域

#### 关键概念
1. **四元代数**：$B = \mathbb{Q} + \mathbb{Q}i + \mathbb{Q}j + \mathbb{Q}k$
   - $i^2 = a, j^2 = b, ij = -ji = k$
   
2. **算术群**：
   - 四元代数整数环的单位群
   - 嵌入到PSL(2, **C**)
   
3. **不变量迹域**：$k(G) = \mathbb{Q}(\{\text{tr}^2(g) : g \in G\})$

#### 具体例子
1. **Bianchi群**：PSL(2, $O_d$)，$O_d$是虚二次域的整数环
2. **Hurwitz群**：与四元数整数相关的群

#### 阅读材料
- [ ] Maclachlan-Reid "The Arithmetic of Hyperbolic 3-Manifolds", Chapters 1-3

#### 里程碑
- [ ] 能识别给定群是否为算术群
- [ ] 计算简单算术群的不变量迹域

---

## 第二阶段：维数计算与实验（第4-6个月）

### Month 4: 选择具体群

#### 候选群列表

**群1: 白群 (Whitehead Link Complement)**
- 名称：W
- 性质：算术群，双曲体积已知
- SnapPy: `M = snappy.Manifold('m003')`

**群2: 八字结补空间 (Figure-8 Knot Complement)**
- 名称：m004
- 性质：最经典的双曲3流形
- SnapPy: `M = snappy.Manifold('m004')`

**群3: Bianchi群 PSL(2, Z[i])**
- 名称：Bi
- 性质：与Q(i)相关
- 极限集：整个复平面（需要更精细的构造）

#### 计算任务
- [ ] 使用SnapPy获取每个群的基本数据
- [ ] 计算极限集的数值逼近
- [ ] 估计Hausdorff维数

### Month 5: Hausdorff维数算法

#### 算法1: 盒维数（数值估计）

```python
def box_dimension(limit_set_points, epsilons):
    """
    计算盒维数
    limit_set_points: 极限集上的点集
    epsilons: 不同尺度的列表
    """
    dimensions = []
    for eps in epsilons:
        # 用边长为eps的盒子覆盖
        N = count_boxes_needed(limit_set_points, eps)
        dimensions.append(-np.log(N) / np.log(eps))
    return dimensions
```

#### 算法2: 压力函数方法（McMullen）

**热力学形式**:
- 压力：$P(s) = \lim_{n\to\infty} \frac{1}{n} \log \sum_{|g|=n} |g'(x)|^s$
- 维数：$\dim_H(\Lambda) = \inf\{s : P(s) < 0\}$

#### 计算任务
- [ ] 实现盒维数算法
- [ ] 使用已知软件（如Indra）验证
- [ ] 记录数值结果

### Month 6: 模形式关联

#### 四元代数模形式

**设置**:
- 给定Kleinian群$G$
- 找到关联的四元代数$B_G$
- 构造模形式空间

**L-函数计算**:
- [ ] 使用SageMath/PARI计算四元代数L-函数
- [ ] 计算特殊值$L(\pi, 1/2)$和$L(\pi, 3/2)$
- [ ] 比较维数与L值比值

```python
# SageMath示例
from sage.lfunctions.lcalc import lcalc

# 计算L-函数值
L = lcalc.create_from_data(...)  # 四元代数模形式数据
value_at_half = L.value(0.5)
value_at_three_half = L.value(1.5)
ratio = value_at_half / value_at_three_half
```

#### 里程碑
- [ ] 至少3个群的完整数据：(群, 维数, L值)
- [ ] 验证假设公式的准确性

---

## 第三阶段：理论探索（第7-12个月）

### Month 7-9: 已有结果调研

#### McMullen的维数公式

**热力学形式框架**:
- Poincaré级数
- 压力函数
- Gibbs测度

**Bowen公式**: 对于几何有限Kleinian群，
$$\dim_H(\Lambda) = \inf\{s > 0 : P(s) = 0\}$$

#### Patterson-Sullivan测度

**构造**:
- 与极限集相关的共形测度
- 谱性质与维数的联系

#### 四元代数L-函数

**性质**:
- 函数方程
- 解析延拓
- 特殊值

### Month 10-12: 理论构建

#### 尝试证明

**策略1: 通过Patterson-Sullivan测度**
- 如果测度的谱可以表示为L-函数
- 则维数可能与L值相关

**策略2: 通过迹公式**
- Selberg迹公式在双曲3空间
- 与四元代数迹公式的联系

**策略3: 通过Motives**（如果适用）
- 算术Kleinian群可能有motive解释
- L-函数是motive的实ization

#### 可能的障碍

1. **技术障碍**: 压力函数方法可能无法直接给出L-函数
2. **概念障碍**: 维数是几何量，L-函数是算术量，联系可能不直接
3. **反例存在**: 某些群的维数可能不满足公式

#### 里程碑
- [ ] 完整的理论框架，或
- [ ] 明确的障碍分析报告

---

## 论文大纲

### 目标期刊
- **首选**: Journal of Number Theory, Geometriae Dedicata
- **备选**: Experimental Mathematics, International Journal of Number Theory

### 论文结构

```
Title: Arithmetic Kleinian Groups and Fractal Dimensions: 
       A Computational and Theoretical Study

Abstract:
We investigate the relationship between the Hausdorff dimension of limit sets 
of arithmetic Kleinian groups and special values of quaternionic L-functions. 
For a sample of arithmetic Kleinian groups, we compute both the limit set 
dimension using thermodynamic formalism and the associated L-values using 
automorphic methods. We find evidence for/contradict to a formula relating 
these quantities and discuss the theoretical implications.

1. Introduction
   1.1 Kleinian groups and their limit sets
   1.2 Arithmetic Kleinian groups and quaternion algebras
   1.3 The dimension-L-value hypothesis
   1.4 Related work (McMullen, etc.)

2. Background
   2.1 Hyperbolic 3-space and Kleinian groups
   2.2 Thermodynamic formalism for limit sets
   2.3 Quaternionic automorphic forms
   2.4 L-functions

3. Computational Methods
   3.1 Numerical computation of Hausdorff dimension
   3.2 Computation of L-functions
   3.3 Software and algorithms

4. Results
   4.1 Data for specific groups
   4.2 Comparison with hypothesis
   4.3 Error analysis

5. Theoretical Discussion
   5.1 Why the formula might hold
   5.2 Obstacles to a general proof
   5.3 Connections to other areas

6. Conclusion and Future Work
```

---

## 风险与应对

### 风险1: 公式不成立
**应对**: 
- 记录详细的负面结果
- 分析为何某些群满足而某些不满足
- 发表负面结果也是有价值的

### 风险2: 计算困难
**应对**:
- 从更简单的情况开始（如Fuchsian群，即双曲2维）
- 使用已有的计算工具和数据库
- 寻求与计算数论专家的合作

### 风险3: 理论超出当前能力
**应对**:
- 专注于计算和数值证据
- 与算术几何专家合作
- 将理论问题留给后续研究

---

## 每周检查清单模板

```markdown
## Week X: [日期范围]

### 完成的工作
- [ ] 项目1
- [ ] 项目2

### 遇到的问题
- 问题描述
- 可能的解决方案

### 下周计划
- [ ] 任务1
- [ ] 任务2

### 关键发现
- 任何重要的观察或想法

### 时间投入
- 本周总时间: X小时
- 与计划对比: 符合/超前/落后
```

---

**开始日期**: [填写开始日期]
**预计完成**: 12个月后
**负责人**: [填写负责人]
**状态**: 🟡 计划中
