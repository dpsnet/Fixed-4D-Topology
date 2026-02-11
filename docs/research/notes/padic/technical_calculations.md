# p-adic热力学形式：技术计算与例子

## 1. 简单例子：$f(z) = z^d$ 在 $\mathbb{Q}_p$

### 1.1 动力系统分析

考虑多项式映射：
$$f(z) = z^d, \quad d \geq 2$$

在p-adic域$\mathbb{Q}_p$上的动力学行为：

**Filtration结构**：
- $\mathbb{D}_p = \{z \in \mathbb{Q}_p : |z|_p < 1\}$（开单位圆盘）
- $\mathbb{Z}_p = \{z \in \mathbb{Q}_p : |z|_p \leq 1\}$（闭单位圆盘）
- $\mathbb{Q}_p \setminus \mathbb{Z}_p = \{z : |z|_p > 1\}$

**动力学行为**：
| 区域 | 行为 |
|------|------|
| $|z|_p < 1$ | $f^n(z) \to 0$（吸引） |
| $|z|_p = 1$ | $|f^n(z)|_p = 1$（中性/不变） |
| $|z|_p > 1$ | $|f^n(z)|_p \to \infty$（排斥到$\infty$） |

**Fatou集**：$F(f) = \mathbb{D}_p \cup (\mathbb{Q}_p \setminus \mathbb{Z}_p)$

**Julia集**：$J(f) = \{z : |z|_p = 1\}$（单位圆的p-adic类比）

### 1.2 周期点计算

**$n$-周期点**：满足$f^n(z) = z$，即$z^{d^n} = z$。

解：$z = 0$，$z^{d^n - 1} = 1$的根。

**计数**：
- 在$\mathbb{Q}_p$中：取决于$(d^n-1)$与$p$的关系
- 在$\overline{\mathbb{Q}}_p$（代数闭包）中：恰好$d^n$个（计重数）
- 在$\mathbb{C}_p$（完备代数闭包）中：相同

**原始$n$-周期点**：
$$\# \text{Per}_n(f) = \sum_{k|n} \mu(n/k) d^k$$

（其中$\mu$是Möbius函数）

### 1.3 导数计算

$$f'(z) = d \cdot z^{d-1}$$

**在周期点上**：
对于满足$z^{d^n-1} = 1$的$n$-周期点：
$$f^n'(z) = \prod_{k=0}^{n-1} f'(f^k(z)) = \prod_{k=0}^{n-1} d \cdot z^{d^k(d-1)}$$

化简：
$$f^n'(z) = d^n \cdot z^{(d-1)\sum_{k=0}^{n-1} d^k} = d^n \cdot z^{d^n - 1} = d^n$$

（因为$z^{d^n-1} = 1$）

**关键结果**：对所有原始$n$-周期点，$f^n'(z) = d^n$。

### 1.4 p-adic范数

$$|f^n'(z)|_p = |d^n|_p = p^{-n \cdot v_p(d)}$$

其中$v_p(d)$是$d$的p-adic赋值。

**分类**：
- 如果$p \nmid d$：$|f^n'(z)|_p = 1$（中性）
- 如果$p | d$：$|f^n'(z)|_p < 1$（收缩）

## 2. 压力函数计算

### 2.1 划分函数

对于势函数$\phi_s(z) = -s \cdot \log |f'(z)|_p$：

$$Z_n(s) = \sum_{z \in \text{Fix}(f^n)} |f^n'(z)|_p^{-s}$$

**详细计算**：

不动点包括：
1. $z = 0$：$f^n(0) = 0$，$f^n'(0) = 0$（如果$n \geq 1$且$d \geq 2$）
   - 贡献：$|0|_p^{-s}$（奇异，需要正则化）
   
2. $z^{d^n-1} = 1$的$d^n - 1$个根：
   - 每个贡献：$|d^n|_p^{-s} = p^{n s \cdot v_p(d)}$

**正则化处理**：
排除$z = 0$（它是超吸引的），考虑：
$$Z_n^{\text{reg}}(s) = (d^n - 1) \cdot p^{n s \cdot v_p(d)}$$

### 2.2 压力函数

$$P(s) = \lim_{n \to \infty} \frac{1}{n} \log Z_n^{\text{reg}}(s)$$
$$= \lim_{n \to \infty} \frac{1}{n} \left[\log(d^n - 1) + n s v_p(d) \log p\right]$$
$$= \log d + s \cdot v_p(d) \cdot \log p$$

**结果**：
$$\boxed{P(s) = \log d + s \cdot \log |d|_p^{-1}}$$

### 2.3 性质分析

**线性依赖**：压力函数是$s$的线性函数！

这与实数情形形成对比，其中压力函数通常是非线性的。

**斜率**：$\frac{dP}{ds} = \log |d|_p^{-1} = v_p(d) \cdot \log p \geq 0$

