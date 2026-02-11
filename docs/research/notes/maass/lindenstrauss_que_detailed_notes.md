# Lindenstrauss: Invariant Measures and Arithmetic Quantum Unique Ergodicity

## 详细研究笔记 (M-008)

---

## 1. 论文概述

### 1.1 历史背景

#### 量子遍历性与QUE猜想

**量子遍历性定理** (Šnirel'man-Colin de Verdière-Zelditch, 1970s-1980s):
对于任何测地流为遍历的紧致黎曼流形$M$，存在Laplace特征函数的密度为1的子序列，使得对应的$L^2$质量测度$|\phi_i|^2 d\text{vol}$弱收敛到均匀测度。

**Rudnick-Sarnak QUE猜想 (1994)**:
对于负截面曲率的紧致黎曼流形，**所有**特征函数序列的$L^2$质量都趋于均匀分布，不存在例外子序列。形式化表述为：

> 设$M$是负曲率紧致黎曼流形，$\{\phi_i\}$是Laplace算子的完备正交特征函数序列，则概率测度$d\tilde{\mu}_i = |\phi_i(x)|^2 d\text{vol}$在弱$*$拓扑下收敛到均匀测度$d\text{vol}$。

#### 微局部提升 (Microlocal Lift)

对于任何弱$*$极限$\tilde{\mu}$，可以构造**量子极限**$\mu$——这是单位切丛$SM$上的测度，满足：
- 投影到$M$上得到$\tilde{\mu}$
- **在测地流作用下不变**

#### 算术曲面与Hecke算子

对于常曲率曲面$M = \Gamma \backslash \mathbb{H}$，其中$\Gamma$是$\mathbb{Q}$上的同余格：
- **Hecke算子**$T_p$：与Laplace算子对易的自伴算子
- **算术量子极限**：来自Laplace算子和所有Hecke算子联合特征函数的量子极限

#### 前期工作

1. **Watson (2001)**: 在广义黎曼假设(GRH)下证明了算术QUE，且给出最优收敛速率
2. **Bourgain-Lindenstrauss (2003, 2004)**: 证明算术量子极限具有正熵（熵$\geq 2/9$）
3. **Ratner测度刚性理论**: 单参数幂零作用的不变测度分类

### 1.2 主要结果

本文证明了以下三个核心定理：

**定理1.1（不变测度分类）**:
设$G = SL(2, \mathbb{R}) \times L$，其中$L$是$S$-代数群。若概率测度$\mu$在$X = \Gamma \backslash G/K$上满足：
1. 关于对角群$A$的所有遍历分支具有**正熵**
2. 关于$T = L/K$是**递归的**

则$\mu$是$SL(2, \mathbb{R})$-不变的代数测度的线性组合。

**定理1.4（算术量子唯一遍历性）**:
设$M = \Gamma \backslash \mathbb{H}$，$\Gamma$是$\mathbb{Q}$上的同余格：
- **紧致情形**：唯一的算术量子极限是归一化体积测度
- **非紧致情形**：任何算术量子极限形如$c \cdot d\text{vol}_{SM}$，$0 \leq c \leq 1$

**定理1.6（Cartan作用的刚性）**:
对于$G = SL(2, \mathbb{R}) \times SL(2, \mathbb{R})$，任何关于两参数对角群$B$遍历的概率测度，要么：
- 是代数的，或
- 关于$B$的每个单参数子群的熵为零

这加强了Katok-Spatzier的结果，去掉了额外的遍历性假设。

### 1.3 技术路线概述

论文采用**测度刚性**方法解决量子遍历性问题，核心策略：

```
┌─────────────────────────────────────────────────────────────┐
│  量子极限 μ（测地流不变）                                    │
│       ↓                                                     │
│  识别为 X = Γ̃\G/K 上的A-不变测度                            │
│       ↓                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 条件1: 正熵性 (Bourgain-Lindenstrauss)              │   │
│  │ 条件2: T-递归性 (Hecke算子结构)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│       ↓                                                     │
│  应用定理1.1 → μ是SL(2,R)-不变的                            │
│       ↓                                                     │
│  由Ratner定理 → μ = 体积测度（代数测度）                    │
└─────────────────────────────────────────────────────────────┘
```

**关键创新**:
- 不假设单参数幂零作用的不变性，而是**推导**出这种不变性
- 将Ratner的H-性质用于建立不变性，而非分类
- 引入递归性作为连接动力系统与数论的桥梁

---

## 2. 核心定理

### 2.1 QUE定理的精确陈述

**定义（量子极限）**: 对于紧致黎曼流形$M$上的Laplace特征函数序列$\{\phi_j\}$：
- $\Delta \phi_j = \lambda_j \phi_j$，$\lambda_j \to \infty$
- $\|\phi_j\|_2 = 1$

微局部提升将$|\phi_j|^2 d\text{vol}$提升为$SM$上的测度$\mu_j$，使得任何弱$*$极限$\mu$满足：
- $\mu$在测地流作用下不变
- $p_*\mu = \lim |\phi_j|^2 d\text{vol}$（投影到$M$）

**定义（算术量子极限）**: 对于$M = \Gamma \backslash \mathbb{H}$，其中$\Gamma$是$\mathbb{Q}$上的同余格：
- Hecke算子$T_p$与$\Delta$对易
- 算术量子极限来自**联合特征函数**序列的量子极限

**定理1.4（精确表述）**:

设$M = \Gamma \backslash \mathbb{H}$，其中$\Gamma$是$\mathbb{Q}$上的同余格：

| 情形 | 结论 |
|------|------|
| $M$紧致 | 唯一的算术量子极限是$\frac{d\text{vol}_{SM}}{\text{vol}(SM)}$ |
| $M$非紧致 | 任何算术量子极限形如$c \cdot \frac{d\text{vol}_{SM}}{\text{vol}(SM)}$，其中$0 \leq c \leq 1$ |

**注**: Watson在GRH下证明了$c = 1$的情形。

### 2.2 不变测度分类（定理1.1）

**设定**:
- $G = SL(2, \mathbb{R}) \times L$，其中$L$是$S$-代数群
- $K < L$是紧子群，$T = L/K$
- $\Gamma < G$是离散子群，$\Gamma \cap L$有限
- $X = \Gamma \backslash G / K$
- $A = \left\{\begin{pmatrix} e^t & 0 \\ 0 & e^{-t} \end{pmatrix} : t \in \mathbb{R}\right\}$

**定义（$T$-递归测度）**:
Radon测度$\mu$在$(G,T)$-空间$X$上称为**$T$-递归的**，如果对于任何可测集$B \subset X$且$\mu(B) > 0$，对几乎每个$x \in B$和每个紧集$K \subset T$，存在$t \in T \setminus K$使得$t_U(x,t) \in B$。

**等价刻画**（命题4.1）: 对于概率测度$\mu$，$\mu$是$T$-递归的当且仅当对$\mu$-几乎每个$x$，条件测度$\mu_{x,T}^U(T) = \infty$。

**定理1.1**:
设$\mu$是$X$上的概率测度，满足：
1. **正熵条件**: 所有$A$-遍历分支关于$A$有正熵
2. **递归条件**: $\mu$是$T$-递归的

则$\mu$是$H = SL(2, \mathbb{R})$-不变的代数测度的线性组合。

**证明思路**:
1. 证明$\mu$是$N^+$-不变的（其中$N^+ = \{n^+(s) = \begin{pmatrix} 1 & s \\ 0 & 1 \end{pmatrix}\}$）
2. 通过对合$i: g \mapsto (g^T)^{-1}$，同理可得$N^-$-不变性
3. 由$N^+$和$N^-$生成$SL(2, \mathbb{R})$，故$\mu$是$H$-不变的
4. 应用Ratner定理分类$H$-不变测度

### 2.3 熵方法简介

**熵的物理意义**:
在动力系统$(X, \mu, \alpha)$中，测度熵$h_\mu(\alpha)$量化了系统的不可预测性：
- $h_\mu(\alpha) > 0$：系统具有混沌性
- $h_\mu(\alpha) = 0$：系统确定性强

**在本文中的应用**:

**Bourgain-Lindenstrauss正熵定理**:
对于算术量子极限$\mu$，所有$A$-遍历分支满足：
$$h_{\mu_\xi^E}(\alpha) \geq \frac{2}{9}$$
（归一化后，体积测度的熵为2）

**Ledrappier-Young理论**（定理7.6）:
对于$A$-不变测度$\mu$：
$$h_\alpha(\mu_\xi^E) > 0 \text{ a.s.} \Leftrightarrow \mu_{y,N^+} \text{是无限测度 a.s.}$$

这建立了**正熵**与**$N^+$-递归性**之间的等价关系，是证明的核心桥梁。

**Einsiedler-Katok引理**（命题6.4）:
设$X$是$S \times T$-空间，$\alpha: X \to X$在$S$-叶上等距作用，在$T$-叶上一致收缩。则对$\mu$-几乎每个$x$：
$$\mu_{x,S \times T}^U = \mu_{x,S}^U \times \mu_{x,T}^U$$

这表明条件测度具有乘积结构，是证明中的关键工具。

---

## 3. 技术工具

### 3.1 Hecke算子的作用

**数论背景**:
对于算术曲面$M = \Gamma \backslash \mathbb{H}$，其中$\Gamma = SL(2, \mathbb{Z}[\frac{1}{p}])$：
- $X = C\Gamma \backslash G / K_p$可识别为$SL(2, \mathbb{Z}) \backslash SL(2, \mathbb{R})$
- $T = G(\mathbb{Q}_p)/C_p G(\mathbb{Z}_p)$是$(p+1)$-正则树

**Hecke算子定义**:
$$T_p f(x) = \sum_{i=1}^{p+1} f(t_U(x, q_i))$$
其中$q_1, \ldots, q_{p+1}$是树$T$上$e$的最近邻。

**递归性的证明**（定理8.1）:

**引理8.3**: 若$S_p f = \lambda f$，则对树球$B_n^T$：
$$\sum_{y \in B_n^T} |f(y)|^2 \geq C_0 n |f(e)|^2$$

**证明要点**:
- **情形1** ($|\lambda| > 2\sqrt{p}$): 利用双曲函数展开
- **情形2** ($|\lambda| \leq 2\sqrt{p}$): 设$\cos \theta = \frac{\lambda}{2\sqrt{p}}$，利用振荡估计

**推论8.4**: 对于Hecke-Maass形式序列的极限测度$\mu$：
$$\sum_{y \in t(x, B_n^T)} \mu(B_r^X(y)) \geq C_0 n \mu(B_r^X(x))$$

这表明$\mu$是**$T$-递归的**，且具有定量下界。

### 3.2 遍历理论方法

#### $(G, T)$-空间框架

**定义2.1**: 局部紧致可分度量空间$X$称为**$(G, T)$-空间**，如果存在：
- 开覆盖$\mathcal{T}$
- 连续映射$t_U: U \times T \to X$满足：
  1. $t_U(x, e) = x$
  2. 传递性条件：若$y \in t_U(x, T)$，则存在$\theta \in G$使得$t_V(y, \cdot) \circ \theta = t_U(x, \cdot)$
  3. 局部单射性

**关键概念**:
- **$T$-叶**: 等价类$[x]_T = t_U(x, T)$
- **嵌入叶**: $t_U(x, \cdot)$是单射的叶
- **递归测度**: Poincaré回归的推广

#### 条件测度构造（§3）

**花朵分解技术**:

**定义3.4**: 对$(A, U)$称为**$r, T$-花朵**，如果：
- $[y]_A = U \cap B_{4r}^T(y)$（原子是开$T$- plaque）
- 对$y \in B$（中心），$[y]_A \supset B_r^T(y)$

**定理3.6**: 存在可测映射$\mu_{x,T}^U: V \to \mathcal{M}_\infty(T)$满足：
1. 归一化：$\mu_{x,T}^U(B_1^T) = 1$
2. 与sigma环分解相容
3. 在$T$-等价点之间仅差等距变换的推前

#### 证明$N^+$-不变性的核心论证

**定理7.1**: 设$\mu$是$A$-不变、$T$-递归的概率测度，且所有$A$-遍历分支有正熵。则$\mu$是$N^+$-不变的。

**证明概要**:
1. **假设反证**: 设$\mu$不是$N^+$-不变的，定义
   $$Z = \{x : \mu_{x,N^+} = \mathcal{H}_{N^+}\} \quad \text{(平移不变)}$$
   $$Y = \{x : \exists a, \mu_{x,N^+} \propto (+a)_*\mu_{x,N^+}\}$$
   由引理7.3，$\mu(Y \setminus Z) = 0$。

2. **H-性质**（引理7.4-7.5）:
   $$n^-(\delta)n^+(t) = n^+\left(\frac{t}{1+\delta t}\right) a(-\ln(1+\delta t)) n^-\left(\frac{\delta}{1+\delta t}\right)$$
   
   对于$x' = xn^-(s_-)n^+(s_+)a(s_a)$，存在$s$使得：
   $$xa(-\tau)n^+(s) \in X_1, \quad x'a(-\tau)n^+(s) \in X_1$$
   且后者接近前者沿$N^+$的平移。

3. **利用递归性**: 由$T$-递归性，找到$x \sim_T x'$，故$\mu_{x,N^+} = \mu_{x',N^+}$。

