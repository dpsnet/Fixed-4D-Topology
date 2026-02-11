# 双曲空间阅读笔记

> **来源**: Ratcliffe《Foundations of Hyperbolic Manifolds》第1-2章 (替代资源: Kapovich讲义, Walkden讲义)
> **阅读日期**: 2026-02-11
> **阅读时长**: 约4小时
> **理解程度**: 85% (核心概念已掌握，部分技术细节需后续深化)

---

## 1. 双曲空间的定义

### 1.1 核心定义

**n维双曲空间** $\mathbb{H}^n$ 是完备的、单连通的黎曼流形，具有常负曲率 $K = -1$。

**与球面的对比**:
- 球面 $S^n$: 常正曲率 $K = +1$，紧致
- 欧氏空间 $\mathbb{R}^n$: 零曲率 $K = 0$
- 双曲空间 $\mathbb{H}^n$: 常负曲率 $K = -1$，非紧致

### 1.2 度规定义（内蕴）

双曲空间可以通过多种等价的模型来实现，所有模型都满足相同的几何性质：
- 任意三角形的内角和小于 $\pi$
- 平行公设不成立（过直线外一点有无穷多条平行线）
- 面积与亏角成正比

---

## 2. 双曲空间的模型

### 2.1 双曲面模型 (Hyperboloid Model)

**别名**: Minkowski模型, Lorentz模型

#### 构造
在 $(n+1)$维 Minkowski 空间 $\mathbb{R}^{n,1}$ 中，配备不定度量：
$$ds^2 = -dx_0^2 + dx_1^2 + \cdots + dx_n^2$$

Minkowski二次型：
$$Q(x_0, x_1, \ldots, x_n) = -x_0^2 + x_1^2 + \cdots + x_n^2$$

**双曲面定义为**:
$$\mathbb{H}^n = \{x \in \mathbb{R}^{n,1} : Q(x) = -1, x_0 > 0\}$$

即双叶双曲面的**上叶**（future sheet）。

#### 双曲距离公式
对于 $u, v \in \mathbb{H}^n$，双曲距离为：
$$d(u, v) = \text{arcosh}(-B(u, v))$$

其中 $B(u, v)$ 是Minkowski双线性形式：
$$B(u, v) = -u_0 v_0 + u_1 v_1 + \cdots + u_n v_n = \frac{Q(u+v) - Q(u) - Q(v)}{2}$$

#### 等距群
$$\text{Isom}(\mathbb{H}^n) = O^+(1, n)$$

保持定向的等距群为：
$$\text{Isom}^+(\mathbb{H}^n) = SO^+(1, n)$$

**维度**: $n(n+1)/2$

#### 优点
- 等距群是线性群，便于代数操作
- 测地线是与原点的连线（平面与双曲面的交线）
- 距离公式简洁
- 适合与狭义相对论联系

#### 缺点
- 嵌入在高维空间中
- 直观几何理解较困难

---

### 2.2 Poincaré球模型 (Poincaré Ball Model)

**定义域**: 单位开球 $B^n = \{x \in \mathbb{R}^n : |x| < 1\}$

#### 度量
$$ds^2 = \frac{4|dx|^2}{(1 - |x|^2)^2} = \frac{4\sum_{i=1}^n dx_i^2}{(1 - \sum_{i=1}^n x_i^2)^2}$$

#### 距离公式
对于 $u, v \in B^n$:

**方法1**（用双曲函数）:
$$d(u, v) = \text{arcosh}\left(1 + \frac{2|u - v|^2}{(1 - |u|^2)(1 - |v|^2)}\right)$$

**方法2**（用对数）:
$$d(u, v) = 2\ln\frac{|u - v| + \sqrt{|u|^2|v|^2 - 2u \cdot v + 1}}{\sqrt{(1 - |u|^2)(1 - |v|^2)}}$$

**特殊情况**（一点在原点）:
$$d(0, r) = \ln\frac{1 + r}{1 - r} = 2\text{artanh}(r)$$

#### 测地线
- 垂直于边界球面 $S^{n-1}$ 的圆弧
- 通过原点的直径

#### 等距群
保持定向的等距群是 Möbius 变换的子群：
$$\text{Isom}^+(\mathbb{H}^n) \cong \text{Conf}(B^n) \cong \text{PSU}(1, n)$$

对于 $n = 2$（单位圆盘）：等距群为 $\text{PSU}(1, 1)$

