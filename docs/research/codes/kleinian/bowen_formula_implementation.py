"""
Bowen公式算法实现：计算Hausdorff维数
基于McMullen "Hausdorff dimension and conformal dynamics III"

本模块实现了特征值算法来计算扩张共形动力系统的Hausdorff维数。
"""

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs
from scipy.optimize import brentq, newton
from typing import List, Tuple, Callable, Optional
import warnings
warnings.filterwarnings('ignore')


class MarkovPartition:
    """
    Markov分划类
    
    表示为 (P_i, f_i) 的集合，其中：
    - P_i: 状态空间中的紧凑子集（块）
    - f_i: 定义在P_i上的共形映射
    """
    
    def __init__(self, blocks: List[dict], transition_graph: Optional[np.ndarray] = None):
        """
        初始化Markov分划
        
        Args:
            blocks: 块列表，每个块为字典 {'center': 中心点, 'map': 映射函数, 'inv_map': 逆映射, 'derivative': 导数}
            transition_graph: 转移关系矩阵 (n x n)，transition_graph[i,j] = 1 表示 i -> j
        """
        self.blocks = blocks
        self.n_blocks = len(blocks)
        if transition_graph is None:
            self.transition_graph = np.ones((self.n_blocks, self.n_blocks))
        else:
            self.transition_graph = transition_graph
        self.sample_points = np.array([b['center'] for b in blocks])
        
    def refine(self) -> 'MarkovPartition':
        """
        精细化分划：每个块根据转移关系分裂
        
        Returns:
            新的精细化Markov分划
        """
        new_blocks = []
        new_sample_points = []
        
        for i, block_i in enumerate(self.blocks):
            f_i = block_i['map']
            df_i = block_i['derivative']
            inv_f_i = block_i['inv_map']
            
            for j in range(self.n_blocks):
                if self.transition_graph[i, j] > 0:
                    # 新块为 f_i^{-1}(P_j) ∩ P_i
                    # 样本点为 y_ij 使得 f_i(y_ij) = x_j
                    try:
                        y_ij = inv_f_i(self.sample_points[j])
                        
                        new_block = {
                            'center': y_ij,
                            'map': f_i,
                            'inv_map': inv_f_i,
                            'derivative': df_i,
                            'parent': i,
                            'target': j
                        }
                        new_blocks.append(new_block)
                        new_sample_points.append(y_ij)
                    except Exception as e:
                        # 如果逆映射失败，跳过
                        pass
        
        # 构建新的转移图（所有可能的转移）
        n_new = len(new_blocks)
        new_graph = np.zeros((n_new, n_new))
        
        for i, block_i in enumerate(new_blocks):
            for j, block_j in enumerate(new_blocks):
                # 转移规则：如果 block_i.target == block_j.parent
                if block_i.get('target') == block_j.get('parent'):
                    new_graph[i, j] = 1
        
        refined = MarkovPartition(new_blocks, new_graph)
        return refined
    
    def get_diameters(self) -> np.ndarray:
        """返回各块的直径估计"""
        # 简化的直径估计：基于样本点之间的距离
        if len(self.sample_points) < 2:
            return np.array([1.0])
        
        # 使用样本点间最大距离作为直径估计
        diameters = []
        for i in range(self.n_blocks):
            # 找到父块相同的所有块
            parent_i = self.blocks[i].get('parent', i)
            siblings = [j for j in range(self.n_blocks) 
                       if self.blocks[j].get('parent', j) == parent_i]
            if len(siblings) > 1:
                pts = self.sample_points[siblings]
                diam = np.max(np.abs(pts[:, None] - pts[None, :]))
            else:
                diam = 1.0 / (self.n_blocks ** (1/2))  # 启发式估计
            diameters.append(diam)
        
        return np.array(diameters)