4. **矛盾**: 取极限得到$z = z'n^+(\tau)$且$\mu_{z,N^+} = \mu_{z',N^+} \propto (+\tau)_*\mu_{z,N^+}$，与$X_1$的定义矛盾。

### 3.3 与Ratner定理的关系

**Ratner测度刚性定理 (1990s)**:
在齐性空间$\Gamma \backslash G$上，由单参数幂零子群生成的群$H$作用的不变测度是代数的：即支撑在闭$N$-轨道上且是$N$-不变的测度。

**本文与Ratner定理的区别**:

| 方面 | Ratner定理 | 本文方法 |
|------|-----------|---------|
| **假设** | 单参数幂零作用的不变性 | 正熵 + 递归性 |
| **结论** | 代数性 | 首先建立幂零不变性，再得代数性 |
| **应用** | 分类已知不变测度 | 建立新的不变性 |

**本文创新**: 
- 使用Ratner的H-性质**建立**幂零不变性，而非仅用于分类
- 将遍历理论方法应用于**非不变**测度的研究

**S-代数版本**:
Margulis-Tomanov [MT94]将Ratner定理推广到$S$-代数群，本文使用此版本完成最终分类。

---

## 4. 证明思路

### 4.1 主要步骤概述

#### 第一阶段：从递归性到$N^+$-不变性（§7）