对于 $n = 3$（单位球）：等距群为 $\text{PSL}(2, \mathbb{C})$（通过球极投影与Möbius群联系）

#### 优点
- 共形模型（保持角度）
- 直观上有限区域表示无限空间
- 与复分析紧密相关（n=2时）

#### 缺点
- 距离计算涉及复杂公式
- 测地线不是欧氏直线（除直径外）

---

### 2.3 Poincaré半空间模型 (Poincaré Half-Space Model)

**定义域**: 上半空间
$$\mathbb{H}^n = \{x = (x_1, \ldots, x_{n-1}, x_n) \in \mathbb{R}^n : x_n > 0\}$$

#### 度量
$$ds^2 = \frac{dx_1^2 + \cdots + dx_n^2}{x_n^2} = \frac{|dx|^2}{x_n^2}$$

这是**最常用**的双曲度量形式。

#### 距离公式
对于 $p = (x_1, y_1)$ 和 $q = (x_2, y_2)$（用2维记号，$y$ 表示高度）：

**一般公式**:
$$d(p, q) = 2\text{arsinh}\left(\frac{|p - q|}{2\sqrt{y_1 y_2}}\right)$$

或等价地:
$$d(p, q) = 2\text{artanh}\left(\frac{|p - q|}{|p - \tilde{q}|}\right)$$

其中 $\tilde{q} = (x_2, -y_2)$ 是 $q$ 关于边界平面的反射。

**特殊情况**（垂直线）:
$$d((x, y_1), (x, y_2)) = |\ln(y_2/y_1)|$$

#### 测地线
- 垂直于边界超平面 $\{x_n = 0\}$ 的半圆
- 垂直于边界的直线（与 $x_n$ 轴平行的直线）

#### 等距群
保持定向的等距群为：
$$\text{Isom}^+(\mathbb{H}^n) = \{x \mapsto \lambda A x + b : \lambda > 0, A \in SO(n-1), b \in \mathbb{R}^{n-1}\}$$

对于 $n = 2$:
$$\text{Isom}^+(\mathbb{H}^2) = \text{PSL}(2, \mathbb{R})$$

作用方式为 Möbius 变换：$z \mapsto \frac{az + b}{cz + d}$，其中 $a, b, c, d \in \mathbb{R}$，$ad - bc = 1$

#### 优点
- 度量形式最简单
- 与复分析、模形式紧密相关
- 边界在无穷远处（便于理解理想点）

#### 缺点
- 不是共形等价于欧氏空间（除角度外）
- 体积元计算需小心

---

### 2.4 Klein模型 (Beltrami-Klein模型)

**别名**: 射影模型

**定义域**: 单位开球 $B^n$（与Poincaré球相同）

#### 构造
从双曲面模型通过**中心投影**（gnomonic投影）得到。

投影映射：
$$(x_0, x_1, \ldots, x_n) \mapsto \left(\frac{x_1}{x_0}, \ldots, \frac{x_n}{x_0}\right)$$

#### 度量
$$ds^2 = \frac{|dx|^2}{1 - |x|^2} + \frac{(x \cdot dx)^2}{(1 - |x|^2)^2}$$

#### 距离公式
对于 $u, v \in B^n$:
$$d(u, v) = \frac{1}{2}\left|\ln\frac{|u - a||v - b|}{|u - b||v - a|}\right|$$

其中 $a, b$ 是通过 $u, v$ 的弦与边界的交点。

#### 测地线
- **欧氏直线段**（弦）

这是Klein模型最重要的特征！

#### 等距群
与双曲面模型相同：$O(1, n)$

#### 优点
- 测地线是直线（最直观）
- 投影关系简单

#### 缺点
- **不是共形的**（角度失真）
- 距离公式复杂
- 圆的像不是欧氏圆

---

## 3. 模型间的转换关系

### 3.1 双曲面模型 ↔ Poincaré球

**双曲面 → Poincaré球**（球极投影）:
$$(x_0, x_1, \ldots, x_n) \mapsto \left(\frac{x_1}{1 + x_0}, \ldots, \frac{x_n}{1 + x_0}\right)$$

**Poincaré球 → 双曲面**:
$$y \mapsto \left(\frac{1 + |y|^2}{1 - |y|^2}, \frac{2y_1}{1 - |y|^2}, \ldots, \frac{2y_n}{1 - |y|^2}\right)$$

