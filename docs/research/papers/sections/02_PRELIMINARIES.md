# 2. Preliminaries

This section establishes the foundational material required for our main theorems. We review Kleinian groups and Patterson-Sullivan theory, p-adic analysis, Berkovich spaces, and thermodynamic formalism. Standard references include [Bea83, Mar07] for Kleinian groups, [Gou97, Rob00] for p-adic analysis, [Ber90, BR10] for Berkovich spaces, and [PP90, Kel98] for thermodynamic formalism.

---

## 2.1 Kleinian Groups and Limit Sets

### 2.1.1 Basic Definitions

Let $\mathbb{H}^3$ denote hyperbolic 3-space, modeled as the upper half-space $\{(x,y,z) : z > 0\}$ with metric $ds^2 = (dx^2 + dy^2 + dz^2)/z^2$. The group of orientation-preserving isometries of $\mathbb{H}^3$ is isomorphic to $\mathrm{PSL}(2,\mathbb{C})$, acting by Möbius transformations on the boundary at infinity $\partial\mathbb{H}^3 \cong \hat{\mathbb{C}} = \mathbb{C} \cup \{\infty\}$.

**Definition 2.1.** A *Kleinian group* $\Gamma < \mathrm{PSL}(2,\mathbb{C})$ is a discrete subgroup that acts properly discontinuously on $\mathbb{H}^3$.

The *limit set* $\Lambda(\Gamma) \subset \hat{\mathbb{C}}$ is the set of accumulation points of any orbit $\Gamma \cdot x$ for $x \in \mathbb{H}^3$:
$$\Lambda(\Gamma) = \overline{\Gamma \cdot x} \cap \partial\mathbb{H}^3$$

The complement $\Omega(\Gamma) = \hat{\mathbb{C}} \setminus \Lambda(\Gamma)$ is called the *domain of discontinuity*, on which $\Gamma$ acts properly discontinuously.

**Definition 2.2.** A Kleinian group $\Gamma$ is *geometrically finite* if it has a finite-sided fundamental polyhedron in $\mathbb{H}^3$. It is *convex cocompact* if the convex core of $\Gamma \backslash \mathbb{H}^3$ is compact.

For convex cocompact groups, the limit set is either all of $\hat{\mathbb{C}}$ (cocompact case) or a perfect, totally disconnected Cantor set (infinite covolume case).

### 2.1.2 Hausdorff Dimension

For a metric space $(X,d)$ and $s \geq 0$, the $s$-dimensional Hausdorff measure is defined by
$$\mathcal{H}_s(E) = \lim_{\delta \to 0} \inf \left\{ \sum_i (\mathrm{diam}\, U_i)^s : E \subset \bigcup_i U_i, \, \mathrm{diam}\, U_i < \delta \right\}$$

The *Hausdorff dimension* of $E$ is
$$\dim_H(E) = \inf\{s \geq 0 : \mathcal{H}_s(E) = 0\} = \sup\{s \geq 0 : \mathcal{H}_s(E) = \infty\}$$

**Theorem 2.3 (Bowen [Bow79]).** For a convex cocompact Kleinian group $\Gamma$ with non-elementary limit set, $0 < \dim_H(\Lambda(\Gamma)) < 2$.

### 2.1.3 Patterson-Sullivan Theory

The *Poincaré series* of $\Gamma$ with exponent $s \geq 0$ is
$$P_s(x,y) = \sum_{\gamma \in \Gamma} e^{-s \cdot d(x, \gamma y)}$$
where $d$ denotes hyperbolic distance.

**Definition 2.4.** The *critical exponent* $\delta(\Gamma)$ is
$$\delta(\Gamma) = \inf\{s \geq 0 : P_s(x,y) < \infty\}$$

**Theorem 2.5 (Patterson [Pat76], Sullivan [Sul79]).** For a geometrically finite Kleinian group:
$$\delta(\Gamma) = \dim_H(\Lambda(\Gamma))$$

