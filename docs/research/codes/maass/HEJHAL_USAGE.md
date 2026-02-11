# Hejhal算法使用文档

## 概述

本文档描述如何使用Hejhal算法实现来计算模群 $SL(2, \mathbb{Z})$ 上Maass尖点形式的特征值。

---

## 安装依赖

### 必需依赖

```bash
pip install numpy scipy
```

### 推荐依赖（用于高级功能）

```bash
pip install matplotlib mpmath
```

### 验证安装

```python
import numpy as np
from scipy.special import kv
from scipy.linalg import svdvals

print("NumPy版本:", np.__version__)
print("SciPy导入成功")
```

---

## 快速开始

### 基本用法

```python
from hejhal_basic_implementation import HejhalAlgorithm, HejhalConfig

# 创建配置
config = HejhalConfig(
    truncation_M=20,      # Fourier截断参数
    num_points=20,        # 配点数量
    parity='even',        # 'even' 或 'odd'
    tolerance=1e-10       # 收敛容差
)

# 初始化算法
hejhal = HejhalAlgorithm(config)

# 搜索特征值
eigenvalues = hejhal.search_eigenvalues(
    t_min=13.0,           # 搜索区间下限
    t_max=14.5,           # 搜索区间上限
    num_samples=500       # 扫描样本数
)

# 打印结果
for t, lam in eigenvalues:
    print(f"t = {t:.10f}, λ = {lam:.10f}")
```

### 命令行使用

```bash
# 运行基本测试
python hejhal_basic_implementation.py test

# 计算前5个偶形式特征值
python hejhal_basic_implementation.py even 5

# 计算前5个奇形式特征值
python hejhal_basic_implementation.py odd 5

# 运行精度基准测试
python hejhal_basic_implementation.py benchmark

# 运行所有测试
python hejhal_basic_implementation.py all
```

---

## 参数说明

### HejhalConfig 配置类

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `truncation_M` | int | 20 | Fourier展开截断参数，控制精度 |
| `num_points` | int | 20 | 配点数量，通常等于或略大于`truncation_M` |
| `y_min` | float | 0.866 | 基本域底部 ($\sqrt{3}/2$) |
| `y_max` | float | 2.0 | y坐标上限 |
| `tolerance` | float | 1e-10 | 收敛容差，用于特征值精化 |
| `parity` | str | 'even' | 奇偶性：'even'（偶形式）或 'odd'（奇形式） |

### 参数选择指南

#### 精度 vs 计算时间

| 目标精度 | truncation_M | num_points | 计算时间 |
|---------|--------------|------------|----------|
| $10^{-5}$ | 10 | 10 | ~1秒 |
| $10^{-8}$ | 15 | 15 | ~5秒 |
| $10^{-10}$ | 20 | 20 | ~20秒 |
| $10^{-12}$ | 25 | 25 | ~60秒 |
| $10^{-15}$ | 30+ | 30+ | ~5分钟 |

#### 不同特征值大小的建议

- **小特征值** ($R < 20$)：$M = 15$ 足够
- **中等特征值** ($20 < R < 50$)：$M = 20-25$
- **大特征值** ($R > 50$)：$M = 30+$，可能需要特殊处理

---

## 输出解释

### 搜索输出示例

```
搜索区间: [13.000000, 14.500000]
样本数: 500
截断参数 M = 20
奇偶性: even
------------------------------------------------------------
扫描中...
  进度: 0/500 (0.0%)
  进度: 100/500 (20.0%)
  进度: 200/500 (40.0%)
  ...
扫描完成，用时: 12.34秒

发现候选特征值: t ≈ 13.77975140, σ_min = 1.23e-12
  精化后: t = 13.7797513519, λ = 190.1315473420
```

### 输出字段说明

| 字段 | 说明 |
|------|------|
| `t` | 谱参数，特征值 $R = t$ |
| `λ` | Laplace特征值，$\lambda = \frac{1}{4} + t^2$ |
| `σ_min` | 最小奇异值，越接近0越可能是特征值 |
| `σ_min` | 最小奇异值，越接近0越可能是特征值 |

---

## API 参考

### HejhalAlgorithm 类

#### 构造方法

```python
hejhal = HejhalAlgorithm(config: Optional[HejhalConfig] = None)
```

#### 主要方法

##### search_eigenvalues

```python
eigenvalues = hejhal.search_eigenvalues(
    t_min: float, 
    t_max: float, 
    num_samples: int = 1000
) -> List[Tuple[float, float]]
```

在指定区间内搜索特征值。

**参数：**
- `t_min`: 搜索区间下限（谱参数）
- `t_max`: 搜索区间上限（谱参数）
- `num_samples`: 扫描样本数

**返回：**
- 列表 `[(t1, lambda1), (t2, lambda2), ...]`

##### construct_matrix

```python
A = hejhal.construct_matrix(t: float) -> np.ndarray
```

构造配点矩阵 $A(t)$。

**参数：**
- `t`: 谱参数

**返回：**
- $M \times M$ 矩阵

##### min_singular_value

```python
sigma = hejhal.min_singular_value(t: float) -> float
```

计算矩阵的最小奇异值。

**参数：**
- `t`: 谱参数

**返回：**
- 最小奇异值（特征值处接近0）

##### compute_fourier_coefficients

```python
coeffs = hejhal.compute_fourier_coefficients(
    t: float, 
    normalize: bool = True
) -> np.ndarray
```

计算给定特征值的Fourier系数。

**参数：**
- `t`: 谱参数（已知特征值）
- `normalize`: 是否归一化（使 $\rho(1) = 1$）

**返回：**
- 系数数组 `[ρ(1), ρ(2), ..., ρ(M)]`

##### verify_hecke_relations