**目标**: 证明满足正熵和递归条件的$A$-不变测度实际上是$N^+$-不变的。

**核心步骤**:

```
正熵 + T-递归 → N+-不变
    ↓
Ledrappier-Young: 正熵 ⇔ N+-递归性
    ↓
H-性质 + 递归性 → 矛盾（若非不变）
```

**关键观察**: 如果$\mu$不是$N^+$-不变的，则存在"不良"点集$Y \setminus Z$具有正测度。通过：
1. 选择"良好"点$x, x'$在相同的$T$-叶上
2. 应用H-性质沿$A$作用流动
3. 构造具有矛盾性质的点$z, z' = zn^+(\tau)$

#### 第二阶段：正熵性的建立（[BL03]）

**Bourgain-Lindenstrauss定理**: 算术量子极限具有正熵。

**核心工具**:
- 有效估计：对任意小管状邻域给出测度的明确上界
- 基于Wolpert、Rudnick-Sarnak、Lindenstrauss的想法
- **下界**: 所有遍历分支的熵$\geq 2/9$

#### 第三阶段：递归性的建立（§8）

**定理8.1**: Hecke特征函数的$L^2$质量极限是$T$-递归的。

**核心估计**: 引理8.3表明Hecke特征函数在$p$-adic树上具有足够的方差：
$$\sum_{y \in B_n^T} |f(y)|^2 \geq C_0 n |f(e)|^2$$