**Definition 2.6.** A Borel measure $\mu$ on $\Lambda(\Gamma)$ is *$\delta$-conformal* if
$$\frac{d\gamma_*\mu}{d\mu}(\xi) = |\gamma'(\xi)|^\delta$$
for all $\gamma \in \Gamma$ and $\mu$-a.e. $\xi \in \Lambda(\Gamma)$.

**Theorem 2.7.** For a convex cocompact Kleinian group $\Gamma$, there exists a unique (up to scaling) $\delta$-conformal probability measure $\mu_{PS}$ on $\Lambda(\Gamma)$, called the *Patterson-Sullivan measure*.

### 2.1.4 Spectral Theory

Let $\Delta_\Gamma$ denote the positive Laplacian on the hyperbolic quotient $M_\Gamma = \Gamma \backslash \mathbb{H}^3$. For geometrically finite $\Gamma$, the spectrum consists of:
- A finite number of discrete eigenvalues in $[0, 1)$
- Absolutely continuous spectrum $[1, \infty)$

The resolvent $R_\Gamma(s) = (\Delta_\Gamma - s(2-s))^{-1}$ admits a meromorphic continuation to $\mathbb{C}$ [MM87, PP01].

**Theorem 2.8 (Lax-Phillips [LP82]).** For convex cocompact $\Gamma$, the resolvent has only finitely many poles in $\mathrm{Re}(s) > 1$, all in $(1, 2)$.

---

## 2.2 p-adic Analysis

### 2.2.1 p-adic Fields

Let $p$ be a prime number. The *p-adic absolute value* $|\cdot|_p$ on $\mathbb{Q}$ is defined by $|p^n \cdot a/b|_p = p^{-n}$ for integers $a,b$ not divisible by $p$. The *p-adic numbers* $\mathbb{Q}_p$ are the completion of $\mathbb{Q}$ with respect to $|\cdot|_p$.

**Definition 2.9.** The *p-adic valuation* $v_p: \mathbb{Q}_p^* \to \mathbb{Z}$ is $v_p(x) = -\log_p |x|_p$.

The algebraic closure $\overline{\mathbb{Q}}_p$ is not complete; we denote by $\mathbb{C}_p$ its completion. The absolute value $|\cdot|_p$ extends uniquely to $\mathbb{C}_p$, and the valuation ring is
$$\mathcal{O}_{\mathbb{C}_p} = \{z \in \mathbb{C}_p : |z|_p \leq 1\}$$
with maximal ideal $\mathfrak{m}_{\mathbb{C}_p} = \{z : |z|_p < 1\}$.

### 2.2.2 The Projective Line

The *p-adic projective line* is $\mathbb{P}^1(\mathbb{C}_p) = \mathbb{C}_p \cup \{\infty\}$. The topology is totally disconnected: open balls
$$B(a,r) = \{z \in \mathbb{C}_p : |z-a|_p < r\}$$
are also closed.

**Proposition 2.10 (Ultrametric Property).** For $x,y \in \mathbb{C}_p$:
$$|x+y|_p \leq \max\{|x|_p, |y|_p\}$$
with equality when $|x|_p \neq |y|_p$.

### 2.2.3 p-adic Dynamics

Let $\phi \in \mathbb{C}_p(z)$ be a rational function of degree $d \geq 2$, written as $\phi = F/G$ with coprime homogeneous polynomials $F,G \in \mathbb{C}_p[X,Y]$ of degree $d$.

**Definition 2.11.** The *Fatou set* $F(\phi)$ is the set of points $z \in \mathbb{P}^1(\mathbb{C}_p)$ where the iterates $\{\phi^n\}$ form a normal family in the sense of Berkovich. The *Julia set* is $J(\phi) = \mathbb{P}^1(\mathbb{C}_p) \setminus F(\phi)$.

**Definition 2.12.** $\phi$ is *hyperbolic* if there exists a metric in which $\phi$ is uniformly expanding on $J(\phi)$.

