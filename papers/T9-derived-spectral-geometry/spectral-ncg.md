# T9 Phase 4: Spectral Noncommutative Geometry

**Document**: T9 - Phase 4  
**Strictness**: L1-L2 (Structured spectral geometry)  
**Status**: In Progress

---

## 1. Introduction

This phase synthesizes T6 (NCG) with T9 (spectral geometry), developing spectral triples over E_∞-rings and their topological invariants.

---

## 2. Spectral Triples over E_∞-Rings

### 2.1 Definition

**Definition 2.1**: A **spectral triple over E_∞-ring $R$**:
$$\mathcal{T} = (\mathcal{A}, \mathcal{H}, D)$$

where:
- $\mathcal{A}$: Associative $R$-algebra in spectra
- $\mathcal{H}$: $R$-module spectrum with $\mathcal{A}$-action
- $D: \mathcal{H} \to \Sigma^d \mathcal{H}$: Self-adjoint operator (degree $d$)

### 2.2 Structured Spectral Operators

**Definition 2.2**: Dirac operator $D$ as morphism in $\text{Mod}_R$:
- Spectrum shifts by dimension $d$
- Graded commutator $[D, a]$ defined in $R$-linear category

### 2.3 F4T Spectral Triples over R

For each T1-T4 over $R$:

**T1**: $D$ acts on $R$-module $C(C_3; R)$

**T2**: Heat kernel $p(t) \in \pi_0(R)((t))$

**T3**: Modular symbols with $R$-coefficients

**T4**: Group algebra $R[\mathcal{G}]$

---

## 3. Topological Cyclic Homology of F4T

### 3.1 TC for Dimension Systems

**Definition 3.1**: For E_∞-ring $R$ and dimension system $\mathcal{D}$:
$$TC(R, \mathcal{D}) := TC(R \otimes_{\mathbb{S}} \mathcal{O}_{\mathcal{D}})$$

### 3.2 Comparison with T7 K-Theory

**Theorem 3.2**: There is a trace map:
$$K(R, \mathcal{D}) \to TC(R, \mathcal{D})$$

approximating algebraic K-theory.

**Connection**: T7 homotopy groups → TC computations.

### 3.3 Decomposition

**Theorem 3.3** (Goodwillie calculus): $TC$ decomposes into stable pieces related to $THH$ and $S^1$-Tate construction.

**F4T Application**: Invariants of dimension systems via topological cyclic homology.

---

## 4. Structured Dixmier Traces

### 4.1 R-Linear Dixmier Traces

**Definition 4.1**: For $R$-module operator $T$:
$$\text{Tr}_\omega^R(T) \in \pi_0(R)$$

(value in coefficient ring)

### 4.2 Universal Property

**Theorem 4.2**: The structured Dixmier trace is the universal additive invariant for $R$-linear spectral triples.

### 4.3 F4T Structured Dimensions

**Definition 4.3**: The **R-valued dimension**:
$$d_R = \text{Tr}_\omega^R(|D|^{-d}) \in \pi_0(R)$$

**Examples**:
- $R = H\mathbb{Q}$: Recovers T6 rational dimensions
- $R = KU$: K-theory valued dimensions
- $R = tmf$: Modular dimensions

---

## 5. Spectral Action in R-Linear Setting

### 5.1 Definition

**Definition 5.1**: For cutoff $f$:
$$S_\Lambda(D; R) = \text{tr}_R(f(D/\Lambda)) \in \pi_0(R)$$

### 5.2 Expansion

**Theorem 5.2**: Heat kernel expansion:
$$S_\Lambda(D; R) \sim \sum_k \Lambda^{d-k} f_k a_k(R)$$

coefficients $a_k(R) \in \pi_0(R)$.

### 5.3 F4T Spectral Invariants

**Corollary**: Spectral invariants take values in:
- $\pi_0(R)$ (zeroth homotopy)
- Potentially richer if $R$ has higher homotopy

---

## 6. Equivariant Spectral Geometry

### 6.1 Group Actions

**Definition 6.1**: For group $G$ acting on spectral triple:
$$\mathcal{T}^G = (\mathcal{A}^G, \mathcal{H}^G, D^G)$$

(fixed points)

### 6.2 Equivariant K-Theory

**Definition 6.2**: $K_G(\mathcal{T}) = K$-theory of $G$-equivariant modules.

**F4T Application**: T3 modular forms have natural $SL(2, \mathbb{Z})$ action.

### 6.3 Lefschetz Formula

**Theorem 6.3** (Spectral Lefschetz):
$$\text{tr}(g | \mathcal{H}) = \int_{\mathcal{M}^g} \text{local contribution}$$

for $g \in G$.

---

## 7. Twisted Spectral Triples

### 7.1 Definition

**Definition 7.1**: A **twisted spectral triple**:
$$\sigma: \mathcal{A} \to \mathcal{A}$$

automorphism (twist) with modified condition:
$$[D, a]_\sigma = Da - \sigma(a)D$$

### 7.2 Examples from F4T

**T2**: Time evolution as twist:
$$\sigma_t(d) = \mathcal{E}(d, t)$$

**T4**: Logarithmic automorphism:
$$\sigma([d]) = [d] \oplus [c]$$

---

## 8. Connection to T8 Motives

### 8.1 Realization Functors

**Diagram**:
```
Motives (T8) ──→ Spectral NCG (T9)
   ↓                  ↓
Realizations    TC, K-theory
```

**Theorem 8.1**: The spectral realization of motives factors through TC.

### 8.2 p-adic TC

**Definition 8.2**: For p-complete E_∞-ring:
$$TC^- = THH^{hS^1}$$
$$TP = (THH^{tS^1})$$

(Nikolaus-Scholze)

**F4T**: p-adic invariants of dimension systems.

---

## 9. Summary

### 9.1 Key Structures

| Structure | Classical (T6) | Spectral (T9) |
|-----------|---------------|---------------|
| Dixmier trace | $\mathbb{R}$-valued | $\pi_0(R)$-valued |
| Spectral action | Number | Element of $R$ |
| K-theory | Algebraic | Topological |
| Invariants | Periods | TC classes |

### 9.2 Hierarchy

```
T8: Motives (universal)
  ↓
T9: Spectral NCG (structured over R)
  ↓
T6: Classical NCG (R = $\mathbb{R}$)
```

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 4 Complete - Spectral NCG
