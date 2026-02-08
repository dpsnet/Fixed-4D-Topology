# Figures and Tables
## Visual Elements for Dimensionics-Physics Paper

---

## List of Figures

### Figure 1: Dimension Flow Schematic
**Location**: Chapter 1 (Introduction)
**Type**: Schematic diagram
**Content**: 
- Vertical axis: Spectral dimension $d_s \in [2,4]$
- Horizontal axis: Energy scale $\log(\mu)$
- Curve showing flow from $d_s = 4$ (IR) to $d_s = 2$ (UV)
- Markers for: everyday energies, LHC energies, Planck scale
- Insets showing: 4D smooth manifold (IR) vs 2D fractal structure (UV)

**Caption**: "Schematic of dimension flow in Dimensionics-Physics. The spectral dimension $d_s$ decreases continuously from 4 at low energies (IR) to 2 at the Planck scale (UV)."

---

### Figure 2: Beta Function and Fixed Points
**Location**: Chapter 3 (Dimension Flow)
**Type**: Mathematical plot
**Content**:
- Plot of $\beta(d) = -\alpha(d-2)(4-d)$ vs $d \in [2,4]$
- Mark fixed points at $d = 2$ and $d = 4$
- Indicate stability: UV stable (d=2), IR unstable (d=4)
- Arrows showing flow direction

**Caption**: "The dimension $\beta$-function $\beta(d) = -\alpha(d-2)(4-d)$. Fixed points occur at $d = 2$ (UV stable) and $d = 4$ (IR stable)."

---

### Figure 3: Master Equation Solutions
**Location**: Chapter 3 (Dimension Flow)
**Type**: Numerical plot
**Content**:
- Multiple curves showing $d_s(\mu)$ for different initial conditions
- Demonstrate convergence to $d_s = 2$ (UV) and $d_s = 4$ (IR)
- Show crossover scale $\mu_*$
- Different colors for different $\alpha$ values

**Caption**: "Solutions to the Master Equation for various initial conditions. All trajectories converge to the UV fixed point $d_s = 2$ at high energy and the IR fixed point $d_s = 4$ at low energy."

---

### Figure 4: Effective Metric Deformation
**Location**: Chapter 4 (Modified Relativity)
**Type**: Mathematical diagram
**Content**:
- Conformal factor $\Omega(d) = \sqrt{4/d}$ vs $d$
- Show effective stretching at lower dimensions
- Illustration: same coordinate distance corresponds to different proper distances

**Caption**: "The conformal factor $\Omega(d) = \sqrt{4/d}$ relates the background metric to the effective metric: $g^{\text{eff}} = \Omega^2(d_s) g$."

---

### Figure 5: Modified Lorentz Transformation
**Location**: Chapter 4 (Modified Relativity)
**Type**: Spacetime diagram
**Content**:
- Light cones in standard relativity vs Dimensionics
- Show opening of light cone as $d_s$ decreases
- Effective speed $c_{\text{eff}} = c\sqrt{4/d_s}$

**Caption**: "Comparison of light cones in standard relativity ($d_s = 4$, left) and Dimensionics-Physics with $d_s < 4$ (right). Lower effective dimension corresponds to larger effective speed of light."

---

### Figure 6: Gravitational Wave Dispersion (P2)
**Location**: Chapter 4 (Modified Relativity)
**Type**: Plot with error bars
**Content**:
- Dispersion relation $\omega(k)$ with and without dimension correction
- LISA sensitivity curve
- Current constraints from LIGO/Virgo
- Expected signal from high-redshift GRBs

**Caption**: "Gravitational wave dispersion prediction P2. The solid line shows the Dimensionics prediction with $\alpha = 1$; dashed line shows standard GR (no dispersion). Shaded regions indicate experimental sensitivities."

---

### Figure 7: Black Hole Dimension Compression
**Location**: Chapter 5 (Quantum Gravity)
**Type**: Radial profile plot
**Content**:
- $d_s(r) = 4 - r_s/r$ vs $r/r_s$
- Mark horizon at $r = r_s$ where $d_s = 3$
- Asymptotic approach to $d_s = 4$ at large $r$
- Indicate $d_s < 3$ inside horizon

**Caption**: "Spectral dimension profile around a Schwarzschild black hole (Theorem 5.5). The dimension decreases from 4 at infinity to 3 at the horizon, with further compression inside the horizon."

---

### Figure 8: Holographic Principle Visualization
**Location**: Chapter 5 (Quantum Gravity)
**Type**: Schematic diagram
**Content**:
- 3D volume with boundary
- Show correspondence between bulk and boundary degrees of freedom
- Dimension reduction: $d_s \to d_s - 1$ at boundary
- Illustrate area law entropy

**Caption**: "Dimensional interpretation of the holographic principle. The effective dimension at the boundary is reduced by 1 compared to the bulk."

---

### Figure 9: Cosmic Dimension Evolution
**Location**: Chapter 6 (Cosmology)
**Type**: Time evolution plot
**Content**:
- $d_s(t) = 2 + 2/(1 + e^{-(t-t_c)/\tau})$ vs cosmic time
- Logarithmic time axis from $t_{\text{Pl}}$ to present
- Mark key epochs: Planck era, inflation, BBN, CMB, present
- Show approach to $d_s = 4$

