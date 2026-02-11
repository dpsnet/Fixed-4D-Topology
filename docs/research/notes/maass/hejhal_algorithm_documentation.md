# Hejhal算法文档：Maass形式特征值计算

## 1. 算法概述

Hejhal算法是由Dennis Hejhal于1980年代提出的计算模曲面上Maass尖点形式特征值的数值方法。该算法基于**配点法（Collocation Method）**，利用Maass形式的Fourier展开和自守条件（模不变性）来求解特征值。

### 1.1 核心思想

Hejhal算法的核心思想是：
1. **Fourier展开**：Maass形式在上半平面的Fourier展开
2. **自守条件**：利用模变换下的不变性建立约束
3. **线性系统**：通过配点法建立线性方程组
4. **特征值搜索**：寻找使线性系统有非零解的特征值

### 1.2 数学背景

**Maass形式**：对于模群 $\Gamma = SL(2, \mathbb{Z})$，Maass形式是满足以下条件的函数 $\phi: \mathbb{H} \to \mathbb{C}$：

1. **模不变性**：$\phi(\gamma z) = \phi(z)$，对所有 $\gamma \in \Gamma$
2. **Laplace特征函数**：$\Delta \phi + \lambda \phi = 0$，其中 $\Delta = y^2(\partial_x^2 + \partial_y^2)$
3. **多项式增长条件**：$\phi(z) = O(y^N)$（当 $y \to \infty$）
4. **尖点条件**：$\int_0^1 \phi(x+iy) dx = 0$（尖点形式）

**Fourier展开**：尖点形式具有Fourier展开：
$$\phi_+(z) = \sum_{n=1}^\infty \rho_\phi(n) y^{1/2} K_{it}(2\pi n y) \cos(2\pi n x)$$
$$\phi_-(z) = \sum_{n=1}^\infty \rho_\phi(n) y^{1/2} K_{it}(2\pi n y) \sin(2\pi n x)$$

其中：
- 特征值 $\lambda = \frac{1}{4} + t^2$
- $K_{it}$ 是修正的Bessel函数（Macdonald函数）
- $\phi_+$ 是偶形式，$\phi_-$ 是奇形式

---

## 2. 算法数学原理

### 2.1 配点法思想

**基本域**：$SL(2, \mathbb{Z})$ 的基本域为：
$$\mathcal{F} = \left\{ z = x+iy \in \mathbb{H} : |z| > 1, |x| < \frac{1}{2} \right\}$$

**截断Fourier展开**：取前 $M$ 项：
$$\phi_M(z; t) = \sum_{n=1}^M \rho(n) y^{1/2} K_{it}(2\pi n y) \cos(2\pi n x)$$

**精度估计**：当 $y \geq \frac{\sqrt{3}}{2}$（基本域底部），截断误差为 $O(e^{-2\pi M})$。

### 2.2 边界条件的建立

**关键变换**：利用模变换 $z \mapsto -1/z$ 下的不变性：
$$\phi\left(-\frac{1}{z}\right) = \phi(z)$$

这给出约束条件：
$$\sum_{n=1}^M \rho(n) I_n(z_j; t) = 0, \quad j = 1, \ldots, M$$

其中：
$$I_n(z; t) = y^{1/2} K_{it}(2\pi n y) \cos(2\pi n x) - \left(\frac{y}{|z|^2}\right)^{1/2} K_{it}\left(\frac{2\pi n y}{|z|^2}\right) \cos\left(\frac{2\pi n x}{|z|^2}\right)$$

（对于偶形式）

### 2.3 线性系统

选择基本域内的 $M$ 个点 $z_1, \ldots, z_M$，建立 $M \times M$ 矩阵：
$$A_{jn}(t) = I_n(z_j; t)$$

**特征值条件**：当 $t$ 使得 $\det A(t) = 0$ 时，对应的 $\lambda = \frac{1}{4} + t^2$ 是特征值。

### 2.4 数值稳定性

**SVD分解**：使用奇异值分解（SVD）代替直接求行列式：
$$A(t) = U \Sigma V^T$$

最小的奇异值 $\sigma_{\min}(t)$ 在特征值处达到极小值。

---

## 3. 算法步骤（详细伪代码）

### 3.1 主算法

```
算法：Hejhal算法（基础版本）
输入：搜索区间 [t_min, t_max]，截断参数 M，容差 ε
输出：特征值列表 eigenvalues

1. 初始化空列表 eigenvalues
2. 选择配点 z_1, ..., z_M 在基本域内
3. 对于 t 在 [t_min, t_max] 中按步长扫描：
   a. 构造矩阵 A(t)，其中 A_{jn} = I_n(z_j; t)
   b. 计算 A(t) 的最小奇异值 σ_min(t)
   c. 如果 σ_min(t) 是局部极小且 σ_min(t) < ε：
      i.  使用Brent方法精确定位零点
      ii. 记录特征值 λ = 1/4 + t²
4. 返回 eigenvalues
```

