## Appendix A: Detailed Spectral Analysis of the Sierpinski Gasket

### A.1 Graph Laplacian Construction

The Sierpinski gasket $SG$ can be approximated by a sequence of graphs $\Gamma_n$ with:
- $\Gamma_0$: Single triangle (3 vertices)
- $\Gamma_{n+1}$: Each edge replaced by two edges meeting at a new vertex

**Number of vertices**: $V_n = \frac{3}{2}(3^n + 1)$

**Adjacency matrix** $A_n$: $A_{ij} = 1$ if vertices $i$ and $j$ are adjacent

**Degree matrix** $D_n$: $D_{ii} = \deg(i)$

**Graph Laplacian**: $L_n = D_n - A_n$

### A.2 Eigenvalue Spectrum

The spectrum of $L_n$ exhibits a fractal structure:

**Primitive eigenvalues**: Those not inherited from previous levels

**Spectral decimation** (Fukushima-Shima): Eigenvalues at level $n$ map to eigenvalues at level $n+1$ via:

$$\lambda^{(n+1)} = \frac{5 \pm \sqrt{25 - 4\lambda^{(n)}}}{2}$$

**Multiplicities**: Follow the pattern $m_k = 3^{n-k-1}$ for appropriate $k$

### A.3 Spectral Zeta Function

$$\zeta_{SG}(s) = \sum_{\lambda \neq 0} \lambda^{-s}$$

**Key properties**:
- Meromorphic continuation to $\mathbb{C}$
- Simple pole at $s = d_s^*/2 = \log 3 / \log 5$
- Residue related to volume

### A.4 Heat Kernel Asymptotics

For the Sierpinski gasket:

$$p(t) = \frac{1}{V_n}\text{Tr}(e^{-tL_n}) \sim t^{-d_s^*/2} \sum_{k=0}^{\infty} c_k t^{k\alpha}$$

where $\alpha = \log(5/3)/\log 5 \approx 0.317$

**Subleading terms** arise from:
1. Localized eigenfunctions
2. Spectral gaps
3. Boundary effects (for finite approximations)

---

## Appendix B: PDE Solution Methods

### B.1 Analytical Solution

The PDE can be written as:

$$\frac{\partial d_s}{\partial t} - \frac{d_s}{t\log t} = \frac{2\langle\lambda\rangle_t}{\log t}$$

**Integrating factor**: $\mu(t) = \frac{1}{\log t}$

**Solution**:
$$d_s(t) = \log t \int_{t_0}^t \frac{2\langle\lambda\rangle_s}{s(\log s)^2} ds + C\log t$$

### B.2 Asymptotic Series

For small $t$:
$$d_s(t) = d_s^* + \sum_{k=1}^{\infty} c_k t^{k\alpha} + \mathcal{O}(e^{-\lambda_1 t})$$

where $\lambda_1$ is the first non-zero eigenvalue.

### B.3 Numerical Integration

**Adaptive methods**: Required due to singularity at $t = 1$ and stiffness for small $t$

**Recommended scheme**: RK4 with adaptive step size

---

## Appendix C: Comparison Table of Fractal Spectral Dimensions

| Fractal | $d_H$ | $d_s$ | $d_w$ | $
u$ |
|---------|-------|-------|-------|-------|
| Sierpinski Gasket | $\log 3/\log 2 \approx 1.585$ | $2\log 3/\log 5 \approx 1.365$ | $\log 5/\log 2 \approx 2.322$ | 0.798 |
| Cantor Set | $\log 2/\log 3 \approx 0.631$ | $2\log 2/\log 3 \approx 1.262$ | $2$ | 1.0 |
| Koch Curve | 1 | 1 | 1 | 1 |
| Menger Sponge | $\log 20/\log 3 \approx 2.727$ | $2\log 20/\log 3 \approx 2.727$ | $\log 3/\log 2 \approx 1.585$ | 0.5 |

**Relations**:
- $d_w = 2d_H/d_s$ (walk dimension)
- $\nu = 1/d_w$ (correlation length exponent)

