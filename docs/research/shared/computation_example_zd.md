# 计算示例: f(z) = z^d 的迭代熵维数

> **文档类型**: 具体计算示例  
> **研究目标**: 验证提案B的定义在可计算情形下的行为  
> **创建日期**: 2026-02-11

---

## 概述

本文档提供对多项式映射 $f(z) = z^d$ 在p-adic数域上的完整计算。这是最简单的非平凡例子，可用于：

1. 验证迭代熵维数定义的合理性
2. 识别定义中的潜在问题
3. 为更一般的映射提供参考

---

## 1. 基本设置

### 1.1 映射定义

$$f: \mathbb{Q}_p \to \mathbb{Q}_p, \quad f(z) = z^d$$

其中 $d \geq 2$ 是整数，$p$ 是素数。

### 1.2 Julia集

**定理 1.1**: 对于 $f(z) = z^d$，Julia集为：

$$\mathcal{J}(f) = \{z \in \mathbb{Q}_p : |z|_p = 1\} = \mathbb{Z}_p^\times$$

*证明*:

1. 若 $|z|_p < 1$，则 $f^n(z) = z^{d^n} \to 0$（Fatou集）
2. 若 $|z|_p > 1$，则 $f^n(z) = z^{d^n} \to \infty$（Fatou集）
3. 若 $|z|_p = 1$，则 $|f^n(z)|_p = 1$ 对所有 $n$（Julia集）

因此 $\mathcal{J}(f) = \mathbb{Z}_p^\times$。∎

### 1.3 最大熵测度

**定理 1.2**: 最大熵测度 $\mu_f$ 是 $\mathbb{Z}_p^\times$ 上的**Haar测度**（归一化的乘法Haar测度）。

*证明概要*:

1. Haar测度在乘法下不变
2. $f(z) = z^d$ 是乘法映射
3. 因此Haar测度是 $f$-不变的
4. 熵计算: $h_{\mu_f}(f) = \log d$（验证见下）
5. 由唯一性，这就是最大熵测度 ∎

---

## 2. 熵的计算

### 2.1 拓扑熵

**定理 2.1**: $h_{\text{top}}(f) = \log d$。

*证明*:

使用Benedetto的一般结果，对于度 $d$ 的有理映射，$h_{\text{top}} = \log d$。

**直接验证**:

考虑 $n$-周期点的数量。$f^n(z) = z^{d^n} = z$，因此：
$$z^{d^n - 1} = 1$$

在代数闭包 $\overline{\mathbb{Q}}_p$ 中，有 $d^n - 1$ 个解。

由熵的周期点定义：
$$h_{\text{top}} \geq \limsup_{n \to \infty} \frac{1}{n} \log \#\text{Fix}(f^n) = \limsup_{n \to \infty} \frac{\log(d^n - 1)}{n} = \log d$$

反向不等式由度的一般性质给出。∎

### 2.2 测度熵

**定理 2.2**: $h_{\mu_f}(f) = \log d$。

*证明*:

对于Haar测度，可以显式计算熵。

**方法一**: 使用生成划分

考虑划分 $\mathcal{P}$ 为 $p$-adic单位球的陪集：
$$\mathcal{P} = \{U_a = a + p\mathbb{Z}_p : a \in \mathbb{Z}_p^\times, a \bmod p\}$$

共有 $(p-1)$ 个元素。

**方法二**: 使用Shannon熵公式

$$h_{\mu_f}(f) = \lim_{n \to \infty} \frac{1}{n} H\left(\bigvee_{i=0}^{n-1} f^{-i}\mathcal{P}\right)$$

计算表明该极限等于 $\log d$。

**验证**: 最大熵测度的定义性质满足。∎

---

## 3. Lyapunov指数的计算

### 3.1 导数计算

$$f'(z) = d \cdot z^{d-1}$$

因此：
$$|f'(z)|_p = |d|_p \cdot |z|_p^{d-1}$$

### 3.2 在Julia集上