**Proposition 2.13 (Benedetto [Ben01]).** For a polynomial $\phi \in \mathbb{C}_p[z]$ of degree $d \geq 2$, the following are equivalent:
1. $\phi$ is hyperbolic
2. $|\phi'(z)|_p > 1$ for all $z \in J(\phi)$
3. $J(\phi)$ is totally disconnected and the critical points are in basins of attracting cycles

### 2.2.4 Non-Archimedean Potential Theory

**Definition 2.14.** A function $f: U \to \mathbb{R} \cup \{\infty\}$ on an open $U \subset \mathbb{P}^1(\mathbb{C}_p)$ is *subharmonic* if it is upper semicontinuous and for every $a \in U$ and sufficiently small $r > 0$:
$$f(a) \leq \frac{1}{\mu(B(a,r))} \int_{B(a,r)} f \, d\mu$$
where $\mu$ is the Haar measure on $\mathbb{C}_p$.

**Theorem 2.15 (Rivera-Letelier [RL03]).** For a rational function $\phi$ of degree $d \geq 2$, there exists a unique measure $\mu_\phi$ on $\mathbb{P}^1_{\mathrm{Berk}}$ satisfying $\phi^*\mu_\phi = d \cdot \mu_\phi$.

---

## 2.3 Berkovich Spaces

### 2.3.1 The Berkovich Affine Line

**Definition 2.16.** The *Berkovich affine line* $\mathbf{A}^1_{\mathrm{Berk}}$ over $\mathbb{C}_p$ is the set of all multiplicative seminorms $[\cdot]_x: \mathbb{C}_p[T] \to \mathbb{R}_{\geq 0}$ extending $|\cdot|_p$ on $\mathbb{C}_p$, equipped with the topology of pointwise convergence.

Points of $\mathbf{A}^1_{\mathrm{Berk}}$ are classified into four types:
- **Type I:** Points corresponding to $a \in \mathbb{C}_p$ via $[f]_a = |f(a)|_p$
- **Type II:** Points corresponding to closed disks $B(a,r)$ with $r \in |\mathbb{C}_p^*|_p$
- **Type III:** Points corresponding to closed disks with $r \notin |\mathbb{C}_p^*|_p$
- **Type IV:** Points corresponding to nested sequences of disks with empty intersection

**Theorem 2.17 (Berkovich [Ber90]).** $\mathbf{A}^1_{\mathrm{Berk}}$ is a locally compact, Hausdorff, path-connected topological space containing $\mathbb{C}_p$ as a dense Type I subset.

### 2.3.2 The Berkovich Projective Line

**Definition 2.18.** The *Berkovich projective line* $\mathbf{P}^1_{\mathrm{Berk}}$ is the one-point compactification of $\mathbf{A}^1_{\mathrm{Berk}}$:
$$\mathbf{P}^1_{\mathrm{Berk}} = \mathbf{A}^1_{\mathrm{Berk}} \cup \{\infty\}$$

Equivalently, $\mathbf{P}^1_{\mathrm{Berk}}$ can be defined as the set of multiplicative seminorms on $\mathbb{C}_p[X,Y]$ not vanishing on the homogeneous polynomials of positive degree, modulo scaling.

**Proposition 2.19.** $\mathbf{P}^1_{\mathrm{Berk}}$ is a compact, Hausdorff, uniquely arcwise connected space.

### 2.3.3 Tree Structure

The Berkovich projective line has the structure of an $\mathbb{R}$-tree with the hyperbolic metric $\rho$.

**Definition 2.20.** The *hyperbolic metric* on $\mathbf{H}_{\mathrm{Berk}} = \mathbf{P}^1_{\mathrm{Berk}} \setminus \mathbb{P}^1(\mathbb{C}_p)$ is defined by:
- For Type II points $\zeta_{B(a,r)}$ and $\zeta_{B(b,s)}$, $\rho(\zeta_{B(a,r)}, \zeta_{B(b,s)}) = \log_p(r/s)$ when one disk contains the other
- Extended by continuity to all points

**Theorem 2.21.** $(\mathbf{H}_{\mathrm{Berk}}, \rho)$ is a complete metric space on which $\mathrm{PGL}(2,\mathbb{C}_p)$ acts by isometries.

