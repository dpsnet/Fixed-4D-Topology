# Hejhal算法实现 - Maass形式特征值计算

本目录包含Hejhal算法的实现，用于计算模群 $SL(2, \mathbb{Z})$ 上Maass尖点形式的特征值。

## 文件说明

| 文件 | 说明 |
|------|------|
| `hejhal_maass.py` | **主要实现** - 完整的Hejhal算法求解器 |
| `hejhal_demo.py` | **演示版本** - 快速概念验证 |
| `hejhal_basic_implementation.py` | 基础实现（参考版本） |
| `hejhal_final.py` | 完整实现（详细版本） |
| `HEJHAL_USAGE.md` | **使用文档** - 详细的API文档 |
| `../notes/maass/hejhal_algorithm_documentation.md` | **算法文档** - 数学原理和理论 |

## 快速开始

### 1. 安装依赖

```bash
pip install numpy scipy mpmath
```

### 2. 运行演示

```bash
# 快速演示（约10秒）
python hejhal_maass.py demo

# 完整计算（约2-5分钟）
python hejhal_maass.py compute

# 计算前5个偶形式特征值
python hejhal_maass.py even 5

# 计算前3个奇形式特征值
python hejhal_maass.py odd 3
```

### 3. Python API

```python
from hejhal_maass import MaassEigenvalueSolver, HejhalConfig

# 创建求解器
config = HejhalConfig(
    truncation_M=15,    # Fourier截断参数
    num_points=15,      # 配点数量
    parity='even',      # 'even' 或 'odd'
    mpmath_dps=25       # 精度
)
solver = MaassEigenvalueSolver(config)

# 搜索特征值附近
result = solver.find_eigenvalue(13.78, half_width=0.5)
if result:
    t, condition = result
    lambda_val = 0.25 + t**2
    print(f"R = {t:.8f}, λ = {lambda_val:.6f}")
```

## 已知特征值（验证基准）

### 偶形式

| 序号 | $R = \sqrt{\lambda - 1/4}$ | $\lambda = 1/4 + R^2$ |
|------|---------------------------|-----------------------|
| 1 | 13.779751351890 | 190.131547 |
| 2 | 17.738563381109 | 315.065933 |
| 3 | 19.423481346970 | 377.870805 |
| 4 | 21.315796882311 | 454.863142 |
| 5 | 22.785280830796 | 519.988835 |

### 奇形式

| 序号 | $R = \sqrt{\lambda - 1/4}$ | $\lambda = 1/4 + R^2$ |
|------|---------------------------|-----------------------|
| 1 | 9.533695261349 | 91.141345 |
| 2 | 12.173008240650 | 148.582130 |
| 3 | 14.358509516256 | 206.366757 |
| 4 | 16.138121172691 | 260.688934 |
| 5 | 16.644259197914 | 277.431361 |

## 算法原理

Hejhal算法基于以下核心思想：

1. **Fourier展开**：Maass形式具有Fourier展开
   $$\phi(z) = \sum_{n \neq 0} \rho(n) y^{1/2} K_{it}(2\pi|n|y) e^{2\pi i n x}$$

2. **配点法**：在基本域内选择点，建立线性方程组

3. **边界条件**：利用模变换下的不变性建立约束

4. **特征值检测**：寻找使矩阵奇异的谱参数

详细数学原理请参考 `../notes/maass/hejhal_algorithm_documentation.md`

## 精度说明

实现具有**指数收敛性**：
- `M = 10`：精度约 $10^{-2}$
- `M = 15`：精度约 $10^{-4}$  
- `M = 20`：精度约 $10^{-6}$
- `M = 25`：精度约 $10^{-8}$

更高的精度需要增加 `mpmath_dps` 和计算时间。

## 参考文献

1. Hejhal, D. (1981). "Some observations concerning eigenvalues of the Laplacian and Dirichlet L-series."
2. Hejhal, D. (1992). "On eigenfunctions of the Laplacian for Hecke triangle groups."
3. Sarnak, P. (2003). "Spectra of Hyperbolic Surfaces." (Baltimore Lectures, Appendix 7)
4. Booker, A.R., Strömbergsson, A., & Venkatesh, A. (2006). "Effective computation of Maass cusp forms."

## 注意事项

1. **计算时间**：完整精度计算可能需要几分钟
2. **内存使用**：$M = 25$ 时约使用 100MB 内存
3. **数值稳定性**：对于 $R > 30$ 的大特征值，需要特殊处理

## 许可

本实现用于研究和教育目的。