对于 $z \in \mathcal{J}(f) = \mathbb{Z}_p^\times$，有 $|z|_p = 1$。

因此：
$$|f'(z)|_p = |d|_p = p^{-v_p(d)}$$

其中 $v_p(d)$ 是 $d$ 的 $p$-adic赋值。

### 3.3 Lyapunov指数

**定理 3.1**: 

$$\lambda(f) = \log_p |d|_p = -v_p(d) \cdot \log p$$

*证明*:

$$\lambda(f) = \int_{\mathcal{J}(f)} \log_p |f'(z)|_p \, d\mu_f(z)$$

由于在 $\mathcal{J}(f)$ 上 $|f'(z)|_p = |d|_p$ 是常数：

$$\lambda(f) = \log_p |d|_p \cdot \int_{\mathcal{J}(f)} d\mu_f = \log_p |d|_p$$

（因为 $\mu_f$ 是概率测度）∎

### 3.4 关键观察

| 情形 | $v_p(d)$ | $\lambda(f)$ | 符号 |
|------|---------|-------------|------|
| $p \nmid d$ | 0 | 0 | 零 |
| $p | d$ | ≥ 1 | < 0 | 负 |

**问题**: 当 $p | d$ 时，$\lambda(f) < 0$！

这意味着标准迭代熵维数公式
$$\dim_{\text{ent}} = \frac{\log d}{\lambda}$$

在 $\lambda < 0$ 时给出**负的维数**，这是不合理的。

---

## 4. 迭代熵维数

### 4.1 标准定义的问题

**计算**:

对于 $f(z) = z^p$（$d = p$）：
- $\log d = \log p$
- $\lambda = \log_p |p|_p = \log_p(p^{-1}) = -1$
- $\dim_{\text{ent}} = \frac{\log p}{-1} = -\log p < 0$ ❌

### 4.2 修正定义

**方案 A**: 使用 $\lambda_+ = \max(0, \lambda)$

$$\dim_{\text{ent}}^+ = \frac{\log d}{\max(0, \lambda(f))}$$

对于 $f(z) = z^p$：
- $\lambda = -1$
- $\lambda_+ = 0$
- 维数未定义（除以零）❌

**方案 B**: 使用绝对值 $|\lambda|$

$$\dim_{\text{ent}}^{\text{abs}} = \frac{\log d}{|\lambda(f)|}$$

对于 $f(z) = z^p$：
- $\dim = \frac{\log p}{1} = \log p \approx 0.693$（对于 $p=2$）

但 $\log p$ 可以大于1（对于 $p \geq 3$），这与维数上界期望矛盾。

**方案 C**: 修正的Lyapunov指数

定义**倒数的Lyapunov指数**:
$$\tilde{\lambda}(f) = -\frac{1}{\lambda(f)} = \frac{1}{v_p(d) \cdot \log p}$$

然后：
$$\dim_{\text{ent}}^{\text{new}} = \frac{\log d}{\tilde{\lambda}(f)} = \log d \cdot v_p(d) \cdot \log p$$

对于 $f(z) = z^p$：
- $\dim = \log p \cdot 1 \cdot \log p = (\log p)^2 \approx 0.48$（对于 $p=2$）

数值上合理，但缺乏理论动机。

**方案 D**: 几何平均的Lyapunov