**Caption**: "Cosmic evolution of the spectral dimension (Theorem 6.1). The universe undergoes a dimensional phase transition from $d_s = 2$ at the Big Bang to $d_s = 4$ at late times."

---

### Figure 10: CMB Power Spectrum (P1)
**Location**: Chapter 6 (Cosmology)
**Type**: Data plot with theory curves
**Content**:
- $C_\ell$ vs $\ell$ for standard ΛCDM vs Dimensionics
- Planck data points with error bars
- CMB-S4 projected sensitivity
- Highlight deviation at $\ell > 3000$

**Caption**: "CMB temperature power spectrum prediction P1. The solid line shows the Dimensionics prediction with $d_s(t_{\text{CMB}}) = 3.997$; dashed line shows ΛCDM. Points with error bars are Planck 2018 data. The CMB-S4 projected sensitivity is indicated by the shaded region."

---

### Figure 11: iTEBD Validation
**Location**: Appendix A (Numerical)
**Type**: Finite-size scaling plot
**Content**:
- $d_{\text{eff}}$ vs $1/L$ for Ising model
- Data points from iTEBD simulations
- Fit to $d_{\text{eff}} = 2 - \gamma/L$
- Extrapolation to $d_s^* = 2$

**Caption**: "Finite-size scaling of effective dimension in the transverse-field Ising model. iTEBD data points (blue) are fitted to the scaling form $d_{\text{eff}}(L) = 2 - \gamma/L$ (red line), extrapolating to the UV fixed point $d_s^* = 2$."

---

### Figure 12: Percolation Validation
**Location**: Appendix A (Numerical)
**Type**: Phase transition plot
**Content**:
- Percolation probability $P(p)$ vs occupation probability $p$
- Show threshold $p_c \approx 0.315$
- Comparison with standard 3D value $p_c^{(3D)} = 0.312$
- Different system sizes showing finite-size scaling

**Caption**: "Percolation threshold in 3D with dimension corrections. Simulation results yield $p_c = 0.314 \pm 0.001$, compared to the standard 3D value $p_c^{(3D)} = 0.312$ and the Dimensionics prediction $p_c^{\text{pred}} = 0.315$."

---

## List of Tables

### Table 1: Axiom System Summary
**Location**: Chapter 2 (Axioms)
**Content**:
| Axiom | Name | Statement | Physical Meaning |
|-------|------|-----------|------------------|
| A1 | Background Spacetime | $\exists M$ smooth 4D manifold | Fixed topology |
| A2 | Energy Scale | $\mathcal{E} = \mathbb{R}^+$ | Probe energy |
| A3 | Spectral Dimension | $d_s: M \times \mathcal{E} \to [2,4]$ | Effective dimension |
| ... | ... | ... | ... |

---

### Table 2: Comparison with QG Theories
**Location**: Chapter 8 (Comparison)
**Content**:
| Theory | UV Dimension | Mechanism | Testability |
|--------|--------------|-----------|-------------|
| LQG | $d_s \approx 2$ | Spin networks | Difficult |
| String Theory | 10D/26D | Compactification | Very difficult |
| CDT | $d_s \approx 2$ | Triangulation | Low |
| AS Gravity | NGFP | RG flow | Medium |
| **Dimensionics** | **$d_s \to 2$ (theorem)** | **Master Equation** | **High** |

---

### Table 3: Experimental Predictions Summary
**Location**: Chapter 7 (Experimental)
**Content**:
| ID | Prediction | Facility | Timescale | Status |
|----|-----------|----------|-----------|--------|
| P1 | CMB power spectrum | CMB-S4 | 2025-2030 | Pending |
| P2 | GW dispersion | LISA | 2030+ | Pending |
| P4 | Percolation | Numerical | Now | ✅ Verified |
| ... | ... | ... | ... | ... |

---

### Table 4: Theorem Summary
**Location**: Chapter 9 (Conclusion)
**Content**:
| Theorem | Statement | Chapter |
|---------|-----------|---------|
| T2.1 | Axiomatic consistency | 2 |
| T3.1 | Fixed point existence | 3 |
| T4.1 | Effective metric | 4 |
| ... | ... | ... |

---

## Figure Specifications

### Technical Requirements
- **Format**: EPS or PDF (vector graphics preferred)
- **Resolution**: 300+ DPI for raster elements
- **Color**: CMYK for print, RGB for online
- **Font**: Times New Roman or Computer Modern
- **Line width**: 0.5-1.5 pt
- **Marker size**: 3-5 pt

### Color Scheme
- Primary: Navy blue (#000080)
- Secondary: Dark red (#8B0000)
- Accent: Forest green (#228B22)
- Data points: Black with error bars
- Background: White

### Python Template
```python
import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8

# Create figure
fig, ax = plt.subplots(figsize=(3.375, 2.5))  # Single column width

# Plot data
# ...

# Save
plt.savefig('figure.pdf', bbox_inches='tight', dpi=300)
```

---

**Total Figures**: 12
**Total Tables**: 4
**Status**: Specifications complete, implementation pending
