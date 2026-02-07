# T9 Phase 2: Spectral Algebraic Geometry

**Document**: T9 - Phase 2  
**Strictness**: L1-L2 (E_∞-ring spectra)  
**Status**: In Progress

---

## 1. Introduction

Spectral Algebraic Geometry (SAG) extends derived algebraic geometry by using E_∞-ring spectra instead of simplicial commutative rings. This connects algebraic geometry to stable homotopy theory.

---

## 2. E_∞-Ring Spectra

### 2.1 Definition

**Definition 2.1**: An **E_∞-ring spectrum** $R$ is a commutative algebra object in the symmetric monoidal ∞-category of spectra:
$$R \in \text{CAlg}(\text{Sp})$$

**Structure**: 
- Underlying spectrum (homotopy groups $\pi_*R$)
- Multiplication $R \wedge R \to R$ (homotopy coherent commutative)
- Unit $\mathbb{S} \to R$

### 2.2 Examples

**Example 2.2**: **Sphere spectrum** $\mathbb{S}$:
- Initial object in $\text{CAlg}(\text{Sp})$
- $\pi_n(\mathbb{S}) = $ stable homotopy groups of spheres

**Example 2.3**: **Eilenberg-MacLane spectra** $HA$:
- For commutative ring $A$
- $\pi_0(HA) = A$, $\pi_{n \neq 0}(HA) = 0$
- Connective cover of ordinary rings

**Example 2.4**: **Complex K-theory** $KU$:
- $E_\infty$-ring from topological K-theory
- $\pi_*(KU) = \mathbb{Z}[u^{\pm 1}]$ ($|u| = -2$)
- Periodic version of K-theory

**Example 2.5**: **Topological modular forms** $tmf$:
- "$E_\infty$-ring of modular forms"
- $\pi_*(tmf)$ related to classical modular forms
- Connects to T3

### 2.3 Postnikov Towers

**Theorem 2.6**: Any E_∞-ring $R$ has Postnikov tower:
$$\cdots \to \tau_{\leq n}R \to \tau_{\leq n-1}R \to \cdots \to \tau_{\leq 0}R = H\pi_0(R)$$

**k-invariants**: In topological André-Quillen cohomology.

---

## 3. Spectral Schemes

### 3.1 Definition (Lurie)

**Definition 3.1**: A **spectral scheme** $(X, \mathcal{O}_X)$:
- $X$: Topological space
- $\mathcal{O}_X$: Sheaf of E_∞-rings on $X$
- Locally equivalent to $\text{Spec}^{spectral}(A)$ for E_∞-ring $A$

### 3.2 Spectral Affine Schemes

**Definition 3.2**: For E_∞-ring $A$:
$$\text{Spec}^{spectral}(A) := (\text{Spec}(\pi_0A), \mathcal{O})$$

where structure sheaf takes values in E_∞-rings.

### 3.3 Truncation

**Theorem 3.3**: Truncation functor:
$$t_0: \text{SpSch} \to \text{Sch}$$
$$(X, \mathcal{O}_X) \mapsto (X, \pi_0\mathcal{O}_X)$$

**Fiber**: Higher homotopy sheaves provide derived/spectral structure.

---

## 4. Quasi-Coherent Sheaves on Spectral Stacks

### 4.1 Definition

**Definition 4.1**: For spectral stack $X$:
$$\text{QCoh}(X) := \lim_{\text{Spec}(A) \to X} \text{Mod}_A$$

where $\text{Mod}_A$ is category of $A$-module spectra.

**Properties**:
- Stable ∞-category
- Symmetric monoidal under $\otimes$
- Compact objects = perfect complexes

### 4.2 T-Structure

**Theorem 4.2**: $\text{QCoh}(X)$ has t-structure:
- $\text{QCoh}(X)_{\geq 0}$: connective sheaves ($\pi_i = 0$ for $i < 0$)
- Heart = classical quasi-coherent sheaves on $t_0(X)$