class BowenFormulaSolver:
    """
    Bowen公式求解器
    
    实现McMullen的特征值算法来计算Hausdorff维数。
    """
    
    def __init__(self, max_iter: int = 50, tolerance: float = 1e-6, verbose: bool = True):
        """
        初始化求解器
        
        Args:
            max_iter: 最大精细化迭代次数
            tolerance: 收敛容差
            verbose: 是否打印进度
        """
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.verbose = verbose
        self.history = []
        
    def _build_transition_matrix(self, partition: MarkovPartition) -> np.ndarray:
        """
        构建转移矩阵 T，其中 T[i,j] = |f'_i(y_ij)|^{-1}
        
        这里 y_ij 满足 f_i(y_ij) = x_j
        """
        n = partition.n_blocks
        T = np.zeros((n, n))
        
        for i in range(n):
            block_i = partition.blocks[i]
            f_i = block_i['map']
            df_i = block_i['derivative']
            inv_f_i = block_i['inv_map']
            
            for j in range(n):
                if partition.transition_graph[i, j] > 0:
                    try:
                        # 求解 y_ij 使得 f_i(y_ij) = x_j
                        y_ij = inv_f_i(partition.sample_points[j])
                        
                        # 计算导数 |f'_i(y_ij)|^{-1}
                        derivative = df_i(y_ij)
                        T[i, j] = 1.0 / abs(derivative)
                    except Exception as e:
                        T[i, j] = 0
        
        return T
    
    def _compute_spectral_radius(self, T_alpha: np.ndarray) -> float:
        """
        计算矩阵的谱半径（最大特征值的模）
        
        使用幂迭代方法
        """
        n = T_alpha.shape[0]
        if n == 0:
            return 0.0
        
        # 对于小矩阵使用直接计算
        if n <= 100:
            try:
                eigenvalues = np.linalg.eigvals(T_alpha)
                return max(abs(eigenvalues))
            except:
                pass
        
        # 幂迭代
        v = np.random.rand(n) + 0.1  # 避免零
        v = v / np.linalg.norm(v)
        
        lambda_old = 0
        for _ in range(1000):
            w = T_alpha @ v
            lambda_new = np.linalg.norm(w)
            if lambda_new < 1e-15:
                return 0.0
            v = w / lambda_new
            
            if abs(lambda_new - lambda_old) < 1e-12:
                return lambda_new
            lambda_old = lambda_new
        
        return lambda_new
    
    def _solve_alpha(self, T: np.ndarray, alpha_min: float = 0.01, 
                     alpha_max: float = 3.0) -> float:
        """
        求解 α 使得 λ(T^α) = 1
        
        使用Brent方法（稳健的二分法+割线法混合）
        """
        def objective(alpha):
            if alpha <= 0:
                return float('inf')
            T_alpha = T ** alpha
            return self._compute_spectral_radius(T_alpha) - 1.0
        
        # 检查边界
        try:
            f_min = objective(alpha_min)
            f_max = objective(alpha_max)
            
            # 扩展搜索范围如果需要
            while f_min > 0 and alpha_min > 0.001:
                alpha_min /= 2
                f_min = objective(alpha_min)
            
            while f_max < 0 and alpha_max < 10:
                alpha_max *= 2
                f_max = objective(alpha_max)
            
            if f_min * f_max > 0:
                # 符号相同，尝试线性搜索
                alphas = np.linspace(alpha_min, alpha_max, 100)
                best_alpha = alpha_min
                best_obj = abs(f_min)
                for a in alphas:
                    obj = abs(objective(a))
                    if obj < best_obj:
                        best_obj = obj
                        best_alpha = a
                return best_alpha
            
            alpha = brentq(objective, alpha_min, alpha_max, xtol=1e-12)
            return alpha
        except Exception as e:
            # 回退到简单二分法
            return self._simple_bisection(T, alpha_min, alpha_max)
    
    def _simple_bisection(self, T: np.ndarray, alpha_min: float, 
                          alpha_max: float) -> float:
        """简单二分法求解"""
        for _ in range(100):
            alpha_mid = (alpha_min + alpha_max) / 2
            T_alpha = T ** alpha_mid
            f_mid = self._compute_spectral_radius(T_alpha) - 1
            
            T_min = T ** alpha_min
            f_min = self._compute_spectral_radius(T_min) - 1
            
            if f_min * f_mid < 0:
                alpha_max = alpha_mid
            else:
                alpha_min = alpha_mid
            
            if alpha_max - alpha_min < 1e-10:
                break
        
        return (alpha_min + alpha_max) / 2
    
    def solve(self, initial_partition: MarkovPartition, 
              adaptive: bool = True, min_blocks: int = 1000) -> dict:
        """
        求解Hausdorff维数
        
        Args:
            initial_partition: 初始Markov分划
            adaptive: 是否使用自适应精细化
            min_blocks: 最小块数（用于自适应控制）
        
        Returns:
            结果字典，包含维数估计、历史记录等
        """
        partition = initial_partition
        self.history = []
        
        for iteration in range(self.max_iter):
            # 构建转移矩阵
            T = self._build_transition_matrix(partition)
            
            # 检查矩阵有效性
            if np.max(T) < 1e-15:
                raise ValueError("转移矩阵全为零，检查输入")
            
            # 求解 α
            alpha = self._solve_alpha(T)
            
            # 计算最大直径
            diameters = partition.get_diameters()
            max_diam = np.max(diameters)
            
            # 记录历史
            self.history.append({
                'iteration': iteration,
                'n_blocks': partition.n_blocks,
                'alpha': alpha,
                'max_diameter': max_diam
            })
            
            if self.verbose:
                print(f"Iter {iteration}: n={partition.n_blocks}, "
                      f"α={alpha:.10f}, diam={max_diam:.2e}")
            
            # 检查收敛
            if iteration > 0 and len(self.history) > 1:
                alpha_prev = self.history[-2]['alpha']
                if abs(alpha - alpha_prev) < self.tolerance and max_diam < self.tolerance * 10:
                    if self.verbose:
                        print(f"收敛！维数估计: {alpha:.10f}")
                    break
            
            # 精细化
            if iteration < self.max_iter - 1:
                partition = partition.refine()
                
                # 自适应控制：如果块数过多，跳过后续精细化
                if adaptive and partition.n_blocks > min_blocks * 10:
                    if self.verbose:
                        print(f"块数过多 ({partition.n_blocks})，停止精细化")
                    break
        
        result = {
            'dimension': alpha,
            'final_partition': partition,
            'history': self.history,
            'iterations': len(self.history)
        }
        
        return result