### 3.2 矩阵构造子程序

```
函数：构造矩阵 A(t)
输入：参数 t，配点列表 {z_j}，截断数 M
输出：M × M 矩阵 A

对于 j = 1 到 M：
    z = z_j = x_j + iy_j
    对于 n = 1 到 M：
        // 计算 I_n(z; t)
        term1 = y^{1/2} * K_{it}(2πn*y) * cos(2πn*x)
        
        y_inv = y / |z|²
        x_inv = -x / |z|²
        term2 = y_inv^{1/2} * K_{it}(2πn*y_inv) * cos(2πn*x_inv)
        
        A[j,n] = term1 - term2
返回 A
```

### 3.3 Bessel函数计算

```
函数：计算 K_{it}(x)
输入：虚阶 it，实数 x > 0
输出：K_{it}(x) 的值

使用 scipy.special.kv(it, x)
注意：需要处理数值稳定性问题
```

### 3.4 特征值精化

```
函数：精化特征值
输入：初始猜测 t₀，容差 ε
输出：精化后的特征值 t*

使用Brent方法在区间 [t₀-δ, t₀+δ] 上寻找 σ_min(t) 的零点
或等价地，寻找 det A(t) = 0 的根
```

---

## 4. 收敛性分析

### 4.1 Fourier展开的收敛速度

**定理**：对于尖点形式 $\phi$，其Fourier系数满足：
$$|\rho(n)| \leq C_\epsilon n^\epsilon$$

（这等价于Ramanujan-Petersson猜想）

**截断误差**：
$$\|\phi - \phi_M\|_{L^2} = O\left(\sum_{n>M} |\rho(n)|^2 |K_{it}(2\pi n y)|^2\right)$$

对于大参数，$K_{it}(u) \sim \sqrt{\frac{\pi}{2u}} e^{-u}$，因此：
$$\text{截断误差} = O(e^{-2\pi M y_{\min}})$$

对于基本域，$y_{\min} = \sqrt{3}/2$，误差为 $O(e^{-\sqrt{3}\pi M})$。

### 4.2 配点法的收敛性

**定理（Hejhal）**：设 $t_*$ 是精确特征值，$t_M$ 是用截断数 $M$ 计算的特征值，则：
$$|t_* - t_M| = O(e^{-cM})$$

其中 $c > 0$ 是依赖于几何的常数。

**数值观察**：
- $M = 10$：误差约 $10^{-5}$
- $M = 20$：误差约 $10^{-10}$
- $M = 50$：误差约 $10^{-20}$

### 4.3 指数收敛性

Hejhal算法具有**指数收敛性**，这是其相对于其他方法的主要优势。对于特征值 $\lambda \approx 1000$（即 $t \approx 31.6$），使用 $M = 50$ 可以达到机器精度。

---

## 5. 误差控制

### 5.1 误差来源

1. **截断误差**：Fourier级数截断
2. **舍入误差**：浮点运算
3. **Bessel函数计算误差**：特殊函数数值计算
4. **线性系统求解误差**：SVD分解

### 5.2 误差估计

**截断误差界**：
$$\epsilon_{\text{trunc}} \leq C \cdot e^{-2\pi M y_{\min}} \cdot \max_n |\rho(n)|$$

**总误差**：
$$\epsilon_{\text{total}} \approx \epsilon_{\text{trunc}} + \epsilon_{\text{round}} + \epsilon_{\text{svd}}$$

### 5.3 参数选择准则

**截断参数 M**：
- 要求精度 $10^{-D}$：$M \geq \frac{D \ln 10}{2\pi y_{\min}} \approx 0.43 D$
- 实际选择：$M \geq D$（考虑其他误差源）

**配点选择**：
- 均匀分布在基本域内
- 避免边界附近（Fourier展开收敛慢）
- 推荐：$y_j \in [\sqrt{3}/2, 1]$，$x_j \in [-1/2, 1/2]$

---

## 6. 复杂度估计

### 6.1 时间复杂度

**矩阵构造**：$O(M^2 \cdot C_{\text{Bessel}})$
- 计算 $M^2$ 个Bessel函数
- 每个Bessel函数计算：$O(1)$（使用渐近展开）

**SVD分解**：$O(M^3)$

**总复杂度**：
- 单次矩阵求值：$O(M^3)$
- 完整搜索（$N$ 个点）：$O(N \cdot M^3)$

### 6.2 空间复杂度

