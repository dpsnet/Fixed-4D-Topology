#!/usr/bin/env python3
"""
文献数据提取模板
用于从论文图表中数字化能级数据
"""

import numpy as np
import json
from datetime import datetime


def create_data_template():
    """
    创建标准化的数据记录模板
    """
    template = {
        "metadata": {
            "paper_title": "",
            "authors": "",
            "journal": "",
            "year": 0,
            "doi": "",
            "extraction_date": datetime.now().isoformat(),
            "extracted_by": "",
            "notes": ""
        },
        "experimental_conditions": {
            "material": "Cu2O",  # 或 GaAs等
            "temperature_K": 0.0,
            "sample_thickness_nm": 0.0,
            "measurement_technique": "",  # 如：absorption, photoluminescence
            "spectral_resolution_ueV": 0.0,
            "excitation_source": "",
            "additional_info": ""
        },
        "energy_levels": [
            # 格式: {"n": 主量子数, "E_meV": 能量, "error_meV": 误差, "assignment": "能级标识"}
        ],
        "analysis": {
            "rydberg_energy_meV": None,  # 拟合提取
            "quantum_defect": None,
            "c1_extracted": None,
            "c1_error": None,
            "fit_quality_chi2": None,
            "notes": ""
        }
    }
    return template


def add_energy_level(data, n, E_meV, error_meV=0.0, assignment=""):
    """
    添加一个能级数据点
    """
    level = {
        "n": int(n),
        "E_meV": float(E_meV),
        "error_meV": float(error_meV),
        "assignment": assignment
    }
    data["energy_levels"].append(level)
    return data


def save_data(data, filename):
    """
    保存数据到JSON文件
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ 数据已保存: {filename}")


def load_data(filename):
    """
    从JSON文件加载数据
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def convert_to_numpy(data):
    """
    将数据转换为NumPy数组，便于分析
    """
    levels = data["energy_levels"]
    n = np.array([l["n"] for l in levels])
    E = np.array([l["E_meV"] for l in levels])
    err = np.array([l["error_meV"] for l in levels])
    return n, E, err


def example_usage():
    """
    使用示例：模拟Cu2O Nature 2014论文的数据结构
    """
    
    # 创建模板
    data = create_data_template()
    
    # 填充元数据
    data["metadata"]["paper_title"] = "Giant Rydberg excitons in the copper oxide Cu2O"
    data["metadata"]["authors"] = "T. Kazimierczuk et al."
    data["metadata"]["journal"] = "Nature"
    data["metadata"]["year"] = 2014
    data["metadata"]["doi"] = "10.1038/nature12654"
    data["metadata"]["notes"] = "从图1b提取的能级数据（示例）"
    
    # 实验条件
    data["experimental_conditions"]["temperature_K"] = 0.015  # 15 mK
    data["experimental_conditions"]["sample_thickness_nm"] = 1000  # 1 mm bulk
    data["experimental_conditions"]["measurement_technique"] = "absorption_spectroscopy"
    data["experimental_conditions"]["spectral_resolution_ueV"] = 0.5
    
    # 添加示例能级数据（这些是占位符，需要从实际论文中提取）
    # 注意：以下数据是模拟的，不是真实数据！
    example_levels = [
        (2, -70.0, 0.1, "2P"),
        (3, -35.0, 0.1, "3P"),
        (4, -21.0, 0.1, "4P"),
        (5, -14.0, 0.1, "5P"),
        (10, -4.0, 0.05, "10P"),
        (15, -2.0, 0.05, "15P"),
        (20, -1.2, 0.05, "20P"),
        (25, -0.8, 0.05, "25P"),
    ]
    
    for n, E, err, assign in example_levels:
        add_energy_level(data, n, E, err, assign)
    
    # 保存
    filename = "cu2o_nature2014_example.json"
    save_data(data, filename)
    
    # 转换为NumPy数组
    n_arr, E_arr, err_arr = convert_to_numpy(data)
    
    print("\n提取的数据:")
    print(f"  能级数量: {len(n_arr)}")
    print(f"  n范围: {n_arr.min()} 到 {n_arr.max()}")
    print(f"  E范围: {E_arr.min():.2f} 到 {E_arr.max():.2f} meV")
    
    return data


def extract_from_paper_guidelines():
    """
    数据提取操作指南
    """
    guidelines = """
    === 数据提取操作指南 ===
    
    1. 获取论文
       - 下载PDF全文
       - 特别关注包含光谱图的页面
    
    2. 图表数字化工具
       - WebPlotDigitizer (推荐): https://apps.automeris.io/wpd/
       - Engauge Digitizer
       - 或手动读取坐标
    
    3. 提取步骤
       a) 上传图表截图到WebPlotDigitizer
       b) 校准坐标轴（设置x=量子数, y=能量）
       c) 点击每个能级峰值记录坐标
       d) 导出CSV数据
    
    4. 数据记录
       - 使用本模板的create_data_template()
       - 完整填写metadata和experimental_conditions
       - 将提取的数据填入energy_levels
    
    5. 误差估计
       - 谱线宽度 → 能量不确定度
       - 峰值读取精度
       - 系统误差（如温度漂移）
    
    6. 验证
       - 检查Rydberg公式拟合
       - 确认量子亏损合理性
       - 与其他论文数据比较
    
    === 注意事项 ===
    
    - 只提取P态（或其他单一角动量系列）
    - 记录能量是绝对值还是相对值
    - 注意单位转换（eV ↔ meV ↔ cm⁻¹）
    - 保存原始截图和数字化数据
    """
    print(guidelines)


if __name__ == "__main__":
    print("="*70)
    print("文献数据提取模板")
    print("="*70)
    
    print("\n[1] 显示操作指南...")
    extract_from_paper_guidelines()
    
    print("\n[2] 创建示例数据结构...")
    example_data = example_usage()
    
    print("\n[3] 模板准备就绪")
    print("   - 使用 create_data_template() 创建新记录")
    print("   - 使用 add_energy_level() 添加数据点")
    print("   - 使用 save_data() 保存为JSON")
    print("   - 使用 load_data() 加载已有数据")
    print("   - 使用 convert_to_numpy() 转换为数组分析")