### 2.3.4 Measures on Berkovich Spaces

Let $\mathcal{M}(\mathbf{P}^1_{\mathrm{Berk}})$ denote the space of Radon probability measures.

**Definition 2.22.** The *weak*\* topology* on $\mathcal{M}(\mathbf{P}^1_{\mathrm{Berk}})$ is defined by $\mu_n \to \mu$ if
$$\int f \, d\mu_n \to \int f \, d\mu$$
for all continuous $f: \mathbf{P}^1_{\mathrm{Berk}} \to \mathbb{R}$.

**Theorem 2.23 (Prokhorov).** A subset $S \subset \mathcal{M}(\mathbf{P}^1_{\mathrm{Berk}})$ is relatively compact in the weak* topology if and only if it is tight: for every $\epsilon > 0$, there exists compact $K_\epsilon$ such that $\mu(K_\epsilon) > 1-\epsilon$ for all $\mu \in S$.

**Theorem 2.24.** $\mathcal{M}(\mathbf{P}^1_{\mathrm{Berk}})$ is compact in the weak* topology.

### 2.3.5 Dynamics on Berkovich Spaces

A rational function $\phi \in \mathbb{C}_p(z)$ extends canonically to $\mathbf{P}^1_{\mathrm{Berk}}$ by functoriality of Berkovich analytification.

**Theorem 2.25 (Rivera-Letelier [RL03]).** For $\phi$ of degree $d \geq 2$:
1. The Julia set $J(\phi) \subset \mathbf{P}^1_{\mathrm{Berk}}$ is compact and nonempty
2. The exceptional set is finite
3. Repelling periodic points are dense in $J(\phi)$

**Definition 2.26.** The *canonical measure* $\mu_\phi$ is the unique probability measure on $\mathbf{P}^1_{\mathrm{Berk}}$ satisfying $\phi^*\mu_\phi = d \cdot \mu_\phi$ and $\phi_*\mu_\phi = \mu_\phi$.

---

## 2.4 Thermodynamic Formalism

### 2.4.1 Topological Pressure

Let $T: X \to X$ be a continuous map on a compact metric space $(X,d)$ and $\varphi: X \to \mathbb{R}$ a continuous potential.

**Definition 2.27.** For $n \geq 1$, the *Bowen metric* is $d_n(x,y) = \max_{0 \leq k < n} d(T^k x, T^k y)$. A set $E \subset X$ is $(n,\epsilon)$-separated if $d_n(x,y) \geq \epsilon$ for distinct $x,y \in E$.

The *topological pressure* is
$$P(\varphi) = \lim_{\epsilon \to 0} \limsup_{n \to \infty} \frac{1}{n} \log \sup_E \sum_{x \in E} e^{S_n\varphi(x)}$$
where $S_n\varphi(x) = \sum_{k=0}^{n-1} \varphi(T^k x)$ and the supremum is over $(n,\epsilon)$-separated sets.

**Theorem 2.28 (Variational Principle, Walters [Wal82]).**
$$P(\varphi) = \sup_{\mu \in \mathcal{M}_T} \left\{ h_\mu(T) + \int \varphi \, d\mu \right\}$$
where $\mathcal{M}_T$ denotes $T$-invariant probability measures.

### 2.4.2 Gibbs Measures

**Definition 2.29.** A measure $\mu$ is a *Gibbs measure* for potential $\varphi$ if there exists $C > 0$ and $P \in \mathbb{R}$ such that for all $n \geq 1$ and $x \in X$:
$$C^{-1} \leq \frac{\mu(B_n(x,\epsilon))}{\exp(-nP + S_n\varphi(x))} \leq C$$
where $B_n(x,\epsilon) = \{y : d_n(x,y) < \epsilon\}$.

**Theorem 2.30 (Bowen [Bow75]).** For a topologically mixing subshift of finite type and Hölder continuous $\varphi$, there exists a unique Gibbs measure $\mu_\varphi$.

### 2.4.3 Transfer Operators

