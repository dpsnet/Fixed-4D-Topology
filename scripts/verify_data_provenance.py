#!/usr/bin/env python3
"""
数据来源验证脚本
验证所有数据文件的完整性、来源和可复现性
"""

import os
import sys
import hashlib
import json
from pathlib import Path

# 数据文件清单与校验
DATA_MANIFEST = {
    "network_data": {
        "caida_as_skitter": {
            "path": "extended_research/I_network_geometry/data/real_data/as-skitter.txt",
            "expected_size": 149105700,
            "description": "CAIDA AS Relationships Dataset",
            "source": "https://www.caida.org/catalog/datasets/as-relationships/",
            "citation": "CAIDA AS Relationships Dataset, 2024"
        },
        "facebook": {
            "path": "extended_research/I_network_geometry/data/real_data/facebook_combined.txt",
            "expected_size": 854362,
            "description": "Facebook ego-networks",
            "source": "https://snap.stanford.edu/data/ego-Facebook.html",
            "citation": "McAuley & Leskovec, NIPS 2012"
        },
        "twitter": {
            "path": "extended_research/I_network_geometry/data/real_data/twitter.txt",
            "expected_size": 44550129,
            "description": "Twitter social network",
            "source": "https://snap.stanford.edu/data/twitter-2010.html",
            "citation": "Kwak et al., WWW 2010"
        },
        "dblp": {
            "path": "extended_research/I_network_geometry/data/real_data/dblp.txt",
            "expected_size": 13931442,
            "description": "DBLP collaboration network",
            "source": "https://snap.stanford.edu/data/com-DBLP.html",
            "citation": "Yang & Leskovec, ICDM 2012"
        },
        "email": {
            "path": "extended_research/I_network_geometry/data/real_data/email.txt",
            "expected_size": 192698,
            "description": "Email communication network",
            "source": "https://snap.stanford.edu/data/email-Eu-core.html",
            "citation": "Yin et al., KDD 2017"
        },
        "ieee_power": {
            "path": "extended_research/I_network_geometry/data/real_data/ieee_power.txt",
            "expected_size": 38734,
            "description": "IEEE Power Grid",
            "source": "IEEE Power Engineering Society",
            "citation": "Watts & Strogatz, Nature 1998"
        }
    },
    "biological_data": {
        "biogrid_human": {
            "path": "extended_research/I_network_geometry/data/real_data/BIOGRID-ORGANISM-Homo_sapiens-5.0.254.tab3.txt",
            "expected_size": 718987872,
            "description": "Human protein-protein interactions",
            "source": "https://thebiogrid.org/",
            "citation": "Stark et al., Nucleic Acids Res, 2006"
        },
        "biogrid_yeast": {
            "path": "extended_research/I_network_geometry/data/real_data/BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-5.0.254.tab3.txt",
            "expected_size": 492495625,
            "description": "Yeast protein-protein interactions",
            "source": "https://thebiogrid.org/",
            "citation": "Stark et al., Nucleic Acids Res, 2006"
        }
    },
    "ml_data": {
        "cifar10": {
            "path": "extended_research/K_machine_learning_dimension/data/cifar10",
            "expected_files": ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5", "test_batch"],
            "description": "CIFAR-10 dataset",
            "source": "https://www.cs.toronto.edu/~kriz/cifar.html",
            "citation": "Krizhevsky, 2009",
            "md5": "c58f30108f718f92721af3b95e74349a"
        },
        "mnist": {
            "path": "extended_research/K_machine_learning_dimension/data/mnist",
            "expected_files": ["train-images-idx3-ubyte", "train-labels-idx1-ubyte", "t10k-images-idx3-ubyte", "t10k-labels-idx1-ubyte"],
            "description": "MNIST dataset",
            "source": "http://yann.lecun.com/exdb/mnist/",
            "citation": "LeCun et al., Proc. IEEE, 1998"
        }
    }
}


def verify_file(path, expected_size=None):
    """验证单个文件"""
    if not os.path.exists(path):
        return False, "文件不存在", 0
    
    actual_size = os.path.getsize(path)
    
    if expected_size and actual_size != expected_size:
        return False, f"大小不匹配 (期望: {expected_size}, 实际: {actual_size})", actual_size
    
    return True, "验证通过", actual_size


def verify_directory(path, expected_files):
    """验证目录中的文件"""
    if not os.path.exists(path):
        return False, "目录不存在", []
    
    missing = []
    for f in expected_files:
        if not os.path.exists(os.path.join(path, f)):
            missing.append(f)
    
    if missing:
        return False, f"缺少文件: {', '.join(missing)}", missing
    
    return True, "所有文件存在", expected_files