### 3.2 Poincaré球 ↔ Klein模型

**Poincaré球 → Klein**:
$$u \mapsto \frac{2u}{1 + |u|^2}$$

**Klein → Poincaré球**:
$$s \mapsto \frac{s}{1 + \sqrt{1 - |s|^2}}$$

### 3.3 Poincaré球 ↔ 上半空间

**通过Cayley变换**:
$$z \mapsto i\frac{1 + z}{1 - z}$$

逆变换:
$$w \mapsto \frac{w - i}{w + i}$$

---

## 4. 关键公式汇总

### 4.1 度量张量

| 模型 | 度量公式 |
|------|----------|
| 双曲面 | $ds^2 = -dx_0^2 + \sum_{i=1}^n dx_i^2$（限制） |
| Poincaré球 | $ds^2 = \frac{4|dx|^2}{(1 - |x|^2)^2}$ |
| Poincaré半空间 | $ds^2 = \frac{|dx|^2}{x_n^2}$ |
| Klein | $ds^2 = \frac{|dx|^2}{1 - |x|^2} + \frac{(x \cdot dx)^2}{(1 - |x|^2)^2}$ |

### 4.2 体积元

**Poincaré半空间**:
$$dV = \frac{dx_1 \cdots dx_n}{x_n^n}$$

**Poincaré球**:
$$dV = \frac{2^n dx_1 \cdots dx_n}{(1 - |x|^2)^n}$$

### 4.3 球面体积与面积

**n维双曲空间中的球**:
- 半径为 $r$ 的球体积:
$$V_n(r) = \frac{2\pi^{n/2}}{\Gamma(n/2)} \int_0^r \sinh^{n-1}(t) dt$$

- 半径为 $r$ 的球面面积:
$$A_{n-1}(r) = \frac{2\pi^{n/2}}{\Gamma(n/2)} \sinh^{n-1}(r)$$

**指数增长**: 体积和表面积随半径指数增长（与欧氏空间的幂律增长不同）

---

## 5. 等距变换的分类

### 5.1 二维情况 (PSL(2, ℝ))

对于 Möbius 变换 $z \mapsto \frac{az + b}{cz + d}$，$ad - bc = 1$：

**分类依据**: $\text{tr}(A) = a + d$ 的值

| 类型 | 条件 | 特征 |
|------|------|------|
| **椭圆型** (Elliptic) | $|\text{tr}(A)| < 2$ | 有唯一不动点在 $\mathbb{H}^2$ 内，旋转 |
| **抛物型** (Parabolic) | $|\text{tr}(A)| = 2$ | 有唯一不动点在边界上，平移极限 |
| **双曲型** (Hyperbolic) | $|\text{tr}(A)| > 2$ | 有两个不动点在边界上，沿测地线平移 |

### 5.2 三维情况 (PSL(2, ℂ))

对于 Möbius 变换作用于 $\hat{\mathbb{C}} = \mathbb{C} \cup \{\infty\}$：

**通过Poincaré延拓**到双曲3空间。

分类类似，但更丰富：
- **椭圆型**: 绕轴旋转
- **抛物型**: 极限旋转（horocycle上的平移）
- **双曲型/loxodromic**: 沿测地线平移 + 绕轴旋转

### 5.3 n维情况

**一般形式**: $O^+(1, n)$ 中的元素

**分解**: 任何等距可分解为
1. 旋转（固定一点）
2. 平移（沿测地线）
3. 极限旋转（抛物型，固定边界一点）
4. 反射（反向等距）

---

## 6. 与Kleinian群的关系

### 6.1 核心联系

**Kleinian群** = PSL(2, ℂ) 的离散子群 = 双曲3空间等距群的离散子群

**作用**: Kleinian群 $\Gamma$ 在双曲3空间 $\mathbb{H}^3$ 上正常不连续地作用。

**商空间**: $\mathbb{H}^3 / \Gamma$ 是双曲3-流形或双曲3-轨道。

### 6.2 极限集与正规集

**极限集** $\Lambda(\Gamma)$: 群作用在边界 $S^2_\infty$ 上的累积点集

**正规集** $\Omega(\Gamma) = S^2_\infty \setminus \Lambda(\Gamma)$: 群作用正常不连续的区域

### 6.3 为什么需要不同模型

