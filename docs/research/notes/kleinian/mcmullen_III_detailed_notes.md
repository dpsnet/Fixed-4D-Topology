# McMullen: Hausdorff Dimension and Conformal Dynamics III - 详细阅读笔记

## 论文信息

- **标题**: Hausdorff dimension and conformal dynamics III: Computation of dimension
- **作者**: Curtis T. McMullen
- **日期**: October 3, 1997
- **发表**: American Journal of Mathematics 1998
- **文件位置**: `Fixed-4D-Topology/docs/research/literature/kleinian/mcmullen_dimIII_hausdorff_conformal.pdf`

---

## 一、论文概述与核心贡献

### 1.1 研究背景

Hausdorff维数是描述分形集合复杂性的基本量。对于共形动力系统（Kleinian群和有理映射），其极限集和Julia集往往具有分数维数。本文提供了**第一个实际可计算的算法**来精确计算这些维数。

### 1.2 核心贡献

1. **特征值算法 (Eigenvalue Algorithm)**: 基于转移算子谱半径逼近压力函数
2. **Bowen公式的计算实现**: 将理论公式转化为可执行的数值方法
3. **丰富的数值例子**: Schottky群、二次多项式、Blaschke积等
4. **误差估计与收敛性分析**: 证明算法以指数速度收敛

---

## 二、理论基础：Bowen公式

### 2.1 精确陈述

**Bowen公式**: 对于扩张共形动力系统，极限集（或Julia集）的Hausdorff维数满足：

$$\dim_H \Lambda = \delta$$

其中 $\delta$ 是以下**压力方程**的唯一解：

