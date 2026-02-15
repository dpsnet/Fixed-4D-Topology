#!/usr/bin/env python3
"""
Figure 26: Advanced Topic Visualization

Part of the Unified Dimension Flow Theory figure set.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 5))

# Left panel
ax1 = fig.add_subplot(121)
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/10)
ax1.plot(x, y, 'b-', lw=2)
ax1.set_xlabel('X', fontsize=12)
ax1.set_ylabel('Y', fontsize=12)
ax1.set_title(f'Figure 26a', fontsize=13)
ax1.grid(True, alpha=0.3)

# Right panel
ax2 = fig.add_subplot(122, projection='3d')
X = np.linspace(-5, 5, 50)
Y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax2.set_title(f'Figure 26b', fontsize=13)

plt.tight_layout()
plt.savefig(f'../fig26_advanced.pdf', dpi=600, bbox_inches='tight')
plt.savefig(f'../fig26_advanced.png', dpi=600, bbox_inches='tight')
print(f'Figure 26 saved: advanced topic')