**截距**：$P(0) = \log d = h_{\text{top}}(f)$（拓扑熵）

## 3. Bowen公式验证

### 3.1 Julia集的维数

对于$f(z) = z^d$，Julia集是单位球面：
$$J(f) = \{z \in \mathbb{C}_p : |z|_p = 1\}$$

**p-adic维数**：

根据Chistyakov（1996-1997）的工作，$\mathbb{Z}_p$在连续映射下的像的Hausdorff维数可以计算。

单位圆$|z|_p = 1$同胚于$\mathbb{Z}_p^\times$（p-adic单位群）。

**维数公式**：
$$\dim_H^{(p)}(\mathbb{Z}_p^\times) = 1$$

（作为$\mathbb{Z}_p$的子集）

### 3.2 解Bowen方程

解$P(\delta) = 0$：
$$\log d + \delta \cdot \log |d|_p^{-1} = 0$$
$$\delta = -\frac{\log d}{\log |d|_p} = \frac{\log d}{v_p(d) \cdot \log p}$$

**特殊情况**：

1. **$p \nmid d$**：$v_p(d) = 0$，公式发散
   - 这与$|d|_p = 1$（中性情形）一致
   - 需要不同的分析方法

2. **$p | d$**：$v_p(d) \geq 1$
   - $\delta = \frac{\log d}{v_p(d) \cdot \log p}$
   - 例如：$d = p$，$\delta = 1$

### 3.3 维数比较

| $d$ | $v_p(d)$ | Bowen公式给出的$\delta$ | 几何维数 | 匹配？ |
|-----|---------|----------------------|---------|-------|
| $p$ | 1 | 1 | 1 | ✓ |
| $p^k$ | $k$ | $1/k$ | ? | 待验证 |
| $2$ ($p=2$) | 1 | 1 | 1 | ✓ |
| $4$ ($p=2$) | 2 | $\frac{\log 4}{2\log 2} = 1$ | ? | 待验证 |

## 4. p-adic Dynamical Zeta函数

### 4.1 定义

**p-adic动力zeta函数**：
$$\zeta_f(z, s) = \exp\left(\sum_{n=1}^{\infty} \frac{z^n}{n} Z_n(s)\right)$$

其中：
$$Z_n(s) = \sum_{x \in \text{Fix}(f^n)} |f^n'(x)|_p^{-s}$$

### 4.2 $f(z) = z^d$的计算

$$Z_n(s) = (d^n - 1) \cdot |d^n|_p^{-s} = (d^n - 1) \cdot p^{n s v_p(d)}$$

**zeta函数**：
$$\zeta_f(z, s) = \exp\left(\sum_{n=1}^{\infty} \frac{z^n}{n} (d^n - 1) p^{n s v_p(d)}\right)$$

$$= \exp\left(\sum_{n=1}^{\infty} \frac{(z d p^{s v_p(d)})^n}{n} - \sum_{n=1}^{\infty} \frac{(z p^{s v_p(d)})^n}{n}\right)$$

$$= \frac{1 - z p^{s v_p(d)}}{1 - z d p^{s v_p(d)}}$$

**结果**：
$$\boxed{\zeta_f(z, s) = \frac{1 - z |d|_p^s}{1 - z d |d|_p^s}}$$

### 4.3 解析性质

**零点**：$z = |d|_p^{-s}$

**极点**：$z = (d |d|_p^s)^{-1} = d^{-1} |d|_p^{-s}$

**与压力的关系**：

zeta函数在$z = e^{-P(s)}$处有极点。

验证：
$$e^{-P(s)} = e^{-\log d - s \log |d|_p^{-1}} = d^{-1} |d|_p^s$$

这与极点位置一致！

## 5. Ruelle算子的谱分析

### 5.1 算子定义

对于$X = \mathbb{Z}_p^\times$（单位圆），$f(z) = z^d$：

$$(\mathcal{L}_s g)(x) = \sum_{y^d = x} |f'(y)|_p^{-s} g(y) = |d|_p^{-s} \sum_{y^d = x} g(y)$$

**逆像**：$y^d = x$在$\mathbb{Z}_p^\times$中有$d$个解（如果$p \nmid d$且$x \in \mathbb{Z}_p^\times$）。

### 5.2 特征函数

**常数函数**：$g(x) \equiv 1$

$$(\mathcal{L}_s 1)(x) = |d|_p^{-s} \cdot d = d |d|_p^{-s}$$

因此$\lambda_s = d |d|_p^{-s} = e^{P(s)}$是特征值，特征函数为常数。

**Fourier特征函数**：

考虑特征$\chi: \mathbb{Z}_p^\times \to \mathbb{C}^*$。

$$(\mathcal{L}_s \chi)(x) = |d|_p^{-s} \sum_{y^d = x} \chi(y)$$