```python
error = hejhal.verify_hecke_relations(
    coeffs: np.ndarray, 
    num_checks: int = 5
) -> float
```

验证Hecke关系。

**参数：**
- `coeffs`: Fourier系数数组
- `num_checks`: 验证的(n,m)对数

**返回：**
- 最大相对误差

---

## 高级用法

### 计算Fourier系数

```python
from hejhal_basic_implementation import HejhalAlgorithm, HejhalConfig

config = HejhalConfig(truncation_M=25, parity='even')
hejhal = HejhalAlgorithm(config)

# 假设我们已知特征值 t ≈ 13.77975
t = 13.779751351890
coeffs = hejhal.compute_fourier_coefficients(t)

print("前10个Fourier系数:")
for i, c in enumerate(coeffs[:10], 1):
    print(f"ρ({i}) = {c:.10f}")

# 验证Hecke关系
error = hejhal.verify_hecke_relations(coeffs, num_checks=10)
print(f"\nHecke关系最大误差: {error:.2e}")
```

### 自定义配点

```python
import numpy as np
from hejhal_basic_implementation import HejhalAlgorithm

hejhal = HejhalAlgorithm()

# 自定义配点
hejhal.points = [complex(x, y) for x, y in [
    (0.0, 1.0), (0.1, 1.0), (-0.1, 1.0),
    (0.0, 1.2), (0.2, 1.2), (-0.2, 1.2),
    # ...
]]
hejhal.config.num_points = len(hejhal.points)

# 继续计算...
```

### 保存和加载结果

```python
import json
import numpy as np

# 保存结果
def save_results(filename, eigenvalues, coeffs):
    data = {
        'eigenvalues': [(float(t), float(lam)) for t, lam in eigenvalues],
        'coefficients': coeffs.tolist() if coeffs is not None else None
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# 加载结果
def load_results(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['eigenvalues'], data['coefficients']

# 使用示例
eigenvalues = hejhal.search_eigenvalues(13.0, 14.0, num_samples=500)
coeffs = hejhal.compute_fourier_coefficients(eigenvalues[0][0])
save_results('results.json', eigenvalues, coeffs)
```

---

## 已知特征值（验证基准）

### 偶形式（Even Maass Cusp Forms）

| 序号 | $R = \sqrt{\lambda - 1/4}$ | $\lambda = 1/4 + R^2$ |
|------|---------------------------|-----------------------|
| 1 | 13.779751351890 | 190.131547 |
| 2 | 17.738563381109 | 315.065933 |
| 3 | 19.423481346970 | 377.870805 |
| 4 | 21.315796882311 | 454.863142 |
| 5 | 22.785280830796 | 519.988835 |

### 奇形式（Odd Maass Cusp Forms）

| 序号 | $R = \sqrt{\lambda - 1/4}$ | $\lambda = 1/4 + R^2$ |
|------|---------------------------|-----------------------|
| 1 | 9.533695261349 | 91.141345 |
| 2 | 12.173008240650 | 148.582130 |
| 3 | 14.358509516256 | 206.366757 |
| 4 | 16.138121172691 | 260.688934 |
| 5 | 16.644259197914 | 277.431361 |

---

## 故障排除

### 问题1：计算时间过长

**症状：** 搜索特征值需要很长时间

**解决方案：**
1. 减小 `truncation_M` 和 `num_points`
2. 减小 `num_samples`（扫描样本数）
3. 缩小区间 `[t_min, t_max]`

```python
# 快速模式
config = HejhalConfig(truncation_M=10, num_points=10)
evs = hejhal.search_eigenvalues(13.5, 14.0, num_samples=100)
```

### 问题2：找不到特征值

**症状：** `search_eigenvalues` 返回空列表

**解决方案：**
1. 确保搜索区间包含特征值
2. 增大 `num_samples`
3. 降低 `tolerance`

```python
# 扩大搜索范围
evs = hejhal.search_eigenvalues(10.0, 20.0, num_samples=1000)
```

### 问题3：数值不稳定

**症状：** 最小奇异值波动很大或不收敛

**解决方案：**
1. 检查 `y_min` 设置（不应太小）
2. 使用更高精度算术（mpmath）
3. 调整配点分布

```python
config = HejhalConfig(y_min=0.9, y_max=1.5)  # 更保守的范围
```

### 问题4：Bessel函数溢出

**症状：** `RuntimeWarning: overflow encountered`

**解决方案：**
这是正常的对于大参数。实现会自动使用渐近近似。如果需要更高精度：

```python
import mpmath
mpmath.mp.dps = 50  # 50位精度
```

---

## 性能优化

### 使用更高效的Bessel函数计算

```python
from scipy.special import kv

# 对于大参数，使用对数Bessel函数
from scipy.special import kve  # K_nu(x) * exp(x)
```

### 并行计算

```python
from multiprocessing import Pool

def compute_for_t(t):
    return hejhal.min_singular_value(t)

# 并行扫描
t_vals = np.linspace(13.0, 14.0, 1000)
with Pool(4) as p:
    sigma_vals = p.map(compute_for_t, t_vals)
```

---

## 参考文献

1. Hejhal, D. (1981). "Some observations concerning eigenvalues of the Laplacian and Dirichlet L-series."
2. Sarnak, P. (2003). "Spectra of Hyperbolic Surfaces" (Baltimore Lectures, Appendix 7)
3. Booker, A.R., et al. (2006). "Effective computation of Maass cusp forms."

---

## 更新日志

### 版本 1.0 (2026-02-11)
- 初始实现
- 支持偶形式和奇形式
- 基本特征值搜索功能
- Fourier系数计算
- Hecke关系验证

---

## 联系与支持

如有问题或建议，请参考项目文档或提交issue。
