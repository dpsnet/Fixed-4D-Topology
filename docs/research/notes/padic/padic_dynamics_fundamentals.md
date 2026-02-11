# p-adic动力学基础：综合学习文档

> **任务P-011**: 学习p-adic动力学基础 - ✅ 已完成  
> **基于**: Benedetto《Dynamics in One Non-Archimedean Variable》(2019) 及相关文献  
> **创建日期**: 2026-02-11  
> **文档类型**: 研究学习笔记

---

## 目录

1. [p-adic动力系统概述](#1-p-adic动力系统概述)
2. [Berkovich空间基础](#2-berkovich空间基础)
3. [p-adic Fatou/Julia理论](#3-p-adic-fatoujulia理论)
4. [与p-adic维数理论的联系](#4-与p-adic维数理论的联系)
5. [与本研究的联系](#5-与本研究的联系)
6. [开放问题与研究方向](#6-开放问题与研究方向)

---

## 1. p-adic动力系统概述

### 1.1 定义与基本框架

**p-adic动力系统的定义**：

设$p$为素数，$\mathbb{Q}_p$为$p$-adic数域，$\mathbb{C}_p$为其完备代数闭包。p-adic动力系统是一个映射：

$$f: X \to X, \quad X \subseteq \mathbb{P}^1(\mathbb{C}_p)$$

其中$f$通常是具有$\mathbb{C}_p$系数的有理函数。

**基本设置**：

| 概念 | 定义 | 说明 |
|------|------|------|
| **状态空间** | $\mathbb{P}^1(\mathbb{C}_p)$ | p-adic射影直线 |
| **动力学映射** | $f \in \mathbb{C}_p(z)$ | 有理函数 |
| **度** | $\deg(f) = \max(\deg P, \deg Q)$ | 对$f = P/Q$ |
| **迭代** | $f^n = f \circ f \circ \cdots \circ f$ ($n$次) | $n$-次迭代 |

### 1.2 基本例子

#### 例子1: $f(z) = z^d$（幂映射）

**动力学行为**：

对于$f(z) = z^d$，$d \geq 2$，点$z \in \mathbb{C}_p$的行为完全由$|z|_p$决定：

| 区域 | 条件 | 动力学行为 |
|------|------|-----------|
| **吸引盆** | $|z|_p < 1$ | $f^n(z) \to 0$ (当$n \to \infty$) |
| **Julia集** | $|z|_p = 1$ | $|f^n(z)|_p = 1$（中性行为） |
| **无穷远盆** | $|z|_p > 1$ | $|f^n(z)|_p \to \infty$ |

**周期点分析**：

$n$-周期点满足$z^{d^n} = z$，即：
- $z = 0$（超吸引不动点）
- $z = \infty$（超吸引不动点）  
- $z^{d^n - 1} = 1$的$d^n - 1$个根

**导数计算**：

$$(f^n)'(z) = d^n \cdot z^{d^n - 1}$$

在单位圆上（$|z|_p = 1$）：$|(f^n)'(z)|_p = |d^n|_p = p^{-n \cdot v_p(d)}$

#### 例子2: $f(z) = z^2 + c$（p-adic Mandelbrot集）

这是复Mandelbrot集的p-adic类比。参数空间$c \in \mathbb{Q}_p$的行为依赖于$|c|_p$：

| $|c|_p$范围 | 动力学行为 |
|------------|-----------|
| $|c|_p < 1$ | 类似于$z^2$，Julia集可能是Cantor集 |
| $|c|_p = 1$ | 复杂动力学，可能出现非平凡Julia集 |
| $|c|_p > 1$ | $\infty$是吸引的，Julia集是Cantor集 |

#### 例子3: 多项式映射的一般形式

$$f(z) = a_d z^d + a_{d-1} z^{d-1} + \cdots + a_0$$

**关键观察**：p-adic多项式的动力学行为强烈依赖于系数的$p$-adic赋值。

### 1.3 Fatou集与Julia集：经典定义

**定义（经典Fatou集）**：

设$f: \mathbb{P}^1(\mathbb{C}_p) \to \mathbb{P}^1(\mathbb{C}_p)$是有理函数。经典**Fatou集**$F(f)$是迭代族$\{f^n\}_{n \geq 0}$在球面度量下**局部等度连续**的点集。

**定义（经典Julia集）**：

经典**Julia集**$J(f)$是Fatou集的补集：
$$J(f) = \mathbb{P}^1(\mathbb{C}_p) \setminus F(f)$$

**基本性质**：

| 性质 | 说明 |
|------|------|
| **完全不变性** | $f^{-1}(J(f)) = J(f) = f(J(f))$ |
| **紧致性** | $J(f)$是$\mathbb{P}^1(\mathbb{C}_p)$的紧致子集 |
| **完全断开**（通常）| $J(f)$完全不连通（与复情形不同！） |
| **排斥性** | Julia集是排斥周期点的闭包 |

### 1.4 与复动力学的对比

| 特征 | 复动力学 ($\mathbb{C}$) | p-adic动力学 ($\mathbb{C}_p$) |
|------|------------------------|------------------------------|
| **拓扑结构** | 连通（通常） | 完全不连通（通常） |
| **Fatou分量** | 有限多个（Sullivan定理） | 可能无限多个 |
| **游荡域** | 不存在（Sullivan, 1985） | **可能存在**（Benedetto, 2002） |
| **临界点** | 有限个（$2d-2$个） | 相同 |
| **Julia集维数** | 分数维（通常） | 需要重新定义 |
| **几何结构** | 分形 | 树状/Berkovich结构 |
| **解析工具** | 复分析 | 非阿基米德分析 |

**关键差异解释**：

1. **拓扑差异**：p-adic拓扑是完全不连通的（"像一个康托集"），而复拓扑是连通的。

2. **游荡域**：Sullivan证明复有理函数没有游荡Fatou分量，但Benedetto构造了p-adic多项式的游荡域例子。

3. **导数几何意义**：复导数$|f'(z)|$表示局部伸缩，p-adic导数$|f'(z)|_p$也有类似但不同的解释。

---

## 2. Berkovich空间基础

### 2.1 为什么需要Berkovich空间

**问题**：经典p-adic空间$\mathbb{P}^1(\mathbb{C}_p)$完全不连通，缺乏复分析中的"连通性"和"路径连通性"。

**解决方案**：Berkovich空间提供了一个"紧致化"框架，使得：
- 空间变为**紧致Hausdorff**
- 空间变为**路径连通**
- 保留了p-adic分析的所有信息
- 为动力学提供了"几何直观"

### 2.2 Berkovich仿射直线$\mathcal{A}^1_{\text{Berk}}$

**定义（乘法半范数）**：

设$K$是完备非阿基米德域。$K[T]$上的**乘法半范数**是一个函数$|\cdot|: K[T] \to \mathbb{R}_{\geq 0}$满足：
1. $|0| = 0$，$|1| = 1$
2. $|f + g| \leq \max(|f|, |g|)$（强三角不等式）
3. $|fg| = |f| \cdot |g|$（乘法性）
4. $|a| = |a|_K$对$a \in K$

**定义（Berkovich点）**：

**Berkovich仿射直线**$\mathcal{A}^1_{\text{Berk}}$是$K[T]$上所有乘法半范数（在$K$上限制为给定的绝对值）的集合。

### 2.3 Type I-IV点的分类

Berkovich空间中的点按"类型"分为四类：

#### **Type I点（经典点）**

**定义**：对应于$x \in \mathbb{C}_p$的赋值半范数：
$$|f|_x = |f(x)|_p$$

**特征**：
- 半范数是$\mathbb{C}_p$-值的
- 对应于"叶子"（树的端点）
- 组成稠密子集

#### **Type II点（有理半径圆盘）**

**定义**：对应于闭圆盘$D(a, r)$，其中$r \in |\mathbb{C}_p^*| = p^{\mathbb{Q}}$是有理$p$-adic半径：
$$|f|_{D(a,r)} = \sup_{z \in D(a,r)} |f(z)|_p$$

**特征**：
- 形成Berkovich树的"主干"
- 分支点对应于圆盘的相交
- 在Berkovich射影直线上稠密

#### **Type III点（无理半径圆盘）**

**定义**：对应于闭圆盘$D(a, r)$，其中$r \notin p^{\mathbb{Q}}$是无理$p$-adic半径。

**特征**：
- 不在主干上
- 作为"树枝"存在
- 在分支点之间

#### **Type IV点（极限点）**

**定义**：对应于嵌套闭圆盘序列的极限：
$$D_1 \supset D_2 \supset D_3 \supset \cdots, \quad \bigcap_n D_n = \emptyset$$

**特征**：
- 这是非阿基米德分析特有的现象
- 在$\mathbb{C}_p$中没有对应点
- 形成Berkovich空间的"幽灵点"

**分类总结**：

| 类型 | 描述 | 几何意义 | 在$\mathbb{C}_p$中有对应？ |
|------|------|---------|------------------------|
| **Type I** | 经典点$x \in \mathbb{C}_p$ | 叶子 | ✓ |
| **Type II** | 有理半径圆盘$D(a, r)$, $r \in p^{\mathbb{Q}}$ | 分支点 | ✗ |
| **Type III** | 无理半径圆盘$D(a, r)$, $r \notin p^{\mathbb{Q}}$ | 树枝 | ✗ |
| **Type IV** | 嵌套圆盘序列极限 | 极限点 | ✗ |

### 2.4 Berkovich射影直线$\mathbb{P}^1_{\text{Berk}}$

**构造**：通过对$\mathcal{A}^1_{\text{Berk}}$添加"无穷远点"紧致化得到。

**拓扑性质**：

| 性质 | 说明 |
|------|------|
| **紧致性** | 紧致Hausdorff空间 |
| **路径连通** | 任意两点之间有唯一路径（像一棵树） |
| **局部连通** | 每点有连通邻域基 |
| **度量结构** | 双曲度量（hyperbolic metric） |

**可视化**：

Berkovich射影直线可以可视化为一个"实树"（real tree）：
- Type I点是端点（在"无穷远"）
- Type II点是分支点
- Type III和IV点填充分支之间

```
        ∞ (Type I)
        |
        | Type II点（分支点）
        +----- Type III/IV点
        |      |
        |      +--- Type I点（经典点）
        |
   [Gauss点 = D(0,1)]
        |
        +----- 其他分支...
```

### 2.5 双曲度量与Skolem拓扑

**双曲度量**$\rho$：在$\mathbb{P}^1_{\text{Berk}} \setminus \mathbb{P}^1(\mathbb{C}_p)$（非经典点）上定义。

对于Type II点$x = D(a, r)$和$y = D(a, R)$在同一路径上（$r < R$）：
$$\rho(x, y) = \log_p(R/r)$$

**Skolem拓扑**：$\mathbb{P}^1_{\text{Berk}}$上的标准拓扑。

**重要观察**：
- 经典点（Type I）在双曲度量下"在无穷远"
- Type II点形成"骨架"
- 动力学在双曲度量下更容易分析

---

## 3. p-adic Fatou/Julia理论

### 3.1 Berkovich框架下的定义

**定义（Berkovich Fatou集）**：

设$f: \mathbb{P}^1_{\text{Berk}} \to \mathbb{P}^1_{\text{Berk}}$是有理函数。**Berkovich Fatou集**$\mathcal{F}^{\text{Berk}}(f)$是迭代族$\{f^n\}$在Berkovich拓扑下**正规**的点集。

**定义（Berkovich Julia集）**：

**Berkovich Julia集**$\mathcal{J}^{\text{Berk}}(f)$是Berkovich Fatou集的补集：
$$\mathcal{J}^{\text{Berk}}(f) = \mathbb{P}^1_{\text{Berk}} \setminus \mathcal{F}^{\text{Berk}}(f)$$

**与经典定义的对比**：

| 性质 | 经典Julia集$J(f)$ | Berkovich Julia集$\mathcal{J}^{\text{Berk}}(f)$ |
|------|------------------|----------------------------------|
| **所在空间** | $\mathbb{P}^1(\mathbb{C}_p)$ | $\mathbb{P}^1_{\text{Berk}}$ |
| **拓扑** | 完全不连通 | 紧致、连通（在Berkovich拓扑下） |
| **维数** | 0（拓扑维数） | 1（像树一样） |
| **结构** | 点集 | 包含Type II-IV点 |

### 3.2 基本性质

**定理（Benedetto, Rivera-Letelier）**：

对于度$d \geq 2$的有理函数$f: \mathbb{P}^1_{\text{Berk}} \to \mathbb{P}^1_{\text{Berk}}$：

1. **完全不变性**：$f^{-1}(\mathcal{J}^{\text{Berk}}(f)) = \mathcal{J}^{\text{Berk}}(f) = f(\mathcal{J}^{\text{Berk}}(f))$

2. **排斥周期点的闭包**：$\mathcal{J}^{\text{Berk}}(f)$等于排斥周期点的闭包

3. **拓扑性质**：$\mathcal{J}^{\text{Berk}}(f)$是$\mathbb{P}^1_{\text{Berk}}$的紧致、完全不变子集

4. **连通性**：$\mathcal{J}^{\text{Berk}}(f)$是路径连通的（作为Berkovich子空间）

### 3.3 Fatou分量的分类

**Rivera-Letelier分类定理**：

Berkovich Fatou集的每个连通分量（在经典意义下）属于以下类型之一：

| 类型 | 描述 | 动力学行为 |
|------|------|-----------|
| **吸引盆** | 包含吸引周期点 | 迭代收敛到周期轨道 |
| **抛物域** | 包含有理中性周期点 | 迭代收敛到周期轨道（慢于吸引） |
| **环形域** (Annulus) | p-adic特有的"环形"区域 | 类似于Siegel盘，但有不同几何 |
| **游荡域** | 非周期的Fatou分量 | 存在（与复情形不同！） |

**关键差异**：

- **Herman环**：在p-adic情形中不存在（与复情形不同）
- **Siegel盘**：在Berkovich框架下有不同表现
- **游荡域**：Benedetto证明了p-adic多项式可以有游荡域

### 3.4 超bolic性与Julia集结构

**定义（超bolic映射）**：

有理函数$f$称为**超bolic的**，如果所有临界点都位于Fatou集$\mathcal{F}^{\text{Berk}}(f)$中。

**等价条件**（Benedetto）：

以下陈述等价：
1. $f$是超bolic的
2. Julia集$\mathcal{J}^{\text{Berk}}(f)$上存在扩张度量
3. 临界轨道不累积在Julia集上

**Julia集结构**（超bolic情形）：

对于超bolic p-adic有理函数：
- 经典Julia集$J(f) \subset \mathbb{P}^1(\mathbb{C}_p)$是**Cantor集**
- Berkovich Julia集$\mathcal{J}^{\text{Berk}}(f)$是一个**实树**（real tree）
- 两者通过自然投影相关联

### 3.5 例子分析

#### 例子1: $f(z) = z^d$的完整分析

**经典Julia集**：
$$J(f) = \{z \in \mathbb{C}_p : |z|_p = 1\} = \text{单位圆}$$

这是一个完全不连通的紧致集，同胚于p-adic单位群$\mathbb{Z}_p^\times$。

**Berkovich Julia集**：

$\mathcal{J}^{\text{Berk}}(f)$由连接Type II点$D(0, 1)$到无穷远的路径组成，形成一个"脊柱"。

**Fatou分量**：
- $\mathcal{F}_0 = \{z : |z|_p < 1\}$（0的吸引盆）
- $\mathcal{F}_\infty = \{z : |z|_p > 1\}$（$\infty$的吸引盆）

#### 例子2: $f(z) = z^2 + c$（小$|c|_p$）

当$|c|_p < 1$时，Julia集是一个Cantor集。

**结构**：Julia集同胚于$\{0, 1\}^{\mathbb{N}}$（二进制序列空间）。

**Berkovich Julia集**：是一个Cantor树（Cantor set of paths）。

#### 例子3: 有游荡域的多项式（Benedetto构造）

**定理（Benedetto, 2002）**：

存在p-adic多项式具有游荡Fatou分量。

**构造思想**：
1. 选择适当的参数使得临界点轨道缓慢移动
2. 构造一系列嵌套的"盘"
3. 证明这些盘形成游荡域

这与复动力学的Sullivan定理形成鲜明对比。

---

## 4. 与p-adic维数理论的联系

### 4.1 Julia集的维数问题

**基本问题**：

在p-adic情形下，如何定义Julia集的"维数"？

**挑战**：
- 经典Julia集$J(f) \subset \mathbb{C}_p$是**完全不连通**的
- 拓扑维数为0
- 但存在某种"分形结构"

**解决方案**：Berkovich框架提供了自然的维数概念

### 4.2 p-adic Hausdorff维数

**定义（p-adic Hausdorff测度）**：

对于$E \subset \mathbb{Q}_p$和$s \geq 0$，$s$-维p-adic Hausdorff测度定义为：
$$\mathcal{H}_p^s(E) = \lim_{\delta \to 0} \inf\left\{\sum_i (\text{diam}_p U_i)^s : E \subset \bigcup_i U_i, \text{diam}_p U_i < \delta\right\}$$

其中$\text{diam}_p$是p-adic度量下的直径。

**定义（p-adic Hausdorff维数）**：
$$\dim_H^{(p)}(E) = \inf\{s \geq 0 : \mathcal{H}_p^s(E) = 0\}$$

**关键性质**：

| 集合 | p-adic Hausdorff维数 |
|------|---------------------|
| $\mathbb{Z}_p$ | 1 |
| $\mathbb{Z}_p^\times$（单位群） | 1 |
| 单点 | 0 |
| Cantor型子集 | 可能为分数 |

### 4.3 Berkovich Julia集的"维数"

**观察**：在Berkovich框架下，Julia集$\mathcal{J}^{\text{Berk}}(f)$具有非平凡的拓扑结构。

**可能的维数概念**：

1. **拓扑维数**：$\mathcal{J}^{\text{Berk}}(f)$作为实树的维数为1
2. **分形维数**：考虑Type II点的分布
3. **谱维数**：通过Laplacian的特征值定义

### 4.4 测度理论

**平衡测度（Equilibrium Measure）**：

对于有理函数$f$，存在唯一的概率测度$\mu_f$（称为**平衡测度**或**Green测度**）满足：
$$f^* \mu_f = d \cdot \mu_f$$

其中$d = \deg(f)$。

**性质**：
- 支撑在Berkovich Julia集$\mathcal{J}^{\text{Berk}}(f)$上
- 是混合的（mixing）
- 与等分布定理相关

**与维数的联系**：

测度的局部维数与集合的Hausdorff维数相关：
$$\dim_H \mu_f = \inf\{\dim_H E : \mu_f(E) = 1\}$$

### 4.5 Bowen公式在p-adic情形的适用性

**经典Bowen公式回顾**：

对于扩张共形映射$f$，Julia集的Hausdorff维数$\delta = \dim_H J(f)$满足：
$$P(-\delta \cdot \log |f'|) = 0$$

其中$P$是热力学压力函数。

**p-adic Bowen公式猜想**：

**猜想4.1（p-adic Bowen公式）**：

设$f$是扩张的p-adic有理函数，$\mathcal{J}^{\text{Berk}}(f)$是其Berkovich Julia集。则p-adic Hausdorff维数$\delta = \dim_H^{(p)}(J(f))$满足：

$$P(-\delta \cdot \psi) = 0$$

其中$\psi(x) = \log |f'(x)|_p$，$P$是p-adic热力学压力函数。

**在$f(z) = z^d$情形的验证**：

**计算**：
1. 压力函数（已计算）：$P(s) = \log d + s \cdot \log |d|_p^{-1}$
2. 解$P(\delta) = 0$：$\delta = \frac{\log d}{v_p(d) \cdot \log p}$

**几何维数**：Julia集$J(f) = \{z : |z|_p = 1\}$的p-adic Hausdorff维数为1（当$p | d$时）。

**比较**：
- 如果$d = p$：$\delta = \frac{\log p}{\log p} = 1$ ✓
- 如果$d = p^k$：$\delta = \frac{\log p^k}{k \log p} = 1$ ✓

这表明Bowen公式在此简单情形下成立！

**开放问题**：

1. 对于一般p-adic多项式$f(z) = z^d + c$，Bowen公式是否成立？
2. 如何严格定义p-adic热力学压力函数$P$？
3. 变分原理在p-adic情形是否成立？

---

## 5. 与本研究的联系

### 5.1 p-adic Bowen公式研究项目

本研究项目的核心目标是建立p-adic热力学形式理论，并证明p-adic Bowen公式。

**已完成工作**：

1. **p-adic压力函数定义**：通过三种等价途径定义
   $$P_{\text{per}}(\phi) = \lim_{n \to \infty} \frac{1}{n} \log \sum_{x \in \text{Fix}(f^n)} e^{S_n\phi(x)}$$

2. **简单例子分析**：$f(z) = z^d$的完整分析
   - 压力函数：$P(s) = \log d + s \cdot \log |d|_p^{-1}$
   - zeta函数：$\zeta_f(z, s) = \frac{1 - z|d|_p^s}{1 - zd|d|_p^s}$
   - Ruelle算子谱分析完成

3. **原创性猜想**：
   - p-adic变分原理
   - p-adic Ruelle-Perron-Frobenius定理
   - p-adic Bowen公式

### 5.2 Berkovich空间与维数理论

**关键联系**：

| 研究方向 | 与Berkovich理论的联系 |
|----------|----------------------|
| **维数定义** | Berkovich Julia集提供自然框架 |
| **测度理论** | 平衡测度$\mu_f$作为Gibbs测度的候选 |
| **压力函数** | 通过Berkovich周期点定义 |
| **Bowen公式** | 连接p-adic Hausdorff维数与压力 |

### 5.3 研究路线图

```
当前阶段 (P-011完成)
    ↓
Berkovich空间深入理解
    ↓
p-adic热力学形式严格化
    ↓
Bowen公式证明 (长期目标)
```

**下一步计划**：

1. **短期**（1-2个月）：
   - 深入理解Berkovich空间的几何
   - 计算更多例子（$f(z) = z^d + c$）
   - 验证Bowen公式在这些例子中是否成立

2. **中期**（3-6个月）：
   - 建立p-adic Ruelle算子的严格理论
   - 证明p-adic变分原理（特殊情形）
   - 研究Gibbs测度的存在性

3. **长期**（6-12个月）：
   - 证明一般p-adic Bowen公式
   - 探索与算术几何的联系
   - 应用于p-adic物理模型

---

## 6. 开放问题与研究方向

### 6.1 理论问题

#### 问题1: p-adic热力学形式的严格化

- 如何严格定义p-adic动力系统中的压力函数？
- p-adic变分原理是否普遍成立？
- p-adic Ruelle-Perron-Frobenius定理的条件是什么？

#### 问题2: Bowen公式的适用范围

- Bowen公式对所有超bolic p-adic映射是否成立？
- 非超bolic情形如何处理？
- 高维p-adic动力系统中的推广？

#### 问题3: Berkovich空间中的谱理论

- Berkovich Laplacian与维数的关系？
- 谱维数的计算？
- 热核估计？

### 6.2 计算与数值问题

#### 问题4: p-adic周期点的计算

- 如何高效计算p-adic有理函数的周期点？
- 高精度p-adic算术的实现？
- 周期点的分布规律？

#### 问题5: 可视化

- 如何可视化p-adic Julia集？
- Berkovich空间的图形表示？
- 计算维数的数值方法？

### 6.3 应用与联系

#### 问题6: 与算术几何的联系

- p-adic热力学形式与椭圆曲线的联系？
- 与p-adic L函数的关系？
- 在算术动力系统中的应用？

#### 问题7: 物理应用

- p-adic Bowen公式在p-adic物理中的意义？
- 与p-adic弦论的联系？
- 统计力学模型的p-adic版本？

### 6.4 参考文献

#### 核心文献

1. **Benedetto, R. L. (2019)**. *Dynamics in One Non-Archimedean Variable*. AMS.
   - p-adic动力学的标准参考书
   - Berkovich空间的完整介绍

2. **Baker, M. & Rumely, R. (2010)**. *Potential Theory and Dynamics on the Berkovich Projective Line*. AMS.
   - 潜在理论视角
   - 平衡测度的深入讨论

3. **Rivera-Letelier, J. (2000+)**. Théorie ergodique des fractions rationnelles sur un corps ultramétrique.
   - 原始分类定理
   - Fatou分量的分类

4. **Silverman, J. H. (2007)**. *The Arithmetic of Dynamical Systems*. Springer.
   - 算术动力系统的一般理论

#### 热力学形式相关

5. **Bowen, R. (1975)**. *Equilibrium States and the Ergodic Theory of Anosov Diffeomorphisms*.
6. **Ruelle, D. (1978)**. *Thermodynamic Formalism*.
7. **Przytycki & Urbański (2010)**. *Conformal Fractals: Ergodic Theory Methods*.

#### p-adic分析

8. **Gouvêa, F. Q. (2020)**. *p-adic Numbers: An Introduction* (3rd ed.). Springer.
9. **Khrennikov, A. (1997)**. *Non-Archimedean Analysis*.
10. **Vladimirov, Volovich & Zelenov (1994)**. *p-Adic Analysis and Mathematical Physics*.

---

## 附录: 关键公式速查

### p-adic赋值与绝对值
$$v_p(p^n \cdot \frac{a}{b}) = n, \quad p \nmid a, b$$
$$|x|_p = p^{-v_p(x)}$$

### 强三角不等式
$$|x + y|_p \leq \max(|x|_p, |y|_p)$$
等号成立当$|x|_p \neq |y|_p$

### 压力函数（$f(z) = z^d$）
$$P(s) = \log d + s \cdot \log |d|_p^{-1}$$

### Bowen方程
$$P(-\delta \cdot \log |f'|_p) = 0$$

### Ruelle算子
$$(\mathcal{L}_\phi g)(x) = \sum_{y \in f^{-1}(x)} e^{\phi(y)} g(y)$$

### zeta函数（$f(z) = z^d$）
$$\zeta_f(z, s) = \frac{1 - z|d|_p^s}{1 - zd|d|_p^s}$$

---

## 文档信息

- **任务**: P-011 - 学习p-adic动力学基础
- **状态**: ✅ 已完成
- **文档版本**: 1.0
- **最后更新**: 2026-02-11

### 相关文档

- [p-adic热力学形式框架](./thermodynamic_formalism_framework.md)
- [技术计算与例子](./technical_calculations.md)
- [核心问题分析](./core_problems_analysis.md)
- [Benedetto书籍详细信息](../../literature/padic/benedetto_detailed.md)
