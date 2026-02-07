# T9 Phase 1: Derived Algebraic Geometry (DAG)

**Document**: T9 - Phase 1  
**Strictness**: L1-L2 (Simplicial/homotopical methods)  
**Status**: In Progress

---

## 1. Introduction

Derived Algebraic Geometry (DAG) extends classical algebraic geometry by replacing commutative rings with simplicial commutative rings or E_∞-ring spectra. This allows for richer geometric structures and better behaved moduli spaces.

---

## 2. Simplicial Commutative Rings

### 2.1 Definition

**Definition 2.1**: A **simplicial commutative ring** $A_\bullet$ is a simplicial object in the category of commutative rings:
$$A: \Delta^{op} \to \text{CRing}$$

Equivalently, a functor from the simplex category to commutative rings.

### 2.2 Homotopy Groups

For simplicial ring $A_\bullet$:
$$\pi_n(A) := \pi_n(|A_\bullet|, 0)$$

**Theorem 2.2**: The homotopy groups $\pi_*(A)$ form a graded commutative ring:
- $\pi_0(A)$ is a commutative ring
- $\pi_n(A)$ is a $\pi_0(A)$-module
- Dold-Kan correspondence with dg-rings

### 2.3 Cotangent Complex

**Definition 2.3**: For morphism $A \to B$ of simplicial rings, the **cotangent complex**:
$$\mathbb{L}_{B/A} \in \text{Mod}_B$$

is the derived module of Kähler differentials.

**Properties**:
- $\pi_0(\mathbb{L}_{B/A}) = \Omega_{B/A}$
- $H_1(\mathbb{L}_{B/A}) = \text{Tor}_1^{A}(B, B)$
- Controls deformations (André-Quillen cohomology)

### 2.4 F4T Simplicial Rings

**Construction 3.1**: For T4 Grothendieck group $\mathcal{G}_D^{(r)}$:
$$A_\bullet = \mathbb{Z}[\mathcal{G}_D^{(r)}] \otimes^\mathbb{L} \mathbb{Z}$$

(simplicial group ring)

**Theorem 3.2**: The cotangent complex:
$$\mathbb{L}_{A/\mathbb{Z}} \simeq \mathcal{G}_D^{(r)}[1]$$

(shifted by 1, connecting to T7 homotopy)

---

## 3. Derived Affine Schemes

### 3.1 Definition

**Definition 3.1**: The **category of derived affine schemes**:
$$\text{dAff} := \text{sCRing}^{op}$$

(opposite of simplicial commutative rings)

**Notation**: $\text{Spec}^{der}(A) \in \text{dAff}$

### 3.2 Functor of Points

**Definition 3.2**: A **derived stack** is a functor:
$$F: \text{dAff}^{op} \to \text{sSet}$$

satisfying étale descent.

**Derived affine scheme as stack**:
$$h_{\text{Spec}(A)}(B) = \text{Map}_{\text{sCRing}}(A, B)$$

(mapping space in simplicial rings)

### 3.3 Classical Truncation

**Definition 3.3**: The **truncation**:
$$t_0: \text{dAff} \to \text{Aff}$$
$$\text{Spec}^{der}(A) \mapsto \text{Spec}(\pi_0(A))$$

**Fiber**: Derived structure lives in higher homotopy groups.

---

## 4. Derived Stacks

### 4.1 Definition

**Definition 4.1**: A **derived stack** $X$ is a sheaf of spaces on dAff for the étale topology.

**Derived Artin stack**: Has smooth atlas by derived affine schemes.

### 4.2 Quasi-Coherent Sheaves

**Definition 4.2**: For derived stack $X$, the category:
$$\text{QCoh}(X) := \lim_{\text{Spec}(A) \to X} \text{Mod}_A$$

(limit over derived affine charts)

**Properties**:
- Stable ∞-category
- Symmetric monoidal (tensor product)
- t-structure with heart classical QCoh

### 4.3 Perfect Complexes

**Definition 4.3**: **Perfect complexes**:
$$\text{Perf}(X) \subset \text{QCoh}(X)$$

