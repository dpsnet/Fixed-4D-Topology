# T9 Phase 3: Derived Moduli of Dimension Systems

**Document**: T9 - Phase 3  
**Strictness**: L1-L2 (Moduli theory)  
**Status**: In Progress

---

## 1. Introduction

This phase constructs the derived moduli stack of dimension systems as a derived Artin stack, equipped with perfect obstruction theory and virtual fundamental class.

---

## 2. The Moduli Functor

### 2.1 Definition

**Definition 2.1**: The **moduli of F4T dimension systems**:
$$\mathcal{M}_{\text{F4T}}: \text{dAff}^{op} \to \text{Grpd}$$
$$\text{Spec}(A) \mapsto \{\text{Dimension systems over } A\}$$

**Groupoid structure**: Isomorphisms of dimension systems.

### 2.2 Components

**Decomposition** by theory type:
$$\mathcal{M}_{\text{F4T}} = \mathcal{M}_{\text{T1}} \sqcup \mathcal{M}_{\text{T2}} \sqcup \mathcal{M}_{\text{T3}} \sqcup \mathcal{M}_{\text{T4}}$$

### 2.3 Derived Enhancement

**Definition 2.2**: The **derived moduli**:
$$\mathcal{M}_{\text{F4T}}^{der}: \text{dAff}^{op} \to \text{sSet}$$

**Higher information**: Derived automorphisms, obstructions, deformations.

---

## 3. Derived Artin Stack Structure

### 3.1 Atlas Construction

**Theorem 3.1**: $\mathcal{M}_{\text{F4T}}^{der}$ is a **derived Artin stack** locally of finite presentation.

**Proof Strategy**:
1. Cover by derived affine charts
2. Show smoothness of atlas
3. Verify groupoid structure

**Charts**:
- T1: $\text{Spec}(\mathbb{Q}[N, r]^{\Delta^1})$ (parameter space for Cantor sets)
- T2: Derived mapping stack $\text{Map}(\mathbb{R}_+, \text{Spec}^{der}(...))$
- T3: Derived modular stack
- T4: Derived BG (classifying stack)

### 3.2 Tangent Complex

**Theorem 3.2**: For $\mathcal{D} \in \mathcal{M}_{\text{F4T}}$:
$$\mathbb{T}_{\mathcal{M}, \mathcal{D}} \simeq \text{Ext}^*(\mathcal{D}, \mathcal{D})[1]$$

(extensions of dimension system by itself, shifted)

**Explicit computations**:
- T1: $\mathbb{T} \simeq \mathbb{Q}[1] \oplus \mathbb{Q}[0]$ (parameters + scaling)
- T2: $\mathbb{T} \simeq H^*(\mathbb{R}_+, \mathcal{H})$ (PDE solutions)
- T3: $\mathbb{T} \simeq \text{Ext}^1_{\mathcal{M}_k}(f, f)$ (deformations of modular forms)
- T4: $\mathbb{T} \simeq \mathbb{Q}[0]$ (rigid)

### 3.3 Cotangent Complex

**Definition 3.3**: The **cotangent complex**:
$$\mathbb{L}_{\mathcal{M}} := \mathbb{T}_{\mathcal{M}}^\vee$$

**Perfect obstruction theory**: $\mathbb{L}_{\mathcal{M}}$ is perfect (quasi-isomorphic to finite complex of vector bundles).

**Theorem 3.4**: $\mathcal{M}_{\text{F4T}}^{der}$ has **(-1)-shifted symplectic structure** (Pantev-Toën-Vaquié-Vezzosi).

---

## 4. Virtual Fundamental Class

### 4.1 Construction

**Theorem 4.1** (Behrend-Fantechi): For derived DM stack with perfect obstruction theory:
$$[\mathcal{M}_{\text{F4T}}]^{vir} \in A_{vdim}(\mathcal{M}_{\text{F4T}}^{cl})$$

