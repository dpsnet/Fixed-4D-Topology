# D1: Cantor类分形的严格定义

**状态**：L1级严格定义  
**验证状态**：待验证  
**依赖**：无（基础定义）

---

## 1. 动机

标准Cantor三分集$C$具有：
- 自相似性
- 完全不连通性
- Lebesgue测度为零
- Hausdorff维数$d = \frac{\log 2}{\log 3}$

我们研究满足类似性质的一类分形，其Hausdorff维数具有特定形式，可用于实数的逼近表示。

---

## 2. 严格定义

### 定义1.1 (广义Cantor构造)

设$\lambda = (\lambda_1, \lambda_2, \ldots, \lambda_m)$满足：
- $0 < \lambda_i < 1$对所有$i = 1, \ldots, m$
- $\sum_{i=1}^m \lambda_i < 1$

定义**压缩映射族**$\{f_i\}_{i=1}^m$，其中$f_i: [0,1] \to [0,1]$：

$$f_i(x) = a_i + \lambda_i x$$

这里$\{a_i\}$满足：
- $0 \leq a_1 < a_1 + \lambda_1 \leq a_2 < a_2 + \lambda_2 \leq \cdots \leq a_m < a_m + \lambda_m \leq 1$
- $a_{i+1} - (a_i + \lambda_i) > 0$（间隙条件）

**广义Cantor集**$C(\lambda, a)$是压缩映射族$\{f_i\}$的唯一不变集：

$$C(\lambda, a) = \bigcup_{i=1}^m f_i(C(\lambda, a))$$

由Hutchinson定理，该集合存在且唯一。

---

### 定义1.2 (Cantor类分形)

**Cantor类分形**$\mathcal{C}$是满足以下条件的广义Cantor集的集合：

**结构条件**：
1. **自相似性**：$C = \bigcup_{i=1}^m f_i(C)$，$f_i$为相似压缩
2. **完全断开性**：$C$完全不连通（无区间）
3. **测度零**：$\mathcal{L}^1(C) = 0$

**维数条件**：
4. **有理对数维数**：Hausdorff维数$d$满足
   $$d = \frac{\log p}{\log q}$$
   其中$p, q \in \mathbb{N}$，$p < q$

**构造条件**：
5. **正则间隙**：间隙比率为有理数
   $$\frac{a_{i+1} - (a_i + \lambda_i)}{1 - \sum \lambda_j} \in \mathbb{Q}$$

---

### 定义1.3 (Cantor维数集)

**Cantor维数集**$\mathcal{D}_C$定义为：

$$\mathcal{D}_C = \{\dim_H(C) : C \in \mathcal{C}\}$$

即所有Cantor类分形的Hausdorff维数集合。

---

## 3. 基本性质

### 引理1.1 (Hausdorff维数公式)

对于$C \in \mathcal{C}$，其Hausdorff维数$d$满足**Moran方程**：

$$\sum_{i=1}^m \lambda_i^d = 1$$

**证明概要**：
- 由自相似性，$C$是满足开集条件的自相似集
- 应用Moran定理，维数方程为$\sum \lambda_i^d = 1$
- 因$\lambda_i$为相似比，该方程有唯一正解$d$

**证毕**。

---

### 引理1.2 (标准Cantor集的包含性)

标准Cantor三分集$C_{1/3} \in \mathcal{C}$。

**证明**：
- 构造：$m=2$，$\lambda_1 = \lambda_2 = \frac{1}{3}$
- $a_1 = 0$，$a_2 = \frac{2}{3}$
- Moran方程：$2 \cdot (\frac{1}{3})^d = 1$
- 解得：$d = \frac{\log 2}{\log 3}$
- 满足所有定义条件

**证毕**。

---

### 引理1.3 (维数的稠密性)

集合$\mathcal{D}_C$在$[0,1]$中稠密。

**证明概要**：
- 对于任意$d \in (0,1)$和$\epsilon > 0$
- 选择适当的$m$和$\lambda_i$使$\sum \lambda_i^d = 1$
- 通过有理逼近使$\lambda_i \in \mathbb{Q}$
- 利用对数的无理数性质，可逼近任意$d$

**详细证明**：待补充（定理T2的一部分）

---

## 4. 例子

### 例1: 标准Cantor集

- $m = 2$
- $\lambda_1 = \lambda_2 = \frac{1}{3}$
- $d = \frac{\log 2}{\log 3} \approx 0.6309$

### 例2: Cantor五分集

- $m = 2$
- $\lambda_1 = \lambda_2 = \frac{1}{5}$
- $d = \frac{\log 2}{\log 5} \approx 0.4307$

### 例3: 多分支Cantor集

- $m = 3$
- $\lambda_1 = \lambda_2 = \lambda_3 = \frac{1}{4}$
- Moran方程：$3 \cdot (\frac{1}{4})^d = 1$
- $d = \frac{\log 3}{\log 4} \approx 0.7925$

---

## 5. 开放问题

**OP1**: 能否显式刻画$\mathcal{D}_C$的所有元素？

**OP2**: $\mathcal{D}_C$是否包含所有形如$\frac{\log p}{\log q}$的数？

**OP3**: 对于给定的$d \in \mathcal{D}_C$，构造是否唯一？

---

## 6. 验证状态

| 项目 | 状态 | 备注 |
|------|------|------|
| 定义严格性 | ✅ 已检查 | 基于标准分形几何 |
| 引理1.1 | ⚠️ 概要证明 | 需补充完整证明 |
| 引理1.2 | ✅ 已验证 | 标准结果 |
| 引理1.3 | ⚠️ 概要证明 | 核心定理，需详细证明 |

---

## 下一步

进入 **D2: 参数空间定义**

目标：建立Cantor类分形的参数空间结构，为线性代数框架做准备。

---

*定义完成。等待参数空间定义完成后一起验证。*
