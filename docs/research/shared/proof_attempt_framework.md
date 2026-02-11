# p-adic维数-L函数关系的严格证明尝试

> **文档类型**: 数学证明尝试框架  
> **证明目标**: 提案B（迭代熵维数）的基本性质  
> **创建日期**: 2026-02-11  
> **严格性等级**: 混合（L1-L4）

---

## 目录

1. [证明目标陈述](#1-证明目标陈述)
2. [已知结果和工具](#2-已知结果和工具)
3. [证明策略概述](#3-证明策略概述)
4. [详细证明步骤](#4-详细证明步骤)
5. [严格性差距识别](#5-严格性差距识别)
6. [严格性评估](#6-严格性评估)
7. [开放问题与下一步](#7-开放问题与下一步)

---

## 1. 证明目标陈述

### 1.1 主要目标

基于提案B（迭代熵维数），证明以下基本性质：

**目标定理 1.1** (迭代熵维数的基本性质)

设 $f: \mathbb{P}^1(\mathbb{Q}_p) \to \mathbb{P}^1(\mathbb{Q}_p)$ 是度 $d \geq 2$ 的有理映射，$\mu_f$ 是最大熵测度。定义迭代熵维数：

$$\dim_{\text{ent}}(f) = \frac{h_{\mu_f}(f)}{\lambda(f)}$$

其中 $h_{\mu_f}(f) = \log d$，$\lambda(f) = \int_{\mathcal{J}(f)} \log_p |f'(z)|_p \, d\mu_f(z)$。

**待证性质**:

| 性质 | 陈述 | 严格性目标 |
|------|------|-----------|
| **(P1) 非负性** | $\dim_{\text{ent}}(f) \geq 0$ | L1 |
| **(P2) 上界** | $\dim_{\text{ent}}(f) \leq 1$ | L1 |
| **(P3) 共轭不变性** | $\dim_{\text{ent}}(\phi \circ f \circ \phi^{-1}) = \dim_{\text{ent}}(f)$ | L2 |
| **(P4) 乘积公式** | $\dim_{\text{ent}}(f \times g) = \dim_{\text{ent}}(f) + \dim_{\text{ent}}(g)$ | L3 |
| **(P5) 单调性** | 若 $E \subset F$，则 $\dim_{\text{ent}}(E) \leq \dim_{\text{ent}}(F)$ | L3 |

### 1.2 修正的维数-L函数关系（基于K-103结果）

**原始公式（已证伪）**:
$$\dim = 1 + \frac{L(s_c)}{L(s_c + 1)}$$

K-103数值验证表明该公式不成立。

**修正猜想 1.2** (对数导数形式)

对于与模形式 $g$ 相关的p-adic动力系统 $f_g$:

$$\boxed{\dim_{\text{ent}}(f_g) = 1 + \frac{1}{\log p} \cdot \text{Re}\left(\frac{L_p'(1, g)}{L_p(1, g)}\right) \cdot \frac{1}{\deg(g)}}$$

或等价地：

$$\dim_{\text{ent}}(f_g) = \frac{\log(\deg f_g)}{\log(\deg f_g) + \lambda_{\text{geo}}(g)}$$

其中 $\lambda_{\text{geo}}(g) = -\text{Re}\left(\frac{L_p'(1, g)}{L_p(1, g)}\right) \cdot \frac{1}{\log p}$。

---

## 2. 已知结果和工具

### 2.1 最大熵测度理论（Baker-Rumely, Benedetto）

**定理 2.1** (最大熵测度存在唯一性) [[L1]](#严格性评估)

对于p-adic有理映射 $f: \mathbb{P}^1_{\text{Berk}} \to \mathbb{P}^1_{\text{Berk}}$，存在唯一的Borel概率测度 $\mu_f$ 使得：

1. $\mu_f$ 在 $f$ 下不变
2. $h_{\mu_f}(f) = h_{\text{top}}(f) = \log(\deg f)$
3. $\mu_f$ 的支撑集是Julia集 $\mathcal{J}(f)$

*参考文献*: 
- Benedetto, R.L. "Dynamics in One Non-Archimedean Variable", AMS GSM 198, 2019
- Baker, M. & Rumely, R. "Potential Theory on the Berkovich Projective Line"

### 2.2 变分原理（部分结果）

**定理 2.2** (p-adic变分原理) [[L1]](#严格性评估)

$$h_{\text{top}}(f) = \sup_{\mu \in \mathcal{M}_f} h_\mu(f)$$

其中 $\mathcal{M}_f$ 是 $f$-不变概率测度集。

*参考文献*: Benedetto, Theorem 10.2

### 2.3 Lyapunov指数的性质

**引理 2.3** (p-adic Lyapunov指数的有限性) [[L2]](#严格性评估)

对于有理映射 $f$，Lyapunov指数 $\lambda(f)$ 有限：

$$-\infty < \lambda(f) < +\infty$$

*证明概要*: 
- 上界：$|f'(z)|_p$ 在Julia集上有界（因 $f$ 是多项式或有理函数）
- 下界：由最大熵测度的正则性保证

### 2.4 p-adic积分理论

**定理 2.4** (Berkovich空间上的积分) [[L1]](#严格性评估)

对于Borel可测函数 $\phi: \mathcal{J}(f) \to \mathbb{R}$，积分 $\int_{\mathcal{J}(f)} \phi \, d\mu_f$ 在Berkovich空间框架下良定义。

---

## 3. 证明策略概述

### 3.1 整体策略

```
┌─────────────────────────────────────────────────────────────┐
│                    证明策略流程图                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 建立基础                                               │
│     ├── 最大熵测度的存在性 ✓ (Benedetto)                  │
│     ├── 熵的计算: h_μ = log d ✓ (Benedetto)               │
│     └── Lyapunov指数的有限性 ✓ (计算估计)                 │
│                                                             │
│  2. 证明非负性 (P1)                                        │
│     ├── 引理: λ(f) ≥ 0 (对多项式映射)                      │
│     └── 或: 使用λ₊ = max(0, λ)的修正定义                   │
│                                                             │
│  3. 证明上界 (P2)                                          │
│     ├── 关键: 证明 λ(f) ≥ log d                           │
│     ├── 使用压力函数 P(-s·log|f'|)                        │
│     └── 应用Bowen公式的p-adic类比                          │
│                                                             │
│  4. 共轭不变性 (P3)                                        │
│     ├── 熵的共轭不变性 (已知)                              │
│     └── Lyapunov指数的变换公式                             │
│                                                             │
│  5. 乘积公式与单调性 (P4, P5)                              │
│     └── 需要发展新的工具                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 关键困难

| 困难 | 描述 | 应对策略 |
|------|------|---------|
| **D1** | p-adic空间中 $|f'|_p$ 可以任意大或小 | 限制在Julia集上，使用最大熵测度的正则性 |
| **D2** | 缺乏标准的Bowen公式 | 发展p-adic压力函数理论 |
| **D3** | Lyapunov指数可能为负 | 考虑修正定义或使用符号计算 |
| **D4** | 乘积公式的证明 | 需要研究Berkovich空间的乘积结构 |

---

## 4. 详细证明步骤

### 4.1 定义和记号

**定义 4.1** (p-adic有理映射)

$$f(z) = \frac{P(z)}{Q(z)}, \quad P, Q \in \mathbb{Q}_p[z], \quad \max(\deg P, \deg Q) = d \geq 2$$

**定义 4.2** (Berkovich Julia集)

$$\mathcal{J}(f) = \partial\{z : f^n(z) \not\to \infty\}$$

（在Berkovich空间 $\mathbb{P}^1_{\text{Berk}}$ 中的边界）

**定义 4.3** (p-adic导数)

$$f'(z) = \frac{P'(z)Q(z) - P(z)Q'(z)}{Q(z)^2}$$

**定义 4.4** (修正Lyapunov指数)

$$\lambda_+(f) = \max(0, \lambda(f))$$

**修正维数定义**:

$$\dim_{\text{ent}}^+(f) = \frac{h_{\mu_f}(f)}{\lambda_+(f) + \epsilon}$$

（其中 $\epsilon > 0$ 是小正则化参数）

### 4.2 引理和辅助结果

#### 引理 4.5: 熵的显式计算 [[L1]](#严格性评估)

$$h_{\mu_f}(f) = \log d$$

*证明*:
1. 由Benedetto定理，$h_{\text{top}}(f) = \log d$
2. 由变分原理和最大熵测度的唯一性，$h_{\mu_f}(f) = h_{\text{top}}(f)$
3. 因此 $h_{\mu_f}(f) = \log d$ ∎

#### 引理 4.6: Lyapunov指数的下界估计 [[L2]](#严格性评估)

对于多项式映射 $f(z) = a_d z^d + \cdots + a_0$ 且 $|a_d|_p = 1$:

$$\lambda(f) \geq \frac{d-1}{d} \log d - C$$

其中 $C$ 是依赖于 $p$ 的常数。

*证明尝试*:

1. 对于大 $|z|_p$，$|f'(z)|_p \approx |d \cdot a_d \cdot z^{d-1}|_p$
2. 在Julia集上，轨道有界或在某种意义下"典型"
3. 最大熵测度 $\mu_f$ 集中在Julia集上
4. 估计积分 $\int \log_p |f'(z)|_p \, d\mu_f(z)$

**严格性缺口**: 第2步需要更精确的陈述。Julia集的结构复杂，需要Berkovich空间分析。

#### 引理 4.7: 压力函数的存在性 [[L3]](#严格性评估)

对于Hölder连续势函数 $\phi: \mathcal{J}(f) \to \mathbb{R}$，压力函数

$$P_f(\phi) = \lim_{n \to \infty} \frac{1}{n} \log \sum_{x \in \text{Fix}(f^n)} e^{S_n\phi(x)}$$

存在（可能为 $-\infty$）。

*证明尝试*:

1. 使用Berkovich空间上的Ruelle-Perron-Frobenius算子理论
2. 参考Baker-Rumely的势理论
3. 对于迭代 $f^n$，不动点计数与熵相关

**严格性缺口**: p-adic情形缺乏完整的Ruelle-Perron-Frobenius理论。

### 4.3 主要定理陈述与证明

#### 定理 4.8: 非负性 (P1) [[L2]](#严格性评估)

对于多项式映射 $f$，$\dim_{\text{ent}}(f) \geq 0$。

*证明*:

1. 由定义，$h_{\mu_f}(f) = \log d \geq 0$（因 $d \geq 2$）
2. 对于多项式映射，$\lambda(f) \geq 0$（需要证明）
   - 直观：多项式在Julia集上"扩张"
   - 在Berkovich空间上，$|f'|_p$ 的行为更规则
3. 因此 $\dim_{\text{ent}}(f) = \frac{\log d}{\lambda(f)} \geq 0$ ∎

**严格性缺口**: 第2步需要严格证明。当前是启发式论证。

#### 定理 4.9: 上界 (P2) [[L3]](#严格性评估)

对于 $\mathbb{P}^1(\mathbb{Q}_p)$ 上的有理映射，$\dim_{\text{ent}}(f) \leq 1$。

*证明尝试*:

**策略**: 证明 $\lambda(f) \geq \log d$。

1. 假设相反：$\lambda(f) < \log d$
2. 则维数 $\dim_{\text{ent}}(f) = \frac{\log d}{\lambda(f)} > 1$
3. 但在 $\mathbb{P}^1$ 上，"几何维数"不应超过1
4. 矛盾？

**问题**: 第3步缺乏严格的"几何维数"定义。

**替代策略**（使用压力函数）:

1. 定义p-adic压力函数：$P_f(-s \cdot \log |f'|)$
2. 猜想：维数 $s$ 是方程 $P_f(-s \cdot \log |f'|) = 0$ 的解
3. 利用 $P_f(0) = h_{\text{top}}(f) = \log d$
4. 需要证明：当 $s = 1$ 时，$P_f(-\log |f'|) \leq 0$

**严格性缺口**: 整个压力函数理论在p-adic情形需要建立。

#### 定理 4.10: 共轭不变性 (P3) [[L2]](#严格性评估)

设 $\phi \in \text{PGL}(2, \mathbb{Q}_p)$ 是Möbius变换。则：

$$\dim_{\text{ent}}(\phi \circ f \circ \phi^{-1}) = \dim_{\text{ent}}(f)$$

*证明*:

1. **熵的不变性**:
   $$h_{\mu_{\phi f \phi^{-1}}}(\phi f \phi^{-1}) = h_{\mu_f}(f) = \log d$$
   （拓扑熵是共轭不变量）

2. **Lyapunov指数的变换**:
   
   对于 $\tilde{f} = \phi \circ f \circ \phi^{-1}$，有：
   $$\tilde{f}'(\phi(z)) = \frac{\phi'(f(z)) \cdot f'(z)}{\phi'(z)}$$
   
   因此：
   $$\log_p |\tilde{f}'(\phi(z))|_p = \log_p |f'(z)|_p + \log_p |\phi'(f(z))|_p - \log_p |\phi'(z)|_p$$

3. **积分计算**:
   
   设 $\tilde{\mu} = \phi_* \mu_f$（推前测度）。则：
   $$\lambda(\tilde{f}) = \int \log_p |\tilde{f}'|_p \, d\tilde{\mu}$$
   $$= \int \left(\log_p |f'|_p + \log_p |\phi' \circ f|_p - \log_p |\phi'|_p\right) \, d\mu_f$$
   $$= \lambda(f) + \int \log_p |\phi' \circ f|_p \, d\mu_f - \int \log_p |\phi'|_p \, d\mu_f$$

4. **不变性**:
   
   由测度 $\mu_f$ 的 $f$-不变性：
   $$\int \log_p |\phi' \circ f|_p \, d\mu_f = \int \log_p |\phi'|_p \, d(f_*\mu_f) = \int \log_p |\phi'|_p \, d\mu_f$$
   
   因此这两项相消，得到 $\lambda(\tilde{f}) = \lambda(f)$。

5. **结论**: 
   $$\dim_{\text{ent}}(\tilde{f}) = \frac{\log d}{\lambda(\tilde{f})} = \frac{\log d}{\lambda(f)} = \dim_{\text{ent}}(f)$$ ∎

**严格性评估**: 这是严格的证明（L2），前提是所有积分良定义。

### 4.4 遇到的困难

#### 困难 1: p-adic压力函数理论缺失

**问题**: 经典的Ruelle-Perron-Frobenius理论和压力函数理论在p-adic情形尚未建立。

**影响**: 无法直接应用Bowen公式的标准证明技术。

**可能的解决方向**:
- 使用Berkovich空间上的势理论（Baker-Rumely）
- 发展基于Markov划分的替代方法
- 考虑特殊的映射类（如多项式 $z^d$）先行证明

#### 困难 2: Lyapunov指数的符号

**问题**: 在p-adic情形，$|f'(z)|_p$ 可以小于1（收缩）或大于1（扩张），取决于点的位置。

**影响**: 标准定义 $\lambda(f)$ 可能为负，导致维数公式出现问题。

**解决方案**: 
- **方案A**: 使用修正定义 $\lambda_+(f) = \max(0, \lambda(f))$
- **方案B**: 限制在"扩张"子集上定义维数
- **方案C**: 发展符号动力系统的框架

#### 困难 3: 乘积公式的Berkovich空间结构

**问题**: Berkovich空间 $\mathbb{P}^1_{\text{Berk}} \times \mathbb{P}^1_{\text{Berk}}$ 的结构复杂，不同于经典情形。

**影响**: 难以直接证明 $\dim_{\text{ent}}(f \times g) = \dim_{\text{ent}}(f) + \dim_{\text{ent}}(g)$。

**可能的解决方向**:
- 先对特殊情形（如 $f(z) = z^d$, $g(w) = w^e$）证明
- 研究Berkovich空间的纤维积结构
- 使用Chambert-Loir和Ducros的测度理论

### 4.5 需要填补的空白

| 空白 | 描述 | 优先级 | 可能的来源 |
|------|------|--------|-----------|
| **G1** | p-adic Ruelle-Perron-Frobenius算子 | P0 | 需要发展 |
| **G2** | p-adic压力函数的变分原理 | P0 | 部分在Benedetto中 |
| **G3** | Lyapunov指数与扩张率的关系 | P1 | 数值验证 + 理论 |
| **G4** | Berkovich空间上的乘积维数理论 | P1 | 几何测度论 |
| **G5** | L-函数与Lyapunov指数的精确关系 | P0 | K-103的延续 |

---

## 5. 严格性差距识别

### 5.1 严格步骤（L1）

| 步骤 | 内容 | 依赖 |
|------|------|------|
| S1 | 最大熵测度存在唯一性 | Benedetto定理 |
| S2 | 拓扑熵 $h_{\text{top}} = \log d$ | Benedetto定理 |
| S3 | 共轭变换的链式法则 | 初等计算 |
| S4 | 测度的不变性 | 定义 |

### 5.2 需要严格化的步骤（L2-L3）

| 步骤 | 当前状态 | 需要的工具 |
|------|----------|-----------|
| L4.6 | 启发式估计 | 最大熵测度的局部行为分析 |
| 4.8.P2 | 假设 $\lambda \geq 0$ | Julia集的扩张性分析 |
| 4.9 | 不完整证明 | p-adic压力函数理论 |
| 4.10 | 依赖积分良定义 | Berkovich积分理论 |

### 5.3 猜想性步骤（L4）

| 猜想 | 内容 | 数值支持 |
|------|------|---------|
| C4.11 | 压力-维数关系 | 无直接数据 |
| C4.12 | 修正的L-函数公式 | 需要K-103后续验证 |
| C4.13 | 乘积公式 | 无数据 |

---

## 6. 严格性评估

### 6.1 严格性等级定义

| 等级 | 名称 | 定义 |
|------|------|------|
| **L1** | 严格证明 | 基于已发表定理的完整证明 |
| **L2** | 严格但有计算成分 | 证明完整，但依赖数值验证或计算辅助 |
| **L3** | 启发式，有理论支持 | 论证合理，但需要额外的严格化工作 |
| **L4** | 猜想 | 基于类比或数值观察的假设 |

### 6.2 各结果的严格性评级

| 结果 | 陈述 | 等级 | 理由 |
|------|------|------|------|
| **R1** | $h_{\mu_f} = \log d$ | L1 | Benedetto定理 |
| **R2** | $\lambda(f)$ 有限 | L2 | 有界性 + 计算估计 |
| **R3** | 共轭不变性 (P3) | L2 | 证明完整，依赖积分定义 |
| **R4** | 非负性 (P1) | L3 | 依赖未证引理 |
| **R5** | 上界 (P2) | L3 | 证明不完整 |
| **R6** | 修正L-函数公式 | L4 | 基于K-103修正的猜想 |
| **R7** | 乘积公式 (P4) | L4 | 纯猜想 |

### 6.3 通往严格证明的路径

```
当前状态 (L3-L4)                      目标 (L1-L2)
     │                                    │
     ▼                                    ▼
┌──────────────────┐              ┌──────────────────┐
│ • 缺少压力理论   │   需要       │ • p-adic压力函数  │
│ • Lyapunov估计   │ ────────▶    │ • 变分原理        │
│   不完整         │   发展       │ • 完整的Bowen公式 │
│ • 与L-函数联系   │              │ • 数值验证        │
│   是猜想         │              │                   │
└──────────────────┘              └──────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│ 推荐研究顺序:                                        │
│ 1. 建立p-adic压力函数理论（6个月）                   │
│ 2. 数值验证简单例子（2个月）                         │
│ 3. 证明Lyapunov指数的下界（3个月）                   │
│ 4. 验证修正的L-函数公式（4个月）                     │
└─────────────────────────────────────────────────────┘
```

---

## 7. 开放问题与下一步

### 7.1 需要解决的关键问题

#### 问题 Q1: p-adic Ruelle-Perron-Frobenius算子

**陈述**: 如何在Berkovich空间上定义和研究Ruelle-Perron-Frobenius算子？

**重要性**: 这是建立压力函数理论和Bowen公式的关键。

**可能的思路**:
- 使用Baker-Rumely的势理论作为基础
- 考虑特殊的映射类（如超椭圆映射）
- 参考实动力系统的技术（如Sarig的工作）

#### 问题 Q2: Lyapunov指数的下界

**陈述**: 对于"一般"的p-adic有理映射，是否有 $\lambda(f) \geq \log d$？

**重要性**: 这直接关系到维数上界的证明。

**数值实验建议**:
```python
# 伪代码
for f in test_functions:
    mu = compute_maximal_entropy_measure(f)
    lyap = compute_lyapunov(f, mu)
    print(f"deg={f.degree}, lyapunov={lyap}, log_d={log(f.degree)}")
```

#### 问题 Q3: 修正L-函数公式的验证

**陈述**: 修正的公式 $\dim = 1 + \frac{1}{\log p} \cdot \frac{L_p'}{L_p}$ 是否正确？

**重要性**: 这是K-103失败后的核心问题。

**验证策略**:
1. 选择已知L-函数的简单模形式
2. 构造相关的p-adic动力系统（如果可能）
3. 数值计算两边并比较

### 7.2 可能的证明策略

#### 策略 S1: 先特殊后一般

1. **阶段1**: 对多项式 $f(z) = z^d$ 证明所有性质
   - Julia集是单位圆盘 $\mathbb{Z}_p$
   - 最大熵测度是Haar测度
   - 所有计算可以显式进行

2. **阶段2**: 扩展到超椭圆多项式 $f(z) = z^d + c$
   - 使用扰动理论
   - 数值验证

3. **阶段3**: 一般有理映射
   - 使用Berkovich空间的结构理论
   - 建立完整的压力函数框架

#### 策略 S2: 数值-理论结合

1. 大规模数值计算建立置信度
2. 识别数值模式
3. 基于模式提出严格陈述
4. 证明严格结果

#### 策略 S3: 跨方向迁移

从Kleinian方向的成功结果迁移技术：
- McMullen的转移算子方法
- Patterson-Sullivan测度理论
- Bowen公式的证明技术

### 7.3 需要发展的新工具

| 工具 | 描述 | 时间估计 |
|------|------|---------|
| **T1** | p-adic压力函数计算库 | 2个月 |
| **T2** | Berkovich空间上的数值积分 | 3个月 |
| **T3** | p-adic L-函数与动力系统的联系理论 | 6个月 |
| **T4** | 高维Berkovich空间的几何测度论 | 12个月 |

### 7.4 短期行动计划（2-4周）

| 周次 | 任务 | 产出 |
|------|------|------|
| 1 | 实现 $f(z) = z^d$ 的显式计算 | 代码 + 数值结果 |
| 2 | 阅读Benedetto关于熵的章节 | 笔记 + 引理提取 |
| 3 | 研究Baker-Rumely的势理论 | 笔记 + 技术总结 |
| 4 | 尝试证明 $f(z) = z^d$ 的P1-P3 | 证明草稿 |

---

## 附录A: 关键公式汇总

### A.1 迭代熵维数

$$\dim_{\text{ent}}(f) = \frac{\log(\deg f)}{\int_{\mathcal{J}(f)} \log_p |f'(z)|_p \, d\mu_f(z)}$$

### A.2 修正的L-函数公式

$$\dim_{\text{ent}}(f_g) = 1 + \frac{1}{\log p} \cdot \frac{L_p'(1, g)}{L_p(1, g)} \cdot \frac{1}{\deg(g)}$$

### A.3 p-adic压力函数（猜想形式）

$$P_f(\phi) = \lim_{n \to \infty} \frac{1}{n} \log \sum_{x \in \text{Fix}(f^n)} e^{S_n\phi(x)}$$

### A.4 变分原理（目标形式）

$$P_f(-s \cdot \log |f'|) = 0 \iff s = \dim_{\text{ent}}(f)$$

---

## 附录B: 参考文献

### 核心参考文献

1. **Benedetto, R.L.** (2019). "Dynamics in One Non-Archimedean Variable". AMS GSM 198.
   - 关键章节: Ch. 10 (熵理论), Ch. 9 (Berkovich空间)

2. **Baker, M. & Rumely, R.** "Potential Theory on the Berkovich Projective Line".
   - 关键章节: 势理论, 容量, 平衡测度

3. **McMullen, C.T.** (1998). "Hausdorff dimension and conformal dynamics III". Amer. J. Math.
   - 迁移技术来源

4. **Bowen, R.** (1979). "Hausdorff dimension of quasi-circles". Publ. IHES.
   - 经典Bowen公式

### 相关文献

5. **Rivera-Letelier, J.** 系列论文 on p-adic dynamics
6. **Favre, C. & Jonsson, M.** "The Valuative Tree"
7. **Chambert-Loir, A. & Ducros, A.** "Formes différentielles réelles et courants sur les espaces de Berkovich"

---

## 文档信息

- **创建者**: Fixed-4D-Topology研究团队
- **最后更新**: 2026-02-11
- **版本**: 1.0
- **相关文档**:
  - `dimension_definition_proposal.md`
  - `dimension_lfunction_correlation_report.md` (K-103)
  - `L_FUNCTIONS.md`

---

*本文档记录了向严格数学理论迈进的尝试。尽管存在严格性差距，但证明策略和识别的问题为后续研究提供了清晰的方向。*