这保证了极限测度在$T$-叶上具有无限条件测度。

#### 第四阶段：综合（从§1推出§4）

结合以上结果：
1. 算术量子极限$\mu$是$A$-不变的（由微局部提升）
2. $\mu$是正熵的（Bourgain-Lindenstrauss）
3. $\mu$是$T$-递归的（定理8.1）
4. 由定理1.1，$\mu$是$SL(2, \mathbb{R})$-不变的
5. 由Ratner定理，$\mu$是体积测度（紧致情形）或其倍数（非紧致情形）

### 4.2 关键引理

#### 引理7.3（平移不变性判别）

设$\mu$是$A$-不变测度。定义：
- $Z = \{x : \mu_{x,N^+} = \mathcal{H}_{N^+}\}$（平移不变）
- $Y = \{x : \exists a, \mu_{x,N^+} \propto (+a)_*\mu_{x,N^+}\}$

则$\mu(Y \setminus Z) = 0$。

**意义**: 如果条件测度是拟不变的（相差一个平移），则它实际上已经是平移不变的。

#### 引理7.4-7.5（H-性质）

对于$SL(2, \mathbb{R})$中的元素：
$$n^-(s_-)n^+(s_+)a(s_a)a(-\tau)n^+(\xi) = xa(-\tau)n^+\left(\frac{s_+ + e^{-2s_a}\xi}{1 + e^{2\tau}s_-(s_+ + e^{-2s_a}\xi)}\right) \cdot B_H^\sigma$$

