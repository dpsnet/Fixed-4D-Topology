#!/usr/bin/env python3
"""
制作论文Figure 1：维度流示意图
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse
import matplotlib.patches as mpatches

plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13

fig = plt.figure(figsize=(12, 4))

# ===== 子图a：维度流概念图 =====
ax1 = fig.add_subplot(131)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('(a) Dimension Flow Concept', fontsize=12, fontweight='bold')

# 绘制轨道
for i, (radius, color, label) in enumerate([
    (1.5, 'blue', 'n=3\n(3D-like)'),
    (3.0, 'purple', 'n=10\n(intermediate)'),
    (4.5, 'red', 'n=25\n(2D-like)')
]):
    circle = plt.Circle((5, 5), radius, fill=False, color=color, linewidth=2, alpha=0.7)
    ax1.add_patch(circle)
    ax1.text(5, 5+radius+0.5, label, ha='center', fontsize=9, color=color)

# 中心点
ax1.plot(5, 5, 'ko', markersize=8)
ax1.text(5, 4.2, 'Core', ha='center', fontsize=9)

# 箭头表示维度流
arrow = FancyArrowPatch((8, 8), (8, 2), 
                        arrowstyle='->', mutation_scale=20,
                        color='green', linewidth=2)
ax1.add_patch(arrow)
ax1.text(8.5, 5, '$d_{eff}$\n3D → 2D', fontsize=9, color='green', va='center')

# ===== 子图b：c₁公式 =====
ax2 = fig.add_subplot(132)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('(b) Dimension Flow Parameter', fontsize=12, fontweight='bold')

# 公式
ax2.text(5, 7, r'$c_1(d, w) = \frac{1}{2^{d-2+w}}$', 
         ha='center', fontsize=14, fontweight='bold')

ax2.text(5, 5, r'$d_{eff}(n) = d_{min} + \frac{d_{max}-d_{min}}{1+(n/n_0)^{1/c_1}}$', 
         ha='center', fontsize=12)

# 数值表
table_text = '''Parameter Values:
• Cu₂O (3D, w=0): c₁ = 0.5
• Graphene (2D, w=1): c₁ = 0.5
• Quantum well (2D, w=0): c₁ = 1.0'''
ax2.text(5, 2.5, table_text, ha='center', fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# ===== 子图c：(d,w) 相图 =====
ax3 = fig.add_subplot(133)

# 创建网格
d_values = np.array([2, 3, 4])
w_values = np.array([0, 0.5, 1])
D, W = np.meshgrid(d_values, w_values)
C1 = 1 / (2**(D - 2 + W))

# 绘制热力图
im = ax3.imshow(C1, cmap='RdYlBu_r', aspect='auto', 
                extent=[1.5, 4.5, -0.2, 1.2], origin='lower',
                vmin=0.1, vmax=1.0)

# 标记特殊点
points = [
    (3, 0, 'Cu₂O\n(3D)', 'white'),
    (2, 1, 'Graphene\n(2D, rel)', 'yellow'),
    (2, 0, 'Quantum well\n(2D)', 'yellow'),
    (4, 0, '4D space', 'white'),
]

for d, w, label, color in points:
    ax3.plot(d, w, 'o', markersize=12, color=color, markeredgecolor='black', markeredgewidth=2)
    ax3.text(d, w+0.15, label, ha='center', fontsize=8, 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax3.set_xlabel('Space dimension $d$', fontsize=11)
ax3.set_ylabel('Time weight $w$', fontsize=11)
ax3.set_title('(c) $(d, w)$ Parameter Space', fontsize=12, fontweight='bold')

# 添加颜色条
cbar = plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
cbar.set_label('$c_1$', fontsize=11)

# 设置刻度
ax3.set_xticks([2, 3, 4])
ax3.set_yticks([0, 0.5, 1])
ax3.set_yticklabels(['0\n(non-rel)', '0.5', '1\n(rel)'])

plt.tight_layout()
plt.savefig('figure1_schematic.png', dpi=300, bbox_inches='tight')
print("✓ Figure 1 已保存: figure1_schematic.png")
plt.close()

# 显示统计信息
print("\n图表内容:")
print("  (a) 维度流概念：从3D到2D的过渡")
print("  (b) c₁公式和典型值")
print("  (c) (d,w)参数空间相图")