# =============================================================================
# 示例实现：具体动力系统的Hausdorff维数计算
# =============================================================================

class CantorSetExample:
    """
    标准三分Cantor集的维数计算
    
    理论维数: log(2)/log(3) ≈ 0.63093
    """
    
    @staticmethod
    def create_partition(n_blocks: int = 2) -> MarkovPartition:
        """创建Cantor集的Markov分划"""
        # 三分Cantor集由两个映射生成：
        # f_1(x) = x/3 在 [0, 1/3]
        # f_2(x) = (x+2)/3 在 [2/3, 1]
        
        blocks = [
            {
                'center': 0.0,  # 左端点（实际上是1/6代表块）
                'map': lambda x: x / 3,
                'inv_map': lambda y: 3 * y,
                'derivative': lambda x: 1/3
            },
            {
                'center': 1.0,  # 右端点
                'map': lambda x: (x + 2) / 3,
                'inv_map': lambda y: 3 * y - 2,
                'derivative': lambda x: 1/3
            }
        ]
        
        # 完全转移图
        transition = np.ones((2, 2))
        
        return MarkovPartition(blocks, transition)
    
    @staticmethod
    def theoretical_dimension() -> float:
        """理论维数"""
        return np.log(2) / np.log(3)


class LinearCantorExample:
    """
    一般线性Cantor集
    
    由比率 r1, r2, ..., rn 生成的Cantor集
    理论维数 δ 满足: r1^δ + r2^δ + ... + rn^δ = 1
    """
    
    def __init__(self, ratios: List[float]):
        """
        Args:
            ratios: 各分支的收缩比率列表
        """
        self.ratios = np.array(ratios)
        self.n = len(ratios)
    
    def create_partition(self) -> MarkovPartition:
        """创建Markov分划"""
        blocks = []
        
        offset = 0.0
        for r in self.ratios:
            block = {
                'center': offset,
                'map': lambda x, r=r: r * x,  # 注意闭包问题
                'inv_map': lambda y, r=r: y / r,
                'derivative': lambda x, r=r: r
            }
            blocks.append(block)
            offset += r
        
        transition = np.ones((self.n, self.n))
        return MarkovPartition(blocks, transition)
    
    def theoretical_dimension(self) -> float:
        """求解 Moran 方程 sum(r_i^δ) = 1"""
        from scipy.optimize import brentq
        
        def equation(delta):
            return np.sum(self.ratios ** delta) - 1
        
        try:
            return brentq(equation, 0.001, 3.0)
        except:
            return None


class QuadraticJuliaSet:
    """
    二次多项式 z^2 + c 的Julia集维数计算（简化版本）
    
    注意：完整实现需要外部射线理论，这里是简化近似
    """
    
    def __init__(self, c: complex, escape_radius: float = 2.0):
        """
        Args:
            c: 复参数
            escape_radius: 逃逸半径
        """
        self.c = c
        self.escape_radius = escape_radius
    
    def f(self, z: complex) -> complex:
        """映射 f(z) = z^2 + c"""
        return z * z + self.c
    
    def df(self, z: complex) -> complex:
        """导数 f'(z) = 2z"""
        return 2 * z
    
    def create_approximate_partition(self, n_points: int = 16) -> MarkovPartition:
        """
        创建近似的Markov分划
        
        使用圆周上的点来近似Julia集（仅在c接近0时较好）
        """
        # 对于小的c，Julia集近似于单位圆
        angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        
        blocks = []
        for theta in angles:
            # 单位圆上的点作为样本
            z = np.exp(1j * theta)
            
            block = {
                'center': z,
                'map': self.f,
                'inv_map': lambda w, z0=z: self._approx_inverse(w, z0),
                'derivative': lambda z: abs(2 * z)
            }
            blocks.append(block)
        
        # 全转移（近似）
        transition = np.ones((n_points, n_points))
        
        return MarkovPartition(blocks, transition)
    
    def _approx_inverse(self, w: complex, z0: complex) -> complex:
        """近似逆映射（使用Newton迭代）"""
        z = z0  # 初始猜测
        for _ in range(10):
            fz = z * z + self.c
            dfz = 2 * z
            if abs(dfz) < 1e-10:
                break
            z = z - (fz - w) / dfz
            if abs(fz - w) < 1e-12:
                break
        return z


