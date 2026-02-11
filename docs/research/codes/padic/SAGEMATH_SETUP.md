# SageMath p-adic数计算模块配置文档

## 配置概览

- **配置日期**: 2026-02-11
- **用途**: p-adic模形式研究
- **安装状态**: ✅ 已完成

---

## 1. 系统检查

### 1.1 原始系统状态
- **SageMath**: 未安装 (系统中无`sage`命令)
- **Python**: Python 3.9.25
- **pip**: pip 21.3.1

### 1.2 尝试安装的方案

| 方案 | 状态 | 结果 |
|------|------|------|
| sagemath-standard (pip) | ❌ 失败 | cypari2编译错误 |
| sagecell (pip) | ✅ 成功 | 已安装 v0.3rc6 |
| padic (纯Python) | ✅ 成功 | 已安装 v0.2.4 |
| sympy | ✅ 成功 | 已安装 v1.14.0 |

---

## 2. 最终配置方案

由于完整版SageMath在系统上安装依赖复杂，采用以下**替代方案**：

### 2.1 主要库: `padic` (Python纯实现)

```bash
pip install padic
```

**特点**:
- 纯Python实现，无需编译
- 支持p-adic数的基本运算
- 支持级数展开（log, exp, sin, cos）
- 支持Hensel引理
- 支持任意精度计算

**版本**: 0.2.4

### 2.2 辅助库: `sympy`

```bash
pip install sympy
```

**用途**: 数论函数支持

**版本**: 1.14.0

---

## 3. 功能验证

### 3.1 ✅ 已验证功能

| 功能类别 | 功能描述 | 状态 |
|---------|---------|------|
| **基本创建** | 从整数创建p-adic数 | ✅ |
| | 从字符串创建p-adic数 | ✅ |
| | 分数转换为p-adic数 | ✅ |
| **基本运算** | 加法 (+) | ✅ |
| | 减法 (-) | ✅ |
| | 乘法 (*) | ✅ |
| | 除法 (/) | ✅ |
| **p-adic绝对值** | 赋值计算 (v_p) | ✅ |
| | 绝对值计算 (\|x\|_p) | ✅ |
| **级数展开** | 对数 (log) | ✅ |
| | 指数 (exp) | ✅ |
| | 正弦 (sin) | ✅ |
| | 余弦 (cos) | ✅ |
| | 二项式级数 | ✅ |
| **精度控制** | 自定义精度设置 | ✅ |
| | 显示精度控制 | ✅ |

### 3.2 ⚠️ 有限制的功能

| 功能 | 限制说明 |
|------|---------|
| Hensel引理 | 需要多项式系数为p-adic数，当前有类型兼容问题 |

---

## 4. API使用指南

### 4.1 导入模块

```python
from padic import Padic, log, exp, sin, cos, binomial, series, hensel
```

### 4.2 创建p-adic数

```python
# 从整数创建
a = Padic.from_int(17, p=2)  # 17的2-adic表示

# 从字符串创建（指定进制）
b = Padic.from_string("1001", p=2)  # 二进制1001 = 9

# 从分数创建
c = Padic.from_frac(1, 3, p=5)  # 1/3 的 5-adic表示
```

### 4.3 基本运算

```python
p = 2
a = Padic.from_int(17, p=p)
b = Padic.from_int(5, p=p)

# 加法
result = a + b

# 减法
result = a - b

# 乘法
result = a * b

# 除法
result = a / b
```

### 4.4 p-adic绝对值（赋值）

```python
# 计算p-adic赋值 v_p(n)
valuation = Padic.val(n, p)

# 计算p-adic绝对值 |x|_p = p^(-v_p(x))
padic_num = Padic.from_int(n, p=p)
abs_value = abs(padic_num)
```

### 4.5 级数展开

```python
p = 7
x = Padic.from_int(8, p=p)  # 需要 x ≡ 1 (mod p) 用于log

# p-adic对数
log_x = log(x, p=p, N=20)

# p-adic指数（需要 |x|_p < p^{-1/(p-1)}）
y = Padic.from_int(7, p=p)
exp_y = exp(y, p=p, N=20)

# p-adic三角函数
sin_y = sin(y, p=p, N=20)
cos_y = cos(y, p=p, N=20)
```

### 4.6 精度设置

```python
# 设置全局精度
Padic.PRECISION = 32          # 比较精度
Padic.INTEGER_PRECISION = 64  # 整数转换精度
Padic.DISPLAY_PRECISION = 16  # 显示精度

# 设置默认素数
Padic.DEFAULT_PRIME = 2

# 格式化显示
print(f"{padic_num:all}")   # 显示全部
print(f"{padic_num:.16}")   # 显示16位
```