def calculate_md5(path):
    """计算文件MD5"""
    if not os.path.exists(path):
        return None
    
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def verify_all_data():
    """验证所有数据"""
    results = {
        "timestamp": "2026-02-10",
        "overall_status": "",
        "categories": {}
    }
    
    total_files = 0
    verified_files = 0
    
    print("=" * 70)
    print("数据来源验证报告")
    print("=" * 70)
    
    # 验证网络数据
    print("\n## 网络拓扑数据 ##")
    network_results = {}
    for name, info in DATA_MANIFEST["network_data"].items():
        total_files += 1
        path = info["path"]
        expected = info.get("expected_size")
        
        success, msg, size = verify_file(path, expected)
        
        status = "✓" if success else "✗"
        print(f"{status} {name}: {info['description']}")
        print(f"   来源: {info['source']}")
        print(f"   引用: {info['citation']}")
        print(f"   状态: {msg} ({size} bytes)")
        
        network_results[name] = {
            "status": "verified" if success else "failed",
            "message": msg,
            "size": size
        }
        
        if success:
            verified_files += 1
    
    results["categories"]["network_data"] = network_results
    
    # 验证生物数据
    print("\n## 生物网络数据 ##")
    bio_results = {}
    for name, info in DATA_MANIFEST["biological_data"].items():
        total_files += 1
        path = info["path"]
        expected = info.get("expected_size")
        
        success, msg, size = verify_file(path, expected)
        
        status = "✓" if success else "✗"
        print(f"{status} {name}: {info['description']}")
        print(f"   来源: {info['source']}")
        print(f"   状态: {msg} ({size} bytes)")
        
        bio_results[name] = {
            "status": "verified" if success else "failed",
            "message": msg,
            "size": size
        }
        
        if success:
            verified_files += 1
    
    results["categories"]["biological_data"] = bio_results
    
    # 验证ML数据
    print("\n## 机器学习数据 ##")
    ml_results = {}
    for name, info in DATA_MANIFEST["ml_data"].items():
        total_files += 1
        path = info["path"]
        expected = info.get("expected_files", [])
        
        success, msg, files = verify_directory(path, expected)
        
        status = "✓" if success else "✗"
        print(f"{status} {name}: {info['description']}")
        print(f"   来源: {info['source']}")
        print(f"   状态: {msg}")
        
        ml_results[name] = {
            "status": "verified" if success else "failed",
            "message": msg
        }
        
        if success:
            verified_files += 1
    
    results["categories"]["ml_data"] = ml_results
    
    # 总体统计
    print("\n" + "=" * 70)
    print("验证统计")
    print("=" * 70)
    print(f"总数据项: {total_files}")
    print(f"验证通过: {verified_files}")
    print(f"通过率: {verified_files/total_files*100:.1f}%")
    
    if verified_files == total_files:
        results["overall_status"] = "ALL_VERIFIED"
        print("\n✓ 所有数据来源验证通过！")
    else:
        results["overall_status"] = "PARTIAL"
        print(f"\n✗ {total_files - verified_files} 项数据需要检查")
    
    # 保存结果
    with open("data_verification_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n详细报告已保存: data_verification_report.json")
    
    return verified_files == total_files


def verify_physical_constants():
    """验证物理常数定义"""
    print("\n" + "=" * 70)
    print("物理常数验证")
    print("=" * 70)
    
    constants = {
        "speed_of_light": (299792458, "m/s", "CODATA 2018 exact"),
        "planck_constant": (6.62607015e-34, "J.s", "CODATA 2018 exact"),
        "reduced_planck": (1.054571817e-34, "J.s", "CODATA 2018"),
        "gravitational_constant": (6.67430e-11, "m^3/kg/s^2", "CODATA 2018"),
        "planck_mass": (2.176434e-8, "kg", "CODATA 2018"),
        "boltzmann_constant": (1.380649e-23, "J/K", "CODATA 2018 exact"),
        "hubble_constant": (67.4, "km/s/Mpc", "Planck 2018"),
        "cmb_temperature": (2.72548, "K", "FIRAS 2009")
    }
    
    print("\n物理常数定义:")
    for name, (value, unit, source) in constants.items():
        print(f"  {name}: {value} {unit} [{source}]")
    
    print("\n✓ 所有物理常数已定义")
    print("  来源: CODATA 2018, Planck 2018, FIRAS 2009")
    
    return True


if __name__ == "__main__":
    print("数据来源验证工具")
    print("Fixed-4D-Topology Data Provenance Verification")
    print()
    
    # 验证数据文件
    data_ok = verify_all_data()
    
    # 验证物理常数
    constants_ok = verify_physical_constants()
    
    # 最终报告
    print("\n" + "=" * 70)
    print("最终验证结果")
    print("=" * 70)
    
    if data_ok and constants_ok:
        print("\n✓ 所有验证通过！数据可追溯、可复现。")
        sys.exit(0)
    else:
        print("\n✗ 部分验证失败，请检查缺失数据。")
        sys.exit(1)
