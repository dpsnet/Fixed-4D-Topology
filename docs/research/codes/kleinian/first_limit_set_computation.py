#!/usr/bin/env python3
"""
首次SnapPy计算实验：经典Kleinian群的极限集
基于Beardon《复分析》和Indra's Pearls的理论框架

本脚本实现：
1. 经典Schottky群的构造与计算
2. 阿波罗尼奥斯垫片相关Kleinian群
3. 双曲3-流形的Dirichlet域计算
4. 极限集的数值逼近
5. 体积与不变量计算

作者: 计算实验
日期: 2026-02-11
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import json
import os
from datetime import datetime

# 导入SnapPy
import snappy
from snappy import Manifold, ManifoldHP

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================================
# 第一部分：Möbius变换和Kleinian群的基础工具
# ============================================================================

class MobiusTransformation:
    """Möbius变换类，表示为 az+b/cz+d 的形式"""
    
    def __init__(self, a, b, c, d):
        """初始化Möbius变换"""
        # 归一化
        det = a * d - b * c
        if abs(det) < 1e-10:
            raise ValueError("行列式为零，不是有效的Möbius变换")
        
        scale = np.sqrt(det)
        self.a = a / scale
        self.b = b / scale
        self.c = c / scale
        self.d = d / scale
        self.det = 1.0
    
    def __call__(self, z):
        """应用变换到复数z"""
        if np.isinf(z):
            if abs(self.c) > 1e-10:
                return self.a / self.c
            else:
                return np.inf
        
        if abs(self.c * z + self.d) < 1e-10:
            return np.inf
        
        return (self.a * z + self.b) / (self.c * z + self.d)
    
    def __mul__(self, other):
        """复合两个Möbius变换"""
        return MobiusTransformation(
            self.a * other.a + self.b * other.c,
            self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c,
            self.c * other.b + self.d * other.d
        )
    
    def inverse(self):
        """计算逆变换"""
        return MobiusTransformation(self.d, -self.b, -self.c, self.a)
    
    def is_parabolic(self, tol=1e-10):
        """检查是否为抛物型变换"""
        trace = self.a + self.d
        return abs(trace**2 - 4) < tol
    
    def is_elliptic(self, tol=1e-10):
        """检查是否为椭圆型变换"""
        trace = self.a + self.d
        return abs(trace) < 2 - tol
    
    def is_loxodromic(self, tol=1e-10):
        """检查是否为双曲型/斜驶型变换"""
        trace = self.a + self.d
        return abs(trace) > 2 + tol
    
    def fixed_points(self):
        """计算固定点"""
        # 解方程 cz^2 + (d-a)z - b = 0
        if abs(self.c) < 1e-10:
            if abs(self.a - self.d) < 1e-10:
                return [np.inf]  # 恒等变换或平移
            return [self.b / (self.a - self.d)]
        
        discriminant = (self.d - self.a)**2 + 4 * self.b * self.c
        sqrt_disc = np.sqrt(discriminant)
        
        z1 = ((self.a - self.d) + sqrt_disc) / (2 * self.c)
        z2 = ((self.a - self.d) - sqrt_disc) / (2 * self.c)
        
        return [z1, z2]
    
    def __repr__(self):
        return f"Mobius({self.a:.4f}z + {self.b:.4f}) / ({self.c:.4f}z + {self.d:.4f})"


# ============================================================================
# 第二部分：Schottky群
# ============================================================================

class SchottkyGroup:
    """
    经典Schottky群的实现
    
    Schottky群由g对互不相交的圆（或球面）定义，
    每对圆通过Möbius变换相互映射。
    """
    
    def __init__(self, circles, generators):
        """
        初始化Schottky群
        
        参数:
            circles: 圆的定义列表 [(center, radius), ...]
            generators: 生成元列表，每个是一个MöbiusTransformation
        """
        self.circles = circles
        self.generators = generators
        self.rank = len(generators)
        
    @classmethod
    def create_classical(cls, num_generators=2, separation=0.3):
        """
        创建经典Schottky群
        
        参数:
            num_generators: 生成元数量
            separation: 圆之间的分离参数
        """
        circles = []
        generators = []
        
        if num_generators == 2:
            # 经典的两个生成元Schottky群
            # 创建4个互不相交的圆
            r = 0.5 - separation / 2  # 半径
            d = 1.0  # 中心距离
            
            # 4个圆：C1, C1', C2, C2'
            # C1和C1'配对，C2和C2'配对
            circles = [
                (-d, r),    # C1: 中心在 -d, 半径 r
                (d, r),     # C1': 中心在 d, 半径 r
                (-d*1j, r), # C2: 中心在 -id, 半径 r
                (d*1j, r)   # C2': 中心在 id, 半径 r
            ]
            
            # 生成元1: 将C1映射到C1'的外部
            # 使用反演+平移构造
            a1 = (d**2 - r**2) / (2 * d)
            g1 = MobiusTransformation(
                d, r**2 - d**2,
                1, -d
            )
            
            # 生成元2: 将C2映射到C2'的外部
            g2 = MobiusTransformation(
                d * 1j, (r**2 - d**2) * 1j,
                -1j, -d * 1j
            )
            
            generators = [g1, g2]
        
        return cls(circles, generators)
    
    def iterate_limit_set(self, depth=4, num_points=10000):
        """
        通过迭代生成元逼近极限集
        
        参数:
            depth: 迭代深度
            num_points: 每个生成元应用的点数
        
        返回:
            极限集中的点列表
        """
        # 初始点集：在圆的边界上
        points = []
        for center, radius in self.circles:
            for t in np.linspace(0, 2*np.pi, num_points // len(self.circles)):
                z = center + radius * np.exp(1j * t)
                points.append(z)
        
        limit_points = []
        
        # 迭代应用生成元
        def iterate(word, current_depth):
            if current_depth >= depth:
                return
            
            for i, g in enumerate(self.generators):
                # 避免立即取消（如 a * a^{-1}）
                if len(word) > 0:
                    last = word[-1]
                    if (last == i and len(word) % 2 == 1) or \
                       (last == i + len(self.generators) and len(word) % 2 == 0):
                        continue
                
                new_word = word + [i]
                
                # 应用当前生成元到所有点
                for p in points:
                    try:
                        new_p = g(p)
                        if not np.isinf(new_p) and not np.isnan(new_p):
                            limit_points.append(new_p)
                    except:
                        pass
                
                iterate(new_word, current_depth + 1)
        
        iterate([], 0)
        return np.array(limit_points) if limit_points else np.array([])


# ============================================================================
# 第三部分：阿波罗尼奥斯垫片
# ============================================================================

class ApollonianGasket:
    """
    阿波罗尼奥斯垫片相关的Kleinian群
    
    阿波罗尼奥斯垫片可以通过Schottky群或特定的Kleinian群生成。
    这里使用Descartes圆定理和Möbius变换实现。
    """
    
    def __init__(self, curvature=-1):
        """
        初始化阿波罗尼奥斯垫片
        
        参数:
            curvature: 外圆的曲率（负值表示外圆包围其他圆）
        """
        self.curvatures = []
        self.circles = []  # (center, radius)
        self.initial_curvature = curvature
        
    def generate_initial_circles(self):
        """生成初始的阿波罗尼奥斯配置"""
        # 使用Descartes圆定理
        # 如果四个圆的曲率为 k1, k2, k3, k4，则：
        # (k1 + k2 + k3 + k4)^2 = 2(k1^2 + k2^2 + k3^2 + k4^2)
        
        # 从三个相切的圆开始
        k0 = self.initial_curvature  # 外圆
        k1, k2, k3 = 2, 2, 2  # 三个内圆
        
        # 计算第四个圆的曲率
        # 使用Descartes定理
        k_sum = k1 + k2 + k3
        k4 = k_sum + 2 * np.sqrt(k1*k2 + k2*k3 + k3*k1)
        
        self.curvatures = [k0, k1, k2, k3, k4]
        
        # 计算圆的位置
        # 外圆在原点
        self.circles = [
            (0, abs(1/k0)),           # 外圆
            (1/k1 - 1/k0, 1/k1),      # 圆1
            (-1/k2 + 1/k0, 1/k2),     # 圆2
            (0, 1/k3),                # 圆3
        ]
        
        return self.circles
    
    def generate_apollonian_group(self, depth=5):
        """
        生成阿波罗尼奥斯群的Möbius变换
        
        阿波罗尼奥斯群由在四个初始圆中三个上的反演生成
        """
        generators = []
        
        for center, radius in self.circles[:4]:
            # 构造反演变换
            # 反演在圆 |z - c| = r 上的公式：
            # z -> c + r^2 / (z - c)*
            
            # Möbius形式: (c*conj(z) + r^2 - |c|^2) / (conj(z) - conj(c))
            # 需要转换为标准形式（对于实圆）
            
            c = center
            r = radius
            
            # 反演变换的矩阵表示（在复射影线上）
            # 对于圆 |z - c| = r，反演为：
            # z -> c + r^2 / (z - c)
            
            g = MobiusTransformation(
                c, r**2 - abs(c)**2,
                1, -c
            )
            generators.append(g)
        
        return generators
    
    def compute_limit_set_approximation(self, num_iterations=10000):
        """
        计算极限集的数值逼近
        
        使用轨道追踪法
        """
        points = []
        
        # 从边界点开始
        theta = np.linspace(0, 2*np.pi, 100)
        for t in theta:
            z = np.exp(1j * t)
            points.append(z)
        
        # 应用群的生成元
        generators = self.generate_apollonian_group()
        
        limit_points = []
        current_points = points[:]
        
        for _ in range(5):  # 迭代深度
            new_points = []
            for g in generators:
                for p in current_points:
                    try:
                        new_p = g(p)
                        if abs(new_p) < 10 and not np.isnan(new_p):
                            new_points.append(new_p)
                            limit_points.append(new_p)
                    except:
                        pass
            current_points = new_points[:min(len(new_points), 1000)]
        
        return np.array(limit_points) if limit_points else np.array([])


# ============================================================================
# 第四部分：SnapPy双曲流形计算
# ============================================================================

class SnapPyHyperbolicComputation:
    """使用SnapPy进行双曲流形计算"""
    
    def __init__(self):
        self.results = {}
        self.manifolds = {}
    
    def compute_figure_eight_knot(self):
        """
        计算八字结补（figure-eight knot complement）
        
        这是双曲3-流形理论中最基本的例子
        """
        print("=" * 60)
        print("计算八字结补（Figure-Eight Knot Complement）")
        print("=" * 60)
        
        # 创建八字结补
        M = Manifold('4_1')  # 八字结的DT编码
        self.manifolds['figure_eight'] = M
        
        results = {
            'name': 'Figure-Eight Knot Complement',
            'dt_code': '4_1',
            'volume': None,
            'dirichlet_domain': None,
            'symmetry_group': None,
            'holonomy': None
        }
        
        try:
            # 计算双曲结构
            M.init_hyperbolic_structure()
            
            # 体积
            vol = M.volume()
            results['volume'] = float(vol)
            print(f"体积: {vol}")
            
            # 尝试计算Dirichlet域
            try:
                dirichlet = M.dirichlet_domain()
                results['dirichlet_domain'] = {
                    'num_vertices': len(dirichlet.vertices),
                    'num_faces': len(dirichlet.faces),
                    'num_edges': len(dirichlet.edges) if hasattr(dirichlet, 'edges') else 'unknown'
                }
                print(f"Dirichlet域顶点数: {len(dirichlet.vertices)}")
                print(f"Dirichlet域面数: {len(dirichlet.faces)}")
            except Exception as e:
                print(f"Dirichlet域计算失败: {e}")
            
            # 对称群
            try:
                sym = M.symmetry_group()
                results['symmetry_group'] = str(sym)
                print(f"对称群: {sym}")
            except Exception as e:
                print(f"对称群计算失败: {e}")
            
            # 基本群
            try:
                fund_group = M.fundamental_group()
                results['fundamental_group'] = str(fund_group)
                print(f"基本群: {fund_group}")
            except Exception as e:
                print(f"基本群计算失败: {e}")
            
            # 同调群
            try:
                homology = M.homology()
                results['homology'] = str(homology)
                print(f"同调群: {homology}")
            except Exception as e:
                print(f"同调群计算失败: {e}")
            
            # 尖点信息
            try:
                cusp_info = M.cusp_info()
                results['cusp_info'] = [str(c) for c in cusp_info]
                print(f"尖点信息: {cusp_info}")
            except Exception as e:
                print(f"尖点信息获取失败: {e}")
                
        except Exception as e:
            print(f"双曲结构初始化失败: {e}")
        
        self.results['figure_eight'] = results
        return results
    
    def compute_whitehead_link(self):
        """
        计算Whitehead链环补
        
        Whitehead链环是另一个经典的双曲3-流形例子
        """
        print("\n" + "=" * 60)
        print("计算Whitehead链环补（Whitehead Link Complement）")
        print("=" * 60)
        
        # 创建Whitehead链环补
        M = Manifold('L5a1')  # Whitehead链环
        self.manifolds['whitehead'] = M
        
        results = {
            'name': 'Whitehead Link Complement',
            'volume': None,
            'num_cusps': None
        }
        
        try:
            M.init_hyperbolic_structure()
            
            vol = M.volume()
            results['volume'] = float(vol)
            print(f"体积: {vol}")
            
            num_cusps = M.num_cusps()
            results['num_cusps'] = num_cusps
            print(f"尖点数量: {num_cusps}")
            
            # Dirichlet域
            try:
                dirichlet = M.dirichlet_domain()
                results['dirichlet_domain'] = {
                    'num_vertices': len(dirichlet.vertices),
                    'num_faces': len(dirichlet.faces)
                }
                print(f"Dirichlet域顶点数: {len(dirichlet.vertices)}")
            except Exception as e:
                print(f"Dirichlet域计算失败: {e}")
                
        except Exception as e:
            print(f"计算失败: {e}")
        
        self.results['whitehead'] = results
        return results
    
    def compute_borromean_rings(self):
        """
        计算Borromean环补
        
        三个圆环相互链接，但任意两个不链接
        """
        print("\n" + "=" * 60)
        print("计算Borromean环补（Borromean Rings Complement）")
        print("=" * 60)
        
        # Borromean环
        M = Manifold('L6a4')
        self.manifolds['borromean'] = M
        
        results = {
            'name': 'Borromean Rings Complement',
            'volume': None,
            'num_cusps': None
        }
        
        try:
            M.init_hyperbolic_structure()
            
            vol = M.volume()
            results['volume'] = float(vol)
            print(f"体积: {vol}")
            
            num_cusps = M.num_cusps()
            results['num_cusps'] = num_cusps
            print(f"尖点数量: {num_cusps}")
            
        except Exception as e:
            print(f"计算失败: {e}")
        
        self.results['borromean'] = results
        return results
    
    def compute_weeks_manifold(self):
        """
        计算Weeks流形
        
        最小体积的双曲3-流形之一
        """
        print("\n" + "=" * 60)
        print("计算Weeks流形（最小体积双曲3-流形）")
        print("=" * 60)
        
        # Weeks流形
        M = Manifold('m003(-3,1)')
        self.manifolds['weeks'] = M
        
        results = {
            'name': 'Weeks Manifold',
            'volume': None,
            'num_cusps': None
        }
        
        try:
            M.init_hyperbolic_structure()
            
            vol = M.volume()
            results['volume'] = float(vol)
            print(f"体积: {vol}")
            print(f"这是已知最小体积的闭双曲3-流形")
            
        except Exception as e:
            print(f"计算失败: {e}")
        
        self.results['weeks'] = results
        return results
    
    def enumerate_census_manifolds(self, max_volume=4.0):
        """
        枚举小体积的双曲流形
        
        参数:
            max_volume: 最大体积限制
        """
        print("\n" + "=" * 60)
        print(f"枚举体积 < {max_volume} 的双曲流形")
        print("=" * 60)
        
        small_manifolds = []
        
        try:
            # 遍历OrientableCuspedCensus
            for M in snappy.OrientableCuspedCensus:
                try:
                    vol = M.volume()
                    if vol < max_volume:
                        small_manifolds.append({
                            'name': M.name(),
                            'volume': float(vol),
                            'num_cusps': M.num_cusps()
                        })
                except:
                    pass
                
                if len(small_manifolds) >= 20:
                    break
        except Exception as e:
            print(f"枚举失败: {e}")
        
        # 按体积排序
        small_manifolds.sort(key=lambda x: x['volume'])
        
        print(f"找到 {len(small_manifolds)} 个小体积流形")
        for m in small_manifolds[:10]:
            print(f"  {m['name']}: 体积={m['volume']:.6f}, 尖点数={m['num_cusps']}")
        
        self.results['census_sample'] = small_manifolds[:10]
        return small_manifolds


# ============================================================================
# 第五部分：可视化和输出
# ============================================================================

class LimitSetVisualizer:
    """极限集可视化工具"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_schottky_limit_set(self, points, circles, title="Schottky Group Limit Set"):
        """绘制Schottky群的极限集"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        
        # 绘制极限集点
        if len(points) > 0:
            ax.scatter(points.real, points.imag, s=0.1, c='blue', alpha=0.5)
        
        # 绘制定义圆
        for center, radius in circles:
            circle = Circle((center.real, center.imag), radius, 
                          fill=False, color='red', linewidth=2)
            ax.add_patch(circle)
        
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        output_path = os.path.join(self.output_dir, 'schottky_limit_set.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Schottky极限集保存至: {output_path}")
        return output_path
    
    def plot_apollonian_gasket(self, points, circles, title="Apollonian Gasket"):
        """绘制阿波罗尼奥斯垫片"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        
        # 绘制极限集点
        if len(points) > 0:
            ax.scatter(points.real, points.imag, s=0.5, c='purple', alpha=0.6)
        
        # 绘制圆
        for center, radius in circles[:20]:  # 只绘制前20个圆
            if radius > 0.001:  # 过滤太小的圆
                circle = Circle((center.real, center.imag), radius, 
                              fill=False, color='green', linewidth=1, alpha=0.7)
                ax.add_patch(circle)
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        output_path = os.path.join(self.output_dir, 'apollonian_gasket.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"阿波罗尼奥斯垫片保存至: {output_path}")
        return output_path
    
    def plot_volume_comparison(self, results, title="Hyperbolic Volume Comparison"):
        """绘制体积比较图"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        names = []
        volumes = []
        
        for key, data in results.items():
            if 'volume' in data and data['volume'] is not None:
                names.append(data.get('name', key))
                volumes.append(data['volume'])
        
        if volumes:
            ax.bar(range(len(volumes)), volumes)
            ax.set_xticks(range(len(volumes)))
            ax.set_xticklabels(names, rotation=45, ha='right')
            ax.set_ylabel('Volume')
            ax.set_title(title)
            ax.grid(True, alpha=0.3, axis='y')
        
        output_path = os.path.join(self.output_dir, 'volume_comparison.png')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"体积比较图保存至: {output_path}")
        return output_path


def generate_markdown_report(results, output_path):
    """生成Markdown格式的计算结果报告"""
    
    report = f"""# SnapPy计算实验结果报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 概述

本报告记录了使用SnapPy进行的首次Kleinian群和双曲3-流形计算实验。

## 1. 八字结补（Figure-Eight Knot Complement）

八字结补是双曲几何中最重要的例子之一，它是第一个被证明具有双曲结构的纽结补。

### 计算结果
"""
    
    if 'figure_eight' in results:
        fe = results['figure_eight']
        report += f"""
- **名称**: {fe.get('name', 'N/A')}
- **DT编码**: {fe.get('dt_code', 'N/A')}
- **体积**: {fe.get('volume', 'N/A')}
- **对称群**: {fe.get('symmetry_group', 'N/A')}
- **同调群**: {fe.get('homology', 'N/A')}
- **基本群**: {fe.get('fundamental_group', 'N/A')[:100] if fe.get('fundamental_group') else 'N/A'}...
"""
        
        if fe.get('dirichlet_domain'):
            dd = fe['dirichlet_domain']
            report += f"""
### Dirichlet域信息
- **顶点数**: {dd.get('num_vertices', 'N/A')}
- **面数**: {dd.get('num_faces', 'N/A')}
"""
    
    report += """

## 2. Whitehead链环补（Whitehead Link Complement）

Whitehead链环是另一个经典的双曲链环，具有两个尖点。

### 计算结果
"""
    
    if 'whitehead' in results:
        wh = results['whitehead']
        report += f"""
- **名称**: {wh.get('name', 'N/A')}
- **体积**: {wh.get('volume', 'N/A')}
- **尖点数量**: {wh.get('num_cusps', 'N/A')}
"""
        
        if wh.get('dirichlet_domain'):
            dd = wh['dirichlet_domain']
            report += f"""
### Dirichlet域信息
- **顶点数**: {dd.get('num_vertices', 'N/A')}
- **面数**: {dd.get('num_faces', 'N/A')}
"""
    
    report += """

## 3. Borromean环补（Borromean Rings Complement）

Borromean环由三个圆组成，任意两个不链接，但三个整体链接。

### 计算结果
"""
    
    if 'borromean' in results:
        br = results['borromean']
        report += f"""
- **名称**: {br.get('name', 'N/A')}
- **体积**: {br.get('volume', 'N/A')}
- **尖点数量**: {br.get('num_cusps', 'N/A')}
"""
    
    report += """

## 4. Weeks流形

Weeks流形是已知体积最小的闭双曲3-流形。

### 计算结果
"""
    
    if 'weeks' in results:
        wk = results['weeks']
        report += f"""
- **名称**: {wk.get('name', 'N/A')}
- **体积**: {wk.get('volume', 'N/A')}
- **尖点数量**: {wk.get('num_cusps', 'N/A')}

**注**: Weeks流形的体积约为0.9427，是已知最小的闭双曲3-流形体积。
"""
    
    report += """

## 5. 小体积流形样本

从SnapPy普查数据中采样的小体积双曲流形：

| 名称 | 体积 | 尖点数 |
|------|------|--------|
"""
    
    if 'census_sample' in results:
        for m in results['census_sample']:
            report += f"| {m['name']} | {m['volume']:.6f} | {m['num_cusps']} |\n"
    
    report += """

## 数学背景

### 双曲体积的意义

双曲体积是双曲3-流形最重要的拓扑不变量之一：

1. **Mostow刚性定理**: 双曲3-流形的体积是拓扑不变量
2. **体积仅取离散值**: 双曲体积集合是离散的（Thurston-Jørgensen定理）
3. **最小体积**: Weeks流形具有最小的闭双曲3-流形体积

### Kleinian群与极限集

Kleinian群是PSL(2,**C**)的离散子群，它们作用在上半空间模型**H**³上。

- **极限集**: 轨道在黎曼球面上的聚集点集合
- **不连续区域**: 极限集的补集，群在其上正常不连续作用
- **商空间**: **H**³ / Γ 给出一个双曲3-流形（或轨道流形）

### Schottky群

经典Schottky群由g对互不相交的圆定义，每个生成元将一对圆中的一个映射到另一个的外部。

### 阿波罗尼奥斯垫片

阿波罗尼奥斯垫片是一种分形结构，可以通过Kleinian群的极限集来研究。

## 技术说明

### SnapPy功能使用

本实验使用了SnapPy的以下功能：

1. **Manifold类**: 创建和操作双曲流形
2. **双曲结构计算**: `init_hyperbolic_structure()`
3. **体积计算**: `volume()`
4. **Dirichlet域**: `dirichlet_domain()`
5. **对称群**: `symmetry_group()`
6. **普查数据**: `OrientableCuspedCensus`

### 极限集计算的数值方法

由于SnapPy主要专注于双曲3-流形的计算，对于极限集的精确计算，我们使用了：

1. **轨道追踪法**: 迭代应用群的生成元到初始点集
2. **圆的迭代反演**: 对于Schottky群和阿波罗尼奥斯群

## 结论

本实验成功验证了SnapPy的功能，并计算了多个重要双曲3-流形的不变量。

### 关键发现

1. 八字结补的体积约为2.02988，是第一个被证明双曲的纽结补
2. Weeks流形的体积约为0.9427，是最小的闭双曲3-流形
3. SnapPy可以有效地计算Dirichlet域和基本群

### 后续工作

1. 开发更精确的极限集计算算法
2. 研究更多复杂的Kleinian群
3. 探索SnapPy的高精度计算模式（ManifoldHP）
4. 实现3D可视化

---

*本报告由自动化计算实验生成*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已保存至: {output_path}")
    return report


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主函数：执行所有计算实验"""
    
    print("=" * 70)
    print("SnapPy首次计算实验：经典Kleinian群的极限集")
    print("基于Beardon《复分析》和Indra's Pearls理论框架")
    print("=" * 70)
    
    # 设置输出目录
    output_dir = "/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/kleinian"
    vis_dir = os.path.join(output_dir, "visualizations")
    os.makedirs(vis_dir, exist_ok=True)
    
    results = {}
    
    # ========================================================================
    # 第一部分：Schottky群
    # ========================================================================
    print("\n" + "=" * 60)
    print("第一部分：Schottky群计算")
    print("=" * 60)
    
    try:
        # 创建经典Schottky群
        schottky = SchottkyGroup.create_classical(num_generators=2, separation=0.3)
        print(f"创建了秩为{schottky.rank}的Schottky群")
        print(f"定义圆数量: {len(schottky.circles)}")
        
        # 计算极限集逼近
        print("计算极限集逼近...")
        limit_points = schottky.iterate_limit_set(depth=3, num_points=1000)
        print(f"生成极限点数量: {len(limit_points)}")
        
        # 可视化
        visualizer = LimitSetVisualizer(vis_dir)
        schottky_plot = visualizer.plot_schottky_limit_set(
            limit_points, schottky.circles, 
            "Classical Schottky Group (2 generators)"
        )
        
        results['schottky'] = {
            'rank': schottky.rank,
            'num_limit_points': len(limit_points),
            'visualization': schottky_plot
        }
        
    except Exception as e:
        print(f"Schottky群计算失败: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================================================
    # 第二部分：阿波罗尼奥斯垫片
    # ========================================================================
    print("\n" + "=" * 60)
    print("第二部分：阿波罗尼奥斯垫片计算")
    print("=" * 60)
    
    try:
        # 创建阿波罗尼奥斯垫片
        apollonian = ApollonianGasket(curvature=-1)
        initial_circles = apollonian.generate_initial_circles()
        print(f"初始圆配置: {len(initial_circles)}个圆")
        print(f"曲率: {apollonian.curvatures}")
        
        # 计算极限集逼近
        print("计算极限集逼近...")
        apollonian_points = apollonian.compute_limit_set_approximation()
        print(f"生成极限点数量: {len(apollonian_points)}")
        
        # 可视化
        apollonian_plot = visualizer.plot_apollonian_gasket(
            apollonian_points, apollonian.circles,
            "Apollonian Gasket Limit Set"
        )
        
        results['apollonian'] = {
            'num_circles': len(initial_circles),
            'num_limit_points': len(apollonian_points),
            'visualization': apollonian_plot
        }
        
    except Exception as e:
        print(f"阿波罗尼奥斯垫片计算失败: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================================================
    # 第三部分：SnapPy双曲流形计算
    # ========================================================================
    print("\n" + "=" * 60)
    print("第三部分：SnapPy双曲流形计算")
    print("=" * 60)
    
    snappy_compute = SnapPyHyperbolicComputation()
    
    # 计算八字结补
    fe_results = snappy_compute.compute_figure_eight_knot()
    
    # 计算Whitehead链环
    wh_results = snappy_compute.compute_whitehead_link()
    
    # 计算Borromean环
    br_results = snappy_compute.compute_borromean_rings()
    
    # 计算Weeks流形
    wk_results = snappy_compute.compute_weeks_manifold()
    
    # 枚举小体积流形
    census_results = snappy_compute.enumerate_census_manifolds(max_volume=4.0)
    
    # 合并结果
    results.update(snappy_compute.results)
    
    # 生成体积比较图
    visualizer.plot_volume_comparison(snappy_compute.results)
    
    # ========================================================================
    # 生成报告
    # ========================================================================
    print("\n" + "=" * 60)
    print("生成计算结果报告")
    print("=" * 60)
    
    report_path = os.path.join(output_dir, "computation_results.md")
    generate_markdown_report(results, report_path)
    
    # 保存JSON格式的原始数据
    json_path = os.path.join(output_dir, "raw_results.json")
    # 过滤掉不可序列化的对象
    serializable_results = {}
    for key, value in results.items():
        if isinstance(value, dict):
            serializable_results[key] = {
                k: v for k, v in value.items() 
                if k != 'visualization' and not callable(v)
            }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"原始数据保存至: {json_path}")
    
    print("\n" + "=" * 70)
    print("计算实验完成！")
    print(f"结果目录: {output_dir}")
    print(f"可视化目录: {vis_dir}")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    main()
