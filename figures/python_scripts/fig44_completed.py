#!/usr/bin/env python3
"""
Figure 44: Scalable Architecture Designs

Part of Unified Dimension Flow Theory review.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Platform comparison
ax1 = axes[0]
platforms = ['Superconducting', 'Trapped Ion', 'Photonic', 'Neutral Atom', 'Topological']
dims = [3.2, 3.5, 2.8, 3.0, 2.5]
colors = ['blue', 'green', 'red', 'purple', 'orange']
bars = ax1.bar(platforms, dims, color=colors, alpha=0.7, edgecolor='black')
ax1.axhline(y=3.0, color='gray', linestyle='--', alpha=0.5, label='Target =3$')
ax1.set_ylabel('Effective Dimension', fontsize=12)
ax1.set_title('Architecture Scalability', fontsize=13)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Right: Performance scaling
ax2 = axes[1]
n_qubits = np.array([10, 20, 50, 100, 200, 500, 1000])
performance = n_qubits**0.8 / (1 + n_qubits/100)
ax2.loglog(n_qubits, performance, 'b-o', lw=2.5, markersize=8)
ax2.fill_between(n_qubits, performance*0.8, performance*1.2, alpha=0.3)
ax2.set_xlabel('Number of Qubits', fontsize=12)
ax2.set_ylabel('Relative Performance', fontsize=12)
ax2.set_title('Scaling Behavior', fontsize=13)
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig(f'../fig44_completed.pdf', dpi=600, bbox_inches='tight')
plt.savefig(f'../fig44_completed.png', dpi=600, bbox_inches='tight')
print(f'Figure 44 completed')
