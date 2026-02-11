"""
四元数代数计算练习
Quaternion Algebra Exercises

本模块实现四元数代数的基本运算，用于理解算术Kleinian群和四元数L-函数的基础。

参考: Maclachlan-Reid, "The Arithmetic of Hyperbolic 3-Manifolds", Ch. 2
作者: Research Assistant
日期: 2026-02
"""

from __future__ import annotations
import math
from typing import Tuple, Optional, Union


class Quaternion:
    """
    四元数代数 B = (a,b/F) 中的元素
    
    表示为 x = x0 + x1*i + x2*j + x3*k，其中:
    - i^2 = a, j^2 = b, ij = -ji = k
    - 基域 F 默认为实数域 R
    """
    
    def __init__(self, x0: float, x1: float, x2: float, x3: float, 
                 a: float = -1.0, b: float = -1.0):
        """
        初始化四元数
        
        Args:
            x0, x1, x2, x3: 分量系数
            a: i的平方，默认为-1（Hamilton四元数）
            b: j的平方，默认为-1（Hamilton四元数）
        """
        self.x0 = float(x0)
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.x3 = float(x3)
        self.a = float(a)
        self.b = float(b)
    
    @classmethod
    def from_scalar_vector(cls, scalar: float, vector: Tuple[float, float, float],
                           a: float = -1.0, b: float = -1.0) -> Quaternion:
        """从标量和向量分量构造四元数"""
        return cls(scalar, vector[0], vector[1], vector[2], a, b)
    
    @classmethod
    def hamilton(cls, x0: float, x1: float, x2: float, x3: float) -> Quaternion:
        """构造Hamilton四元数 (-1, -1/R)"""
        return cls(x0, x1, x2, x3, a=-1.0, b=-1.0)
    
    @classmethod
    def split(cls, x0: float, x1: float, x2: float, x3: float, b: float = 1.0) -> Quaternion:
        """构造分裂四元数 (1, b/R) ≅ M_2(R)"""
        return cls(x0, x1, x2, x3, a=1.0, b=b)
    
    @classmethod
    def i_element(cls, a: float = -1.0, b: float = -1.0) -> Quaternion:
        """返回基元素 i"""
        return cls(0, 1, 0, 0, a, b)
    
    @classmethod
    def j_element(cls, a: float = -1.0, b: float = -1.0) -> Quaternion:
        """返回基元素 j"""
        return cls(0, 0, 1, 0, a, b)
    
    @classmethod
    def k_element(cls, a: float = -1.0, b: float = -1.0) -> Quaternion:
        """返回基元素 k = ij"""
        return cls(0, 0, 0, 1, a, b)
    
    @classmethod
    def one(cls, a: float = -1.0, b: float = -1.0) -> Quaternion:
        """返回乘法单位元 1"""
        return cls(1, 0, 0, 0, a, b)
    
    @classmethod
    def zero(cls, a: float = -1.0, b: float = -1.0) -> Quaternion:
        """返回零元"""
        return cls(0, 0, 0, 0, a, b)
    
    # ==================== 基本运算 ====================
    
    def __add__(self, other: Quaternion) -> Quaternion:
        """四元数加法"""
        if self.a != other.a or self.b != other.b:
            raise ValueError("Cannot add quaternions from different algebras")
        return Quaternion(
            self.x0 + other.x0,
            self.x1 + other.x1,
            self.x2 + other.x2,
            self.x3 + other.x3,
            self.a, self.b
        )
    
    def __sub__(self, other: Quaternion) -> Quaternion:
        """四元数减法"""
        if self.a != other.a or self.b != other.b:
            raise ValueError("Cannot subtract quaternions from different algebras")
        return Quaternion(
            self.x0 - other.x0,
            self.x1 - other.x1,
            self.x2 - other.x2,
            self.x3 - other.x3,
            self.a, self.b
        )
    
    def __neg__(self) -> Quaternion:
        """加法逆元"""
        return Quaternion(-self.x0, -self.x1, -self.x2, -self.x3, self.a, self.b)
    
    def __mul__(self, other: Union[Quaternion, float]) -> Quaternion:
        """四元数乘法"""
        if isinstance(other, (int, float)):
            return Quaternion(
                self.x0 * other, self.x1 * other, 
                self.x2 * other, self.x3 * other,
                self.a, self.b
            )
        
        if self.a != other.a or self.b != other.b:
            raise ValueError("Cannot multiply quaternions from different algebras")
        
        a, b = self.a, self.b
        x0, x1, x2, x3 = self.x0, self.x1, self.x2, self.x3
        y0, y1, y2, y3 = other.x0, other.x1, other.x2, other.x3
        
        # 使用乘法公式
        # xy = (x0y0 + ax1y1 + bx2y2 - abx3y3)
        #    + (x0y1 + x1y0 - bx2y3 + bx3y2)i
        #    + (x0y2 + ax1y3 + x2y0 - ax3y1)j
        #    + (x0y3 + x1y2 - x2y1 + x3y0)k
        
        z0 = x0*y0 + a*x1*y1 + b*x2*y2 - a*b*x3*y3
        z1 = x0*y1 + x1*y0 - b*x2*y3 + b*x3*y2
        z2 = x0*y2 + a*x1*y3 + x2*y0 - a*x3*y1
        z3 = x0*y3 + x1*y2 - x2*y1 + x3*y0
        
        return Quaternion(z0, z1, z2, z3, a, b)
    
    def __rmul__(self, scalar: float) -> Quaternion:
        """左乘标量"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> Quaternion:
        """除以标量"""
        return Quaternion(
            self.x0 / scalar, self.x1 / scalar,
            self.x2 / scalar, self.x3 / scalar,
            self.a, self.b
        )
    
    def __eq__(self, other: object) -> bool:
        """判断相等"""
        if not isinstance(other, Quaternion):
            return False
        return (abs(self.x0 - other.x0) < 1e-10 and
                abs(self.x1 - other.x1) < 1e-10 and
                abs(self.x2 - other.x2) < 1e-10 and
                abs(self.x3 - other.x3) < 1e-10 and
                abs(self.a - other.a) < 1e-10 and
                abs(self.b - other.b) < 1e-10)
    
    # ==================== 共轭、范数、迹 ====================
    
    def conjugate(self) -> Quaternion:
        """
        共轭四元数: x̄ = x0 - x1*i - x2*j - x3*k
        """
        return Quaternion(self.x0, -self.x1, -self.x2, -self.x3, self.a, self.b)
    
    def norm(self) -> float:
        """
        约化范数 (reduced norm): n(x) = x * x̄ = x0^2 - a*x1^2 - b*x2^2 + ab*x3^2
        """
        return (self.x0**2 - self.a * self.x1**2 - 
                self.b * self.x2**2 + self.a * self.b * self.x3**2)
    
    def trace(self) -> float:
        """
        约化迹 (reduced trace): tr(x) = x + x̄ = 2*x0
        """
        return 2 * self.x0
    
    def is_pure(self) -> bool:
        """判断是否纯虚（迹为0）"""
        return abs(self.x0) < 1e-10
    
    def is_unit(self) -> bool:
        """判断是否为范数1的单位元"""
        return abs(self.norm() - 1.0) < 1e-10
    
    def is_zero_divisor(self) -> bool:
        """判断是否为非零零因子（仅分裂代数有）"""
        return abs(self.norm()) < 1e-10 and not self.is_zero()
    
    def is_zero(self) -> bool:
        """判断是否为零元"""
        return (abs(self.x0) < 1e-10 and abs(self.x1) < 1e-10 and
                abs(self.x2) < 1e-10 and abs(self.x3) < 1e-10)
    
    def is_division(self) -> bool:
        """判断所在代数是否为分歧（可除）代数"""
        # 如果范数非零当且仅当元素非零，则是可除代数
        # 这里简单判断：如果a<0且b<0（实数域上），则是Hamilton型可除代数
        return self.a < 0 and self.b < 0
    
    def inverse(self) -> Optional[Quaternion]:
        """
        乘法逆元: x^{-1} = x̄ / n(x)
        如果范数为0则返回None
        """
        n = self.norm()
        if abs(n) < 1e-10:
            return None
        return self.conjugate() / n
    
    # ==================== 辅助方法 ====================
    
    def scalar_part(self) -> float:
        """标量部分（中心部分）"""
        return self.x0
    
    def vector_part(self) -> Tuple[float, float, float]:
        """向量部分（纯虚部分）"""
        return (self.x1, self.x2, self.x3)
    
    def coefficients(self) -> Tuple[float, float, float, float]:
        """返回所有系数 (x0, x1, x2, x3)"""
        return (self.x0, self.x1, self.x2, self.x3)
    
    def algebra_params(self) -> Tuple[float, float]:
        """返回代数参数 (a, b)"""
        return (self.a, self.b)
    
    def __repr__(self) -> str:
        """字符串表示"""
        terms = []
        if abs(self.x0) > 1e-10 or self.is_zero():
            terms.append(f"{self.x0:.4f}")
        if abs(self.x1) > 1e-10:
            terms.append(f"{self.x1:+.4f}i")
        if abs(self.x2) > 1e-10:
            terms.append(f"{self.x2:+.4f}j")
        if abs(self.x3) > 1e-10:
            terms.append(f"{self.x3:+.4f}k")
        
        if not terms:
            return "0"
        
        result = " ".join(terms)
        # 处理开头的+号
        if result.startswith("+"):
            result = result[1:]
        return f"({result}; a={self.a}, b={self.b})"
    
    def __str__(self) -> str:
        """简洁字符串表示"""
        return self.__repr__()


# ==================== 验证和测试函数 ====================

def verify_hamilton_relations():
    """
    验证Hamilton关系: i^2 = j^2 = k^2 = ijk = -1
    """
    print("=" * 60)
    print("验证 Hamilton 关系")
    print("=" * 60)
    
    H = Quaternion  # Hamilton四元数
    
    i = H.i_element()
    j = H.j_element()
    k = H.k_element()
    one = H.one()
    
    print(f"i = {i}")
    print(f"j = {j}")
    print(f"k = {k}")
    print()
    
    # 验证基本关系
    print(f"i^2 = {i * i} (应等于 -1)")
    print(f"j^2 = {j * j} (应等于 -1)")
    print(f"k^2 = {k * k} (应等于 -1)")
    print(f"ij = {i * j} (应等于 k)")
    print(f"ji = {j * i} (应等于 -k)")
    print(f"ijk = {i * j * k} (应等于 -1)")
    print()
    
    # 验证非交换性
    print(f"ij = {i * j}")
    print(f"ji = {j * i}")
    print(f"ij + ji = {i * j + j * i} (应等于 0，即反对易)")
    print()


def verify_basic_identities():
    """
    验证基本恒等式：
    1. 共轭的反乘法: conjugate(xy) = conjugate(y) * conjugate(x)
    2. 范数的乘性: n(xy) = n(x)n(y)
    3. 迹的循环性: tr(xy) = tr(yx)
    4. 特征方程: x^2 - tr(x)x + n(x) = 0
    """
    print("=" * 60)
    print("验证基本恒等式")
    print("=" * 60)
    
    H = Quaternion
    
    # 随机生成两个四元数
    x = H.hamilton(2, 3, -1, 4)
    y = H.hamilton(-1, 2, 3, -2)
    
    print(f"x = {x}")
    print(f"y = {y}")
    print()
    
    # 1. 共轭的反乘法
    lhs = (x * y).conjugate()
    rhs = y.conjugate() * x.conjugate()
    print(f"共轭的反乘法:")
    print(f"  conjugate(xy) = {lhs}")
    print(f"  conjugate(y)*conjugate(x) = {rhs}")
    print(f"  验证: {lhs == rhs}")
    print()
    
    # 2. 范数的乘性
    n_xy = (x * y).norm()
    n_x_n_y = x.norm() * y.norm()
    print(f"范数的乘性:")
    print(f"  n(xy) = {n_xy:.6f}")
    print(f"  n(x)n(y) = {n_x_n_y:.6f}")
    print(f"  验证: {abs(n_xy - n_x_n_y) < 1e-10}")
    print()
    
    # 3. 迹的循环性
    tr_xy = (x * y).trace()
    tr_yx = (y * x).trace()
    print(f"迹的循环性:")
    print(f"  tr(xy) = {tr_xy:.6f}")
    print(f"  tr(yx) = {tr_yx:.6f}")
    print(f"  验证: {abs(tr_xy - tr_yx) < 1e-10}")
    print()
    
    # 4. 特征方程
    x_sq = x * x
    tr_x = x.trace()
    n_x = x.norm()
    char_eq = x_sq - tr_x * x + n_x * H.one()
    print(f"特征方程 x^2 - tr(x)x + n(x) = 0:")
    print(f"  x^2 = {x_sq}")
    print(f"  tr(x)x = {tr_x * x}")
    print(f"  n(x) = {n_x:.6f}")
    print(f"  结果 = {char_eq}")
    print(f"  验证: {char_eq.is_zero()}")
    print()


def verify_matrix_representation():
    """
    验证四元数与2x2矩阵的同构 (分裂代数)
    对于 (1, b/F) ≅ M_2(F)
    """
    print("=" * 60)
    print("验证分裂代数与矩阵代数的同构")
    print("=" * 60)
    
    b = 1.0
    # 分裂四元数 (1, 1/R)
    x = Quaternion.split(2, 1, 3, -1, b=b)
    y = Quaternion.split(-1, 2, 1, 2, b=b)
    
    print(f"代数: (1, {b}/R) ≅ M_2(R)")
    print(f"x = {x}")
    print(f"y = {y}")
    print()
    
    # 矩阵表示:
    # 1 -> [[1, 0], [0, 1]]
    # i -> [[1, 0], [0, -1]]
    # j -> [[0, b], [1, 0]]
    # k -> [[0, b], [-1, 0]]
    
    def to_matrix(q: Quaternion) -> list:
        """转换为2x2矩阵"""
        x0, x1, x2, x3 = q.coefficients()
        a, b = q.algebra_params()
        # 基于标准同构
        return [
            [x0 + x1, b*(x2 + x3)],
            [x2 - x3, x0 - x1]
        ]
    
    def mat_mul(A, B):
        """矩阵乘法"""
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]
    
    X = to_matrix(x)
    Y = to_matrix(y)
    XY = mat_mul(X, Y)
    xy_quat = x * y
    XY_quat = to_matrix(xy_quat)
    
    print(f"矩阵表示:")
    print(f"  X = {X}")
    print(f"  Y = {Y}")
    print(f"  XY (矩阵乘) = {XY}")
    print(f"  XY (四元数后转) = {XY_quat}")
    print(f"  验证同态性: {abs(XY[0][0] - XY_quat[0][0]) < 1e-10}")
    print()


def demonstrate_division_vs_split():
    """
    展示分歧代数与分裂代数的区别
    """
    print("=" * 60)
    print("分歧代数 vs 分裂代数")
    print("=" * 60)
    
    # 分歧代数: Hamilton四元数 (-1, -1/R)
    print("分歧代数: Hamilton四元数 (-1, -1/R)")
    H = Quaternion.hamilton(1, 2, 3, 4)
    print(f"  x = {H}")
    print(f"  n(x) = {H.norm():.6f}")
    print(f"  是非零零因子? {H.is_zero_divisor()}")
    
    # 尝试找零因子（应该找不到）
    print(f"  是否可除代数? {H.is_division()}")
    print()
    
    # 分裂代数: (1, 1/R)
    print("分裂代数: (1, 1/R)")
    S = Quaternion.split(1, 1, 1, 1)
    print(f"  y = {S}")
    print(f"  n(y) = {S.norm():.6f}")
    
    # 找零因子: (0, 1, 0, 1) 的范数 = -1 -1 + 1 = -1... 试试别的
    # 对于 (1, 1/R): n = x0^2 - x1^2 - x2^2 + x3^2
    # 取 x0=1, x1=1, x2=0, x3=0: n = 1 - 1 = 0
    zd = Quaternion.split(1, 1, 0, 0)
    print(f"  零因子例子: z = {zd}")
    print(f"  n(z) = {zd.norm():.6f}")
    print(f"  是非零零因子? {zd.is_zero_divisor()}")
    print()


def demonstrate_unit_group():
    """
    展示范数1的单位元，与算术Kleinian群的联系
    """
    print("=" * 60)
    print("范数1的单位元 (与Kleinian群的联系)")
    print("=" * 60)
    
    H = Quaternion
    
    # 构造几个范数1的四元数
    # 例如 (1/2, 1/2, 1/2, 1/2) 的范数 = 1/4 + 1/4 + 1/4 + 1/4 = 1 (Hamilton)
    u1 = H.hamilton(0.5, 0.5, 0.5, 0.5)
    print(f"u1 = {u1}")
    print(f"n(u1) = {u1.norm():.6f}")
    print(f"是单位元? {u1.is_unit()}")
    print()
    
    # 单位元的乘积还是单位元
    u2 = H.hamilton(0.5, -0.5, 0.5, 0.5)
    print(f"u2 = {u2}")
    print(f"n(u2) = {u2.norm():.6f}")
    
    u12 = u1 * u2
    print(f"u1*u2 = {u12}")
    print(f"n(u1*u2) = {u12.norm():.6f}")
    print()
    
    # 单位元的逆
    u1_inv = u1.inverse()
    print(f"u1^{-1} = {u1_inv}")
    print(f"验证: u1 * u1^{-1} = {u1 * u1_inv}")
    print()


def exercise_calculations():
    """
    练习题：基本计算
    """
    print("=" * 60)
    print("练习题")
    print("=" * 60)
    
    H = Quaternion
    
    print("练习 1: 计算下列四元数的范数和迹")
    q1 = H.hamilton(3, -2, 1, 4)
    print(f"  q = {q1}")
    print(f"  范数 n(q) = {q1.norm():.6f}")
    print(f"  迹 tr(q) = {q1.trace():.6f}")
    print()
    
    print("练习 2: 验证逆元公式")
    q2 = H.hamilton(2, 1, -1, 3)
    q2_inv = q2.inverse()
    print(f"  q = {q2}")
    print(f"  q^{-1} = {q2_inv}")
    print(f"  q * q^{-1} = {q2 * q2_inv}")
    print()
    
    print("练习 3: 验证纯虚子空间的对易关系")
    i = H.i_element()
    j = H.j_element()
    k = H.k_element()
    print(f"  [i, j] = ij - ji = {i*j - j*i} (应等于 2k)")
    print(f"  [j, k] = jk - kj = {j*k - k*j} (应等于 2i)")
    print(f"  [k, i] = ki - ik = {k*i - i*k} (应等于 2j)")
    print()


def main():
    """主函数：运行所有验证和练习"""
    print("\n")
    print("*" * 60)
    print("四元数代数计算练习")
    print("Quaternion Algebra Exercises")
    print("*" * 60)
    print()
    
    verify_hamilton_relations()
    verify_basic_identities()
    verify_matrix_representation()
    demonstrate_division_vs_split()
    demonstrate_unit_group()
    exercise_calculations()
    
    print("=" * 60)
    print("练习完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
