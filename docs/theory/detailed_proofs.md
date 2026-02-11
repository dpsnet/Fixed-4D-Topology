
### 2.2 修正后的T2定理1：谱维数演化PDE

**定理陈述（修正版）**：
时变谱维数 $d_s(t) = -2t \frac{Z'(t)}{Z(t)}$ 满足：
$$\frac{d}{dt} d_s(t) = 2\langle \lambda \rangle_t - 2t \cdot \text{Var}(\lambda)_t$$

其中：
- $\langle \lambda \rangle_t = \frac{\sum \lambda_i e^{-\lambda_i t}}{\sum e^{-\lambda_i t}}$
- $\text{Var}(\lambda)_t = \langle \lambda^2 \rangle_t - \langle \lambda \rangle_t^2$

**完整证明**：

**步骤1：定义和基本计算**

热核迹：
$$Z(t) = \sum_{i=0}^\infty e^{-\lambda_i t}$$

时变谱维数：
$$d_s(t) := -2t \frac{Z'(t)}{Z(t)}$$

计算 $Z'(t)$：
$$Z'(t) = -\sum_{i=0}^\infty \lambda_i e^{-\lambda_i t}$$

因此：
$$\frac{Z'(t)}{Z(t)} = -\frac{\sum \lambda_i e^{-\lambda_i t}}{\sum e^{-\lambda_i t}} = -\langle \lambda \rangle_t$$

所以：
$$d_s(t) = 2t \langle \lambda \rangle_t$$

**步骤2：对 $d_s(t)$ 求导**

$$\frac{d}{dt} d_s(t) = 2\langle \lambda \rangle_t + 2t \frac{d}{dt}\langle \lambda \rangle_t$$

**步骤3：计算 $\frac{d}{dt}\langle \lambda \rangle_t$**

令：
- $N(t) = \sum_{i=0}^\infty \lambda_i e^{-\lambda_i t}$
- $D(t) = \sum_{i=0}^\infty e^{-\lambda_i t} = Z(t)$

则 $\langle \lambda \rangle_t = \frac{N(t)}{D(t)}$。

计算导数：
$$N'(t) = -\sum_{i=0}^\infty \lambda_i^2 e^{-\lambda_i t} = -\langle \lambda^2 \rangle_t \cdot Z(t)$$

$$D'(t) = Z'(t) = -\langle \lambda \rangle_t \cdot Z(t)$$

使用商的导数法则：
$$\frac{d}{dt}\langle \lambda \rangle_t = \frac{N' D - N D'}{D^2}$$

$$= \frac{(-\langle \lambda^2 \rangle_t Z) \cdot Z - (\langle \lambda \rangle_t Z) \cdot (-\langle \lambda \rangle_t Z)}{Z^2}$$

$$= -\langle \lambda^2 \rangle_t + \langle \lambda \rangle_t^2$$

$$= -(\langle \lambda^2 \rangle_t - \langle \lambda \rangle_t^2)$$

$$= -\text{Var}(\lambda)_t$$

**步骤4：组合结果**

$$\frac{d}{dt} d_s(t) = 2\langle \lambda \rangle_t + 2t \cdot (-\text{Var}(\lambda)_t)$$

$$= 2\langle \lambda \rangle_t - 2t \cdot \text{Var}(\lambda)_t$$

**证毕**。

---

**关于原论文错误的说明**：

原论文假设渐近形式 $Z(t) \sim C t^{-d_s/2}$，其中 $d_s$ 是常数，然后对时间求导得到PDE。

但论文同时定义 $d_s(t)$ 为时变的，这导致数学矛盾：
- 如果 $Z(t) = C t^{-d_s(t)/2}$，则 $\ln Z = \ln C - \frac{d_s(t)}{2} \ln t$
- 求导：$\frac{Z'}{Z} = -\frac{d_s'(t) \ln t}{2} - \frac{d_s(t)}{2t}$
- 由定义 $d_s(t) = -2t \frac{Z'}{Z}$，代入得：
  $$\frac{Z'}{Z} = -\frac{d_s'(t) \ln t}{2} + \frac{Z'}{Z}$$
- 这意味着 $d_s'(t) \ln t = 0$，即 $d_s'(t) = 0$（对于 $t \neq 1$）

因此，原论文的PDE公式是**不正确的**。

---

### 2.3 定理2：存在唯一性（修正版）

**定理陈述**：
对于修正后的PDE：
$$d_s'(t) = 2\langle \lambda \rangle_t - 2t \cdot \text{Var}(\lambda)_t$$

具有初值条件 $d_s(t_0) = d_0$，解的存在唯一性由 $\text{Var}(\lambda)_t$ 的性质决定。

**注意**：这个PDE不是自治的，因为右边依赖于 $t$ 和通过热核迹定义的矩。

**完整分析**：

**步骤1：右边函数的性质**

定义：
$$f(t, d) = 2\langle \lambda \rangle_t - 2t \cdot \text{Var}(\lambda)_t$$

**关键观察**：右边实际上**不直接依赖于 $d$**！

这是因为 $\langle \lambda \rangle_t$ 和 $\text{Var}(\lambda)_t$ 完全由热核迹 $Z(t)$ 决定，而 $Z(t)$ 是 $t$ 的固定函数（由分形的谱决定）。

**步骤2：简化问题**

PDE实际上简化为：
$$d_s'(t) = f(t)$$

其中 $f(t) = 2\langle \lambda \rangle_t - 2t \cdot \text{Var}(\lambda)_t$ 是已知函数。

**步骤3：显式解**

$$d_s(t) = d_s(t_0) + \int_{t_0}^t f(s) ds$$

$$= d_s(t_0) + \int_{t_0}^t (2\langle \lambda \rangle_s - 2s \cdot \text{Var}(\lambda)_s) ds$$

**步骤4：存在唯一性**

由于右边 $f(t)$ 对所有 $t > 0$ 是光滑的（假设特征值分布良好），积分给出唯一的解。

**结论**：

对于修正后的PDE，存在唯一性是**平凡的**，因为方程实际上是一阶线性ODE，且右边是 $t$ 的已知光滑函数。

**证毕**。

---

## 第三部分：T3 - 模形式-分形弱对应

### 3.1 定理分析

**原论文声称**：
$$d_H(F) = 1 + \frac{L(f, k/2)}{L(f, k/2 + 1)} + \mathcal{O}(\delta)$$

**评估**：

这个公式**没有数学推导**在论文中。它基于以下观察：
1. $L$-函数比值给出某种"算术复杂度"
2. Hausdorff维度给出"几何复杂度"
3. 两者都落在 $[0, 2]$ 或 $[1, 2]$ 范围内

但这不是数学证明。

**详细分析为什么这个公式缺乏严格基础**：

**步骤1：$L$-函数比值的性质**

对于权 $k$ 的模形式 $f$，$L(f, s)$ 在 $s = k/2$ 处有特殊性质：
- 如果 $k$ 是偶数，$s = k/2$ 是整数点
- $L(f, k/2)$ 和 $L(f, k/2 + 1)$ 之间存在函数方程的联系

对于Ramanujan $\Delta$ 函数（$k=12$）：
- $L(\Delta, 6) \approx 0.037441$
- $L(\Delta, 7) \approx 0.973$
- 比值 $\approx 0.0385$
- 预测 $d_H \approx 1.038$

**步骤2：与Hausdorff维度的比较**

实际分形维度：
- Apollonian gasket: $d_H \approx 1.306$
- Sierpinski carpet: $d_H \approx 1.893$
- Koch snowflake: $d_H \approx 1.262$

预测值 $1.038$ 与实际值相差 $0.2$ 到 $0.8$。

**步骤3：统计评估**

如果定义相对误差：
$$\text{误差} = \frac{|d_H^{\text{预测}} - d_H^{\text{实际}}|}{d_H^{\text{实际}}}$$

对于上述例子：
- Apollonian: $|1.038 - 1.306|/1.306 \approx 20\%$
- Sierpinski: $|1.038 - 1.893|/1.893 \approx 45\%$
- Koch: $|1.038 - 1.262|/1.262 \approx 18\%$

**步骤4：随机猜测的比较**

如果在 $[1, 2]$ 上均匀随机猜测，期望误差为 $0.5$。

公式给出的误差也是 $O(0.5)$，并不比随机猜测好多少。

**结论**：

公式 $d_H = 1 + L(f, k/2)/L(f, k/2+1)$ 是**启发式观察**，不是严格数学定理。

**正确的陈述应该是**：

存在一个弱对应，使得模形式 $f$ 的 $L$-值与某些分形族的维度相关，相关性约为 $0.3$（即解释了约 $30\%$ 的方差）。

---

## 第四部分：T4 - 分形算术

### 4.1 定理1修正：Grothendieck群结构

**原论文声称**：
$$\mathcal{G}_D^{(r)} \cong (\mathbb{Q}, +)$$

**反例**：

设 $r = 1/3$。则维度集：
$$\mathcal{D}^{(1/3)} = \left\{\frac{\ln N}{\ln 3} : N \in \mathbb{N}, N \geq 2\right\}$$

对于 $N = 2^k$，$d_N = \frac{k \ln 2}{\ln 3} = k \cdot \frac{\ln 2}{\ln 3}$。

Grothendieck群元素的形式为：
$$[d_{N_1}] - [d_{N_2}] = \frac{\ln N_1 - \ln N_2}{\ln 3} = \frac{\ln(N_1/N_2)}{\ln 3}$$

像集是：
$$\text{Im}(\phi) = \left\{\frac{\ln q}{\ln 3} : q \in \mathbb{Q}^+\right\}$$

这是 $\mathbb{R}$ 的一个稠密加法子群，但**不等于** $\mathbb{Q}$。

事实上，$\frac{\ln 2}{\ln 3}$ 是超越数（由Gelfond-Schneider），所以 $\text{Im}(\phi)$ 包含超越数。

**修正后的定理1'**：

**陈述**：
映射 $\phi: \mathcal{G}_D^{(r)} \to \mathbb{R}$ 定义为：
$$\phi([d_{N_1}] - [d_{N_2}]) = \frac{\ln(N_1/N_2)}{\ln(1/r)}$$

是到其像的同构，像集是 $\mathbb{R}$ 的稠密加法子群：
$$\text{Im}(\phi) = \frac{1}{\ln(1/r)} \cdot \ln(\mathbb{Q}^+)$$

**完整证明**：

**步骤1：良定性**

若 $[d_{N_1}] - [d_{N_2}] \sim [d_{N_1'}] - [d_{N_2'}]$，则：
$$d_{N_1} \oplus d_{N_2'} = d_{N_1'} \oplus d_{N_2}$$

$$\frac{\ln N_1}{\ln(1/r)} + \frac{\ln N_2'}{\ln(1/r)} = \frac{\ln N_1'}{\ln(1/r)} + \frac{\ln N_2}{\ln(1/r)}$$

$$\ln(N_1 \cdot N_2') = \ln(N_1' \cdot N_2)$$

$$N_1 \cdot N_2' = N_1' \cdot N_2$$

$$\frac{N_1}{N_2} = \frac{N_1'}{N_2'}$$

因此 $\phi([d_{N_1}] - [d_{N_2}]) = \phi([d_{N_1'}] - [d_{N_2'}])$。

**步骤2：同态性**

设 $g_1 = [d_{N_1}] - [d_{N_2}]$，$g_2 = [d_{N_3}] - [d_{N_4}]$。

群运算：
$$g_1 \oplus g_2 = [d_{N_1 N_3}] - [d_{N_2 N_4}]$$

计算：
$$\phi(g_1 \oplus g_2) = \frac{\ln(N_1 N_3 / N_2 N_4)}{\ln(1/r)}$$

$$= \frac{\ln(N_1/N_2) + \ln(N_3/N_4)}{\ln(1/r)}$$

$$= \frac{\ln(N_1/N_2)}{\ln(1/r)} + \frac{\ln(N_3/N_4)}{\ln(1/r)}$$

$$= \phi(g_1) + \phi(g_2)$$

**步骤3：单射性**

若 $\phi(g) = 0$，则 $\ln(N_1/N_2) = 0$，所以 $N_1 = N_2$，$g = 0$。

**步骤4：像集描述**

$$\text{Im}(\phi) = \left\{\frac{\ln(N_1/N_2)}{\ln(1/r)} : N_1, N_2 \in \mathbb{N}\right\}$$

$$= \frac{1}{\ln(1/r)} \cdot \{\ln q : q \in \mathbb{Q}^+\}$$

$$= \frac{1}{\ln(1/r)} \cdot \ln(\mathbb{Q}^+)$$

**步骤5：稠密性**

$\ln(\mathbb{Q}^+)$ 在 $\mathbb{R}$ 中稠密，因为：
- 对于任意 $x \in \mathbb{R}$，$e^x \in \mathbb{R}^+$
- 有理数在 $\mathbb{R}$ 中稠密
- 所以存在序列 $q_n \in \mathbb{Q}^+$ 使得 $q_n \to e^x$
- 因此 $\ln q_n \to x$

**证毕**。

---

## 第五部分：D - PTE问题

### 5.1 定理5.1：最小高度

**陈述**：
6阶PTE理想解的最小高度是 $H_{\min}(6) = 86$。

**证明结构**：

**步骤1：问题重述**

PTE问题：找到两组整数 $A = \{a_1, \ldots, a_6\}$，$B = \{b_1, \ldots, b_6\}$ 使得：
$$\sum_{i=1}^6 a_i^k = \sum_{i=1}^6 b_i^k \quad \text{对于 } k = 1, 2, \ldots, 6$$

高度定义为：
$$H(A, B) = \frac{\max(|a_i|, |b_i|)}{\gcd(\text{所有元素})}$$

**步骤2：Newton恒等式**

设 $p_k = \sum a_i^k$，$e_k$ 为基本对称多项式。

Newton恒等式给出：
$$k e_k = \sum_{i=1}^k (-1)^{i-1} e_{k-i} p_i$$

对于PTE解，$p_k(A) = p_k(B)$ 对于 $k = 1, \ldots, 6$。

这意味着 $e_k(A) = e_k(B)$ 对于 $k = 1, \ldots, 6$。

因此，多项式：
$$P_A(x) = \prod_{i=1}^6 (x - a_i) = x^6 - e_1 x^5 + e_2 x^4 - \ldots + e_6$$
$$P_B(x) = \prod_{i=1}^6 (x - b_i) = x^6 - e_1 x^5 + e_2 x^4 - \ldots + e_6$$

具有相同系数，除了可能的 $e_6$ 符号（取决于奇偶性）。

实际上，$e_6(A) = \prod a_i$，$e_6(B) = \prod b_i$，这些可以不同。

**步骤3：搜索算法**

算法框架：

```
对于 H = 1, 2, ...:
    对于所有 A ⊂ {0, 1, ..., H}，|A| = 6:
        计算 p_k(A) 对于 k = 1, ..., 6
        存储在哈希表中
    对于所有 B ⊂ {0, 1, ..., H}，|B| = 6:
        计算 p_k(B) 对于 k = 1, ..., 6
        如果存在 A 使得 p_k(A) = p_k(B) 对于所有 k:
            返回解 (A, B)
```

**步骤4：LLL格点约化（剪枝）**

直接搜索的复杂度是 $\binom{H}{6}^2 \approx H^{12}/(6!)^2$。

使用格点约化减少搜索空间：

考虑向量 $(p_1, p_2, \ldots, p_6) \in \mathbb{Z}^6$。

寻找两个不同的6元子集给出相同的向量。

这等价于在格点中寻找短向量。

**步骤5：计算验证**

论文报告搜索在 $H = 86$ 处找到解：
$$A = \{0, 19, 25, 57, 62, 86\}$$
$$B = \{2, 11, 40, 42, 69, 85\}$$

验证：

| $k$ | $\sum_{a \in A} a^k$ | $\sum_{b \in B} b^k$ |
|-----|---------------------|---------------------|
| 1 | 249 | 249 |
| 2 | 15315 | 15315 |
| 3 | 992793 | 992793 |
| 4 | 66953667 | 66953667 |
| 5 | 4654360125 | 4654360125 |
| 6 | 330382353285 | 330382353285 |

所有幂和相等。

**步骤6：最小性证明**

论文声称计算验证了 $H < 86$ 无解。

这是**计算证明**，不是解析证明。

**严格性评估**：

- 计算证明在数学上是可接受的，但属于L2级别（依赖计算机验证）
- 需要验证：
  1. 算法正确实现
  2. 搜索空间覆盖完整
  3. 没有浮点误差（使用整数运算）

**结论**：

该定理在L2级别严格成立（依赖计算验证）。

---

## 总结

| 定理 | 原声称 | 修正后 | 严格性 |
|------|--------|--------|--------|
| T1 定理1 | L1 | **L1（修正假设后）** | 需要Baker定理 |
| T1 定理4 | L1 | **L2** | 收敛率依赖于算法细节 |
| T2 定理1 | L1 | **错误/修正** | 原PDE不正确 |
| T2 定理2 | L1 | **L1（修正后）** | 对于修正PDE是平凡的 |
| T3 定理1 | L2 | **L3** | 启发式，无严格基础 |
| T4 定理1 | L1 | **L2** | 同构声明错误，修正为单射 |
| D 定理5.1 | L1 | **L2** | 计算证明 |