class SchottkyGroupExample:
    """
    Schottky群示例：对称三圆配置
    
    三个圆与单位圆正交，生成Fuchsian群
    """
    
    def __init__(self, theta: float):
        """
        Args:
            theta: 每个圆与单位圆相交的弧长（弧度）
        """
        self.theta = theta
        
        # 计算三个圆的参数
        # 圆心在单位圆上，间隔 2π/3
        self.centers = [np.exp(1j * 2*np.pi*k/3) for k in range(3)]
        
        # 圆的半径：与单位圆相交弧长为 θ
        # 交点满足角度差为 θ/2
        self.radii = [np.sin(theta/2) for _ in range(3)]
    
    def reflection(self, z: complex, k: int) -> complex:
        """关于第k个圆的反射"""
        c = self.centers[k]
        r = self.radii[k]
        
        # 圆反射公式：z -> c + r^2 / (conj(z - c))
        if abs(z - c) < 1e-15:
            return float('inf')
        return c + r**2 / np.conj(z - c)
    
    def d_reflection(self, z: complex, k: int) -> float:
        """反射映射的导数（模）"""
        c = self.centers[k]
        r = self.radii[k]
        dz = abs(z - c)
        if dz < 1e-15:
            return float('inf')
        # |d/dz (c + r^2 / conj(z-c))| = r^2 / |z-c|^2
        return r**2 / dz**2
    
    def create_partition(self) -> MarkovPartition:
        """创建Markov分划"""
        blocks = []
        
        for k in range(3):
            # 样本点：圆盘的"中心"方向
            z0 = self.centers[k] * (1 - self.radii[k])
            
            block = {
                'center': z0,
                'map': lambda z, k=k: self.reflection(z, k),
                'inv_map': lambda w, k=k: self.reflection(w, k),  # 反射是自逆的
                'derivative': lambda z, k=k: self.d_reflection(z, k)
            }
            blocks.append(block)
        
        # 转移图：每个圆映射到其他两个圆
        transition = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ])
        
        return MarkovPartition(blocks, transition)


# =============================================================================
# 测试和演示
# =============================================================================

def demo_cantor_set():
    """演示：三分Cantor集的维数计算"""
    print("=" * 60)
    print("示例 1: 三分Cantor集")
    print("=" * 60)
    
    # 创建Cantor集示例
    cantor = CantorSetExample()
    partition = cantor.create_partition()
    
    # 理论值
    theoretical = cantor.theoretical_dimension()
    print(f"理论维数: log(2)/log(3) = {theoretical:.10f}")
    print()
    
    # 数值计算
    solver = BowenFormulaSolver(max_iter=15, tolerance=1e-8, verbose=True)
    result = solver.solve(partition, adaptive=False)
    
    print()
    print(f"计算结果: {result['dimension']:.10f}")
    print(f"绝对误差: {abs(result['dimension'] - theoretical):.2e}")
    print(f"迭代次数: {result['iterations']}")
    print()


def demo_linear_cantor():
    """演示：一般线性Cantor集"""
    print("=" * 60)
    print("示例 2: 线性Cantor集 (1/4, 1/4, 1/4)")
    print("=" * 60)
    
    # 三等分，每段比率 1/4
    ratios = [1/4, 1/4, 1/4, 1/4]
    cantor = LinearCantorExample(ratios)
    partition = cantor.create_partition()
    
    # 理论值：4 * (1/4)^δ = 1 => δ = 1
    theoretical = cantor.theoretical_dimension()
    print(f"理论维数: {theoretical:.10f} (如果存在)")
    print()
    
    # 数值计算
    solver = BowenFormulaSolver(max_iter=10, tolerance=1e-6, verbose=True)
    result = solver.solve(partition, adaptive=False)
    
    print()
    print(f"计算结果: {result['dimension']:.10f}")
    print(f"迭代次数: {result['iterations']}")
    print()