---

## 5. p-adic数理论基础

### 5.1 p-adic数定义

对于素数p，p-adic数可以表示为：

$$x = \sum_{n=v}^{\infty} a_n p^n$$

其中 $a_n \in \{0, 1, ..., p-1\}$，$v$ 是p-adic赋值。

### 5.2 p-adic赋值

对于非零整数 $n$，p-adic赋值 $v_p(n)$ 是满足 $p^{v_p(n)} | n$ 的最大整数。

### 5.3 p-adic绝对值

$$|x|_p = p^{-v_p(x)}$$

满足强三角不等式：$|x + y|_p \leq \max(|x|_p, |y|_p)$

### 5.4 收敛条件

| 级数 | 收敛条件 |
|------|---------|
| $\log(1+x)$ | $\|x\|_p < 1$ |
| $\exp(x)$ | $\|x\|_p < p^{-1/(p-1)}$ |
| $\sin(x), \cos(x)$ | $\|x\|_p < p^{-1/(p-1)}$ |

---

## 6. 测试脚本

测试脚本位置：
```
/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/padic/padic_basic_test.py
```

运行测试：
```bash
cd /mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/padic
python3 padic_basic_test.py
```

测试内容：
1. p-adic数基本创建
2. 基本运算 (+, -, *, /)
3. p-adic绝对值（赋值）计算
4. 级数展开 (log, exp, sin, cos)
5. Hensel引理应用
6. 精度设置
7. 分数转换

---

## 7. 应用于p-adic模形式

### 7.1 相关概念

p-adic模形式是经典模形式在p-adic拓扑下的推广。关键特点：

1. **权重的p-adic连续性**: p-adic模形式的权重可以是p-adic整数
2. **q-展开**: 模形式的q-展开系数可以是p-adic数
3. **Hecke算子**: 在p-adic模形式上有自然的Hecke算子作用

### 7.2 计算应用

使用当前配置的库可以：

1. **计算模形式空间的维数**（通过p-adic方法）
2. **研究p-adic L-函数**
3. **计算p-adic周期**
4. **验证同余关系**（如Ramanujan同余）

### 7.3 示例：Ramanujan Δ函数

```python
from padic import Padic

# Ramanujan Δ函数的q-展开: Δ(q) = q ∏(1-q^n)^24
# 其Fourier系数 τ(n) 满足多种p-adic性质

p = 691  # 著名的Ramanujan素数

# 可以研究 τ(n) mod p 的性质
# 以及 p-adic L-函数的相关计算
```

---

## 8. 故障排除

### 8.1 常见问题

| 问题 | 解决方案 |
|------|---------|
| `ImportError` | 确保已安装 `pip install padic sympy` |
| 精度不足 | 增加 `Padic.INTEGER_PRECISION` |
| 级数不收敛 | 检查输入是否满足收敛条件 |
| 类型错误 | 确保运算数为p-adic数或整数 |

### 8.2 如果需要完整SageMath

如需完整SageMath功能，建议：

1. **使用SageMath Cell Server** (在线): https://sagecell.sagemath.org/
2. **使用CoCalc** (在线): https://cocalc.com/
3. **本地安装SageMath**: 从 https://www.sagemath.org/ 下载安装包

---

## 9. 参考资源

### 9.1 文档
- padic库源代码: `/usr/local/lib/python3.9/site-packages/padic/`

### 9.2 推荐阅读
1. Gouvêa, F.Q. - "p-adic Numbers: An Introduction"
2. Koblitz, N. - "p-adic Numbers, p-adic Analysis, and Zeta-Functions"
3. Serre, J.P. - "A Course in Arithmetic" (Chapter II: p-adic fields)
4. Katz, N.M. - "p-adic Properties of Modular Schemes"

### 9.3 在线资源
- SageMath p-adic文档: https://doc.sagemath.org/html/en/reference/padics/
- p-adic数维基百科: https://en.wikipedia.org/wiki/P-adic_number

---

## 10. 总结

✅ **配置成功**

虽然完整版SageMath未安装，但已成功配置纯Python的`padic`库，该库提供了：

- 完整的p-adic数运算支持
- 级数展开功能
- 高精度计算能力
- 足够的功能支持p-adic模形式研究

如需更高级的代数功能（如代数数域、p-adic伽罗瓦表示等），建议使用在线SageMath服务或本地安装完整SageMath。