The *Ruelle-Perron-Frobenius (RPF) operator* is defined by
$$(\mathcal{L}_\varphi f)(x) = \sum_{y \in T^{-1}(x)} e^{\varphi(y)} f(y)$$

**Theorem 2.31 (Ruelle-Perron-Frobenius).** For a mixing subshift of finite type and Hölder continuous $\varphi$:
1. $\mathcal{L}_\varphi$ has a simple maximal eigenvalue $\lambda = e^{P(\varphi)}$
2. There exists a unique eigenmeasure $\nu$ with $\mathcal{L}_\varphi^* \nu = \lambda \nu$
3. There exists a unique eigenfunction $h > 0$ with $\mathcal{L}_\varphi h = \lambda h$
4. The Gibbs measure is $d\mu_\varphi = h \, d\nu$

### 2.4.4 Entropy and Dimension

**Definition 2.32.** The *measure-theoretic entropy* of $\mu \in \mathcal{M}_T$ is
$$h_\mu(T) = \lim_{\epsilon \to 0} \limsup_{n \to \infty} \frac{1}{n} H_\mu(\mathcal{P}_n)$$
where $\mathcal{P}$ is a generating partition and $\mathcal{P}_n = \bigvee_{k=0}^{n-1} T^{-k}\mathcal{P}$.

**Theorem 2.33 (Shannon-McMillan-Breiman).** For an ergodic measure $\mu$:
$$-\frac{1}{n} \log \mu(\mathcal{P}_n(x)) \to h_\mu(T) \quad \mu\text{-a.e.}$$

**Definition 2.34.** The *pointwise dimension* of a measure $\mu$ at $x$ is
$$d_\mu(x) = \lim_{r \to 0} \frac{\log \mu(B(x,r))}{\log r}$$
when the limit exists.

**Theorem 2.35 (Young [You82]).** For an ergodic measure with constant pointwise dimension $d_\mu$:
$$\dim_H(\mu) = h_\mu(T) / \chi_\mu$$
where $\chi_\mu = \int \log |T'| \, d\mu$ is the Lyapunov exponent.

### 2.4.5 Bowen Formula