def demo_schottky():
    """演示：Schottky群"""
    print("=" * 60)
    print("示例 3: 对称Schottky群 (theta = 2π/3)")
    print("=" * 60)
    print("注：这是简化实现，用于演示算法结构")
    print()
    
    # theta = 2π/3 对应圆圈相切，极限集为单位圆
    schottky = SchottkyGroupExample(theta=2*np.pi/3 - 0.1)
    partition = schottky.create_partition()
    
    try:
        solver = BowenFormulaSolver(max_iter=8, tolerance=1e-5, verbose=True)
        result = solver.solve(partition, adaptive=True, min_blocks=100)
        
        print()
        print(f"计算结果: {result['dimension']:.6f}")
        print(f"参考值（theta接近2π/3时应接近1）: ~0.9-1.0")
    except Exception as e:
        print(f"计算出错: {e}")
    print()


def demo_dimension_graph():
    """生成维数随参数变化的图"""
    print("=" * 60)
    print("示例 4: 维数随参数变化")
    print("=" * 60)
    print("计算不同收缩比率下的Cantor集维数")
    print()
    
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    
    ratios_list = np.linspace(0.1, 0.45, 10)
    dimensions = []
    theoretical_dims = []
    
    for r in ratios_list:
        ratios = [r, r]  # 两分支Cantor集
        cantor = LinearCantorExample(ratios)
        
        try:
            partition = cantor.create_partition()
            solver = BowenFormulaSolver(max_iter=8, tolerance=1e-5, verbose=False)
            result = solver.solve(partition, adaptive=False)
            dimensions.append(result['dimension'])
            
            # 理论值：2*r^δ = 1 => δ = -log(2)/log(r)
            theo = -np.log(2) / np.log(r) if r < 0.5 else None
            theoretical_dims.append(theo)
        except Exception as e:
            dimensions.append(None)
            theoretical_dims.append(None)
    
    # 输出表格
    print("比率 r | 计算维数 | 理论维数")
    print("-" * 40)
    for r, d, t in zip(ratios_list, dimensions, theoretical_dims):
        if d is not None:
            print(f"{r:.3f}   | {d:.6f}  | {t:.6f}")
    
    # 保存图
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        valid_dims = [d for d in dimensions if d is not None]
        valid_ratios = [ratios_list[i] for i, d in enumerate(dimensions) if d is not None]
        valid_theo = [t for t in theoretical_dims if t is not None]
        
        ax.plot(valid_ratios, valid_dims, 'o-', label='计算值', markersize=8)
        ax.plot(valid_ratios, valid_theo, 's--', label='理论值', markersize=6, alpha=0.7)
        ax.set_xlabel('收缩比率 r', fontsize=12)
        ax.set_ylabel('Hausdorff维数', fontsize=12)
        ax.set_title('两分支Cantor集的维数', fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        output_path = '/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/kleinian/cantor_dimension_graph.png'
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        print(f"\n图已保存至: {output_path}")
    except Exception as e:
        print(f"绘图出错: {e}")
    
    print()


def print_algorithm_summary():
    """打印算法总结"""
    print("=" * 60)
    print("Bowen公式特征值算法总结")
    print("=" * 60)
    print("""
算法步骤:
1. 构造Markov分划 P = {(P_i, f_i)}
2. 选择样本点 x_i ∈ P_i
3. 对于每个转移对 i → j:
   - 计算 y_ij 使得 f_i(y_ij) = x_j
   - 计算 T_ij = |f'_i(y_ij)|^{-1}
4. 求解 α 使得 λ(T^α) = 1
5. 精细化分划并重复直到收敛

关键公式:
- Bowen公式: dim_H(Λ) = δ, 其中 P(-δ log|f'|) = 0
- 压力-谱关系: P(-s log|f'|) = log λ(T^s)
- 误差估计: |α - δ| = O(max diam(P_i))
- 收敛速度: O(ξ^{-n}) 指数收敛

理论保证:
- 对于扩张系统，算法收敛到真值
- 每轮精细化大约获得固定数量正确数字
- 需要 O(N) 轮精细化获得 N 位精度
""")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("McMullen Bowen公式算法实现")
    print("Hausdorff维数计算")
    print("=" * 60 + "\n")
    
    # 运行示例
    print_algorithm_summary()
    
    demo_cantor_set()
    demo_linear_cantor()
    demo_schottky()
    demo_dimension_graph()
    
    print("=" * 60)
    print("所有示例完成")
    print("=" * 60)
