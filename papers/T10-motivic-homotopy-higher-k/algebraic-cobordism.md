# T10 Phase 2: Algebraic Cobordism

**Document**: T10 - Phase 2  
**Strictness**: L1-L2 (Oriented cohomology)  
**Status**: In Progress

---

## 1. Introduction

Algebraic cobordism, developed by Levine and Morel, is the universal oriented cohomology theory on algebraic varieties. It provides the algebro-geometric analogue of complex cobordism MU in topology.

---

## 2. Oriented Cohomology Theories

### 2.1 Definition

**Definition 2.1**: An **oriented cohomology theory** $A^*$ on $\text{Sm}_k$:
1. Contravariant functor $A^*: \text{Sm}_k^{op} \to \text{Graded Rings}$
2. Pushforwards for projective morphisms
3. Extended homotopy property
4. Projective bundle formula
5. **Orientation**: First Chern classes $c_1^A(L) \in A^1(X)$ for line bundles

### 2.2 Formal Group Law

**Theorem 2.2**: For any oriented theory $A^*$, there is a **formal group law**:
$$F_A(u, v) \in A^*(k)[[u, v]]$$

such that:
$$c_1^A(L_1 \otimes L_2) = F_A(c_1^A(L_1), c_1^A(L_2))$$

**Examples**:
- Chow theory: $F_{CH}(u, v) = u + v$ (additive)
- K-theory: $F_K(u, v) = u + v - uv$ (multiplicative)
- Complex cobordism: Universal FGL $F_{MU}$

### 2.3 Lazard Ring

**Theorem 2.3** (Lazard): The **universal formal group law** exists over:
$$\mathbb{L} = \mathbb{Z}[x_1, x_2, \ldots]$$

(infinite polynomial ring)

**Universal property**: Any FGL over ring $R$ comes from map $\mathbb{L} \to R$.

---

## 3. Algebraic Cobordism

### 3.1 Definition (Levine-Morel)

**Definition 3.1**: **Algebraic cobordism** $\Omega^*$ is the universal oriented cohomology theory:
$$\Omega^*(X) := \text{cobordism classes of projective morphisms } [Y \to X]$$

modulo relations:
- Dimension axiom
- Extended homotopy
- Projective bundle formula
- Double point degeneration

### 3.2 Universal Property

**Theorem 3.2** (Levine-Morel): For any oriented theory $A^*$:
$$\exists! \text{ morphism } \vartheta_A: \Omega^* \to A^*$$

preserving the oriented structure.

### 3.3 Comparison with Chow and K-Theory

**Theorem 3.3**:
- $\Omega^0(X) = CH^0(X) = \mathbb{Z}$ (connected components)
- $\Omega^1(X) = \text{Pic}(X)$ (line bundles)
- Rationally: $\Omega^*_\mathbb{Q}(X) \cong CH^*_\mathbb{Q}(X)[t_1, t_2, \ldots]$

---

## 4. MGL: Motivic Cobordism

### 4.1 Definition

**Definition 4.1**: The **motivic cobordism spectrum**:
$$MGL := \text{Thom spectrum of universal vector bundle}$$

Analogous to $MU$ in topology.

**Properties**:
- $MGL$ is an $E_\infty$-ring spectrum in $\mathcal{SH}(k)$
- $\Omega^*(X) = MGL^{2*,*}(X_+)$

### 4.2 Quillen's Theorem (Motivic)

**Theorem 4.2**: The formal group law of MGL is the **universal formal group law**:
$$F_{MGL} = F_{univ}: \mathbb{L} \to MGL^{-*}(k)$$

### 4.3 Slice of MGL

**Theorem 4.3** (Levine): The slice filtration of MGL:
$$s_n(MGL) \simeq \Sigma^{2n,n} H\mathbb{Z} \otimes MU_{2n}$$

where $MU_*$ are coefficients of complex cobordism.

---

## 5. F4T Algebraic Cobordism

### 5.1 Construction

**Definition 5.1**: **F4T algebraic cobordism**:
$$\Omega^*_{\text{F4T}}(\mathcal{D}) := \{\text{cobordism classes of maps to dimension system}\}$$

### 5.2 Formal Group Law for F4T

**Conjecture 5.2**: The F4T formal group law depends on dimension type:
- T1: Additive FGL $F(u, v) = u + v$ (discrete)
- T2: Multiplicative FGL $F(u, v) = u + v - uv$ (continuous)
- T3: Elliptic FGL (modular)
- T4: Universal FGL (algebraic)

### 5.3 Divisor Classes

**Definition 5.3**: For dimension system with "divisor" $D$:
$$[D] \in \Omega^1(\mathcal{D})$$

**Intersection theory**:
$$[D_1] \cdot [D_2] = F_{F4T}([D_1], [D_2])$$

---

## 6. Chern Classes in F4T

### 6.1 Definition

**Definition 6.1**: For "vector bundle" $E$ over dimension system:
$$c_i(E) \in \Omega^i(\mathcal{D})$$

**Total Chern class**:
$$c(E) = 1 + c_1(E) + c_2(E) + \cdots$$

### 6.2 Splitting Principle

**Theorem 6.2**: Any vector bundle can be split (after pullback) as sum of line bundles.

**Application**: Reduce computations to $c_1$ of line bundles.

### 6.3 Todd Class and Riemann-Roch

**Definition 6.3**: **Todd class**:
$$\text{Td}(E) = \prod_i \frac{x_i}{1 - e^{-x_i}}$$

where $x_i = c_1(L_i)$ are Chern roots.

**Theorem 6.4** (Motivic Riemann-Roch):
$$f_*(- \cdot \text{Td}(T_f)) = \text{ch} \circ f_* \circ \text{Td}$$

for proper morphism $f$ with tangent bundle $T_f$.

---

## 7. Cobordism and Stable Homotopy

### 7.1 MGL as Oriented Theory

**Theorem 7.1**: $MGL$ is the universal oriented theory in $\mathcal{SH}$:
$$[MGL, E] \cong \{\text{orientations of } E\}$$

### 7.2 Bousfield Localization

**Definition 7.2**: The **MGL-localization**:
$$L_{MGL}: \mathcal{SH} \to \mathcal{SH}_{MGL}$$

**Conjecture 7.3**: $MGL$-localization captures all oriented information.

### 7.3 F4T Cobordism Spectrum

**Construction**: F4T version of MGL:
$$MGL_{\text{F4T}} := \text{colim} \text{Th}(\text{universal bundle over } \mathcal{M}_{\text{F4T}})$$

---

## 8. Applications to Enumerative Geometry

### 8.1 Gromov-Witten Invariants

**GW invariants**: Count curves in varieties.

**Reformulation**: Using virtual fundamental classes in algebraic cobordism.

### 8.2 F4T Enumerative Invariants

**Definition 8.1**: **Cobordism Gromov-Witten invariants**:
$$\langle \tau_{d_1}(\gamma_1) \cdots \rangle^{\Omega} = \int_{[\overline{\mathcal{M}}]^{vir}}^{\Omega} \prod \psi_i^{d_i} \cup \gamma_i$$

### 8.3 Comparison

**Theorem 8.2**: Cobordism invariants specialize to:
- Chow invariants (additive FGL)
- K-theoretic invariants (multiplicative FGL)

---

## 9. Next Phase Preview

Phase 3 will explore:
1. **Higher algebraic K-theory**
2. **Noncommutative motives**
3. **Cyclotomic trace**

---

**Document Version**: 1.0  
**Date**: 2026-02-07  
**Status**: Phase 2 Complete - Algebraic Cobordism
