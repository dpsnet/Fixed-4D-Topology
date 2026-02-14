#!/usr/bin/env python3
"""
搜索更多 (d=2, w=0) 系统的数据源

目标：找到更多具有Rydberg系列或系统结合能数据的2D系统

潜在数据源：
1. GaAs/AlGaAs QW - 更系统的结合能vs阱宽数据
2. InGaAs/GaAs QW - 应变量子阱
3. MoS2, WSe2等TMD单层 - 2D激子
4. 钙钛矿量子阱 - 有机-无机杂化
5. 其他半导体量子阱系统
"""

import subprocess
import json

# 搜索查询策略
search_queries = {
    "GaAs QW binding energy systematic": {
        "description": "GaAs量子阱结合能系统研究",
        "relevance": "高 - 直接相关",
        "expected_c1": 1.0
    },
    "quantum well exciton binding energy vs width": {
        "description": "量子阱激子结合能vs阱宽",
        "relevance": "高 - 维度流验证",
        "expected_c1": 1.0
    },
    "2D exciton Rydberg series quantum well": {
        "description": "2D激子Rydberg系列",
        "relevance": "高 - 如果有数据",
        "expected_c1": 1.0
    },
    "MoS2 exciton binding energy": {
        "description": "MoS2激子结合能",
        "relevance": "中 - 纯2D系统",
        "expected_c1": 1.0
    },
    "WSe2 Rydberg excitons": {
        "description": "WSe2 Rydberg激子",
        "relevance": "高 - 可能有高n数据",
        "expected_c1": 1.0
    },
    "perovskite quantum well exciton": {
        "description": "钙钛矿量子阱激子",
        "relevance": "中 - 新兴材料",
        "expected_c1": 1.0
    },
    "graphene Landau level spectroscopy multiple transitions": {
        "description": "石墨烯Landau能级多跃迁",
        "relevance": "高 - 用于(d=2,w=1)",
        "expected_c1": 0.5
    },
    "topological insulator surface state Landau levels": {
        "description": "拓扑绝缘体表面态Landau能级",
        "relevance": "中 - 替代狄拉克系统",
        "expected_c1": 0.5
    }
}

print("=" * 80)
print("扩展数据搜索策略 - 完善Strategy C验证")
print("=" * 80)
print()

print("潜在数据源评估：")
print("-" * 80)

for query, info in search_queries.items():
    print(f"\n查询: {query}")
    print(f"  描述: {info['description']}")
    print(f"  相关性: {info['relevance']}")
    print(f"  预期c₁: {info['expected_c1']}")

print("\n" + "=" * 80)
print("优先级建议：")
print("=" * 80)

priorities = """
第一优先级 (高影响，可行性高)：
1. WSe2/MoS2 Rydberg激子
   - 2D材料中的Rydberg系列已有报道
   - 可能直接获得n=1,2,3...数据
   - 纯2D极限，理论更清晰

2. GaAs/AlGaAs QW系统研究
   - 经典系统，数据丰富
   - 需要找到结合能vs阱宽的系统数据

第二优先级 (概念验证)：
3. 石墨烯多Landau能级数据
   - 寻找IR/THz光谱的完整数据
   - 可能需要联系原作者获取数值

4. 拓扑绝缘体表面态
   - Bi2Se3, Bi2Te3等
   - 表面态的量子霍尔效应
"""

print(priorities)

# 保存搜索策略
with open('extended_search_strategy.json', 'w') as f:
    json.dump(search_queries, f, indent=2)

print("\n搜索策略已保存至: extended_search_strategy.json")
