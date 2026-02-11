# Sarnak《双曲曲面的谱》详细阅读笔记

> **文献信息**
> - 作者：Peter Sarnak
> - 标题：Spectra of Hyperbolic Surfaces
> - 来源：Baltimore Lectures, January 2003
> - 阅读日期：2026年2月11日
> - 任务编号：M-005

---

## 目录

1. [引言部分](#1-引言部分)
2. [Maass形式理论](#2-maass形式理论)
3. [迹公式](#3-迹公式)
4. [量子混沌](#4-量子混沌)
5. [与本研究的关系](#5-与本研究的关系)

---

## 1. 引言部分

### 1.1 双曲曲面的定义

**上半平面模型**

讲义以上半平面 $H = \{z = x + iy \mid y > 0\}$ 为基本几何对象，配备：

- **复结构**：标准的复坐标 $z = x + iy$
- **黎曼度量**：线元为 $ds = \frac{|dz|}{y}$
- **曲率**：$K = -1$（常负曲率）
- **面积元**：$dA(z) = \frac{dxdy}{y^2}$

**双曲Laplacian**

在 $(H, ds)$ 上，Laplacian算子为：

$$\Delta = y^2\left(\frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2}\right)$$

这个算子与 $G = SL(2, \mathbb{R})$ 的作用可交换。

**群作用**

$SL(2, \mathbb{R})$ 通过分式线性变换作用在上半平面：

$$g = \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \quad gz = \frac{az+b}{cz+d}$$

这个作用保持复结构和黎曼结构。

### 1.2 模曲面

**模群**

$$\Gamma(1) = SL(2, \mathbb{Z}) = \left\{\begin{pmatrix} a & b \\ c & d \end{pmatrix} \mid a,b,c,d \in \mathbb{Z}, ad-bc=1\right\}$$

**主同余子群**（level N）：

$$\Gamma(N) = \left\{\gamma \in SL(2,\mathbb{Z}) \mid \gamma \equiv I \pmod{N}\right\}$$

**模曲面**：$X(N) = \Gamma(N) \backslash H$

- 有限面积、非紧的双曲曲面
- 具有复结构，是Riemann曲面（代数曲线）
- 亏格大约随 $N^3$ 增长
- 也是椭圆曲线的模空间

**$X(1)$ 的基本区域**：

$$\mathcal{F}(1) = \left\{z \in H \mid |z| > 1, |\text{Re}(z)| < \frac{1}{2}\right\}$$

**$X(1)$ 的面积**：

$$\text{Area}(X(1)) = \frac{\pi}{3}$$

### 1.3 谱理论的基本问题

**基本谱问题**：寻找非零平方可积解满足

$$\begin{cases}
\Delta \phi + \lambda \phi = 0 \\
\phi(\gamma z) = \phi(z), \quad \gamma \in \Gamma(N) \\
\int_{X(N)} |\phi(z)|^2 dA(z) < \infty
\end{cases}$$

**谱的离散性**：满足上述条件的特征值 $0 = \lambda_0 < \lambda_1 \leq \lambda_2 \leq \cdots$ 是离散的。

**Maass形式**：满足上述条件的解 $\phi_\lambda(z)$ 称为Maass形式。

**数值结果**（Hejhal, Steil）：
- 已计算 $X(1)$ 的前10,000个特征值
- 前几个特征值：$0, 91.14\cdots, 148.43\cdots, 190.13\cdots, 206.16\cdots$
- 特征函数关于 $x=0$ 有奇偶对称性

### 1.4 与数论的联系

**Artin L-函数**

设 $K/\mathbb{Q}$ 为Galois扩张，$\rho: \text{Gal}(K/\mathbb{Q}) \to GL(2,\mathbb{C})$ 为不可约二维复表示。

对非分歧素数 $p$，定义Frobenius共轭类 $\text{Frob}_p$。

**Artin L-函数**：

$$L(s, \rho) = \prod_p \det(I - \rho(\text{Frob}_p)p^{-s})^{-1} = \sum_{n=1}^\infty \lambda_\rho(n)n^{-s}$$

**Artin猜想**：$L(s,\rho)$ 可延拓为整函数。

**与Maass形式的对应**（Sarnak的结果）：

若 $L(s,\rho)$ 是整函数，则

$$\phi(z) = \sum_{n=1}^\infty \lambda_\rho(n) y^{1/2} K_0(2\pi n y) \cos(2\pi n x)$$

是 $X(N)$ 上的Maass形式，特征值为 $\lambda_\phi = \frac{1}{4}$。

这里 $N$ 是 $\rho$ 的导子，$K_0$ 是修正Bessel函数：

$$K_\nu(y) = \int_0^\infty e^{-y\cosh t} \cosh(\nu t) dt$$

**重要推论**：
- 偶Galois表示 $\Rightarrow$ 特征值 $1/4$ 的Maass形式
- 奇Galois表示 $\Rightarrow$ 权1的全纯形式

**解析数论应用**

考虑位移和：

$$D(s; q_1, q_2, h) = \sum_{\substack{q_1 m - q_2 n = h}} \lambda_\rho(n)\lambda_\rho(m)(q_1 m + q_2 n)^{-s}$$

该级数在 $\text{Re}(s) > 1$ 绝对收敛。

**关键结果**：若 $0 < \lambda_\phi < 1/4$，则 $D(s;q_1,q_2,h)$ 在 $\text{Re}(s) > 1/2$ 解析（有极点 $s=1\pm it_\phi$）。

这给出了和式中的"平方根"消去：

$$\sum_{n \leq x} \lambda(n)\lambda(n+h) = O_{\epsilon,\phi}(x^{1/2+\epsilon})$$

---

## 2. Maass形式理论

### 2.1 定义和性质

**定义**：Maass形式是满足以下条件的函数 $\phi$：

1. **自守性**：$\phi(\gamma z) = \phi(z)$，$\forall \gamma \in \Gamma$
2. **特征方程**：$\Delta \phi + \lambda \phi = 0$
3. **尖点条件**：$\phi$ 在尖点处消失（cuspidal条件）
4. **可积性**：$\int_X |\phi|^2 dA < \infty$

**特征值的参数化**：

对于特征值 $\lambda \geq 1/4$，设 $\lambda = \frac{1}{4} + t^2$，$t \geq 0$。

### 2.2 Fourier展开

**一般展开**：

对于特征值 $\lambda = \frac{1}{4} + t^2$ 的Maass形式，有Fourier展开：

$$\phi(z) = \sum_{n \neq 0} a(n) y^{1/2} K_{it}(2\pi |n| y) e^{2\pi i n x}$$

其中 $K_{it}$ 满足修正Bessel方程：

$$K_{it}'' + \frac{1}{y}K_{it}' + \left(1 - \frac{t^2}{y^2}\right)K_{it} = 0$$

**验证**：对任意系数 $a(n)$，

$$\tilde{\phi}(z) = \sum_{n=1}^\infty a(n) y^{1/2} K_{it}(2\pi n y) \cos(2\pi n x)$$

满足 $\Delta \tilde{\phi} + (\frac{1}{4} + t^2)\tilde{\phi} = 0$。

**关键问题**：$\Gamma(N)$-不变性是非平凡的。

### 2.3 Hecke算子

**定义**：对 $(n,N) = 1$，Hecke算子 $T_n$ 定义为：

$$T_n f(z) = \frac{1}{\sqrt{n}} \sum_{ad=n} \sum_{b \pmod d} f\left(\frac{az+b}{d}\right)$$

**性质**：
- $T_n: L^2(X(N)) \to L^2(X(N))$
- $T_n$ 与 $\Delta$ 可交换
- $T_n$ 是正规算子
- Hecke算子彼此可交换
- 保持尖点形式空间 $L^2_{\text{cusp}}(X(N))$

**Maass-Hecke特征形式**：

可同时使 $\Delta$ 和 $\{T_n : (n,N)=1\}$ 对角化：

$$\Delta \phi_\lambda = \lambda \phi_\lambda, \quad T_n \phi_\lambda = \lambda_\phi(n) \phi_\lambda$$

**Ramanujan猜想（Hecke算子版本）**：

$$\|T_p|_{L^2_{\text{cusp}}(X(N))}\| \leq 2$$

等价于：$|\lambda_\phi(p)| \leq 2$。

**平凡界**：$\|T_p\| \leq p^{1/2} + p^{-1/2}$。

**最佳已知结果**（Kim-Sarnak）：

$$\|T_p|_{L^2_{\text{cusp}}(X(N))}\| \leq p^{7/64} + p^{-7/64}$$

---

## 3. 迹公式

### 3.1 Selberg迹公式概述

**基本形式**：对于适当的测试函数 $h$，有

$$\sum_{\lambda_j} h(t_j) = \text{几何侧}$$

其中 $\lambda_j = \frac{1}{4} + t_j^2$ 跑遍谱。

**几何侧**包括：
1. 恒等贡献（体积项）
2. 双曲贡献（闭测地线）
3. 抛物贡献（尖点）
4. 椭圆贡献（椭圆点）

### 3.2 几何侧和谱侧

**谱侧**：

$$\sum_{\phi_j} h(t_{\phi_j}) + \text{连续谱贡献}$$

**几何侧**（$X(1)$情形）：

原始闭测地线的长度恰为 $2\log \varepsilon_d$，其中 $0 < d \equiv 0,1 \pmod 4$ 无平方因子，$\varepsilon_d = t_0 + u_0\sqrt{d}$ 是Pell方程 $t^2 - du^2 = 4$ 的基本解。

重数为判别式 $d$ 的整二元二次型的类数 $h(d)$。

**关键应用**：

取 $h_T(t) = H\left(\frac{t}{T}\right)$，$H \to 1$，当 $T$ 足够大时，双曲共轭类贡献为零，得到：

$$\sum_{|t_j| \leq T} 1 \sim \frac{\text{Area}(X(1))}{4\pi} T^2$$

这证明了Weyl定律：$\#\{\lambda_j \leq T\} \sim \frac{\text{Area}(X)}{4\pi} T$。

### 3.3 应用

**1. 特征值的多重性估计**

对一般双曲曲面 $X$：

$$\limsup_{\lambda \to \infty} \frac{m_X(\lambda) \log \lambda}{\sqrt{\lambda}} \leq \frac{\text{Area}(X)}{2}$$

对 $X(1)$ 使用相对迹公式（Kloosterman和代替闭测地线）：

$$\limsup_{\lambda \to \infty} \frac{m_{X(1)}(\lambda) \log \lambda}{\sqrt{\lambda}} \leq \frac{\pi}{12}$$

**2. 本质尖点性**

$X(1)$ 是**本质尖点的**（essentially cuspidal）：大部分谱质量来自离散谱。

**3. 函子性提升**

迹公式建立了不同群之间的谱对应：

$$\text{sym}^k: GL(2) \to GL(k+1), \quad k \geq 1$$

- sym²提升 $\Rightarrow$ $\lambda_1 > 3/16$（Gelbart-Jacquet）
- sym³和sym⁴提升 $\Rightarrow$ $\lambda_1 > 21/100$（Kim-Shahidi）

**4. 循环基变换**

迹公式建立了数域 $L$ 和其循环扩张 $K/L$ 的自守谱之间的精确关系。

---

## 4. 量子混沌

### 4.1 量子遍历性

**测地流**

在 $S(X) = \Gamma \backslash G$（单位余切丛）上，测地流为：

$$G_t: (\Gamma g) \mapsto \left(\Gamma g \begin{pmatrix} e^{t/2} & 0 \\ 0 & e^{-t/2} \end{pmatrix}\right)$$

$G_t$ 保持Haar测度 $dg$。

**经典遍历性**：负曲率流形的测地流是遍历的、Anosov的、具有正Lyapunov指数——是"混沌"的Hamilton系统。

**量子化**

Laplacian特征值问题对应于这个经典混沌动力学的量子化。

**量子遍历性定理**（Shnirelman, Colin de Verdière, Zelditch）：

设 $\{\phi_j\}$ 为 $L^2(X)$ 的正交基（$X = X(N)$ 时取尖点形式基），$f \in C_0^\infty(\Gamma \backslash G)$，则当 $\lambda \to \infty$：

$$\frac{1}{\#\{j: \lambda_j \leq \lambda\}} \sum_{\lambda_j \leq \lambda} \left|\mu_{\phi_j}(f) - \bar{f}\right|^2 \to 0$$

其中 $\mu_{\phi_j}$ 是微局提升，$\bar{f} = \int_{\Gamma \backslash G} f(g)dg$。

**推论**：几乎所有（按特征值密度）的 $\mu_{\phi_j}$ 在 $\lambda_j \to \infty$ 时趋于等分布。

### 4.2 特征值分布

**特征值间距**

定义缩放特征值 $\tilde{\lambda}_j = \lambda_j / 12$，平均间距为1。

**数值发现**（Steil）：$X(1)$ 的相邻间距服从**Poisson分布**：

对 $0 \leq \alpha < \beta < \infty$，

$$\frac{\#\{j \leq N : \alpha \leq \tilde{\lambda}_{j+1} - \tilde{\lambda}_j \leq \beta\}}{N} \to \int_\alpha^\beta e^{-x} dx$$

当 $N \to \infty$。

**与随机矩阵理论的对比**：

混沌Hamilton系统的量子化通常预测特征值间距服从**GOE（Gauss正交系综）**分布，而非Poisson分布。

**解释**：$X(1)$ 的异常行为可能源于 $\Delta$ 与Hecke算子的可交换性。

对于没有Hecke算子的三角形（$q = 3,4,6$），数值发现间距服从GOE规律。

### 4.3 与随机矩阵理论的联系

**GOE分布**

随机实对称大矩阵的特征值间距分布在 $x=0$ 处有一阶零点，表明特征值相互排斥，谱是"刚性"的。

相比之下，Poisson律有近简并。

**量子唯一遍历性（QUE）猜想**

**猜想5** [Rudnick-Sarnak]：

测度 $\mu_\phi$ 在 $\lambda \to \infty$ 时关于 $dg$ 等分布。

等价表述：任何量子极限（$\mu_\phi$ 的弱极限）就是 $dg$。

**与scarring的关系**：

- 物理学猜测：混沌量子化的特征态可能集中在不稳定周期轨道上（scarring现象）
- QUE猜想否定了这种强scarring的可能性

**进展**：

1. **正熵结果** [Rudnick-Sarnak, Bourgain-Lindenstrauss]：
   任何量子极限 $\mu$ 必须对测地流 $G_t$ 有正熵。

2. **连续谱的QUE** [Luo-Sarnak, Jakobson]：
   对Eisenstein级数 $E(z, 1/2 + it)$，微局提升 $\mu_t$ 满足：
   
   $$\lim_{t \to \infty} \frac{\mu_t(K_2)}{\mu_t(K_1)} = \frac{\text{Vol}(K_2)}{\text{Vol}(K_1)}$$

3. **紧算术曲面的QUE** [Lindenstrauss]：
   对紧算术商 $X = \Gamma \backslash H$（$\Gamma$ 不可约格，如 $SL(2, \mathbb{Z}[\sqrt{2}])$），若 $\phi_\lambda$ 也是Hecke特征形式，则QUE成立。

4. **$X(1)$的部分结果** [Soundararajan]：
   对 $X(1)$，量子极限 $\mu = c \cdot dg$，$0 \leq c \leq 1$。

**测度刚性现象**

在高维情形（如Hilbert模曲面），量子极限在两参数Cartan作用下不变。

测地流的刚性不变测度比Cartan作用的多，这是证明QUE的关键。

---

## 5. 与本研究的关系

### 5.1 分形双曲曲面的特殊性

**标准vs分形**

Sarnak讲义主要讨论**算术双曲曲面** $X(N) = \Gamma(N)\backslash H$：
- 有限面积（$\text{Area}(X(N)) < \infty$）
- 非紧（有尖点）
- 极限集是整个边界 $\mathbb{R} \cup \{\infty\}$
- Hausdorff维数 $\delta = 1$

**分形双曲曲面**（本研究对象）：
- 由Schottky群或准Fuchs群构造
- 通常是**无限面积**（除非特别构造）
- 极限集是**分形**（Cantor集类型）
- Hausdorff维数 $\delta < 1$

### 5.2 极限集维数与谱的关系

**基本区别**

| 特征 | 算术曲面 $X(N)$ | 分形双曲曲面 |
|------|----------------|-------------|
| 面积 | 有限 | 通常无限 |
| 极限集 | 整个边界 | 分形（Cantor型）|
| $\delta$ | 1 | $< 1$ |
| Laplacian谱 | $[1/4, \infty)$ 连续 + 离散 | 取决于几何 |
| 迹公式 | Selberg迹公式 | 需要推广 |

**Laplacian的本质谱**

对无限面积双曲曲面，本质谱是 $[\delta(1-\delta)/4, \infty)$，其中 $\delta$ 是极限集的Hausdorff维数。

**关键洞察**：

当 $\delta \leq 1/2$，可能有**无离散谱**的情形。

当 $\delta > 1/2$，离散谱非空，特征值位于 $(0, \delta(1-\delta)/4)$。

### 5.3 待探索的问题

**理论问题**

1. **分形曲面的Maass形式**：
   - 当极限集是Cantor集时，Maass形式的结构如何？
   - Fourier展开在尖点（现在是分形边界）附近的行为？

2. **迹公式的推广**：
   - 对无限面积分形曲面，Selberg迹公式如何修正？
   - Patterson-Sullivan理论的作用？

3. **量子混沌的扩展**：
   - 当经典动力学限制在分形极限集上时，量子遍历性如何表述？
   - 特征值间距统计是否仍然Poissonian？

4. **数论联系**：
   - 分形双曲曲面的谱是否与某种"分形"L-函数有关？
   - 动力学zeta函数的新形式？

**计算方法**

1. **Hejhal算法的适应性**：
   - 讲义中Hejhal算法针对有限面积曲面
   - 如何修改以处理无限面积和分形边界？

2. **维数估计**：
   - 从谱数据反推极限集维数
   - 热核方法、波迹方法的推广

**与本项目具体联系**

1. **4D拓扑应用**：
   - 讲义中的谱理论可指导理解4D瞬子的模空间几何
   - Donaldson理论中的谱问题

2. **重正化群流**：
   - 讲义中的高/低能谱分离与RG流的联系
   - 紫外/红外极限的谱解释

3. **离散vs连续**：
   - 讲义中离散尖点谱与连续谱的相互作用
   - 在4D拓扑中的类似结构（瞬子贡献vs微扰贡献）

**参考文献推荐**

讲义中提及的进一步阅读：
- Venkov, Hejhal, Iwaniec: 双曲曲面、迹公式、Eisenstein级数
- Langlands, Borel: 表示论方法
- Lax-Phillips: 散射理论方法

针对分形情形：
- Patterson, Sullivan: 极限集、Hausdorff维数
- Borthwick: 散射理论在无限面积曲面的应用
- Lalley, Pollicott: 热力学形式与动力学zeta函数

---

## 附录：核心公式汇总

### A. 双曲几何

**线元**：$ds^2 = \frac{dx^2 + dy^2}{y^2}$

**面积元**：$dA = \frac{dx \wedge dy}{y^2}$

**Laplacian**：$\Delta = y^2\left(\frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2}\right)$

**测地线**：垂直于实轴的半圆或垂直线

### B. Maass形式

**Fourier展开**：
$$\phi(z) = \sum_{n \neq 0} a(n) y^{1/2} K_{it}(2\pi|n|y) e^{2\pi i n x}$$

其中 $\lambda = \frac{1}{4} + t^2$。

**Hecke特征值**：$T_n \phi = \lambda_\phi(n) \phi$

### C. Selberg迹公式（简化形式）

$$\sum_j h(t_j) = \frac{\text{Area}(X)}{4\pi} \int_{-\infty}^\infty h(t) t \tanh(\pi t) dt + \sum_{\gamma} \frac{\ell_{\gamma_0}}{e^{\ell_\gamma/2} - e^{-\ell_\gamma/2}} g(\ell_\gamma)$$

其中 $\gamma$ 跑遍本原闭测地线，$\ell_\gamma$ 是长度。

### D. Weyl定律

$$\#\{\lambda_j \leq T\} \sim \frac{\text{Area}(X)}{4\pi} T$$

---

## 阅读总结

Sarnak的这份讲义是双曲曲面谱理论的经典入门文献，主要涵盖：

1. **基础**：双曲几何、模群、模曲面
2. **核心**：Maass形式、Hecke算子、迹公式
3. **前沿**：量子混沌、QUE猜想、随机矩阵联系

**对本研究的启示**：

- 讲义中的有限面积算术曲面理论为理解**分形双曲曲面**提供了基准
- 迹公式方法需要针对无限面积情形进行实质性修改
- 量子混沌框架可扩展到分形边界情形
- 数论联系（L-函数）在分形情形可能有新的表现形式

**后续阅读计划**：

1. Hejhal的数值计算论文（原始算法）
2. Borthwick的《Spectral Theory of Infinite-Area Hyperbolic Surfaces》
3. Patterson-Sullivan关于极限集的经典工作
4. Lindenstrauss关于QUE的原始论文

---

*笔记完成时间：2026年2月11日*
*任务状态：M-005 已完成*