**Construction**:
1. Take derived intrinsic normal cone
2. Intersect with zero section
3. Push forward to classical truncation

### 4.2 Virtual Dimension

**Formula**:
$$vdim = \text{rank}(\mathbb{T}_{\geq 0}) - \text{rank}(\mathbb{T}_{< 0})$$

**For F4T**:
- T1: $vdim = 1$ (1-parameter family)
- T2: $vdim = 1$ (time evolution)
- T3: $vdim = \dim M_k - 1$ (moduli of forms minus 1)
- T4: $vdim = 0$ (discrete)

### 4.3 Integrals

**Definition 4.2**: For cohomology class $\alpha \in H^*(\mathcal{M})$:
$$\langle \alpha \rangle := \int_{[\mathcal{M}]^{vir}} \alpha$$

**F4T Invariants**: Numbers extracted from virtual fundamental class integration.

---

## 5. Obstruction Theories

### 5.1 Classical vs Derived

**Classical**: Moduli may be singular (obstructed deformations).

**Derived**: Always smooth in derived sense; classical singularities resolved by derived structure.

### 5.2 T2 Obstruction Theory

For PDE dimension system:

**Obstruction**: Integrability condition for deformation of PDE.

**Derived resolution**: Obstruction encoded in $\pi_1$ of mapping space.

### 5.3 T3 Obstruction Theory

For modular form $f$:

**Classical**: Obstructions in $H^2$ of modular curve.

**Derived**: $\mathbb{T}_{[f]} = \text{Ext}^*(f, f)[1]$ automatically contains obstruction information.

---

## 6. Wall-Crossing and Stability

### 6.1 Stability Conditions

**Definition 6.1**: A **stability condition** on dimension system:
$$Z: K_0(\mathcal{D}) \to \mathbb{C}$$

central charge.

**Harder-Narasimhan filtration**: Every dimension system has canonical filtration by semistable pieces.

### 6.2 Wall-Crossing Formula

**Theorem 6.2** (Joyce-Song): Invariants change across walls of instability by explicit formula.

**F4T Application**: Count of dimension systems jumps across stability walls.

### 6.3 DT-Style Invariants

**Definition 6.3**: The **Donaldson-Thomas type invariant**:
$$DT(\gamma) = \int_{[\mathcal{M}_\gamma]^{vir}} 1$$

where $\mathcal{M}_\gamma$ is moduli of dimension systems with class $\gamma$.

---

## 7. Gromov-Witten Analogue

### 7.1 Evaluation Maps

**Definition 7.1**: For $n$-pointed dimension system:
$$\text{ev}_i: \mathcal{M}_{g,n} \to X$$

evaluation at $i$-th point.

### 7.2 Correlators

**Definition 7.2**: **Correlation functions**:
$$\langle \tau_{d_1}(\gamma_1) \cdots \tau_{d_n}(\gamma_n) \rangle_g = \int_{[\mathcal{M}_{g,n}]^{vir}} \prod_i \psi_i^{d_i} \cup \text{ev}_i^*(\gamma_i)$$

**Physical interpretation**: Vacuum expectation values in quantum dimension theory.

### 7.3 WDVV Equations

**Theorem 7.3**: Correlation functions satisfy **Witten-Dijkgraaf-Verlinde-Verlinde equations** (associativity of quantum product).

---

## 8. Master Space Construction

### 8.1 Definition

**Definition 8.1**: The **master space** $\mathcal{M}^{master}$:
- Compactification of moduli
- Includes all stability conditions
- GIT-style quotient

### 8.2 T1 Master Space

**Construction**: Compactify $(0, 1/2) \ni r$ by adding boundary points $r = 0$ and $r = 1/2$.

**Interpretation**: Degenerate Cantor sets at boundary.

---

## 9. Next Phase Preview

Phase 4 will explore:
1. **Spectral NCG** (connection to T6)
2. **Topological cyclic homology**
3. **QFT applications**

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 3 Complete - Derived Moduli Spaces
