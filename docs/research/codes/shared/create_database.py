#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建高精度结果数据库
Create High-Precision Results Database

创建SQLite数据库，包含：
- kleinian_high_precision: Kleinian群高精度结果
- padic_high_precision: p-adic多项式高精度结果
- validation_results: 验证结果
- uncertainty_estimates: 不确定性估计

作者：AI Research Assistant
日期：2026-02-11
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def create_database(db_path: str = "/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/data/key_examples_high_precision.sqlite"):
    """创建高精度结果数据库"""
    
    print("=" * 80)
    print("创建高精度结果数据库")
    print("=" * 80)
    
    # 确保目录存在
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n数据库路径: {db_path}")
    
    # ============================================================
    # 1. Kleinian群高精度结果表
    # ============================================================
    print("\n创建表: kleinian_high_precision")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kleinian_high_precision (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_type TEXT NOT NULL,
            hausdorff_dim REAL,
            hausdorff_dim_high_precision TEXT,  -- Decimal存储为字符串
            hausdorff_dim_error REAL,
            hausdorff_dim_error_hp TEXT,
            heat_kernel_trace_t_0001 TEXT,
            heat_kernel_trace_t_001 TEXT,
            heat_kernel_trace_t_01 TEXT,
            heat_kernel_trace_t_1 TEXT,
            l_function_derivative_s_0500 TEXT,
            l_function_derivative_s_1000 TEXT,
            l_function_derivative_s_1500 TEXT,
            convergence_radius REAL,
            convergence_radius_hp TEXT,
            convergence_factor REAL,
            convergence_factor_hp TEXT,
            computation_time REAL,
            method_used TEXT,
            validation_status TEXT,
            pressure_method_dim TEXT,
            pressure_method_error TEXT,
            dimension_method_dim TEXT,
            dimension_method_error TEXT,
            mcqueen_method_dim TEXT,
            mcqueen_method_error TEXT,
            weighted_average_dim TEXT,
            max_difference TEXT,
            consistency_check TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    print("  ✓ 表创建完成")
    
    # 创建索引
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_kleinian_name ON kleinian_high_precision(name)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_kleinian_type ON kleinian_high_precision(group_type)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_kleinian_dim ON kleinian_high_precision(hausdorff_dim)
    ''')
    print("  ✓ 索引创建完成")
    
    # ============================================================
    # 2. p-adic多项式高精度结果表
    # ============================================================
    print("\n创建表: padic_high_precision")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS padic_high_precision (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            prime INTEGER NOT NULL,
            degree INTEGER NOT NULL,
            coefficients TEXT,  -- JSON格式存储系数
            hausdorff_dim REAL,
            hausdorff_dim_high_precision TEXT,
            hausdorff_dim_error REAL,
            hausdorff_dim_error_hp TEXT,
            pressure_s_0500 TEXT,
            pressure_s_1000 TEXT,
            pressure_s_1500 TEXT,
            pressure_s_2000 TEXT,
            bowen_delta REAL,
            bowen_delta_hp TEXT,
            bowen_delta_error REAL,
            gibbs_measure_entropy REAL,
            gibbs_measure_entropy_hp TEXT,
            gibbs_measure_error REAL,
            topological_entropy REAL,
            topological_entropy_hp TEXT,
            lyapunov_exponent REAL,
            lyapunov_exponent_hp TEXT,
            lyapunov_error REAL,
            julia_dim REAL,
            julia_dim_hp TEXT,
            julia_connected INTEGER,  -- Boolean
            truncation_error TEXT,
            rounding_error TEXT,
            iteration_error TEXT,
            total_error TEXT,
            known_dim REAL,
            computation_time REAL,
            method_used TEXT,
            validation_status TEXT,
            bowen_method_dim TEXT,
            bowen_method_error TEXT,
            counting_method_dim TEXT,
            counting_method_error TEXT,
            spectral_method_dim TEXT,
            spectral_method_error TEXT,
            analytic_check TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    print("  ✓ 表创建完成")
    
    # 创建索引
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_padic_name ON padic_high_precision(name)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_padic_prime ON padic_high_precision(prime)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_padic_degree ON padic_high_precision(degree)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_padic_dim ON padic_high_precision(hausdorff_dim)
    ''')
    print("  ✓ 索引创建完成")
    
    # ============================================================
    # 3. 验证结果表
    # ============================================================
    print("\n创建表: validation_results")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            example_name TEXT NOT NULL,
            example_type TEXT NOT NULL,  -- 'kleinian' or 'padic'
            unified_formula_check INTEGER,  -- Boolean
            unified_formula_error REAL,
            unified_formula_error_hp TEXT,
            unified_formula_expected_hp TEXT,
            unified_formula_computed_hp TEXT,
            bowen_formula_check INTEGER,  -- Boolean
            bowen_formula_error REAL,
            bowen_formula_error_hp TEXT,
            bowen_dim_hp TEXT,
            bowen_delta_hp TEXT,
            cross_validation_consistency INTEGER,  -- Boolean
            cross_validation_max_diff REAL,
            cross_validation_max_diff_hp TEXT,
            analytic_deviation REAL,
            analytic_deviation_hp TEXT,
            overall_status TEXT,  -- 'PASS', 'WARNING', 'FAIL'
            confidence_score REAL,
            created_at TEXT
        )
    ''')
    print("  ✓ 表创建完成")
    
    # 创建索引
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_validation_name ON validation_results(example_name)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_validation_type ON validation_results(example_type)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_validation_status ON validation_results(overall_status)
    ''')
    print("  ✓ 索引创建完成")
    
    # ============================================================
    # 4. 不确定性估计表
    # ============================================================
    print("\n创建表: uncertainty_estimates")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uncertainty_estimates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            example_name TEXT NOT NULL,
            example_type TEXT NOT NULL,
            
            -- 误差分量
            truncation_error REAL,
            truncation_error_hp TEXT,
            rounding_error REAL,
            rounding_error_hp TEXT,
            iteration_error REAL,
            iteration_error_hp TEXT,
            approximation_error REAL,
            approximation_error_hp TEXT,
            
            -- 统计量
            mean_estimate REAL,
            mean_estimate_hp TEXT,
            std_estimate REAL,
            std_estimate_hp TEXT,
            confidence_interval_lower REAL,
            confidence_interval_lower_hp TEXT,
            confidence_interval_upper REAL,
            confidence_interval_upper_hp TEXT,
            confidence_level REAL,  -- e.g., 0.95 for 95%
            
            -- 敏感性分析
            parameter_sensitivity TEXT,  -- JSON
            method_comparison TEXT,  -- JSON
            
            -- 元数据
            computation_method TEXT,
            sample_size INTEGER,
            created_at TEXT
        )
    ''')
    print("  ✓ 表创建完成")
    
    # 创建索引
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_uncertainty_name ON uncertainty_estimates(example_name)
    ''')
    print("  ✓ 索引创建完成")
    
    # ============================================================
    # 5. 元数据表
    # ============================================================
    print("\n创建表: metadata")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            description TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    print("  ✓ 表创建完成")
    
    # 插入元数据
    timestamp = datetime.now().isoformat()
    metadata = [
        ('database_version', '1.0', '数据库版本'),
        ('created_at', timestamp, '数据库创建时间'),
        ('precision_bits', '80', 'Decimal计算精度（位）'),
        ('python_version', '3.x', 'Python版本'),
        ('sqlite_version', sqlite3.sqlite_version, 'SQLite版本'),
        ('description', '关键例子高精度计算结果数据库', '数据库描述'),
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO metadata (key, value, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', [(k, v, d, timestamp, timestamp) for k, v, d in metadata])
    print("  ✓ 元数据插入完成")
    
    # ============================================================
    # 6. 视图
    # ============================================================
    print("\n创建视图...")
    
    # 综合结果视图
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS v_all_results AS
        SELECT 
            k.name as example_name,
            'kleinian' as example_type,
            k.group_type as subtype,
            k.hausdorff_dim as dimension,
            k.hausdorff_dim_high_precision as dimension_hp,
            k.validation_status,
            v.overall_status,
            v.confidence_score
        FROM kleinian_high_precision k
        LEFT JOIN validation_results v ON k.name = v.example_name
        UNION ALL
        SELECT 
            p.name as example_name,
            'padic' as example_type,
            'p=' || p.prime as subtype,
            p.hausdorff_dim as dimension,
            p.hausdorff_dim_high_precision as dimension_hp,
            p.validation_status,
            v.overall_status,
            v.confidence_score
        FROM padic_high_precision p
        LEFT JOIN validation_results v ON p.name = v.example_name
    ''')
    print("  ✓ 视图 v_all_results 创建完成")
    
    # 验证摘要视图
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS v_validation_summary AS
        SELECT 
            example_type,
            overall_status,
            COUNT(*) as count,
            AVG(confidence_score) as avg_confidence,
            MIN(confidence_score) as min_confidence,
            MAX(confidence_score) as max_confidence
        FROM validation_results
        GROUP BY example_type, overall_status
    ''')
    print("  ✓ 视图 v_validation_summary 创建完成")
    
    # 提交更改
    conn.commit()
    
    # 验证表结构
    print("\n数据库表结构验证:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} 条记录")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    views = cursor.fetchall()
    for view in views:
        print(f"  - {view[0]} (视图)")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("数据库创建完成")
    print("=" * 80)
    print(f"数据库路径: {db_path}")
    
    return db_path

if __name__ == "__main__":
    db_path = create_database()
