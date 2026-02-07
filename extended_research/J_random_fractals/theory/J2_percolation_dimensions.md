# J2: Percolation Critical Phenomena and Dimensions
## Effective Dimensions in Disordered Systems

---

## 1. Percolation Theory Basics

### 1.1 Critical Phenomena

Percolation exhibits a continuous phase transition at critical probability $p_c$:
- $p < p_c$: Finite clusters only
- $p = p_c$: Infinite cluster emerges (fractal)
- $p > p_c$: Giant component dominates

**Critical exponents** (universal for given dimension):
- $\nu$: Correlation length $\xi \sim |p - p_c|^{-\nu}$
- $\beta$: Order parameter $P_\infty \sim (p - p_c)^\beta$
- $d_f$: Fractal dimension of infinite cluster

### 1.2 Dimension Hierarchy in Percolation

| Dimension | Type | Value (3D) | Scaling |
|-----------|------|------------|---------|
| $d$ | Euclidean | 3 | Fixed |
| $d_f$ | Hausdorff | 2.52 | $M \sim r^{d_f}$ |
| $d_s$ | Spectral | 1.32 | $\rho(\omega) \sim \omega^{d_s/2 - 1}$ |
| $d_w$ | Walk | 3.48 | $\langle r^2 \rangle \sim t^{2/d_w}$ |
| $d_{\text{eff}}$ | Effective | 1.8-2.2 | From Master Equation |

**Relation**:
$$d_s = \frac{2d_f}{d_w}$$

---

## 2. Dimensionics Framework for Percolation

### 2.1 Percolation Master Equation

For percolation clusters near criticality:

$$d_{\text{eff}}(p) = \arg\min_d \left[ \Delta E(d, p) - T_{\text{dis}} S(d) + \Lambda_{\text{perc}}(d, p) \right]$$

where:
- $\Delta E(d, p)$: Energy cost of cluster formation (depends on $p - p_c$)
- $T_{\text{dis}}$: Disorder temperature (related to $p$)
- $S(d)$: Configuration entropy of clusters
- $\Lambda_{\text{perc}}$: Percolation correction (finite-size effects)

### 2.2 Critical Dimension Flow

**Prediction J2.1**: As $p \to p_c$, effective dimension approaches universal value:

$$d_{\text{eff}}(p) = d_{\text{eff}}^c + A|p - p_c|^{\phi}$$

where $\phi$ is a new critical exponent related to dimension flow.

**Numerical prediction for 3D**:
- $d_{\text{eff}}^c \approx 2.0$
- $\phi \approx \nu \approx 0.88$

### 2.3 Cluster Size Dependence

For clusters of size $s$:

$$d_{\text{eff}}(s) = d_{\text{min}} + (d_{\text{eff}}^c - d_{\text{min}}) \cdot f(s/s_\xi)$$

where:
- $s_\xi \sim \xi^{d_f}$ is correlation volume
- $f(x)$: scaling function
- $d_{\text{min}} \approx 1.0$ (small clusters are tree-like)

---

## 3. Numerical Simulation Strategy

### 3.1 Monte Carlo Setup

**Algorithm**:
1. Generate L³ lattice (L = 30-100)
2. Occupation probability $p$
3. Identify clusters (Hoshen-Kopelman)
4. Measure dimension of largest cluster
5. Average over 1000-10000 realizations

### 3.2 Dimension Measurement

**Box-counting on clusters**:
```python
for cluster in clusters:
    for box_size in box_sizes:
        N_boxes = count_boxes_needed(cluster, box_size)
    d_f = -slope(log(N_boxes) vs log(1/box_size))
```

**Spectral dimension** (random walks):
1. Launch random walker on cluster
2. Measure return probability $P(t)$
3. $d_s = -2 \cdot d(\log P)/d(\log t)$

### 3.3 Finite-Size Scaling

Near $p_c$, observables scale as:

$$d_{\text{eff}}(L, p) = d_{\text{eff}}^c + L^{-1/\nu} \cdot g((p - p_c)L^{1/\nu})$$

