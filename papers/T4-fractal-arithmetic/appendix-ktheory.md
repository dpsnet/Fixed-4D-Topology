## Appendix A: K-Theory and Fractal Dimensions

### A.1 Topological K-Theory Basics

For a topological space $X$, the K-groups are:
- $K^0(X)$: Grothendieck group of vector bundles
- $K^1(X)$: Suspension of $K^0$

**Bott periodicity**: $K^n(X) \cong K^{n+2}(X)$

### A.2 Fractal K-Groups

For a fractal $F$ viewed as a metric space:

**Definition**: $K^0_{\text{frac}}(F) = \mathcal{G}_D^{(r)} \otimes \mathbb{Z}$

**Relation to standard K-theory**: For p.c.f. fractals embedded in $\mathbb{R}^n$:

$$K^0_{\text{frac}}(F) \hookrightarrow K^0(F) \otimes \mathbb{Q}$$

### A.3 Chern Character

The Chern character provides a bridge:

$$\text{ch}: K^0(F) \to H^{\text{even}}(F; \mathbb{Q})$$

For fractals, the "dimension" can be viewed as the degree-0 part:

$$\dim(F) = \text{ch}_0([F])$$

---

## Appendix B: Non-Commutative Geometry Perspective

### B.1 Spectral Triples

A spectral triple $(\mathcal{A}, \mathcal{H}, D)$ consists of:
- $\mathcal{A}$: algebra of functions
- $\mathcal{H}$: Hilbert space
- $D$: Dirac operator

**Dimension spectrum**: Set of poles of $\zeta_D(s) = \text{Tr}(|D|^{-s})$

### B.2 Fractal Spectral Triples

For the Sierpinski gasket (Connes-Dubois-Violette):
- $\mathcal{A} = C(SG)$
- $\mathcal{H} = L^2(SG, \mu)$
- $D$ constructed from the Laplacian

**Key result**: The dimension spectrum includes $d_s^* = 2\log 3/\log 5$

### B.3 Dixmier Trace

The Dixmier trace generalizes the integral for non-integer dimensions:

$$\int_D a := \text{Tr}_\omega(a|D|^{-d_s^*})$$

This provides a "integral calculus" on fractals.

---

## Appendix C: Categorical Formulation

### C.1 Category of Fractal Dimensions

**Objects**: Pairs $(F, d)$ where $F$ is a fractal and $d \in \mathcal{G}_D^{(r)}$

**Morphisms**: Self-similarity maps $f: F \to F'$ with scaling factor $s$

The Grothendieck group construction is the left adjoint to the forgetful functor from abelian groups to commutative monoids.

### C.2 Functorial Properties

Given a self-similarity morphism $\phi: F \to F$ with scaling $r$:

$$\phi_*: \mathcal{G}_D^{(r)}(F) \to \mathcal{G}_D^{(r)}(F)$$

acts by multiplication by the number of copies.

### C.3 Exact Sequences

For a fractal $F$ and sub-fractal $F' \subset F$:

$$0 \to \mathcal{G}_D^{(r)}(F') \to \mathcal{G}_D^{(r)}(F) \to \mathcal{G}_D^{(r)}(F/F') \to 0$$

whenever the quotient makes sense geometrically.