compact objects, locally equivalent to bounded complexes of finite projectives.

**Theorem 4.4**: For $X$ quasi-compact derived scheme:
$$\text{Perf}(X) = \text{QCoh}(X)^\omega$$

(compact = perfect)

---

## 5. Derived Moduli of Dimension Systems

### 5.1 Moduli Functor

**Definition 5.1**: The **derived moduli of dimension systems**:
$$\mathcal{M}_{\text{F4T}}^{der}: \text{dAff}^{op} \to \text{sSet}$$
$$\text{Spec}(A) \mapsto \{\text{Dimension systems over } A\}$$

### 5.2 Derived Artin Stack Structure

**Theorem 5.2**: $\mathcal{M}_{\text{F4T}}^{der}$ is a **derived Artin stack** locally of finite presentation.

**Atlas**: Cover by derived affine schemes corresponding to T1-T4 presentations.

### 5.3 Cotangent Complex of Moduli

**Theorem 5.3**: For dimension system $\mathcal{D} \in \mathcal{M}_{\text{F4T}}$:
$$\mathbb{L}_{\mathcal{M}, \mathcal{D}} \simeq \mathbb{T}_{\mathcal{D}}^*[1]$$

(cotangent = shifted dual of tangent complex from T7)

### 5.4 Virtual Dimension

**Definition 5.4**: The **virtual dimension**:
$$\text{vdim}(\mathcal{M}) = \text{rank}(\mathbb{L}_{\mathcal{M}}^{\bullet})$$

alternating sum of ranks of cotangent complex.

**Calculation**: For F4T:
$$\text{vdim} = \sum_i (-1)^i \dim \pi_i(\mathcal{M})$$

---

## 6. Intersection Theory on Derived Stacks

### 6.1 Virtual Fundamental Class

**Theorem 6.1** (Behrend-Fantechi): For derived DM stack $X$ with obstruction theory:
$$[X]^{vir} \in A_{vdim}(X)$$

**Construction**: From derived intrinsic normal cone.

### 6.2 Gromov-Witten Style Invariants

For F4T:
$$\langle \tau_{d_1}(\gamma_1) \cdots \tau_{d_n}(\gamma_n) \rangle_g = \int_{[\mathcal{M}_{g,n}]^{vir}} \prod_i \psi_i^{d_i} \cup \text{ev}_i^*(\gamma_i)$$

**Interpretation**: "Correlation functions" of dimension systems.

---

## 7. Deformation Theory Revisited

### 7.1 Derived Deformations

For classical moduli problem with obstruction:

**Classical**: Deformations controlled by $H^1$, obstructions by $H^2$.

**Derived**: All information encoded in tangent complex:
$$\mathbb{T}_X = \mathbb{L}_X^\vee$$

### 7.2 T2 PDE as Derived Deformation

The T2 PDE:
$$\frac{\partial d}{\partial t} = \mathcal{F}(d, t)$$

**Derived interpretation**: Flow on derived moduli space.

**Theorem 7.1**: Solutions are paths in $\mathcal{M}_{\text{F4T}}^{der}$.

### 7.3 Derived Critical Loci

For function $f: \mathcal{M} \to \mathbb{A}^1$:

**Derived critical locus**:
$$\text{Crit}^{der}(f) = \text{fiber product}(\mathcal{M} \xrightarrow{0} T^*\mathcal{M} \xleftarrow{df} \mathcal{M})$$

**F4T Application**: Variational principles for dimension evolution.

---

## 8. Comparison with Classical

| Aspect | Classical AG | Derived AG |
|--------|-------------|-----------|
| Rings | Commutative | Simplicial commutative |
| Schemes | Ordinary | Derived (higher homotopy) |
| Moduli | May be singular | Smooth derived structure |
| Deformations | $H^1/H^2$ obstruction | Tangent complex |
| Intersections | Transversality needed | Always defined |

---

## 9. Next Phase Preview

Phase 2 will explore:
1. **Spectral algebraic geometry** (E_∞-rings)
2. **Spectral schemes**
3. **Connection to stable homotopy theory**

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 1 Complete - DAG Foundations