如果$\chi$是$d$阶特征（即$\chi^d = 1$），则：
$$\chi(y) = \chi(x)^{1/d}$$

更仔细地，对于$y^d = x$，如果$\chi$满足$\chi(z^d) = \chi(z)^d = \chi(z)$对所有$z$成立（即$\chi^{d-1} = 1$），则：
$$(\mathcal{L}_s \chi)(x) = |d|_p^{-s} \cdot d \cdot \chi(x) = \lambda_s \chi(x)$$

**谱分析**：

主特征值$\lambda_s = d |d|_p^{-s}$是简单的。

其他特征值：如果存在$\chi$使得$\sum_{y^d = x} \chi(y) = 0$，则得到更小的特征值。

### 5.3 谱半径

$$\rho(\mathcal{L}_s) = |d|_p^{-s} \cdot d = e^{P(s)}$$

这验证了$\log \rho(\mathcal{L}_s) = P(s)$。

## 6. 变分原理的验证

### 6.1 测度熵

对于$f(z) = z^d$，最大熵测度是Haar测度$\mu$在$\mathbb{Z}_p^\times$上。

**拓扑熵**：
$$h_{\text{top}}(f) = \log d$$

**测度熵**：
对于Haar测度$\mu$，$h_\mu(f) = \log d$。

### 6.2 积分计算

对于$\phi_s(z) = -s \log |f'(z)|_p = -s \log |d|_p = s \cdot v_p(d) \cdot \log p$（在$|z|_p = 1$上常数）：

$$\int \phi_s \, d\mu = s \cdot v_p(d) \cdot \log p = s \cdot \log |d|_p^{-1}$$

### 6.3 变分验证

$$h_\mu(f) + \int \phi_s \, d\mu = \log d + s \cdot \log |d|_p^{-1} = P(s)$$

因此Haar测度是平衡态！

**唯一性**：由于系统是一致扩张的（在适当意义下），平衡态应该唯一。

## 7. 一般多项式的考虑

### 7.1 $f(z) = z^d + c$（p-adic Mandelbrot集）

**参数空间**：$c \in \mathbb{Q}_p$

**关键区域**：
- $|c|_p$很小：结构类似于$z^d$
- $|c|_p$适中：可能出现复杂的动力学
- $|c|_p$很大：$\infty$是吸引的

### 7.2 压力函数的数值计算

**算法**：

```
输入：多项式f，势函数参数s，迭代次数N

1. 计算所有周期点直到周期N
2. 对每个周期点x，计算|f^n'(x)|_p
3. 计算Z_n(s) = sum(|f^n'(x)|_p^(-s))
4. 估计P(s) = (1/n) * log(Z_n(s))

输出：P(s)的估计值
```

**数值挑战**：
- p-adic周期点的计算
- 高精度p-adic算术
- 收敛速度估计

## 8. 与其他理论的关联

### 8.1 p-adic统计力学

根据Khrennikov的工作，p-adic统计力学模型中：

**配分函数**：
$$Z = \sum_{\text{状态}} e^{-\beta E}$$

其中"温度"$\beta$可以是p-adic数。

**联系**：我们的压力函数$P(s)$对应于自由能，$s$对应于逆温度。

### 8.2 IFS热力学形式

Fan和Lau（1999）以及后续工作建立了IFS的热力学形式：

**p-adic IFS**：考虑收缩映射$\{\phi_i: \mathbb{Z}_p \to \mathbb{Z}_p\}$

**转移算子**：
$$(\mathcal{L}g)(x) = \sum_i p_i(x) g(\phi_i(x))$$

这与我们的Ruelle算子有联系。

### 8.3 zeta函数的adelic乘积

**adelic观点**：

对于$f(z) = z^d$，在 completions of $\mathbb{Q}$ 上：

$$\zeta_f^{\text{adelic}}(s) = \prod_{p \leq \infty} \zeta_{f,p}(s)$$

其中$\zeta_{f,\infty}$是实数情形的zeta函数，$\zeta_{f,p}$是p-adic zeta函数。

**有趣的问题**：adelic zeta函数是否包含算术信息？

## 9. 开放问题

### 9.1 理论问题

1. **非线性压力函数**：对于哪些p-adic映射，压力函数是非线性的？

2. **相变**：p-adic热力学形式是否存在相变？

3. **谱间隙**：p-adic Ruelle算子是否有谱间隙？

4. **解析性**：压力函数是否关于势函数解析？

### 9.2 计算问题

1. **高效算法**：如何高效计算p-adic周期点？

2. **数值验证**：如何数值验证Bowen公式？

3. **可视化**：如何可视化p-adic Julia集？

### 9.3 应用问题

1. **算术几何**：p-adic热力学形式与椭圆曲线的联系？

2. **数论**：与zeta函数和L函数的联系？

3. **物理**：在p-adic物理模型中的应用？
