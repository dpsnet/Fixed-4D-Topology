# 四元数代数基础 (Quaternion Algebra Basics)

> **学习目标**：建立四元数代数的坚实基础，理解其与算术Kleinian群和四元数L-函数的深刻联系。
> 
> **参考文献**：Maclachlan-Reid, *The Arithmetic of Hyperbolic 3-Manifolds*, Ch. 2 & 6

---

## 目录

1. [四元数代数定义](#1-四元数代数定义)
2. [基本运算](#2-基本运算)
3. [四元数代数的分类](#3-四元数代数的分类)
4. [序Orders](#4-序orders)
5. [与Kleinian群的联系](#5-与kleinian群的联系)
6. [四元数L-函数](#6-四元数l-函数)
7. [参考资源](#7-参考资源)

---

## 1. 四元数代数定义

### 1.1 一般四元数代数

**定义 1.1** (Hilbert符号定义)：设 $F$ 是一个特征不为2的域，$a, b \in F^\times$。四元数代数 $B = (a,b/F)$ 是由基 $\{1, i, j, k\}$ 生成的 $F$-代数，满足乘法关系：

$$
i^2 = a, \quad j^2 = b, \quad ij = -ji = k
$$

**乘法表**：

| $\cdot$ | $1$ | $i$ | $j$ | $k$ |
|---------|-----|-----|-----|-----|
| $1$ | $1$ | $i$ | $j$ | $k$ |
| $i$ | $i$ | $a$ | $k$ | $aj$ |
| $j$ | $j$ | $-k$ | $b$ | $-bi$ |
| $k$ | $k$ | $-aj$ | $bi$ | $-ab$ |

**一般元素表示**：
对于 $x \in B$，可以唯一表示为：

$$
x = x_0 + x_1 i + x_2 j + x_3 k, \quad x_0, x_1, x_2, x_3 \in F
$$

### 1.2 经典例子：Hamilton四元数

**定义 1.2** (Hamilton四元数)：取 $F = \mathbb{R}$，$a = b = -1$，得到Hamilton四元数：

$$
\mathbb{H} = (-1, -1/\mathbb{R})
$$

其中 $i^2 = j^2 = k^2 = ijk = -1$（Hamilton关系）。

**性质**：
- $\mathbb{H}$ 是 $\mathbb{R}$ 上的 **中心可除代数**（division algebra）
- $\mathbb{H} \cong \mathbb{R}^4$ 作为向量空间
- $\mathbb{H}^\times = \mathbb{H} \setminus \{0\}$ 构成乘法群

**Frobenius定理**：实数域 $\mathbb{R}$ 上的有限维可除代数只有：
- $\mathbb{R}$（1维）
- $\mathbb{C}$（2维）
- $\mathbb{H}$（4维）

### 1.3 其他重要例子

**例 1.3** (矩阵代数)：四元数代数 $(1, b/F) \cong M_2(F)$，同构映射：

$$
1 \mapsto \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad
i \mapsto \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \quad
j \mapsto \begin{pmatrix} 0 & b \\ 1 & 0 \end{pmatrix}
$$

**例 1.4** (数域上的四元数)：设 $K$ 是数域，例如：
- $B = (-1, -1/\mathbb{Q})$（在有理数上的Hamilton四元数）
- $B = (2, 3/\mathbb{Q})$（分裂代数）

---

## 2. 基本运算

### 2.1 加法和乘法

**加法**（分量相加）：
设 $x = x_0 + x_1 i + x_2 j + x_3 k$，$y = y_0 + y_1 i + y_2 j + y_3 k$

$$
x + y = (x_0 + y_0) + (x_1 + y_1)i + (x_2 + y_2)j + (x_3 + y_3)k
$$

**乘法**（利用分配律和基本关系）：

$$
xy = (x_0 y_0 + a x_1 y_1 + b x_2 y_2 - ab x_3 y_3) \\
+ (x_0 y_1 + x_1 y_0 - b x_2 y_3 + b x_3 y_2)i \\
+ (x_0 y_2 + a x_1 y_3 + x_2 y_0 - a x_3 y_1)j \\
+ (x_0 y_3 + x_1 y_2 - x_2 y_1 + x_3 y_0)k
$$

**注意**：四元数乘法 **不可交换**！$xy \neq yx$ 一般成立。

### 2.2 共轭 (Conjugation)

**定义 2.1** (标准对合)：映射 $\bar{\cdot}: B \to B$ 定义为：

$$
\overline{x_0 + x_1 i + x_2 j + x_3 k} = x_0 - x_1 i - x_2 j - x_3 k
$$

**性质**：
1. $\overline{x + y} = \bar{x} + \bar{y}$（加法同态）
2. $\overline{xy} = \bar{y} \cdot \bar{x}$（反乘法，注意顺序！）
3. $\bar{\bar{x}} = x$（对合）
4. $x \in F$（中心）当且仅当 $\bar{x} = x$

### 2.3 范数 (Reduced Norm)

**定义 2.2** (约化范数)：$n: B \to F$ 定义为：

$$
n(x) = x\bar{x} = \bar{x}x = x_0^2 - a x_1^2 - b x_2^2 + ab x_3^2
$$

**性质**：
1. $n(x) = 0 \Leftrightarrow x = 0$
2. $n(xy) = n(x)n(y)$（乘性）
3. $n(x) \in F$（取值在基域中）
4. $B$ 可除 $\Leftrightarrow n(x) = 0 \Rightarrow x = 0$

**逆元公式**：当 $n(x) \neq 0$ 时：

$$
x^{-1} = \frac{\bar{x}}{n(x)}
$$

### 2.4 迹 (Reduced Trace)

**定义 2.3** (约化迹)：$tr: B \to F$ 定义为：

$$
tr(x) = x + \bar{x} = 2x_0
$$

**性质**：
1. $\tr(x) = 0 \Leftrightarrow x_0 = 0$（纯虚四元数）
2. $\tr(xy) = \tr(yx)$（循环性）
3. $x^2 - \tr(x)x + n(x) = 0$（特征方程）

### 2.5 纯虚子空间

**定义 2.4**：$B_0 = \{x \in B : \tr(x) = 0\}$ 称为 **纯虚四元数子空间**。

**维数**：$\dim_F B_0 = 3$，基为 $\{i, j, k\}$。

---

## 3. 四元数代数的分类

### 3.1 分裂代数 vs 分歧代数

**定义 3.1**：设 $B$ 是域 $F$ 上的四元数代数。

- **分裂** (split)：$B \cong M_2(F)$（与 $2 \times 2$ 矩阵代数同构）
- **分歧/可除** (ramified/division)：$B \not\cong M_2(F)$（可除代数）

**判别准则**：

$$
B \text{ 分裂} \Leftrightarrow n(x) = 0 \text{ 对某个 } x \neq 0 \text{ 成立}
$$

**等价表述**：$B$ 分裂 $\Leftrightarrow$ 存在非零的零因子。

### 3.2 Hilbert符号

**定义 3.2** (Hilbert符号)：$(a, b)_v \in \{\pm 1\}$ 定义为：

$$
(a, b)_v = \begin{cases}
+1 & \text{若 } (a, b/F_v) \text{ 分裂} \\
-1 & \text{若 } (a, b/F_v) \text{ 分歧}
\end{cases}
$$

其中 $v$ 是 $F$ 的位 (place)，$F_v$ 是完备化。

**性质**：
1. **双线性**：$(a, b)_v$ 对每个变量都是乘性的
2. **对称性**：$(a, b)_v = (b, a)_v$
3. **乘积公式**（全局）：$\prod_v (a, b)_v = 1$

### 3.3 判别式 (Discriminant)

**定义 3.3** (判别式)：设 $B$ 是数域 $K$ 上的四元数代数。$B$ 的 **判别式** $\disc(B)$ 是如下定义的整理想：

$$
\disc(B) = \prod_{\mathfrak{p} \text{ 分歧}} \mathfrak{p}
$$

其中乘积取遍所有使 $B \otimes_K K_{\mathfrak{p}}$ 分歧的有限素理想 $\mathfrak{p}$。

**性质**：
1. $B$ 分裂（全局）$\Leftrightarrow \disc(B) = \mathcal{O}_K$
2. 判别式完全决定了 $B$ 的同构类

### 3.4 局部-全局原理

**定理 3.4** (Hasse原理)：设 $K$ 是数域，$B_1, B_2$ 是 $K$ 上的四元数代数。则：

$$
B_1 \cong B_2 \Leftrightarrow B_1 \otimes_K K_v \cong B_2 \otimes_K K_v \text{ 对所有位 } v
$$

**推论**：四元数代数的分类由局部行为完全决定。

---

## 4. 序 (Orders)

### 4.1 定义与例子

**定义 4.1**：设 $B$ 是数域 $K$ 上的四元数代数，$\mathcal{O}_K$ 是 $K$ 的整数环。

$\mathcal{O} \subset B$ 称为 **序** (order)，如果：
1. $\mathcal{O}$ 是有限生成 $\mathcal{O}_K$-模
2. $\mathcal{O}$ 包含 $K$ 的基（即 $K \cdot \mathcal{O} = B$）
3. $\mathcal{O}$ 对乘法和加法封闭
4. $1 \in \mathcal{O}$

**例 4.2** (标准序)：

$$
\mathcal{O}_0 = \mathcal{O}_K \oplus \mathcal{O}_K i \oplus \mathcal{O}_K j \oplus \mathcal{O}_K k
$$

### 4.2 极大序

**定义 4.3** (极大序)：序 $\mathcal{O}$ 称为 **极大** 的，如果不存在序 $\mathcal{O}'$ 使得 $\mathcal{O} \subsetneq \mathcal{O}' \subset B$。

**判别准则**：序 $\mathcal{O}$ 极大 $\Leftrightarrow$ 其判别式等于 $B$ 的判别式。

**存在性**：每个四元数代数都有极大序（一般不唯一）。

### 4.3 判别式与理想

**定义 4.4** (序的判别式)：设 $\mathcal{O}$ 是 $B$ 的序。其 **判别式** $d(\mathcal{O})$ 定义为：

$$
d(\mathcal{O})^2 = \det(\tr(x_i x_j))_{i,j}
$$

其中 $\{x_1, x_2, x_3, x_4\}$ 是 $\mathcal{O}$ 的 $\mathcal{O}_K$-基。

**性质**：
1. $d(\mathcal{O})$ 是 $\mathcal{O}_K$ 的整理想
2. $\mathcal{O}$ 极大 $\Leftrightarrow d(\mathcal{O}) = \disc(B)$

### 4.4 单位群

**定义 4.5**：序 $\mathcal{O}$ 的 **单位群**：

$$
\mathcal{O}^1 = \{x \in \mathcal{O}^\times : n(x) = 1\}
$$

（范数为1的单位）

**定理 4.6** (算术Kleinian群的来源)：设 $B$ 在 $K$ 的一个实嵌入处分歧，在其余实嵌入处分裂，则 $\mathcal{O}^1$ 在 $PSL(2, \mathbb{C})$ 中的像构成 **算术Kleinian群**。

---

## 5. 与Kleinian群的联系

### 5.1 四元数代数与双曲3-空间

**设定**：设 $B$ 是数域 $K$ 上的四元数代数，满足：
- 在 $K$ 的一个实嵌入 $\sigma_1: K \hookrightarrow \mathbb{R}$ 处：**分歧**（即 $B \otimes_{\sigma} \mathbb{R} \cong \mathbb{H}$）
- 在其余实嵌入和复嵌入处：**分裂**（即 $B \otimes_{\sigma} \mathbb{R} \cong M_2(\mathbb{R})$ 或 $M_2(\mathbb{C})$）

**嵌入**：在复嵌入处，我们有嵌入：

$$
\rho: B \hookrightarrow M_2(\mathbb{C})
$$

**定义 5.1** (双曲3-空间)：

$$
\mathbb{H}^3 = \{(z, t) : z \in \mathbb{C}, t > 0\}
$$

配备度量 $ds^2 = \frac{|dz|^2 + dt^2}{t^2}$。

**等距群**：$Isom^+(\mathbb{H}^3) \cong PSL(2, \mathbb{C})$。

### 5.2 算术Kleinian群的构造

**构造 5.2**：设 $\mathcal{O}$ 是 $B$ 的极大序，则：

$$
\Gamma_{\mathcal{O}} = P\rho(\mathcal{O}^1) \subset PSL(2, \mathbb{C})
$$

是 **算术Kleinian群**。

**一般形式**：若 $A$ 是 $B$ 的任意序，则 $\Gamma_A$ 称为 **算术Kleinian群**。

**定义 5.3** (算术流形)：商空间 $M_\Gamma = \mathbb{H}^3 / \Gamma$ 称为 **算术双曲3-流形**。

### 5.3 共轭类与类数

**定义 5.4** (型类)：四元数代数 $B$ 的极大序的 **型类** (type number) 是共轭类的个数。

**公式** (Eichler)：型类数 $T(B)$ 可以用类数公式计算。

**重要性**：不同极大序对应不同的（但密切相关的）算术Kleinian群。

---

## 6. 四元数L-函数

### 6.1 定义

**设定**：设 $B$ 是数域 $K$ 上的四元数代数，$\mathcal{O}$ 是极大序。

**定义 6.1** (四元数L-函数)：与 $(B, \mathcal{O})$ 相关的 **四元数L-函数** 定义为：

$$
\zeta_B(s) = \sum_{\mathfrak{a}} \frac{1}{N(\mathfrak{a})^s}
$$

其中求和取遍 $\mathcal{O}$ 的整左理想的等价类，$N(\mathfrak{a})$ 是范数。

**Euler乘积**（当 $B$ 分歧时）：

$$
\zeta_B(s) = \zeta_K(2s) \prod_{\mathfrak{p} \nmid \disc(B)} \left(1 - \frac{1}{N(\mathfrak{p})^{2s-1}}\right)^{-1}
$$

### 6.2 Jacquet-Langlands对应

**定理 6.2** (Jacquet-Langlands)：设 $B$ 是分歧四元数代数，则存在对应：

$$
\{\text{B上的自守表示}\} \longleftrightarrow \{\text{GL(2)上的尖点表示，在}\disc(B)\text{处分歧}\}
$$

**推论**：四元数L-函数与GL(2)的L-函数通过Jacquet-Langlands对应相联系。

**精确关系**：

$$
L(s, \pi_B) = L(s, \pi_{JL})
$$

其中 $\pi_B$ 是 $B^\times$ 的表示，$\pi_{JL}$ 是GL(2)的对应表示。

### 6.3 在体积公式中的作用

**定理 6.3** (Borel体积公式)：算术双曲3-流形 $M_\Gamma = \mathbb{H}^3 / \Gamma$ 的体积：

$$
\vol(M_\Gamma) = \frac{2\pi^2 \cdot |\disc(K)|^{3/2} \cdot \zeta_K(2)}{(4\pi^2)^{[K:\mathbb{Q}]-1}} \cdot \prod_{\mathfrak{p} | \disc(B)} \frac{N(\mathfrak{p}) - 1}{N(\mathfrak{p}) + 1}
$$

其中：
- $\disc(K)$ 是数域 $K$ 的判别式
- $\zeta_K(s)$ 是Dedekind zeta函数
- 乘积取遍 $B$ 的所有分歧素理想

**四元数L-函数的作用**：体积公式中的Euler因子实际上来源于四元数L-函数在 $s=2$ 处的值。

---

## 7. 参考资源

### 7.1 主要文献

1. **Maclachlan-Reid** (核心参考书)
   - Colin Maclachlan and Alan W. Reid, *The Arithmetic of Hyperbolic 3-Manifolds*
   - Graduate Texts in Mathematics 219, Springer, 2003
   - **重点章节**：Ch. 2 (Quaternion Algebras), Ch. 6 (Arithmetic Kleinian Groups)

2. **Vigneras** (经典教材)
   - Marie-France Vigneras, *Arithmetique des Algebres de Quaternions*
   - Lecture Notes in Mathematics 800, Springer, 1980

3. **Reiner** (序的理论)
   - I. Reiner, *Maximal Orders*
   - London Mathematical Society Monographs, Academic Press, 1975

### 7.2 在线资源

- Keith Conrad的讲义：*Quaternion Algebras* (excellent expository notes)
- Pete L. Clark: *Quaternion Algebras* (初步讲义)
- John Voight: *Quaternion Algebras* (综合专著，可在其主页免费获取)

### 7.3 相关论文

- Borel, A. "Commensurability classes and volumes of hyperbolic 3-manifolds"
- Chinburg, T. and Friedman, E. "The smallest arithmetic hyperbolic three-orbifold"
- Clozel, L. "Nombre de classes des ordres des corps de quaternions"

### 7.4 计算工具

- **SageMath**: `sage.algebras.quatalg`
- **Magma**: Quaternion algebra packages
- **PARI/GP**: `qfborchardt` 等四元数函数

---

## 8. 要点总结

```
四元数代数 B = (a,b/F)
├── 基 {1, i, j, k}，满足 i^2=a, j^2=b, ij=-ji=k
├── 运算：范数 n(x)=x̄x，迹 tr(x)=x+x̄
├── 分类：分裂(M_2(F)) vs 分歧(可除代数)
│   └── 判别式 disc(B) = prod_{分歧素数} p
├── 序 O：有限生成 O_K-子代数
│   └── 极大序 <-> disc(O) = disc(B)
└── 与Kleinian群的联系
    ├── B在1个实嵌入处分歧 -> H^3的等距群
    ├── O^1 -> PSL(2,C) 给出算术Kleinian群
    └── 体积公式中的L-函数：zeta_B(s) <-> zeta_K(s)
```

---

*最后更新：2026年2月*
