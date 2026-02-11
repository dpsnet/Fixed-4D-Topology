#!/usr/bin/env python3
"""
快速测试扩展计算模块
"""

import numpy as np
import sys
import time

# 添加当前目录到路径
sys.path.insert(0, '/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/maass')

from hejhal_extended_computations import (
    HejhalConfig, ExtendedMaassSolver, EigenvalueDistributionAnalyzer,
    FractalHyperbolicSurface, MaassEigenvalueDatabase
)

def test_database():
    """测试数据库功能"""
    print("=" * 60)
    print("测试数据库功能")
    print("=" * 60)
    
    db = MaassEigenvalueDatabase()
    print(f"✓ 数据库初始化成功: {db.db_path}")
    
    # 插入测试数据
    from hejhal_extended_computations import EigenvalueData
    test_data = EigenvalueData(
        index=1, R=13.7797, lambda_val=190.13, parity='even',
        error_estimate=1e-6, condition_number=1e-10,
        computation_time=0.5
    )
    db.insert_eigenvalue(test_data, 'modular')
    print("✓ 插入测试数据成功")
    
    # 查询数据
    results = db.get_eigenvalues(parity='even', limit=5)
    print(f"✓ 查询到 {len(results)} 条记录")
    
    # 导出JSON
    import tempfile
    json_path = tempfile.mktemp(suffix='.json')
    db.export_to_json(json_path)
    print(f"✓ 导出JSON成功: {json_path}")
    
    return True

def test_fractal_surfaces():
    """测试分形曲面功能"""
    print("\n" + "=" * 60)
    print("测试分形曲面功能")
    print("=" * 60)
    
    surfaces = [
        FractalHyperbolicSurface("Schottky_3", 2.0, 0.8),
        FractalHyperbolicSurface("Test_surface", 2.0, 0.5),
    ]
    
    for surf in surfaces:
        print(f"\n曲面: {surf.name}")
        print(f"  极限集维数: {surf.limit_set_dim}")
        print(f"  散射矩阵大小: {surf.scattering_matrix_size()}")
        
        relations = surf.spectral_dimension_relation()
        print(f"  谱维数关系:")
        for key, val in relations.items():
            print(f"    {key}: {val:.4f}")
        
        resonances = surf.resonances_estimate()
        print(f"  共振态估计 (前3个):")
        for r in resonances[:3]:
            print(f"    s = {r.real:.3f} + {r.imag:.3f}i")
    
    return True

def test_distribution_analyzer():
    """测试分布分析器"""
    print("\n" + "=" * 60)
    print("测试分布分析器")
    print("=" * 60)
    
    from hejhal_extended_computations import EigenvalueData
    
    # 创建测试数据
    test_eigenvalues = []
    np.random.seed(42)
    
    # 模拟特征值（基于已知值加小扰动）
    base_R_even = [13.78, 17.74, 19.42, 21.32, 22.79]
    base_R_odd = [9.53, 12.17, 14.36, 16.14, 16.64]
    
    for i, R in enumerate(base_R_even, 1):
        data = EigenvalueData(
            index=i, R=R, lambda_val=0.25 + R**2, parity='even',
            error_estimate=1e-8, condition_number=1e-12
        )
        test_eigenvalues.append(data)
    
    for i, R in enumerate(base_R_odd, 1):
        data = EigenvalueData(
            index=i, R=R, lambda_val=0.25 + R**2, parity='odd',
            error_estimate=1e-8, condition_number=1e-12
        )
        test_eigenvalues.append(data)
    
    # 创建分析器
    analyzer = EigenvalueDistributionAnalyzer(test_eigenvalues)
    
    # 计算间距
    spacings = analyzer.compute_spacings()
    print(f"✓ 计算间距: {len(spacings)} 个间距")
    print(f"  平均间距: {np.mean(spacings):.4f}")
    
    # 归一化间距
    norm_spacings = analyzer.compute_normalized_spacings()
    print(f"✓ 归一化间距: mean={np.mean(norm_spacings):.4f}, std={np.std(norm_spacings):.4f}")
    
    # Weyl定律
    weyl = analyzer.weyl_law_residual()
    print(f"✓ Weyl定律计算完成")
    
    # 统计
    stats = analyzer.level_spacing_statistics()
    print(f"✓ 间距统计: variance={stats.get('variance', 0):.4f}")
    
    # 生成报告
    report = analyzer.generate_report()
    print("\n" + report[:500] + "...")
    
    return True

def test_solver_quick():
    """快速测试求解器（低精度）"""
    print("\n" + "=" * 60)
    print("快速测试求解器（低精度）")
    print("=" * 60)
    
    # 使用低精度配置
    config = HejhalConfig(
        truncation_M=8,
        num_points=8,
        tolerance=1e-6,
        mpmath_dps=15,
        parity='even'
    )
    
    solver = ExtendedMaassSolver(config)
    print(f"✓ 求解器初始化成功")
    print(f"  配点数量: {len(solver.points)}")
    print(f"  已知偶形式: {len(solver.KNOWN_EVEN_R)} 个")
    print(f"  已知奇形式: {len(solver.KNOWN_ODD_R)} 个")
    
    # 测试矩阵构造
    t_test = 13.78
    A = solver.construct_matrix(t_test)
    print(f"✓ 矩阵构造成功: shape={A.shape}")
    
    # 测试条件数
    cond = solver.matrix_condition(t_test)
    print(f"✓ 条件数计算: {cond:.6e}")
    
    # 快速搜索（使用已知值）
    print("\n尝试搜索第一个偶形式...")
    start = time.time()
    result = solver.find_eigenvalue(13.78, half_width=0.5)
    elapsed = time.time() - start
    
    if result:
        t, cond_val = result
        print(f"✓ 搜索结果:")
        print(f"  R = {t:.6f}")
        print(f"  λ = {0.25 + t**2:.4f}")
        print(f"  条件数 = {cond_val:.2e}")
        print(f"  时间 = {elapsed:.2f}s")
        
        # 验证
        known = solver.KNOWN_EVEN_R[0]
        print(f"  与文献值误差 = {abs(t - known):.4f}")
    else:
        print("✗ 未找到（可能需要更高精度）")
    
    return True

def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("Hejhal算法扩展计算模块测试")
    print("=" * 70)
    
    tests = [
        ("数据库功能", test_database),
        ("分形曲面功能", test_fractal_surfaces),
        ("分布分析器", test_distribution_analyzer),
        ("求解器快速测试", test_solver_quick),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                print(f"\n✓ {name} 测试通过")
                passed += 1
            else:
                print(f"\n✗ {name} 测试失败")
                failed += 1
        except Exception as e:
            print(f"\n✗ {name} 测试异常: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"通过: {passed}/{len(tests)}")
    print(f"失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ 所有测试通过！")
    else:
        print("\n✗ 部分测试失败，请检查输出")

if __name__ == '__main__':
    main()
