# T10 Phase 3: Higher Algebraic K-Theory

**Document**: T10 - Phase 3  
**Strictness**: L1-L2 (Stable ∞-categories)  
**Status**: In Progress

---

## 1. Introduction

Higher algebraic K-theory extends Quillen's K-theory to stable ∞-categories, providing universal additive invariants. This connects T4 (Grothendieck groups) to the highest categorical structures.

---

## 2. Stable ∞-Categories

### 2.1 Definition

**Definition 2.1**: A **stable ∞-category** $\mathcal{C}$:
1. Finitely complete and cocomplete
2. Zero object
3. Fiber and cofiber sequences coincide

**Examples**:
- $D^b(X)$: Bounded derived category
- $\text{Perf}(X)$: Perfect complexes
- $\text{Sp}$: Spectra

### 2.2 Triangulated Structure

**Theorem 2.2**: The homotopy category $h\mathcal{C}$ of stable ∞-category is triangulated.

**Distinguished triangles**: From fiber sequences.

### 2.3 F4T Stable ∞-Category

**Definition 2.3**: The **F4T stable ∞-category**:
$$\text{Perf}_{\text{F4T}} := \text{Ind}(\{\text{perfect complexes on dimension systems}\})$$

**Compact objects**: $\text{Perf}_{\text{F4T}}^\omega$ (T4 Grothendieck groups are $K_0$).

---

## 3. Higher K-Theory of Stable ∞-Categories

### 3.1 Blumberg-Gepner-Tabuada Definition

**Definition 3.1**: For stable ∞-category $\mathcal{C}$:
$$K(\mathcal{C}) := \text{corepresented by } \mathbb{S}[\mathcal{C}]$$

in the ∞-category of additive invariants.

**Alternative**: Waldhausen S-construction generalized.

### 3.2 Universal Property

**Theorem 3.2** (BGT): $K$-theory is the **universal localizing invariant**:
$$K: \text{Cat}_\infty^{ex} \to \text{Sp}$$

such that:
- Sends exact sequences to fiber sequences
- Preserves filtered colimits

### 3.3 Comparison with Classical

**Theorem 3.3**: For exact category $\mathcal{E}$:
$$K(Ch^b(\mathcal{E})) \simeq K^Q(\mathcal{E})$$

(Quillen's K-theory)

---

## 4. Noncommutative Motives

### 4.1 Definition (Tabuada)

**Definition 4.1**: The **category of noncommutative motives**:
$$\text{NCMot} := \text{Cat}_\infty^{ex}[W^{-1}]$$

localization at Morita equivalences.

**Universal property**: Universal additive invariant of dg-categories.

### 4.2 Motivic vs Noncommutative

**Theorem 4.2** (Cisinski-Tabuada): There is a fully faithful functor:
$$\mathcal{DM}(k) \hookrightarrow \text{NCMot}_k$$

**Conjecture 4.3**: All noncommutative motives are geometric (from dg-algebras).

### 4.3 F4T Noncommutative Motives

**Definition 4.4**: The **F4T noncommutative motive**:
$$\mathcal{U}_{\text{dg}}(\text{Perf}_{\text{F4T}}) \in \text{NCMot}$$

**Theorem 4.5**: This motive captures all K-theoretic information of F4T.

---

## 5. Additivity and Localization

### 5.1 Additivity Theorem

**Theorem 5.1**: For exact sequence of stable ∞-categories:
$$0 \to \mathcal{A} \to \mathcal{B} \to \mathcal{C} \to 0$$

we have fiber sequence:
$$K(\mathcal{A}) \to K(\mathcal{B}) \to K(\mathcal{C})$$

### 5.2 Localization

**Theorem 5.2**: For open immersion $j: U \to X$ with complement $i: Z \to X$:
$$K(Z) \xrightarrow{i_*} K(X) \xrightarrow{j^*} K(U)$$

is a fiber sequence.

### 5.3 F4T Localization

**Application**: For dimension system with "substructure":
$$K(\mathcal{D}_{sub}) \to K(\mathcal{D}) \to K(\mathcal{D}/\mathcal{D}_{sub})$$

---

## 6. Cyclotomic Trace

### 6.1 Definition

**Definition 6.1**: The **cyclotomic trace**:
$$\text{tr}: K(R) \to TC(R)$$

from K-theory to topological cyclic homology.

**Theorem 6.2** (Dundas-Goodwillie-McCarthy): The trace is an equivalence "locally" (relative K-theory).

### 6.2 Assemblies

**Assembly map**:
$$\alpha: H_*(BG; \mathbb{K}(R)) \to K_*(R[G])$$

**Novikov conjecture**: Related to injectivity of assembly.

### 6.3 F4T Cyclotomic Trace

**Construction**: For E_∞-ring spectrum $R$ and F4T:
$$K(R[\mathcal{G}_D^{(r)}]) \to TC(R[\mathcal{G}_D^{(r)}])$$

**Information**: TC captures "higher'' Grothendieck invariants.

---

## 7. K-Theory of F4T Categories

### 7.1 K-Groups

**Definition 7.1**: **Higher K-groups**:
$$K_n(\mathcal{C}) := \pi_n(K(\mathcal{C}))$$

**Low degrees**:
- $K_0$: Grothendieck group (T4)
- $K_1$: Automorphisms
- $K_2$: Relations (Steinberg symbols)

### 7.2 Computations

**Theorem 7.2**: For T1 Cantor set:
$$K_0(C_{N,r}) = \mathbb{Z}$$
$$K_1(C_{N,r}) = \mathcal{O}^\times$$
$$K_n(C_{N,r}) = 0, \quad n \geq 2$$

**T4**: Matches Grothendieck group computation.

### 7.3 Chern Character

**Definition 7.3**: The **Chern character**:
$$\text{ch}: K(\mathcal{C}) \to HN(\mathcal{C})$$

to negative cyclic homology.

**Riemann-Roch**: Compatibility with pushforwards.

---

## 8. Regulators and Periods

### 8.1 Borel Regulator

**Theorem 8.1** (Borel): For number field $F$:
$$K_{2n-1}(\mathcal{O}_F) \otimes \mathbb{R} \cong \mathbb{R}^{r_1 + r_2}$$

**Regulator map**:
$$\text{reg}: K_{2n-1}(\mathcal{O}_F) \to \mathbb{R}^{d_n}$$

### 8.2 Beilinson Regulator

**Theorem 8.2**: Regulator from motivic cohomology to Deligne cohomology.

**Connection to T8**: Periods appear as regulator values.

### 8.3 F4T Regulator

**Conjecture 8.3**: Regulator for dimension systems:
$$\text{reg}_{\text{F4T}}: K_{n}(\mathcal{D}) \to \text{periods}$$

---

## 9. Next Phase Preview

Phase 4 will explore:
1. **Higher categories of motives**
2. **DG-enhancements**
3. **A_∞-categories**

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 3 Complete - Higher Algebraic K-Theory