**Theorem 2.36 (Bowen [Bow79], Ruelle [Rue82]).** For a conformal expanding repeller $J \subset \mathbb{C}$:
$$\dim_H(J) = s^*$$
where $s^*$ is the unique solution to $P(-s \log |T'|) = 0$.

---

## 2.5 Notation

### Sets and Spaces

| Symbol | Meaning |
|--------|---------|
|$\mathbb{H}^3$ | Hyperbolic 3-space |
|$\partial\mathbb{H}^3$ | Boundary at infinity |
|$\Gamma$ | Kleinian group |
|$\Lambda(\Gamma)$ | Limit set |
|$\Omega(\Gamma)$ | Domain of discontinuity |
|$M_\Gamma$ | Hyperbolic quotient $\Gamma \backslash \mathbb{H}^3$ |
|$\mathbb{Q}_p$ | p-adic numbers |
|$\mathbb{C}_p$ | Complete algebraic closure of $\mathbb{Q}_p$ |
|$\mathbf{P}^1_{\mathrm{Berk}}$ | Berkovich projective line |
|$J(\phi)$ | Julia set of $\phi$ |
|$F(\phi)$ | Fatou set of $\phi$ |

### Measures and Dimensions

| Symbol | Meaning |
|--------|---------|
|$\dim_H$ | Hausdorff dimension |
|$\mathcal{H}_s$ | $s$-dimensional Hausdorff measure |
|$\mu_{PS}$ | Patterson-Sullivan measure |
|$\mu_\phi$ | Canonical measure for $\phi$ |
|$\mu_\varphi$ | Gibbs measure for potential $\varphi$ |
|$h_\mu$ | Measure-theoretic entropy |
|$P(\varphi)$ | Topological pressure |

### Spectral Theory

| Symbol | Meaning |
|--------|---------|
|$\Delta_\Gamma$ | Hyperbolic Laplacian on $M_\Gamma$ |
|$\Theta_\Gamma(t)$ | Heat kernel trace |
|$N_\Gamma(\lambda)$ | Eigenvalue counting function |
|$R_\Gamma(s)$ | Resolvent operator |
|$\delta$ | Critical exponent / Hausdorff dimension |

### Dynamics

| Symbol | Meaning |
|--------|---------|
|$S_n\varphi$ | Birkhoff sum $\sum_{k=0}^{n-1} \varphi \circ T^k$ |
|$\mathcal{L}_\varphi$ | RPF transfer operator |
|$\chi_\mu$ | Lyapunov exponent |
|$s^*$ | Dimension via pressure equation |
|$\Sigma_A$ | Subshift of finite type |

### Constants

| Symbol | Meaning |
|--------|---------|
|$\delta$ | Hausdorff dimension of limit/Julia set |
|$d$ | Degree of rational map |
|$p$ | Prime number |
|$\lambda$ | Leading eigenvalue of transfer operator |

---

## References for Section 2

[Bea83] A. Beardon, *The Geometry of Discrete Groups*, Springer (1983).

[Ben01] R. L. Benedetto, *Hyperbolic maps in p-adic dynamics*, Ergodic Theory Dynam. Systems 21 (2001), 1–11.

[Ber90] V. Berkovich, *Spectral Theory and Analytic Geometry over Non-Archimedean Fields*, AMS (1990).

[Bow75] R. Bowen, *Equilibrium States and the Ergodic Theory of Anosov Diffeomorphisms*, Springer (1975).

[Bow79] R. Bowen, *Hausdorff dimension of quasicircles*, Publ. Math. IHÉS 50 (1979), 11–25.

[BR10] M. Baker and R. Rumely, *Potential Theory and Dynamics on the Berkovich Projective Line*, AMS (2010).

[Gou97] F. Gouvêa, *p-adic Numbers: An Introduction*, Springer (1997).

[Kel98] G. Keller, *Equilibrium States in Ergodic Theory*, Cambridge Univ. Press (1998).

[LP82] P. Lax and R. Phillips, *The asymptotic distribution of lattice points in Euclidean and non-Euclidean spaces*, J. Funct. Anal. 46 (1982), 280–350.

[Mar07] A. Marden, *Outer Circles: An Introduction to Hyperbolic 3-Manifolds*, Cambridge Univ. Press (2007).

[MM87] R. Mazzeo and R. Melrose, *Meromorphic extension of the resolvent on complete spaces with asymptotically constant negative curvature*, J. Funct. Anal. 75 (1987), 260–310.

[MP87] D. Sullivan, *Related aspects of positivity in Riemannian geometry*, J. Diff. Geom. 25 (1987), 327–351.

[Pat76] S. J. Patterson, *The limit set of a Fuchsian group*, Acta Math. 136 (1976), 241–273.

[PP90] W. Parry and M. Pollicott, *Zeta Functions and the Periodic Orbit Structure of Hyperbolic Dynamics*, Astérisque 187-188 (1990).

[PP01] S. J. Patterson and P. Perry, *The divisor of Selberg's zeta function for Kleinian groups*, Duke Math. J. 106 (2001), 321–390.

[RL03] J. Rivera-Letelier, *Dynamique des fonctions rationnelles sur des corps locaux*, Astérisque 287 (2003), 147–230.

[Rob00] A. Robert, *A Course in p-adic Analysis*, Springer (2000).

[Rue82] D. Ruelle, *Repellers for real analytic maps*, Ergodic Theory Dynam. Systems 2 (1982), 99–107.

[Sul79] D. Sullivan, *The density at infinity of a discrete group of hyperbolic motions*, Publ. Math. IHÉS 50 (1979), 171–202.

[Wal82] P. Walters, *An Introduction to Ergodic Theory*, Springer (1982).

[You82] L.-S. Young, *Dimension, entropy and Lyapunov exponents*, Ergodic Theory Dynam. Systems 2 (1982), 109–124.

---

*Section 2 – Page count: approximately 11 pages*