**Data collapse**: Plot $L^{1/\nu}(d_{\text{eff}} - d_{\text{eff}}^c)$ vs $(p-p_c)L^{1/\nu}$

---

## 4. Dimensional Crossover Phenomena

### 4.1 2D to 3D Crossover

Question: How does percolation dimension change with thickness?

**Thin films** (few layers):
- Effectively 2D
- $d_{\text{eff}} \approx 1.9$

**Thick films** (many layers):
- Approaches 3D
- $d_{\text{eff}} \approx 2.0$

**Crossover thickness**: $t_c \sim \xi_{2D}$

### 4.2 Anisotropic Percolation

Systems with different probabilities in different directions:
- $p_x \neq p_y \neq p_z$
- Anisotropic dimension tensor?
- $d_{\text{eff}, x} \neq d_{\text{eff}, y}$

**Applications**:
- Composite materials
- Fractured rocks
- Biological tissues

---

## 5. Connection to Random Walks

### 5.1 Anomalous Diffusion

On percolation clusters at $p_c$:
$$\langle r^2(t) \rangle \sim t^{2/d_w}$$

where $d_w > 2$ (anomalous diffusion, slower than normal).

**Dimensionics interpretation**:
- Walk dimension $d_w$ emerges from Master Equation
- Competition between cluster geometry and random walk entropy

### 5.2 First-Passage Time

Mean first-passage time:
$$\tau \sim L^{d_w}$$

**Prediction**: Systems with higher $d_{\text{eff}}$ have shorter passage times (more paths available).

---

## 6. Experimental Connections

### 6.1 Electrical Conductivity

AC conductivity on percolating networks:
$$\sigma(\omega) \sim \omega^x$$

where $x = (d - 2 + \tilde{\zeta})/d_w$ depends on dimension.

### 6.2 Mechanical Properties

Elastic modulus near $p_c$:
- 3D percolation: $E \sim (p - p_c)^{f}$
- Dimension affects exponent $f$

### 6.3 Fluid Flow in Porous Media

Permeability in porous rocks:
$$k \sim (p - p_c)^\mu$$

**Application**: Oil reservoir characterization via dimension measurements.

---

## 7. Open Questions

1. **Is there a universal $d_{\text{eff}}$ at $p_c$?**
   - Does it depend only on Euclidean dimension $d$?
   - Or also on percolation type (site vs bond)?

2. **What is the upper critical dimension for $d_{\text{eff}}$?**
   - Above $d = 6$, mean-field should apply
   - Does $d_{\text{eff}}$ also become mean-field?

3. **Can we predict transport exponents from $d_{\text{eff}}$?**
   - Conductivity exponent
   - Diffusion constant
   - Viscosity

4. **Quantum percolation?**
   - Anderson transition
   - Many-body localization
   - Role of quantum interference

---

## 8. Numerical Targets

### Phase 1: Critical Properties (Month 1)
- [ ] $p_c$ refinement: 3D site percolation
- [ ] Fractal dimension $d_f$: high precision (error < 1%)
- [ ] Spectral dimension $d_s$: via random walks

### Phase 2: Dimension Flow (Month 2)
- [ ] $d_{\text{eff}}(p)$ curve near criticality
- [ ] Critical exponent $\phi$ extraction
- [ ] Finite-size scaling verification

### Phase 3: Applications (Month 3)
- [ ] Conductivity simulation
- [ ] Elastic network study
- [ ] Comparison with experimental data

---

## 9. References

- Stauffer, Aharoni (1994): Introduction to Percolation Theory
- Bunde, Havlin (1996): Fractals and Disordered Systems
- ben-Avraham, Havlin (2000): Diffusion and Reactions in Fractals and Disordered Systems
- Christensen et al. (2000): Effective dimensions in percolation

---

**Status**: Theory framework complete, simulations ongoing  
**Next**: Large-scale Monte Carlo simulations