- 存储矩阵：$O(M^2)$
- SVD分解工作空间：$O(M^2)$

### 6.3 实际性能

对于 $M = 50$：
- 单次矩阵求值：约 0.01 秒
- 搜索区间（100个点）：约 1 秒
- 计算前10个特征值：约 10-30 秒

---

## 7. 已知特征值（验证基准）

根据文献记录，模群 $SL(2, \mathbb{Z})$ 的前几个Maass尖点形式特征值为：

### 7.1 偶形式

| 序号 | R = √(λ - 1/4) | λ = 1/4 + R² | 参考文献 |
|------|----------------|--------------|----------|
| 1 | 13.779751351890... | 190.131547... | [Hejhal 1992] |
| 2 | 17.738563381109... | 315.065933... | [Hejhal 1992] |
| 3 | 19.423481346970... | 377.870805... | [Hejhal 1992] |
| 4 | 21.315796882311... | 454.863142... | [Hejhal 1992] |
| 5 | 22.785280830796... | 519.988835... | [Hejhal 1992] |

### 7.2 奇形式

| 序号 | R = √(λ - 1/4) | λ = 1/4 + R² | 参考文献 |
|------|----------------|--------------|----------|
| 1 | 9.533695261349... | 91.141345... | [Hejhal 1992] |
| 2 | 12.173008240650... | 148.582130... | [Hejhal 1992] |
| 3 | 14.358509516256... | 206.366757... | [Hejhal 1992] |
| 4 | 16.138121172691... | 260.688934... | [Hejhal 1992] |
| 5 | 16.644259197914... | 277.431361... | [Hejhal 1992] |

---

## 8. 算法变体与扩展

### 8.1 大特征值方法（Strombergsson）

对于大 $t$（$t \leq 11000$）：
1. 截断级数于 $M \approx 5t$
2. 对小 $y$，利用Fourier系数公式：
   $$\rho(n) y^{1/2} K_{it}(2\pi n y) = \int_0^1 \phi_+(x+iy) \cos(2\pi n x) dx$$
3. 用求和代替积分，建立线性方程组
4. 最小化不同 $y$ 值得到的系数差异

### 8.2 迹公式方法（Gutzwiller-Sarnak）

利用Selberg迹公式结合 $X(1)$ 的长度谱显式知识：
$$\sum_\phi h(t_\phi) = \text{几何项}$$

优点：不需要计算特征函数，直接得到特征值。

### 8.3 Hecke关系验证

计算得到Fourier系数后，验证Hecke关系：
$$\rho(nm) = \sum_{d|(n,m)} \rho(nm/d^2)$$

这是自守性的强验证。

---

## 9. 实现要点

### 9.1 数值稳定性

1. **Bessel函数**：使用对数Bessel函数避免溢出
2. **矩阵条件数**：使用SVD代替行列式
3. **配点选择**：避免退化配置

### 9.2 优化技巧

1. **缓存Bessel函数**：对固定 $t$，$K_{it}(u)$ 在不同点复用
2. **自适应截断**：根据 $y$ 值调整截断数
3. **并行计算**：矩阵行独立计算

### 9.3 验证方法

1. **已知值对比**：与文献值对比
2. **Hecke关系**：验证乘法性
3. **自守条件**：验证边界条件
4. **正交性**：不同特征函数正交

---

## 10. 参考文献

1. **Hejhal, D. (1981)**. "Some observations concerning eigenvalues of the Laplacian and Dirichlet L-series." *Computers in Number Theory*.

2. **Hejhal, D. (1992)**. "On eigenfunctions of the Laplacian for Hecke triangle groups." *Emerging Applications of Number Theory*.

3. **Sarnak, P. (2003)**. "Spectra of Hyperbolic Surfaces." *Baltimore Lectures*.（附录7）

4. **Strombergsson, A. (1999)**. "Studies in the analytical and spectral theory of automorphic forms." *PhD Thesis*.

5. **Booker, A.R., Strömbergsson, A., & Venkatesh, A. (2006)**. "Effective computation of Maass cusp forms." *IMRN*.

---

## 11. 总结

Hejhal算法是计算Maass形式特征值的标准方法，具有以下特点：

**优点**：
- 指数收敛，高精度
- 概念清晰，易于实现
- 适用于中小特征值

**局限**：
- 大特征值需要大量计算资源
- 矩阵条件数可能恶化
- 需要精细的参数调整

**应用前景**：
- 验证L-函数的特殊值
- 量子混沌研究
- 算术量子混沌的数值验证
- 自守形式的机器学习研究

---

**文档版本**：1.0  
**最后更新**：2026-02-11  
**作者**：基于Sarnak讲义附录7和Hejhal原始文献