其中$\sigma = C\max(\xi e^{2\tau}|s_-|, e^{-2\tau}|s_+|, |\xi|^{-1})$。

**关键应用**: 如果$x' = xn^-(s_-)n^+(s_+)a(s_a)$，则通过适当选择$\tau$，可以使：
- $xa(-\tau)n^+(s)$和$x'a(-\tau)n^+(s)$都在"良好"集合$X_1$中
- 二者沿$N^+$的平移距离$\tau$有界且非零

#### 引理7.9（技术性引理）

设$x, x' \in X$满足$d(x, x') < \delta$且$x \sim_T x'$。则存在两种情况之一：

**情形1**: $|s_a| > |s_-|^{10/21}$
- 存在$\xi_1 > C_0^{-1}\delta^{-1}$使得对所有$0 < \tau < \kappa \ln \xi_1$：
- $\xi_1 \in D_{\rho, C_0, \delta^{1/4}}(xa(-\tau), x'a(-\tau))$

**情形2**: $|s_a| \leq |s_-|^{10/21}$
- 存在$\xi_1 > C_0^{-1}\delta^{-1/2}$使得对所有$\kappa'|\ln \xi_1| < \tau < 2\kappa'|\ln \xi_1|$：
- $e^{-\tau}\xi_1 \in D_{\rho, C_0, \delta^{1/4}}(xa(-\tau), x'a(-\tau))$

### 4.3 难点和突破

#### 难点1：非不变测度的处理

**问题**: 传统遍历理论处理**不变**测度，而本文需要研究仅满足某些弱条件的测度。

**突破**: 
- 引入**条件测度**$\mu_{x,T}^U$的概念
- 发展非不变测度的**极大遍历定理**（附录A）
- 利用$(G,T)$-空间的框架

#### 难点2：从递归性到不变性

**问题**: 如何从$T$-递归性和正熵性导出$N^+$-不变性？

**突破**:
- **H-性质**的新应用：不用于分类，而用于建立不变性
- **点wise论证**：通过具体计算$SL(2, \mathbb{R})$元素的乘积关系
- **双曲几何与代数结构的结合**

#### 难点3：加倍条件的移除

**简化证明的假设**（§7.1）: 条件测度满足加倍条件
$$\mu_{x,N^+}(B_r^{N^+}) > 2\mu_{x,N^+}(B_{\rho r}^{N^+})$$

**完整证明的处理**（§7.2）:
- 定义**加倍半径集**$R_\rho(x)$和**位移半径集**$D_{\rho,C,\gamma}(x,x')$
- 证明这两个集合"经常"相交（通过Poincaré回归）
- 在相交时刻应用H-性质

#### 难点4：紧致性假设的处理

**紧致情形**（简化）：
- 可以直接应用遍历分解
- 所有极限点都在紧集中

**非紧致情形**：
- 需要处理质量逃逸到无穷的可能性
- 结论：$\mu = c \cdot d\text{vol}_{SM}$，其中$0 \leq c \leq 1$
- Watson在GRH下证明$c = 1$

---

## 5. 与本研究的关系

### 5.1 对分形双曲曲面的启示

#### 分形双曲曲面的量子遍历性

对于**分形双曲曲面**（具有分形谱维数的双曲系统），本文提供了以下启示：

1. **正熵条件的验证**:
   - 需要建立适用于分形系统的熵估计
   - 分形几何可能引入额外的复杂性

2. **递归性的替代条件**:
   - Hecke算子的结构依赖于算术性质
   - 对于非算术分形曲面，需要寻找新的"数论"结构

3. **测度刚性框架的适用性**:
   - $(G,T)$-空间的抽象框架可能适用于更一般的叶状结构
   - 分形叶状结构上的递归性定义需要调整

#### 可能的推广路径

```
本文框架（算术曲面）
        ↓
┌──────────────────────────────────────────┐
│ 1. 修改Hecke算子结构                      │
│    - 寻找分形类似物                       │
│    - 建立相应的递归性估计                 │
└──────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────┐
│ 2. 熵估计的推广                           │
│    - 分形熵的定义                         │
│    - 正熵性的证明                         │
└──────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────┐
│ 3. 测度分类                               │
│    - 应用修改后的定理1.1                  │
│    - 得到分形QUE                          │
└──────────────────────────────────────────┘
```

### 5.2 是否可以推广

#### 技术可推广性分析

| 技术成分 | 可推广性 | 障碍/机会 |
|---------|---------|----------|
| $(G,T)$-空间 | **高** | 适用于一般叶状系统 |
| 条件测度构造 | **高** | 需要sigma紧性 |
| H-性质 | **中** | 依赖于$SL(2,\mathbb{R})$的具体结构 |
| 极大遍历定理 | **高** | 一般框架已建立 |
| Hecke算子 | **低** | 强烈的算术依赖性 |

#### 可能的推广方向

1. **S-代数群的一般化**:
   - 将$SL(2,\mathbb{R}) \times L$推广到更一般的S-代数群乘积
   - 高秩情形：与Einsiedler-Katok [EK03]的工作结合

2. **非齐性空间**:
   - 将$\Gamma \backslash G$推广到更一般的非齐性动力系统
   - 需要新的不变测度分类工具

3. **分形动力系统**:
   - 建立分形版本的递归性概念
   - 研究分形叶状结构的刚性

4. **量子混沌的随机版本**:
   - 对于随机双曲曲面（Weil-Petersson体积形式）
   - 概率版本的QUE猜想

### 5.3 开放问题

#### 直接推广

**问题1（紧致QUE猜想）**: 对于**任意**紧致负曲率黎曼流形（不一定是算术的），是否成立量子唯一遍历性？

**状态**: 完全开放。Lindenstrauss的方法严重依赖算术结构（Hecke算子）。

**问题2（非紧致的$c=1$问题）**: 对于非紧致算术曲面，是否$c = 1$？即在无穷远处没有质量逃逸？

**状态**: Watson在GRH下证明。无条件证明是开放问题。

**问题3（最优速率）**: 算术QUE的收敛速率是什么？是否可以达到Watson在GRH下证明的速率？

#### 本研究的潜在问题

**问题4（分形系统的QUE）**: 对于具有分形谱维数的双曲量子系统，是否存在类似的遍历性结果？

**可能的途径**:
- 发展分形系统的熵理论
- 寻找分形"Hecke算子"的类似物

**问题5（测度刚性的分形版本）**: 对于分形叶状动力系统，正熵+递归性是否蕴含某种不变性？

**问题6（高维推广）**: 将Lindenstrauss的方法推广到更高维的双曲流形或Teichmüller空间。

**进展**: Eskin-Mirzakhani [EM13]在Teichmüller空间的类似结果。

#### 理论发展问题

**问题7（熵的下界优化）**: 算术量子极限的熵下界$2/9$是否是最佳的？

**问题8（递归性的定量版本）**: 定理8.1给出了$T$-递归性的定量估计。这种定量信息是否可以用于改进QUE的收敛速率？

**问题9（遍历分支的分类）**: 对于具有正熵但非遍历的测度，能否对每个遍历分支给出更精细的分类？

---

## 附录：核心公式汇编

### H-性质公式

对于$SL(2, \mathbb{R})$中的元素：

$$n^-(\delta)n^+(t) = n^+\left(\frac{t}{1+\delta t}\right) a(-\ln(1+\delta t)) n^-\left(\frac{\delta}{1+\delta t}\right)$$

### 熵公式

对于$A$-不变测度$\mu$，熵与条件测度的关系：
$$h_\alpha(\mu) = \text{const} \cdot \int \log \frac{d\mu_{x,N^+}(B_{e^{-t}}^{N^+})}{d\mu_{x,N^+}(B_{e^{-(t+1)}}^{N^+})} d\mu(x)$$

### Hecke算子估计

对于$S_p f = \lambda f$，设$\cosh \alpha = \frac{|\lambda|}{2\sqrt{p}}$（超bolic情形）：
$$\sum_{k=0}^n \lambda_{p^{2k}} = p^n \frac{\sinh(2n+1)\alpha}{\sinh \alpha}$$

对于$\cos \theta = \frac{\lambda}{2\sqrt{p}}$（椭圆情形）：
$$\sum_{k=0}^n \lambda_{p^{2k}} = p^n \frac{\sin(2n+1)\theta}{\sin \theta}$$

---

## 参考文献

1. **Lindenstrauss, E.** (2006). Invariant measures and arithmetic quantum unique ergodicity. *Annals of Mathematics*, 163(1), 165-219.

2. **Bourgain, J., & Lindenstrauss, E.** (2003). Entropy of quantum limits. *Communications in Mathematical Physics*, 233(1), 153-171.

3. **Ratner, M.** (1991). On Raghunathan's measure conjecture. *Annals of Mathematics*, 134(3), 545-607.

4. **Margulis, G. A., & Tomanov, G. M.** (1994). Invariant measures for actions of unipotent groups over local fields on homogeneous spaces. *Inventiones Mathematicae*, 116(1), 347-392.

5. **Rudnick, Z., & Sarnak, P.** (1994). The behaviour of eigenstates of arithmetic hyperbolic manifolds. *Communications in Mathematical Physics*, 161(1), 195-213.

6. **Watson, T.** (2001). Rankin triple products and quantum chaos. *Ph.D. Thesis, Princeton University*.

7. **Einsiedler, M., & Katok, A.** (2003). Invariant measures on $G/\Gamma$ for split simple Lie groups $G$. *Communications on Pure and Applied Mathematics*, 56(8), 1184-1221.

8. **Host, B.** (1995). Nombres normaux, entropie, translations. *Israel Journal of Mathematics*, 91(1-3), 419-428.

---

*任务编号*: M-008  
*状态*: ✅ 完成  
*笔记创建*: 2026-02-11  
*阅读范围*: 全文（55页）  
*深度*: 详细定理陈述、证明思路、技术工具和潜在应用