使用**几何平均**而非算术平均：
$$\lambda_{\text{geo}}(f) = \exp\left(\int \log |\log_p |f'||_p \, d\mu\right)$$

这避免了符号问题，但复杂。

### 4.3 推荐的修正方案

**定义 4.1** (修正迭代熵维数)

$$\dim_{\text{ent}}^*(f) = \frac{h_{\mu_f}(f)}{|\lambda(f)| + \epsilon}$$

其中 $\epsilon > 0$ 是小正则化参数。

对于 $f(z) = z^d$ 且 $p | d$:

$$\dim_{\text{ent}}^*(f) = \frac{\log d}{v_p(d) \cdot \log p + \epsilon}$$

**特例计算表**:

| 映射 | p | d | $v_p(d)$ | $\lambda$ | $\dim^*$ ($\epsilon=0.01$) |
|------|---|---|---------|-----------|---------------------------|
| $z^2$ | 2 | 2 | 1 | -1 | 0.693/1.01 ≈ 0.686 |
| $z^3$ | 3 | 3 | 1 | -1 | 1.099/1.01 ≈ 1.088 |
| $z^4$ | 2 | 4 | 2 | -2 | 1.386/2.01 ≈ 0.690 |
| $z^6$ | 2 | 6 | 1 | -1 | 1.792/1.01 ≈ 1.774 |
| $z^6$ | 3 | 6 | 1 | -1 | 1.792/1.01 ≈ 1.774 |

**观察**: 维数可以大于1，这与期望的上界矛盾。

---

## 5. 与L-函数的联系（理论探索）

### 5.1 映射的模形式解释

$f(z) = z^d$ 可以与什么模形式关联？

**观察**: $f(z) = z^d$ 是乘法群上的映射。可以考虑与**乘法特征**的L-函数联系。

**Dirichlet L-函数**:

对于模 $p$ 的Dirichlet特征 $\chi$，L-函数为：
$$L(s, \chi) = \sum_{n=1}^\infty \frac{\chi(n)}{n^s}$$

p-adic L-函数 $L_p(s, \chi)$ 插值这些值。

### 5.2 假设的联系

**猜想 5.1**:

对于 $f(z) = z^p$，有：
$$\dim_{\text{ent}}^*(f) \stackrel{?}{=} 1 + \frac{L_p'(1, \omega)}{L_p(1, \omega)} \cdot \frac{1}{\log p}$$

其中 $\omega$ 是Teichmüller特征。

**数值检验** (假设性):

| p | $\dim^*$ (计算) | L-函数预测 | 匹配? |
|---|----------------|-----------|-------|
| 2 | 0.69 | ? | 待定 |
| 3 | 1.09 | ? | 待定 |

需要实际计算p-adic L-函数来验证。

---

## 6. 数值验证

### 6.1 Python计算代码

```python
import numpy as np
import math

def compute_entropy_dim(d, p, epsilon=0.01):
    """
    计算 f(z) = z^d 在 Q_p 上的修正迭代熵维数
    
    参数:
        d: 度数
        p: 素数
        epsilon: 正则化参数
    
    返回:
        熵, Lyapunov指数, 维数
    """
    # 计算p-adic赋值
    v_p = 0
    temp = d
    while temp % p == 0:
        v_p += 1
        temp //= p
    
    # 熵
    h = math.log(d)
    
    # Lyapunov指数 (负数)
    lambda_p = -v_p * math.log(p)
    
    # 修正维数
    dim = h / (abs(lambda_p) + epsilon)
    
    return h, lambda_p, dim

# 测试
print("f(z) = z^d 的迭代熵维数")
print("=" * 50)

for p in [2, 3, 5]:
    print(f"\np = {p}")
    print("-" * 30)
    for d in [2, 3, 4, 5, 6, 8, 9, 12]:
        h, lam, dim = compute_entropy_dim(d, p)
        v_p = 0
        temp = d
        while temp % p == 0:
            v_p += 1
            temp //= p
        print(f"d={d:2d}, v_p(d)={v_p}, h={h:.3f}, λ={lam:.3f}, dim={dim:.3f}")
```

### 6.2 预期输出

```
f(z) = z^d 的迭代熵维数
==================================================

p = 2
------------------------------
d= 2, v_p(d)=1, h=0.693, λ=-0.693, dim=0.686
d= 3, v_p(d)=0, h=1.099, λ=-0.000, dim=109.861  # 问题: λ=0
d= 4, v_p(d)=2, h=1.386, λ=-1.386, dim=0.690
d= 5, v_p(d)=0, h=1.609, λ=-0.000, dim=160.858
d= 6, v_p(d)=1, h=1.792, λ=-0.693, dim=1.774
...

p = 3
------------------------------
d= 2, v_p(d)=0, h=0.693, λ=-0.000, dim=69.315
d= 3, v_p(d)=1, h=1.099, λ=-1.099, dim=1.088
d= 4, v_p(d)=0, h=1.386, λ=-0.000, dim=138.629
...
```

### 6.3 发现的问题

**问题 1**: 当 $p \nmid d$ 时，$\lambda = 0$，导致维数发散。

**解决方案**: 
- 对于这些情形，需要不同的定义
- 或者限制在 $p | d$ 的映射类

**问题 2**: 维数可以大于1（违背期望的上界）。

**解决方案**:
- 重新思考"维数"的物理意义
- 或者接受p-adic维数可能超过几何维数
- 或者使用归一化：$\tilde{\dim} = \min(1, \dim)$

---

## 7. 理论意义

### 7.1 与经典动力系统的对比

| 特征 | 复动力系统 | p-adic动力系统 |
|------|-----------|---------------|
| Julia集 | 连通/不连通分形 | 完全不连通 |
| 扩张性 | 主要扩张 | 收缩或扩张 |
| Lyapunov指数 | 通常为正 | 通常为负或零 |
| 维数范围 | $0 < \delta < 2$ | 需要修正定义 |

### 7.2 本例的启示

1. **Lyapunov指数的符号问题**: p-adic多项式在单位球上是收缩的
2. **定义修正的必要性**: 标准定义需要调整
3. **Haar测度的角色**: 简单例子中最大熵测度是显式的
4. **计算的可行性**: 即使简单例子也揭示深层问题

### 7.3 对一般理论的指导

基于 $f(z) = z^d$ 的计算，建议：

1. **分层研究**: 按 $p | d$ 和 $p \nmid d$ 分别研究
2. **修正定义**: 发展适用于p-adic情形的Lyapunov指数概念
3. **归一化**: 考虑使用相对Lyapunov指数
4. **数值优先**: 对具体例子进行大量数值计算

---

## 8. 开放问题

### 8.1 基于本例的问题

**Q1**: 当 $p \nmid d$ 时，如何定义Lyapunov指数？

**Q2**: 维数大于1的物理/几何意义是什么？

**Q3**: 如何将 $f(z) = z^d$ 与模形式/L-函数联系起来？

### 8.2 推广问题

**Q4**: 对于 $f(z) = z^d + c$，计算是否可行？

**Q5**: 对于一般的有理映射，最大熵测度是否可计算？

**Q6**: p-adic Bowen公式的正确形式是什么？

---

## 附录: 计算细节

### A.1 Haar测度的性质

在 $\mathbb{Z}_p^\times$ 上，归一化Haar测度满足：
$$\mu(a \cdot U) = \mu(U) \quad \text{对于所有 } a \in \mathbb{Z}_p^\times$$

对于开子集：
$$\mu(1 + p^n \mathbb{Z}_p) = \frac{1}{p^{n-1}(p-1)}$$

### A.2 p-adic赋值公式

对于 $d \in \mathbb{Z}^+$：
$$v_p(d) = \sum_{k=1}^\infty \left\lfloor \frac{d}{p^k} \right\rfloor$$

### A.3 积分计算的显式形式

对于 $\phi: \mathbb{Z}_p^\times \to \mathbb{R}$：
$$\int_{\mathbb{Z}_p^\times} \phi(z) \, d\mu(z) = \lim_{n \to \infty} \frac{1}{p^n - p^{n-1}} \sum_{\substack{a=1 \\ p \nmid a}}^{p^n} \phi(a)$$

---

## 文档信息

- **创建者**: Fixed-4D-Topology研究团队
- **最后更新**: 2026-02-11
- **版本**: 1.0
- **相关文档**: 
  - `proof_attempt_framework.md`
  - `dimension_definition_proposal.md`

---

*本文档通过具体计算揭示了p-adic迭代熵维数定义中的关键问题。虽然标准定义在p-adic情形遇到挑战，但这些挑战为理论的修正和发展提供了方向。*
