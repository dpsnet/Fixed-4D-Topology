#!/usr/bin/env python3
"""
搜索石墨烯相关文献数据
"""

import requests
from datetime import datetime

# 搜索关键词
KEYWORDS = [
    "graphene Landau levels energy spectroscopy",
    "graphene exciton Rydberg series",
    "graphene interband transitions doping",
    "graphene optical conductivity frequency",
]

print("="*70)
print("石墨烯数据搜索报告")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*70)

print("\n搜索关键词:")
for i, kw in enumerate(KEYWORDS, 1):
    print(f"  {i}. {kw}")

print("\n目标数据:")
print("  - Landau能级位置 (n=0, ±1, ±2...)")
print("  - 能量随掺杂/磁场变化")
print("  - 光学谱数据")
print("  - 预期 c₁ ≈ 0.5 (相对论性)")

print("\n潜在数据源:")
print("  1. Nature Physics 石墨烯 Landau 能级")
print("  2. PRL 石墨烯红外光谱")
print("  3. Science 石墨烯激子")
print("  4. arXiv 最新预印本")

print("\n" + "="*70)
