# P-adic数计算练习解答

## 目录
1. [基本概念与符号说明](#基本概念与符号说明)
2. [练习1: p-adic数的基本创建](#练习1-p-adic数的基本创建)
3. [练习2: p-adic绝对值与赋值](#练习2-p-adic绝对值与赋值)
4. [练习3: 基本运算验证](#练习3-基本运算验证)
5. [练习4: Hensel引理应用](#练习4-hensen引理应用)
6. [练习5: p-adic级数展开](#练习5-p-adic级数展开)
7. [练习6: 综合问题解答](#练习6-综合问题解答)
8. [常见问题与注意事项](#常见问题与注意事项)

---

## 基本概念与符号说明

### 定义回顾

**p-adic赋值** (p-adic valuation): 对于非零有理数 $x = p^n \frac{a}{b}$，其中 $p \nmid a, p \nmid b$，定义
$$v_p(x) = n$$

**p-adic绝对值** (p-adic absolute value):
$$|x|_p = p^{-v_p(x)}$$
约定 $|0|_p = 0$。

**p-adic数的标准形式**:
$$x = p^{v_p(x)} \cdot u$$
其中 $u$ 是 p-adic 单位（即 $|u|_p = 1$）。

### 符号约定
- $\mathbb{Q}_p$: p-adic数域
- $\mathbb{Z}_p$: p-adic整数环
- $\mathbb{Z}_p^\times$: p-adic单位群
- $v_p(x)$: p-adic赋值
- $|x|_p$: p-adic绝对值

---

## 练习1: p-adic数的基本创建

### 解答1.1: 不同素数p的p-adic数创建

**问题**: 在 $\mathbb{Q}_2, \mathbb{Q}_3, \mathbb{Q}_5, \mathbb{Q}_7$ 中创建相同的整数和分数。

**解答**:

```python
# 代码实现
import padic

primes = [2, 3, 5, 7]
for p in primes:
    # 从整数创建
    a = padic.Padic.from_int(100, p=p, N=20)
    
    # 从分数创建
    b = padic.Padic.from_frac(1, p+1, p=p, N=15)
    
    # 直接构造: p^v * s
    c = padic.Padic(20, 3, 2, p)  # p^3 * 2
```

**关键观察**:
1. 同一个有理数在不同p-adic域中有不同的展开
2. 整数100 = $2^2 \cdot 25$ 在 $\mathbb{Q}_2$ 中赋值为2
3. 整数100 = $5^2 \cdot 4$ 在 $\mathbb{Q}_5$ 中赋值为2

### 解答1.2: p-adic展开式

**问题**: 计算数在p-adic域中的展开式。

**理论背景**:
每个p-adic整数 $x \in \mathbb{Z}_p$ 有唯一的展开:
$$x = a_0 + a_1 p + a_2 p^2 + a_3 p^3 + \cdots$$
其中 $a_i \in \{0, 1, \ldots, p-1\}$。

**具体例子** (在 $\mathbb{Q}_5$ 中):

| 数值 | p-adic展开 |
|------|-----------|
| 1 | $1$ |
| 2 | $2$ |
| 3 | $3$ |
| $\frac{1}{2}$ | $3 + 2\cdot5 + 2\cdot5^2 + 2\cdot5^3 + \cdots$ |
| $\frac{1}{3}$ | $2 + 3\cdot5 + 1\cdot5^2 + 3\cdot5^3 + \cdots$ |

**验证 $\frac{1}{2}$ 的展开**:

我们需要找到 $x$ 使得 $2x = 1$ 在 $\mathbb{Z}_5$ 中。

设 $x = a_0 + a_1 \cdot 5 + a_2 \cdot 5^2 + \cdots$

**模5**: $2a_0 \equiv 1 \pmod{5}$

由于 $2 \cdot 3 = 6 \equiv 1 \pmod{5}$，所以 $a_0 = 3$。

**模25**: $2(a_0 + 5a_1) \equiv 1 \pmod{25}$
$6 + 10a_1 \equiv 1 \pmod{25}$
$10a_1 \equiv -5 \equiv 20 \pmod{25}$
$2a_1 \equiv 4 \pmod{5}$
$a_1 = 2$

继续这个过程得到展开式: $x = 3 + 2\cdot 5 + 2\cdot 5^2 + \cdots$

---

## 练习2: p-adic绝对值与赋值

### 解答2.1: p-adic赋值和绝对值计算

**问题**: 计算不同整数的 $v_p(n)$ 和 $|n|_p$。

**算法**:
```python
def padic_valuation(n, p):
    """计算p-adic赋值"""
    if n == 0:
        return float('inf')
    val = 0
    while n % p == 0:
        n //= p
        val += 1
    return val

def padic_absolute_value(n, p):
    """计算p-adic绝对值"""
    if n == 0:
        return 0
    return p ** (-padic_valuation(n, p))
```

**关键数值表**:

| n | $v_2(n)$ | $\|n\|_2$ | $v_3(n)$ | $\|n\|_3$ |
|---|---------|----------|---------|----------|
| 1 | 0 | 1.000000 | 0 | 1.000000 |
| 2 | 1 | 0.500000 | 0 | 1.000000 |
| 3 | 0 | 1.000000 | 1 | 0.333333 |
| 4 | 2 | 0.250000 | 0 | 1.000000 |
| 6 | 1 | 0.500000 | 1 | 0.333333 |
| 8 | 3 | 0.125000 | 0 | 1.000000 |
| 9 | 0 | 1.000000 | 2 | 0.111111 |
| 12 | 2 | 0.250000 | 1 | 0.333333 |
| 16 | 4 | 0.062500 | 0 | 1.000000 |
| 18 | 1 | 0.500000 | 2 | 0.111111 |

### 解答2.2: 强三角不等式验证

**理论**: p-adic绝对值满足**强三角不等式**:
$$|x + y|_p \leq \max(|x|_p, |y|_p)$$

当 $|x|_p \neq |y|_p$ 时，等号成立:
$$|x + y|_p = \max(|x|_p, |y|_p)$$

**证明**:

设 $v_p(x) = m, v_p(y) = n$，不妨设 $m \leq n$。

则 $x = p^m \cdot u, y = p^n \cdot v$，其中 $u, v$ 是p-adic单位。

$$x + y = p^m(u + p^{n-m}v)$$

由于 $n - m \geq 0$，我们有 $u + p^{n-m}v \in \mathbb{Z}_p$。

**情况1**: 如果 $m < n$，则 $u + p^{n-m}v \equiv u \not\equiv 0 \pmod{p}$，所以 $v_p(x+y) = m$。

**情况2**: 如果 $m = n$，则 $x + y = p^m(u + v)$，可能有 $v_p(x+y) \geq m$。

因此:
$$|x + y|_p = p^{-v_p(x+y)} \leq p^{-m} = \max(p^{-m}, p^{-n}) = \max(|x|_p, |y|_p)$$

**验证结果**:

在 $\mathbb{Q}_5$ 中:

| x | y | $\|x\|_5$ | $\|y\|_5$ | $\|x+y\|_5$ | 验证结果 |
|---|---|----------|----------|------------|---------|
| 25 | 5 | 0.04 | 0.20 | 0.20 | ✓ 等号 |
| 25 | 50 | 0.04 | 0.04 | 0.04 | ✓ |
| 5 | 3 | 0.20 | 1.00 | 1.00 | ✓ 等号 |
| 125 | 25 | 0.008 | 0.04 | 0.04 | ✓ 等号 |
| 1 | 4 | 1.00 | 1.00 | 0.04 | ✓ 严格 |

**现象解释**:

最后一种情况 $|1 + 4|_5 = |5|_5 = 0.04 < \max(1, 1) = 1$，这是严格不等式，因为两个数的赋值相同（都是0），但它们的和在模5下为0。

---

## 练习3: 基本运算验证

### 解答3.1: 加减乘除运算

**问题**: 在 $\mathbb{Q}_7$ 中验证基本运算。

**结果**:

设 $a = 10, b = 3, c = \frac{1}{2}$ 在 $\mathbb{Q}_7$ 中:

| 运算 | 结果 | 验证 |
|-----|------|-----|
| $a + b$ | 13 | ✓ |
| $a - b$ | 7 | ✓ |
| $a \times b$ | 30 | ✓ |
| $a \times c$ | 5 | ✓ (10 × 1/2 = 5) |
| $a^3$ | 1000 | ✓ |

### 解答3.2: 运算性质验证

**结合律**: $(a + b) + c = a + (b + c)$

在 $\mathbb{Q}_5$ 中，设 $a = 2, b = 3, c = 4$:
- $(a + b) + c = 5 + 4 = 9$
- $a + (b + c) = 2 + 7 = 9$ ✓

**分配律**: $a \times (b + c) = a \times b + a \times c$

- $a \times (b + c) = 2 \times 7 = 14$
- $a \times b + a \times c = 6 + 8 = 14$ ✓

---

## 练习4: Hensel引理应用

### 解答4.1: 计算平方根

**Hensel引理**: 

设 $f(x) \in \mathbb{Z}_p[x]$，$a_0 \in \mathbb{Z}$ 满足:
1. $f(a_0) \equiv 0 \pmod{p}$
2. $f'(a_0) \not\equiv 0 \pmod{p}$

则存在唯一的 $\alpha \in \mathbb{Z}_p$ 使得 $f(\alpha) = 0$ 且 $\alpha \equiv a_0 \pmod{p}$。

#### (a) √2 在 $\mathbb{Q}_7$ 中

**问题**: 2在$\mathbb{Q}_7$中是否有平方根？

**解答**:

检查模7: $x^2 \equiv 2 \pmod{7}$

测试: $3^2 = 9 \equiv 2 \pmod{7}$ ✓

$f(x) = x^2 - 2$，$f'(x) = 2x$

$f'(3) = 6 \not\equiv 0 \pmod{7}$ ✓

由Hensel引理，存在唯一的 $\sqrt{2} \in \mathbb{Z}_7$ 满足 $\sqrt{2} \equiv 3 \pmod{7}$。

**计算结果**:
```
√2 = 3 + 1·7 + 2·7² + 6·7³ + ...
```

#### (b) √(-1) 在 $\mathbb{Q}_5$ 中

**问题**: -1在$\mathbb{Q}_5$中是否有平方根？

**解答**:

检查模5: $x^2 \equiv -1 \equiv 4 \pmod{5}$

测试: $2^2 = 4 \equiv -1 \pmod{5}$ ✓

$f(x) = x^2 + 1$，$f'(x) = 2x$

$f'(2) = 4 \not\equiv 0 \pmod{5}$ ✓

由Hensel引理，存在 $\sqrt{-1} \in \mathbb{Z}_5$。

**计算结果**:
```
√(-1) = 2 + 1·5 + 2·5² + ...
```

#### (c) √2 在 $\mathbb{Q}_3$ 中

**问题**: 2在$\mathbb{Q}_3$中是否有平方根？

**解答**:

检查模3: $x^2 \equiv 2 \pmod{3}$

测试:
- $0^2 = 0 \not\equiv 2$
- $1^2 = 1 \not\equiv 2$
- $2^2 = 4 \equiv 1 \not\equiv 2$

**结论**: 2不是模3的二次剩余，因此2在$\mathbb{Q}_3$中没有平方根。

**理论解释**: 

对于奇素数 $p$，$-1$ 是模 $p$ 的二次剩余当且仅当 $p \equiv 1 \pmod{4}$。

对于 $p = 3 \equiv 3 \pmod{4}$，$-1$ 不是模3的二次剩余。

更一般地，2是模 $p$ 的二次剩余当且仅当 $p \equiv \pm 1 \pmod{8}$。

对于 $p = 7 \equiv -1 \pmod{8}$，2是二次剩余 ✓

对于 $p = 3 \equiv 3 \pmod{8}$，2不是二次剩余 ✗

### 解答4.2: 解多项式方程

**问题**: 解 $x^3 - 2 = 0$ 在 $\mathbb{Q}_5$ 中。

**解答**:

检查模5: $x^3 \equiv 2 \pmod{5}$

测试:
- $0^3 = 0$
- $1^3 = 1$
- $2^3 = 8 \equiv 3$
- $3^3 = 27 \equiv 2$ ✓
- $4^3 = 64 \equiv 4$

所以 $x_0 = 3$ 是模5的解。

$f(x) = x^3 - 2$，$f'(x) = 3x^2$

$f'(3) = 27 \equiv 2 \not\equiv 0 \pmod{5}$ ✓

由Hensel引理，存在唯一的 $p$-adic解。

---

## 练习5: p-adic级数展开

### 解答5.1: p-adic指数函数

**定义**:
$$\exp(x) = \sum_{n=0}^{\infty} \frac{x^n}{n!}$$

**收敛条件**: 在 $\mathbb{Q}_p$ 中，$\exp(x)$ 收敛当且仅当 $|x|_p < p^{-1/(p-1)}$。

**收敛半径**:

| p | 收敛半径 $p^{-1/(p-1)}$ |
|---|---------------------|
| 2 | $1/2 = 0.5$ |
| 3 | $3^{-1/2} \approx 0.577$ |
| 5 | $5^{-1/4} \approx 0.669$ |
| 7 | $7^{-1/6} \approx 0.732$ |

**性质**: $\exp(x + y) = \exp(x)\exp(y)$（当两边都收敛时）

**验证**:

在 $\mathbb{Q}_5$ 中，取 $x = 5$:
- $|5|_5 = 1/5 < 5^{-1/4} \approx 0.669$ ✓
- $\exp(5)$ 收敛
- $\exp(5) \cdot \exp(-5) = 1$ ✓

### 解答5.2: p-adic对数函数

**定义**:
$$\log(1 + x) = \sum_{n=1}^{\infty} (-1)^{n+1} \frac{x^n}{n}$$

**收敛条件**: 在 $\mathbb{Q}_p$ 中，$\log(1+x)$ 收敛当且仅当 $|x|_p < 1$（即 $x \equiv 0 \pmod{p}$）。

**等价表述**: $\log(y)$ 对 $y \equiv 1 \pmod{p}$ 有定义。

**性质**: $\log(\exp(x)) = x$ 和 $\exp(\log(1+x)) = 1+x$（在收敛域内）

### 解答5.3: p-adic三角函数

**定义**:
$$\sin(x) = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{(2n+1)!}$$

$$\cos(x) = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n}}{(2n)!}$$

**收敛条件**: 与 $\exp$ 相同，$|x|_p < p^{-1/(p-1)}$。

**重要观察**: 由于阶乘的分母，收敛半径通常很小。

**验证恒等式**: $\sin^2(x) + \cos^2(x) = 1$

---

## 练习6: 综合问题解答

### 解答6.1: p-adic整数的单位群结构

**定理**: 
$$\mathbb{Z}_p^\times \cong \mu_{p-1} \times (1 + p\mathbb{Z}_p)$$

其中:
- $\mu_{p-1}$ 是 $(p-1)$ 次单位根群（有限循环群）
- $1 + p\mathbb{Z}_p$ 是主单位群（pro-$p$群）

**结构分析**:

| p | $\mathbb{Z}_p^\times$ 结构 |
|---|--------------------------|
| 3 | $\mu_2 \times (1+3\mathbb{Z}_3) \cong \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}_3$ |
| 5 | $\mu_4 \times (1+5\mathbb{Z}_5) \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}_5$ |
| 7 | $\mu_6 \times (1+7\mathbb{Z}_7) \cong \mathbb{Z}/6\mathbb{Z} \times \mathbb{Z}_7$ |

**应用**: 这个结构在类域论和局部类域论中非常重要。

### 解答6.2: p-adic球的性质

**定义**: 以 $x$ 为中心，半径 $r = p^{-n}$ 的开球:
$$B(x, r) = \{y \in \mathbb{Q}_p : |x - y|_p < r\} = x + p^n \mathbb{Z}_p$$

**闭球**:
$$\overline{B}(x, r) = \{y \in \mathbb{Q}_p : |x - y|_p \leq r\} = x + p^n \mathbb{Z}_p$$

**惊人性质**:

1. **每个点都是中心**: 若 $y \in B(x, r)$，则 $B(x, r) = B(y, r)$

2. **开球也是闭球**: 在p-adic拓扑中，每个开球也是闭集

3. **球不交或重合**: 两个p-adic球要么不交，要么一个包含另一个

**证明性质1**:

若 $y \in B(x, r)$，则 $|x - y|_p < r$。

对任意 $z \in B(x, r)$:
$$|z - y|_p = |(z - x) + (x - y)|_p \leq \max(|z-x|_p, |x-y|_p) < r$$

所以 $z \in B(y, r)$，即 $B(x, r) \subseteq B(y, r)$。

同理 $B(y, r) \subseteq B(x, r)$。

### 解答6.3: 二次型在$\mathbb{Q}_p$中的可解性

**Hilbert符号**:

对于 $a, b \in \mathbb{Q}_p^\times$，定义 Hilbert 符号 $(a, b)_p \in \{\pm 1\}$:

$(a, b)_p = 1$ 当且仅当方程 $ax^2 + by^2 = z^2$ 在 $\mathbb{Q}_p$ 中有非平凡解。

**判定法则**:

对于奇素数 $p$，设 $a = p^{\alpha}u, b = p^{\beta}v$，其中 $u, v$ 是单位:

$$(a, b)_p = (-1)^{\alpha\beta\frac{p-1}{2}} \left(\frac{u}{p}\right)^{\beta} \left(\frac{v}{p}\right)^{\alpha}$$

其中 $\left(\frac{\cdot}{p}\right)$ 是Legendre符号。

**Hasse-Minkowski原理**:

二次型在$\mathbb{Q}$中有解当且仅当它在所有$\mathbb{Q}_p$（包括$\mathbb{R} = \mathbb{Q}_\infty$）中有解。

**例子**: $x^2 + y^2 + z^2 = 0$

- 在 $\mathbb{Q}_3$ 中: 需要检查 $(-1, -1)_3$
- 在 $\mathbb{Q}_5$ 中: 需要检查 $(-1, -1)_5$

---

## 常见问题与注意事项

### 1. 精度问题

p-adic计算中精度至关重要。在进行多次运算后，精度可能会降低。

**建议**: 
- 设置足够高的初始精度
- 注意运算后检查结果的可靠性

### 2. p=2的特殊性

许多p-adic理论对 $p=2$ 有特殊处理:
- 收敛半径不同
- Hensel引理的条件更强
- 单位群结构不同

### 3. 数值稳定性

在p-adic计算中:
- 加法不会降低精度
- 乘法可能增加赋值（降低绝对值）
- 除法需要确保分母非零

### 4. 级数收敛

务必检查级数收敛条件:
- $\exp(x)$: $|x|_p < p^{-1/(p-1)}$
- $\log(1+x)$: $|x|_p < 1$
- 三角函数: 同 $\exp$

### 5. 与实数分析的区别

| 性质 | 实数 | p-adic |
|-----|------|--------|
| 三角不等式 | $|x+y| \leq |x| + |y|$ | $|x+y|_p \leq \max(|x|_p, |y|_p)$ |
| 拓扑 | 连通 | 完全不连通 |
| 球 | 有无穷多个中心 | 每个点都是中心 |
| 级数收敛 | 绝对收敛 | 项趋于0即可 |
| 指数收敛 | $|x| < \infty$ | $|x|_p < p^{-1/(p-1)}$ |

---

## 扩展阅读

1. **经典教材**:
   - Gouvêa, F.Q. "p-adic Numbers: An Introduction"
   - Koblitz, N. "p-adic Numbers, p-adic Analysis, and Zeta-Functions"
   - Serre, J.P. "Local Fields" (更高级)

2. **计算工具**:
   - SageMath: 内置p-adic数支持
   - PARI/GP: 强大的数论计算
   - Python `padic` 库

3. **进阶主题**:
   - p-adic L-函数
   - p-adic模形式
   - p-adic霍奇理论
   - 完美胚空间 (Perfectoid Spaces)