| 用途 | 首选模型 |
|------|----------|
| 代数操作、等距群计算 | 双曲面模型 |
| 极限集可视化、共形几何 | Poincaré球 |
| 模形式、Fuchsian群 | Poincaré半空间 |
| 测地线追踪 | Klein模型 |

---

## 7. 核心概念清单

### 7.1 已掌握概念 ✅

- [x] 双曲空间的多种模型定义
- [x] 各模型的度量和距离公式
- [x] 模型间的转换关系
- [x] 等距变换的分类（椭圆/抛物/双曲）
- [x] PSL(2, ℝ) 和 PSL(2, ℂ) 的作用
- [x] 体积元的计算
- [x] Kleinian群的基本定义

### 7.2 需深入理解的部分 🔍

- [ ] 双曲三角学（双曲正弦/余弦定理）
- [ ] 双曲多面体的体积计算
- [ ] 理想双曲多面体
- [ ] 等距群的李代数结构
- [ ] 双曲空间中的极坐标
- [ ] horosphere（极限球面）的详细性质

### 7.3 与其他文献的联系

| 概念 | 相关文献 |
|------|----------|
| Möbius变换 | Beardon第4章 |
| Fuchsian群 | Beardon第5章, Iwaniec第1章 |
| 双曲3-流形 | Ratcliffe全书, Thurston讲义 |
| 算术群 | Maclachlan-Reid |
| 极限集维数 | McMullen论文 |

---

## 8. 学习检查点

### 8.1 能否解释不同双曲模型的区别？

**答案框架**:

1. **双曲面模型**: 嵌入Minkowski空间的上叶双曲面，等距群为线性Lorentz群，距离用双线性形式计算。

2. **Poincaré球**: 单位球内部，共形模型，测地线为垂直于边界的圆弧，等距群为Möbius变换。

3. **Poincaré半空间**: 上半空间，度量最简形式，测地线为垂直半圆或直线，与复分析紧密相关。

4. **Klein模型**: 单位球内部，测地线为直线（最直观），但非共形，角度失真。

### 8.2 能否计算双曲距离？

**示例**: 计算Poincaré上半平面中 $p = (0, 1)$ 到 $q = (0, 2)$ 的距离。

**解**: 两点在同一垂直线上，使用公式：
$$d(p, q) = |\ln(2/1)| = \ln 2$$

**验证**: 这也是沿测地线（垂直线 $x=0$）的积分：
$$\int_1^2 \frac{dy}{y} = \ln 2$$

### 8.3 能否描述等距变换的类型？

**二维情况**（PSL(2, ℝ)）:
- 椭圆: 旋转，如 $z \mapsto \frac{\cos(\theta/2) z + \sin(\theta/2)}{-\sin(\theta/2) z + \cos(\theta/2)}$
- 抛物: 平移极限，如 $z \mapsto z + 1$
- 双曲: 沿测地线平移，如 $z \mapsto \lambda z$（$\lambda > 0$）

**三维情况**（PSL(2, ℂ)）:
- 加上"螺旋"等距：沿测地线平移同时绕轴旋转

---

## 9. 延伸阅读建议

1. **Ratcliffe第3章**: 双曲流形的具体构造
2. **Beardon第7章**: 双曲几何的深入性质
3. **Thurston《3D Geometry and Topology》**: 几何化观点
4. **Kapovich讲义**: Kleinian群的现代观点
5. **Mumford《Indra's Pearls》**: 极限集的可视化

---

## 10. 关键公式速查卡

### 双曲距离公式

**双曲面模型**: $d(u, v) = \text{arcosh}(-B(u, v))$

**Poincaré球**: $d(0, r) = \ln\frac{1+r}{1-r}$

**Poincaré半空间**: $d(p, q) = 2\text{arsinh}\left(\frac{|p-q|}{2\sqrt{y_p y_q}}\right)$

### 体积公式

**n维球体积**: $V_n(r) \sim \frac{2\pi^{n/2}}{\Gamma(n/2)(n-1)} e^{(n-1)r}$（$r \to \infty$）

### 等距群

$$\text{Isom}(\mathbb{H}^n) = O^+(1, n)$$
$$\text{Isom}^+(\mathbb{H}^2) = \text{PSL}(2, \mathbb{R})$$
$$\text{Isom}^+(\mathbb{H}^3) = \text{PSL}(2, \mathbb{C})$$

---

*笔记完成于 2026-02-11*