$$P(-\delta \cdot \log |f'|) = 0$$

### 2.2 压力函数的热力学定义

对于位势函数 $\phi = -s \cdot \log |f'|$，压力定义为：

$$P(\phi) = \lim_{n \to \infty} \frac{1}{n} \log \sum_{x \in \text{Fix}(f^n)} e^{S_n \phi(x)}$$

其中 $S_n \phi(x) = \sum_{k=0}^{n-1} \phi(f^k(x))$ 是Birkhoff和。

### 2.3 简化形式（Markov情形）

对于具有Markov分划的系统，压力等于**转移算子的对数谱半径**：

$$P(-s \cdot \log |f'|) = \log \lambda(T^s)$$

其中 $T^s_{ij} = |f'_i(y_{ij})|^{-s}$ 是加权转移矩阵。

---

## 三、特征值算法详解

### 3.1 Markov分划的定义

**定义**: Markov分划是满足以下条件的有限集合 $\mathcal{P} = \{(P_i, f_i)\}$：

1. **覆盖性**: $f_i(P_i) \supset \bigcup_{i \to j} P_j$ （转移关系 $i \to j$ 表示 $\mu(f_i(P_i) \cap P_j) > 0$）
2. **同胚性**: $f_i$ 在 $P_i \cap f_i^{-1}(P_j)$ 的邻域上是同胚
3. **正测度**: $\mu(P_i) > 0$
4. **几乎不交**: $\mu(P_i \cap P_j) = 0$ （当 $i \neq j$）
5. **测度守恒**: $\mu(f_i(P_i)) = \sum_{i \to j} \mu(P_j)$

**扩张条件**: 存在共形度量 $\rho$ 和常数 $\xi > 1$ 使得 $|f'_i(x)|_\rho > \xi > 1$。

### 3.2 算法步骤（伪代码）

```
算法: Eigenvalue Algorithm for Hausdorff Dimension
输入: Markov分划 P = {(P_i, f_i)}，样本点 x_i ∈ P_i，收敛阈值 ε
输出: Hausdorff维数 δ 的近似值 α

1. 初始化：
   - 设置当前分划 P^(0) = P
   - 设置样本点 x_i^(0) = x_i
   - 设置迭代计数器 n = 0

2. 循环直到收敛：
   
   a. 构建转移矩阵 T^(n)：
      对于每个转移对 i → j：
        - 求解 y_ij ∈ P_i^(n) 使得 f_i(y_ij) = x_j^(n)
        - 计算 T_ij = |f'_i(y_ij)|^{-1}
      其他元素设为 0
   
   b. 求解特征值方程：
      - 找到 α^(n) ≥ 0 使得 λ((T^(n))^α) = 1
      - 其中 (T^α)_ij = (T_ij)^α
   
   c. 检查收敛性：
      - 如果 max diam(P_i^(n)) < ε，返回 α^(n)
   
   d. 精细化分划：
      - 对于每个块 R_ij = f_i^{-1}(P_j) ∩ P_i
      - 设置新样本点 x_ij = y_ij
      - 更新分划 P^(n+1) = {(R_ij, f_i)}
      - n ← n + 1
```

### 3.3 转移矩阵的具体构造

**矩阵元素**:
$$T_{ij} = \begin{cases} |f'_i(y_{ij})|^{-1} & \text{if } i \to j \\ 0 & \text{otherwise} \end{cases}$$

**关键计算**: 求解 $y_{ij} \in P_i$ 使得 $f_i(y_{ij}) = x_j$（需要计算逆映射）。

**加权矩阵**: $(T^\alpha)_{ij} = (T_{ij})^\alpha = |f'_i(y_{ij})|^{-\alpha}$

### 3.4 谱半径计算

**Perron-Frobenius理论**: 对于非负矩阵 $T$，谱半径 $\lambda(T)$ 满足：

1. $\lambda(T)$ 是正实特征值
2. 存在唯一的正特征向量 $v$（在标量倍数意义下）
3. 可以通过幂迭代计算：$v_{k+1} = T v_k / \|T v_k\|$

**算法实现**:
```
计算 λ(T^α):
  v ← 随机正向量
  重复直到收敛:
    w ← (T^α)v
    λ ← ||w|| / ||v||
    v ← w / ||w||
  返回 λ
```

**求解 α**: 使用牛顿法求解 $\lambda(T^\alpha) = 1$

---

## 四、收敛性分析

### 4.1 主要定理（Theorem 2.2）

**定理**: 设 $\mathcal{P}$ 是扩张Markov分划，$\mu$ 是维数为 $\delta$ 的不变密度。则：

$$\alpha(R^n(\mathcal{P})) \to \delta \quad \text{当 } n \to \infty$$

并且最多需要 $O(N)$ 次精细化来获得 $N$ 位精度。

### 4.2 误差估计

**关键不等式**: 设 $S_{ij}$ 和 $U_{ij}$ 分别是 $|f'_i|^{-1}$ 在 $P_{ij} = P_i \cap f_i^{-1}(P_j)$ 上的最小值和最大值。

则：
$$S^\delta m \leq m \leq U^\delta m$$

其中 $m_i = \mu(P_i)$。这推出：
$$\lambda(S^\delta) \leq 1 \leq \lambda(U^\delta)$$

**误差界**: 
$$|\alpha(\mathcal{P}) - \delta| \leq 2\beta = O(\max_i \text{diam}(P_i))$$

**精细化后的误差**:
$$|\alpha(R^n(\mathcal{P})) - \delta| = O(\xi^{-n})$$

其中 $\xi > 1$ 是扩张常数。

### 4.3 指数收敛

由于精细化后的块直径以 $O(\xi^{-n})$ 速度减小，误差也以相同速度指数衰减。这意味着每轮迭代大约获得固定数量的正确数字（与经典方法如蒙特卡洛相比是巨大改进）。

---

## 五、具体应用实例

### 5.1 Schottky群（反射生成的Kleinian群）

**对称三圆配置** ($\Gamma_\theta$):
- 三个圆均与单位圆正交
- 每个圆与单位圆相交的弧长为 $\theta$
- 极限集 $\Lambda_\theta \subset S^1$

**Markov分划**: 由三个生成圆围成的圆盘 $D(C_i)$ 构成，映射为反射 $\rho_i$。

**渐近行为**:
- 当 $\theta \to 0$: $\dim_H(\Lambda_\theta) \sim \frac{\log 2}{\log 12 - 2\log\theta} \asymp \frac{1}{|\log\theta|}$
- 当 $\theta \to 2\pi/3$: $1 - \dim_H(\Lambda_\theta) \asymp \sqrt{2\pi/3 - \theta}$

**Hecke群** ($\Gamma_r$):
- 由直线 $\text{Re } z = \pm 1$ 和圆 $|z| = r$ 的反射生成
- 当 $r \to 0$: $\dim_H(\Lambda_r) = 1 + \frac{r}{2} + O(r^2)$

### 5.2 阿波罗尼亚 gasket

- 由四个相互切触的圆的反射生成
- **计算结果**: $\dim_H(\Lambda) \approx 1.305688$
- Boyd的严格界限: $1.300197 < \dim_H(\Lambda) < 1.314534$
- 需要的Markov分划大小：约 140 万块

### 5.3 二次多项式的Julia集

**映射**: $f_c(z) = z^2 + c$

**Markov分划构造**:
- 通过外部角度（external angles）构造
- 利用Riemann映射 $\phi_c: S^1 \to J(f_c)$
- 分为两块：$P_1 = \phi_c([0, 1/2])$, $P_2 = \phi_c([1/2, 1])$

**关键计算结果**:
- $z^2 - 1$: $\dim_H \approx 1.26835$
- Douady兔子 ($c \approx -0.122561 + 0.744861i$): $\dim_H \approx 1.3934$
- $z^2 + 1/4$: $\dim_H \approx 1.0812$

**Ruelle公式** (c 接近 0):
$$\dim_H(J(f_c)) = 1 + \frac{|c|^2}{4\log 2} + O(|c|^3)$$

**抛物点不连续性**: 在 $c = 1/4$ 处，维数发生跳跃（抛物内爆现象）。

### 5.4 Blaschke积

**第一类** ($f_t(z) = z/t - 1/z$, $0 < t \leq 1$):
- 当 $t \to 0$: $\dim_H \sim \frac{\log 2}{\log(2/t - 1)} \asymp \frac{1}{|\log t|}$
- 当 $t \to 1$: $\dim_H \to 1$

**第二类** ($f_r(z) = z + 1 - r/z$, $r > 0$):
- 当 $r \to 0$: $\dim_H = 1 + \frac{\sqrt{r}}{2} + O(r)$

---

## 六、数值实现细节

### 6.1 实用考虑

1. **稀疏矩阵**: 转移矩阵 $T$ 的每行非零元数量恒定，使用稀疏矩阵存储需要 $O(|\mathcal{P}|)$ 而非 $O(|\mathcal{P}|^2)$ 空间。

2. **自适应精细化**: 只精细化超过临界直径 $r$ 的块，保持各块大小相近以提高精度。

3. **严格界限**: 通过上下界 $S_{ij}$ 和 $U_{ij}$ 可以获得严格的维数界限。

4. **收敛判断**: 观察 $\alpha(\mathcal{P})$ 在精细化下的变化来估计精度。

### 6.2 计算复杂度

- **空间复杂度**: $O(|\mathcal{P}|)$（稀疏存储）
- **时间复杂度**: 每轮迭代 $O(|\mathcal{P}|)$（矩阵-向量乘法）
- **总复杂度**: $O(N \cdot |\mathcal{P}|_N)$ 对于 $N$ 位精度

### 6.3 数值数据汇总

| 对象 | 分划大小 | 最大直径 | 维数 |
|------|---------|---------|------|
| 阿波罗尼亚 gasket | 1,397,616 | 0.0005 | 1.305688 |
| Douady兔子 | 7,200,122 | 0.000025 | 1.3934 |
| $J(z^2-1)$ | 5,145,488 | 0.000012 | 1.26835 |
| $J(z^2+1/4)$ | 1,209,680 | 0.000012 | 1.0812 |

---

## 七、与其他理论的关联

### 7.1 与Beardon工作的对比

- **Beardon**: 关注Poincaré级数的指数收敛性，给出维数的理论界限
- **McMullen**: 提供实际计算维数的算法，将理论转化为可执行代码

### 7.2 热力学形式体系 (Thermodynamic Formalism)

本文是热力学形式理论在共形动力系统中计算应用的典范：
- Gibbs测度 ↔ 共形测度 $\mu$
- 转移算子 ↔ Ruelle-Perron-Frobenius算子
- 压力函数 ↔ 谱半径对数
- 变分原理 ↔ Bowen公式

### 7.3 与Selberg zeta函数的联系

对于Fuchsian群，维数与Laplacian特征值的关系：
$$\lambda_0(\mathbb{H}^2/\Gamma) = D(1-D)$$

其中 $D = \dim_H(\Lambda(\Gamma))$。

### 7.4 与L-函数的可能联系（本项目视角）

**观察**: Hecke群例子中的渐近公式使用了Riemann zeta函数：
$$2\zeta(2\delta) = (r/2)^{-2\delta}(1 + O(r))$$

这暗示了维数计算与**算术L-函数**的深层联系。对于更一般的Kleinian群，可能涉及：
- Selberg zeta函数
- 与扭曲L-函数的联系
- 维度作为L-函数特殊值的某种体现

**未来研究方向**:
1. 探索维数计算的解析延拓性质
2. 研究维度与L-函数零点分布的关系
3. 将算法推广到与自守形式相关的动力系统

---

## 八、关键公式汇总

### 8.1 Bowen公式
$$\dim_H \Lambda = \delta, \quad P(-\delta \log |f'|) = 0$$

### 8.2 转移矩阵
$$T_{ij} = |f'_i(y_{ij})|^{-1}, \quad y_{ij} \in P_i, \, f_i(y_{ij}) = x_j$$

### 8.3 特征值方程
$$\lambda(T^\alpha) = 1$$

### 8.4 误差估计
$$|\alpha - \delta| = O(\max_i \text{diam}(P_i))$$

### 8.5 精细化收敛
$$|\alpha(R^n(\mathcal{P})) - \delta| = O(\xi^{-n})$$

---

## 九、可改进或扩展的方向

### 9.1 算法改进

1. **高阶方法**: 使用更高阶的逼近方法来加速收敛
2. **并行计算**: 转移矩阵构造和谱计算可并行化
3. **自适应采样**: 基于局部几何复杂性动态调整采样密度

### 9.2 理论扩展

1. **非扩张情形**: 处理含抛物点的系统（需要修改算法）
2. **高维推广**: 扩展到高维共形动力系统
3. **随机扰动**: 研究随机扰动下的维数变化

### 9.3 应用领域

1. **谱几何**: 与双曲流形Laplacian特征值的精确计算
2. **数论应用**: 连分数、Diophantine逼近中的维数计算
3. **物理应用**: 量子混沌、分形弦理论

---

## 十、参考文献关联

| 引用 | 内容关联 |
|------|---------|
| [4] Bowen | Bowen公式原始工作 |
| [22] Ruelle | 热力学形式理论、实解析映射 |
| [17] McMullen I | Kleinian群的维数连续性 |
| [18] McMullen II | 几何有限有理映射 |
| [24] Sullivan | 共形测度理论 |
| [5] Boyd | 阿波罗尼亚 gasket 的界限 |

---

## 十一、个人理解与思考

### 11.1 核心洞见

本文的核心创新在于将**热力学形式理论**中的抽象概念（压力、Gibbs测度）转化为**可计算的矩阵问题**。这种转化之所以可能，是因为：

1. **Markov结构**: 允许用有限状态近似无限动力学
2. **扩张性**: 保证近似以指数速度收敛
3. **共形性**: 简化导数计算，使得一维信息足够

### 11.2 技术难点

1. **Markov分划构造**: 对于一般动力系统，显式构造Markov分划是困难的
2. **逆映射计算**: 需要求解 $f_i^{-1}$，对于复杂映射可能需要数值方法
3. **精度控制**: 自适应精细化策略对最终结果精度至关重要

### 11.3 与本项目的关联

本文为本项目（Fixed-4D-Topology）提供了：
1. **计算工具**: 实现维数计算的Python代码框架
2. **理论背景**: 理解维度与动力系统关系的严格数学基础
3. **研究线索**: 维数与L-函数、谱理论的潜在联系

---

**笔记完成日期**: 2026-02-11  
**阅读者**: AI Assistant  
**状态**: 完整阅读并分析