### 4.3 Descent and Gluing

**Theorem 4.3** (Lurie): $\text{QCoh}$ satisfies flat descent on spectral stacks.

**Implication**: Can glue quasi-coherent sheaves from affine covers.

---

## 5. Spectral Deligne-Mumford Stacks

### 5.1 Definition

**Definition 5.1**: A **spectral DM stack** $X$:
- Étale sheaf of spaces
- Admits étale cover by affine spectral schemes
- Diagonal is representable and affine

### 5.2 Etale Fundamental Group

**Definition 5.2**: For spectral DM stack $X$:
$$\pi_1^{ét}(X) := \pi_1^{ét}(t_0(X))$$

(defined via truncation)

**Connection to T8**: Anabelian geometry applies to spectral stacks.

### 5.3 F4T Spectral Stack

**Theorem 5.3**: There exists a **spectral DM stack**:
$$\mathcal{M}_{\text{F4T}}^{spectral}$$

representing dimension systems over E_∞-rings.

**Structure**:
- $t_0(\mathcal{M}_{\text{F4T}}^{spectral}) = \mathcal{M}_{\text{F4T}}^{cl}$ (classical moduli)
- Higher homotopy encodes higher automorphisms (from T7)

---

## 6. Topological Cyclic Homology (TC)

### 6.1 Definition

**Definition 6.1**: For E_∞-ring $R$:
$$TC(R) := \text{holim}_{\substack{\longleftarrow \\ p}} THH(R)^{hS^1}$$

(topological cyclic homology)

**Components**:
- $THH$: Topological Hochschild homology
- $S^1$-action: Circle action on THH
- Fixed points: Takes $S^1$-invariants

### 6.2 Motivic Trace

**Theorem 6.2** (Dundas-Goodwillie-McCarthy): For $R \to S$:
$$\text{fiber}(K(R) \to K(S)) \simeq \text{fiber}(TC(R) \to TC(S))$$

**Significance**: TC approximates algebraic K-theory.

### 6.3 F4T Application

**Construction**: For T4 Grothendieck group:
$$TC(\mathbb{S}[\mathcal{G}_D^{(r)}])$$

computes "higher Grothendieck invariants."

---

## 7. Spectral Noncommutative Geometry

### 7.1 Spectral Triples over E_∞-Rings

**Definition 7.1**: A **spectral triple over $R$**:
- $\mathcal{A}$: $R$-algebra (associative)
- $\mathcal{H}$: $R$-module spectrum with $\mathcal{A}$-action
- $D$: Self-adjoint operator on $\mathcal{H}$

### 7.2 Structured Dirac Operator

**Definition 7.2**: Dirac operator $D$ as map of $R$-module spectra:
$$D: \mathcal{H} \to \Sigma^{d}\mathcal{H}$$

where $d$ is the dimension (in grading).

### 7.3 Spectral Action over E_∞-Rings

**Definition 7.3**: For cutoff function $f$:
$$S_\Lambda(D) = \text{tr}_R(f(D/\Lambda)) \in \pi_0(R)$$

(trace in $R$-module category)

---

## 8. Comparison: Derived vs Spectral

| Feature | Derived AG | Spectral AG |
|---------|-----------|-------------|
| Rings | Simplicial commutative | E_∞-rings |
| Base | $\mathbb{Z}$ | $\mathbb{S}$ (sphere) |
| Homotopy | Discrete | Connective spectra |
| K-theory | Algebraic | Topological |
| TC | Not defined | Canonical |

**Theorem 8.1**: Over $\mathbb{Q}$, derived and spectral AG coincide (rational homotopy theory).

---

## 9. Next Phase Preview

Phase 3 will explore:
1. **Derived moduli spaces** in detail
2. **Virtual fundamental classes**
3. **Obstruction theories**

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 2 Complete - Spectral Algebraic Geometry
