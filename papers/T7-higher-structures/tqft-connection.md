# T7 Phase 4: Topological Quantum Field Theory Connection

**Document**: T7 - Phase 4  
**Strictness**: L2-L3 (Mathematical physics)  
**Status**: In Progress

---

## 1. Introduction

This document explores the connection between F4T and Topological Quantum Field Theory (TQFT), showing how dimension systems can be organized into a fully extended TQFT via the cobordism hypothesis.

---

## 2. Cobordism Categories

### 2.1 Definition

**Definition 2.1**: The **bordism category** $\text{Bord}_n$ has:
- **Objects**: Closed $(n-1)$-manifolds
- **Morphisms**: $n$-dimensional bordisms
- **Composition**: Gluing along boundaries

### 2.2 Framed vs Oriented

Variants:
- $\text{Bord}_n^{\text{fr}}$: Framed bordisms
- $\text{Bord}_n^{\text{or}}$: Oriented bordisms
- $\text{Bord}_n^{\text{spin}}$: Spin bordisms

### 2.3 F4T Bordism Category

**Definition 2.2**: $\text{Bord}_n^{\text{F4T}}$ has:
- **Objects**: Dimension systems on $(n-1)$-manifolds
- **Morphisms**: Dimension systems on $n$-manifolds with boundary

**Structure**: Symmetric monoidal (∞,n)-category.

---

## 3. TQFT Axioms

### 3.1 Atiyah-Segal Axioms

**Definition 3.1**: An **n-dimensional TQFT** is a symmetric monoidal functor:
$$Z: \text{Bord}_n \to \text{Vect}$$

**Properties**:
1. $Z(\emptyset) = k$ (ground field)
2. $Z(M_1 \sqcup M_2) = Z(M_1) \otimes Z(M_2)$
3. $Z(\partial W) = \langle Z(W), Z(W)\rangle$ (gluing)

### 3.2 Extended TQFT

**Definition 3.2**: A **fully extended n-TQFT**:
$$Z: \text{Bord}_n \to \mathcal{C}$$

to an (∞,n)-category $\mathcal{C}$.

Assigns:
- Points → objects of $\mathcal{C}$
- 1-manifolds → 1-morphisms
- ...
- n-manifolds → n-morphisms (numbers)

### 3.3 Cobordism Hypothesis

**Theorem 3.3** (Lurie): A fully extended TQFT is determined by its value on a point:
$$Z(*) = x \in \mathcal{C}$$

where $x$ is **fully dualizable**.

**Classification**:
$$\text{TQFT}_n(\mathcal{C}) \cong (\mathcal{C}^{\text{fd}})^{\sim}$$

---

## 4. F4T as TQFT

### 4.1 The Functor

**Definition 4.1**: The **F4T TQFT**:
$$Z_{\text{F4T}}: \text{Bord}_n^{\text{F4T}} \to \mathbf{F4T}_\infty$$

**On objects**: 
$$Z_{\text{F4T}}(M^{n-1}) = \{\text{dimension systems on } M\}$$

### 4.2 Point Value

**Theorem 4.2**: The value on a point:
$$Z_{\text{F4T}}(*) = \mathbf{F4T}_\infty$$

is the (∞,2)-category of dimension systems.

**Fully Dualizable?**: Requires verification of dualizability conditions.

### 4.3 Circle Value

**Theorem 4.3**: For $S^1$:
$$Z_{\text{F4T}}(S^1) = \{\text{cyclically invariant dimension systems}\}$$

**Dimension**: $\text{Tr}(\text{id})$ in categorical trace.

### 4.4 Partition Functions

For closed n-manifold $M$:
$$Z_{\text{F4T}}(M) = \text{partition function on } M$$

**Example**: $n=2$, genus $g$ surface:
$$Z_{\text{F4T}}(\Sigma_g) = \sum_{\mathcal{D}} \frac{1}{|\text{Aut}(\mathcal{D})|}$$

(sum over isomorphism classes of dimension systems).

---

## 5. State Spaces

### 5.1 Hilbert Spaces from Categories

**Definition 5.1**: For object $X \in \mathbf{F4T}_\infty$:
$$\mathcal{H}_X := \text{End}(X)$$

(internal endomorphisms)

### 5.2 T2: PDE State Space

For T2 dimension system on manifold $M$:
$$\mathcal{H}_M = L^2(\{\text{solutions to T2 PDE on } M\})$$

### 5.3 T4: Algebraic State Space

$$\mathcal{H}_{\mathcal{G}} = \ell^2(\mathcal{G}_D^{(r)})$$

### 5.4 Inner Product

**Definition**: For states $\psi_1, \psi_2 \in \mathcal{H}_M$:
$$\langle\psi_1, \psi_2\rangle = \text{Tr}(\psi_1^* \psi_2)$$

(Hermitian inner product)

---

## 6. Anomalies and Central Charges

### 6.1 Anomaly Theory

**Definition 6.1**: An **anomaly** is an obstruction to lifting TQFT to a higher category.

**F4T Anomaly**: Lives in:
$$\text{H}^{n+1}(\text{Bord}_n, \text{U}(1))$$

### 6.2 Central Charge

For 2D TQFT:
$$c = \text{central charge}$$

characterizes the conformal field theory.

**F4T Prediction**: From T2 spectral dimension:
$$c = 6 \cdot d_s$$

(modulo quantization conditions)

### 6.3 Gravitational Anomaly

**Definition**: Failure of functoriality under diffeomorphisms.

**F4T Case**: Anomaly controlled by spectral flow of Dirac operator.

---

## 7. Defects and Interfaces

### 7.1 Domain Walls

**Definition 7.1**: A **domain wall** (codimension-1 defect) between TQFTs $Z_1$ and $Z_2$:
$$Z_{12}: Z_1 \to Z_2$$

**F4T**: Domain wall between T1 and T2 dimension systems.

### 7.2 Wilson Lines

**Definition 7.2**: **Wilson line** along curve $\gamma$:
$$W_\gamma = \text{Tr}_\rho(\text{P}\exp \oint_\gamma A)$$

**F4T**: Spectral flow along path in moduli space.

### 7.3 Fusion of Defects

**Fusion**: For defects $Z_{12}$ and $Z_{23}$:
$$Z_{23} \circ Z_{12}: Z_1 \to Z_3$$

**Category of defects**: Monoidal category structure.

---

## 8. Relation to Other TQFTs

### 8.1 Turaev-Viro TQFT

| Aspect | Turaev-Viro | F4T |
|--------|-------------|-----|
| Input | Fusion category | Dimension systems |
| State space | Graph invariants | Spectral invariants |
| Partition function | State sum | Spectral trace |

### 8.2 Dijkgraaf-Witten TQFT

| Aspect | Dijkgraaf-Witten | F4T |
|--------|-----------------|-----|
| Gauge group | Finite $G$ | Automorphism group of $\mathcal{D}$ |
| Action | $H^n(BG, \text{U}(1))$ | Spectral action |

### 8.3 Chern-Simons Theory

| Aspect | Chern-Simons | F4T |
|--------|--------------|-----|
| Gauge group | Compact Lie group | Unitary group of spectral triple |
| Level $k$ | Integer | Related to Dixmier trace |

---

## 9. Next Phase Preview

Phase 5 will explore:
1. **E_n-algebra structures**
2. **Operadic composition**
3. **Factorization homology**

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 4 Complete - TQFT Connection Established
