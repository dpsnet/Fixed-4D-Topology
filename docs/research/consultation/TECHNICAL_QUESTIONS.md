# Technical Questions for Expert Consultation

## Overview

This document contains detailed technical questions customized for each of the six experts we plan to contact. Questions are organized by expert specialty and reflect our current understanding gaps at the L1→L2 transition.

---

## Part A: For Robert Benedetto & Juan Rivera-Letelier (p-adic Dynamics Experts)

### Context
We have constructed a thermodynamic formalism for p-adic polynomial dynamics using Berkovich spaces. Our construction parallels the classical complex case but involves several technical adaptations.

### Questions

#### Q1: Gibbs Measure Uniqueness Conditions
**Question:** What are the weakest known conditions on a polynomial $\phi \in \mathbb{Q}_p[z]$ ensuring uniqueness of the Gibbs measure $\mu_\phi$ on $J_\phi^{Berk}$ for a Hölder continuous potential $\varphi$?

**Our Current Understanding:**
- Existence: Proven via transfer operator spectral analysis
- Uniqueness: Established for **expanding** maps (uniform hyperbolicity)

**Specific Sub-questions:**
- Does topological mixing on $J_\phi^{Berk}$ suffice for uniqueness?
- What role does the good reduction hypothesis play?
- Can the uniqueness criterion of Denker-Urbański be adapted to Berkovich spaces?

**Relevant Background:** Our potential has the form $\varphi_s = -s\log|d\phi|_p$. The derivative $|d\phi|_p$ is non-Archimedean and piecewise constant on type I points.

---

#### Q2: Handling Non-Expanding Polynomials
**Question:** What strategies exist for extending thermodynamic formalism to p-adic polynomials that are not expanding on their Julia sets?

**Specific Cases of Interest:**
1. Polynomials with indifferent periodic points
2. Maps with critical points accumulating on $J_\phi^{Berk}$
3. Polynomials of bad reduction

**Our Approach So Far:**
- We use the hyperbolic metric on the Berkovich projective line
- The issue: $|d\phi|_p$ can vanish at critical points (type I)

**Question:** Can we use:
- Inducing schemes (as in complex dynamics)?
- Cone techniques adapted to non-Archimedean setting?
- Regularization of the potential near critical points?

---

#### Q3: Berkovich Space Technical Verification
**Question:** Can you verify the following technical details of our Berkovich space construction?

**Claim 1:** For $\phi$ with good reduction, the Julia set $J_\phi^{Berk}$ is contained in the Berkovich hyperbolic space $\mathbb{H}_p$ except for countably many type I points.

**Claim 2:** The measure $\mu_\phi$ constructed via eigenfunctions of the transfer operator is supported on the hyperbolic Julia set.

**Claim 3:** The entropy $h_{\mu_\phi}(\phi)$ can be computed via:
$$h_{\mu_\phi}(\phi) = \lim_{n\to\infty} \frac{1}{n} H_{\mu_\phi}\left(\bigvee_{i=0}^{n-1} \phi^{-i}\mathcal{P}\right)$$
for any generating partition $\mathcal{P}$.

**Potential Issues:**
- Standard generators may not exist in the Berkovich topology
- The measure may have atoms at type I points
- Branched coverings complicate entropy calculations

---

#### Q4: Technical Differences from Real Bowen Formula
**Question:** What are the essential technical differences between proving the Bowen dimension formula in the p-adic case versus the classical real/complex case?

**Bowen Formula (Classical):**
$$\dim_H(J) = \sup\left\{\frac{h_\mu}{\lambda_\mu} : \mu \in \mathcal{M}_\phi\right\}$$

**Our Adaptation:**
$$\dim_{Berk}(J_\phi) = \frac{h_{\mu_\phi}(\phi)}{\int \log|d\phi|_p \, d\mu_\phi}$$

**Specific Concerns:**
1. **Metric structure:** The Berkovich metric vs. Euclidean metric
2. **Covering arguments:** p-adic disks have different geometric properties
3. **Thermodynamic formalism:** Pressure definition adaptations
4. **Dimension theory:** Hausdorff dimension vs. Berkovich dimension

---

#### Q5: Simplification Pathways
**Question:** Are there known simplifications or shortcuts in the p-adic case that don't exist in complex dynamics?

**Examples We Wonder About:**
- Non-Archimedean absolute value being ultrametric simplifies some estimates
- Potential discontinuities at critical points may be "removable" in some sense
- Berkovich space compactness may eliminate some technical difficulties

**Conversely, are there complications unique to the p-adic setting?**

---

## Part B: For Richard Taylor & Peter Sarnak (Langlands Program Experts)

### Context
We have defined "fractal Hecke operators" acting on spaces of functions on self-similar sets and proposed a connection to L-functions through a generalized trace formula.

### Questions

#### Q1: Precedents for Fractal Hecke Theory
**Question:** Does our proposed "fractal Hecke theory" have any precedents or connections to existing structures in the Langlands program?

**Our Construction:**
For the Sierpiński gasket $SG$ with scaling maps $\{F_i\}_{i=0}^2$, define:
$$(T_p f)(x) = \sum_{\substack{y \in SG \\ F_i(y) = x \text{ for some } i}} f(y) \cdot w_p(y)$$

where weights $w_p$ are chosen so that eigenfunctions correspond to L-function coefficients.

**Questions:**
- Are there known Hecke-type operators on fractals?
- Do p-adic L-functions admit similar constructions?
- Any connections to the Jacquet-Langlands correspondence for non-archimedean fields?

---

#### Q2: L'/L Connection to Dimension
**Question:** Is the relationship between $L'/L(1, \pi)$ (logarithmic derivative of L-function) and fractal dimension known or expected in the Langlands framework?

**Our Finding:**
We observe numerically that:
$$d_s \sim \frac{2}{\log N} \cdot \frac{L'}{L}(1, \pi_{SG})$$

where $\pi_{SG}$ is our conjectural automorphic representation associated to the gasket.

**Question:** Does this resemble:
- The explicit formula for L-functions?
- Stark's conjectures on derivatives?
- The GUE hypothesis for zero spacing?

---

#### Q3: Jacquet-Langlands for Fractals
**Question:** What are the fundamental obstacles to extending the Jacquet-Langlands correspondence to "fractal automorphic representations"?

**Background:** The classical JL correspondence relates:
- Automorphic forms on $GL_2(\mathbb{A}_\mathbb{Q})$
- Automorphic forms on quaternion division algebras

**Our Goal:** Extend to representations "supported on" fractal limit sets.

**Specific Obstacles We Identify:**
1. Lack of underlying algebraic group structure
2. Non-integer "dimensions" of representation spaces
3. Absence of standard Whittaker models

**Question:** Which of these is fundamental, and which might be circumvented?

---

#### Q4: Maass Pressure Definition
**Question:** Is our proposed "Maass pressure" definition reasonable from the automorphic perspective?

**Definition:**
$$P_{Maass}(s) = \lim_{T \to \infty} \frac{1}{T} \log \sum_{\substack{\gamma \in \Gamma \\ \ell(\gamma) < T}} e^{-s\ell(\gamma)} \cdot a_\gamma$$

where $a_\gamma$ are Fourier coefficients of a Maass form.

**Claims We Make:**
1. This converges for $\Re(s) > 1$
2. It has a meromorphic continuation
3. Its poles correspond to Laplacian eigenvalues

**Questions:**
- Does this relate to Selberg zeta functions?
- Any connection to the Arthur trace formula?
- Is this the "right" definition from your perspective?

---

#### Q5: Connections to Other Parts of Langlands
**Question:** Beyond the immediate scope of our work, what other parts of the Langlands program might connect to fractal spectral theory?

**Possibilities We're Exploring:**
- Functoriality for fractal groups
- Geometric Langlands over fractal curves
- p-adic Langlands and fractal Galois representations

**Question:** Which directions seem most promising to you?

---

## Part C: For Curtis McMullen & Mark Pollicott (Thermodynamic Formalism Experts)

### Context
We have unified three definitions of pressure (thermodynamic, Maass, Berkovich) for a class of dynamical systems spanning fractals, automorphic forms, and p-adic dynamics.

### Questions

#### Q1: Fundamental Mechanism of Pressure Unification
**Question:** What is the deep mathematical reason why three apparently different pressure definitions coincide?

**The Three Pressures:**

| Pressure | Definition | Context |
|----------|-----------|---------|
| $P_{thermo}$ | $\sup_\mu \{h_\mu + \int \varphi \, d\mu\}$ | Statistical mechanics |
| $P_{Maass}$ | Growth rate of weighted periodic orbits | Automorphic forms |
| $P_{Berk}$ | $\lim \frac{1}{n}\log \mathcal{L}_\phi^n 1$ | p-adic dynamics |

**Our Proof:** Uses spectral analysis of the Ruelle-Langlands operator.

**Question:** Is there a:
- Categorical explanation?
- Representation-theoretic interpretation?
- Physical/statistical mechanics intuition?

---

#### Q2: Thermodynamic Formalism on Fractal Limit Sets
**Question:** What is the current state of thermodynamic formalism for infinite conformal iterated function systems with overlaps?

**Our System:** The Sierpiński gasket IFS has:
- Finite alphabet ($\{0, 1, 2\}$)
- Open set condition (no overlaps)
- But: Infinite type structure in the spectral analysis

**Specific Questions:**
1. Can the methods of Mauldin-Urbański (infinite IFS) be adapted?
2. What about the "phase transitions" phenomenon in pressure?
3. Are there known examples where the dimension formula fails?

**Related Work:** We are aware of your work on Hausdorff dimension algorithms and Pollicott's work on zeta functions for interval maps.

---

#### Q3: Analogy with Teichmüller Theory
**Question:** Does our unified pressure formula relate to known structures in Teichmüller theory?

**Observation:** The formula:
$$d_s = 2\frac{P(0)}{P'(0)}$$

resembles:
- **Weil-Petersson metric:** Similar derivative formulas
- **Thurston's stretch maps:** Pressure-like quantities
- **McMullen's Hausdorff dimension formula:** For limit sets of Kleinian groups

**Question:** Could our framework be interpreted as a "fractal Teichmüller theory"?

---

#### Q4: Theoretical Status of Our Unified Formula
**Question:** How should we understand the theoretical status of our unified pressure formula in the landscape of existing results?

**Our Formula:**
$$P_{unified}(s) = \lim_{n\to\infty} \frac{1}{n} \log \sum_{x \in \text{Fix}(\phi^n)} \prod_{k=0}^{n-1} L\left(s + k\frac{d}{n}, \pi_x\right)$$

**Questions:**
1. Is this fundamentally new, or a reformulation of known results?
2. Does it generalize existing formulas or specialize them?
3. What is its "natural domain" of applicability?
4. Can it be derived from more general principles (e.g., non-commutative geometry)?

---

#### Q5: Generalization Possibilities
**Question:** To what settings can our unified framework be extended?

**Settings We Have in Mind:**

| Setting | Obstacles | Potential Approach |
|---------|-----------|-------------------|
| Random IFS | Lack of deterministic structure | Random dynamical systems |
| Non-conformal maps | Distortion estimates fail | Sub-additive thermodynamics |
| Infinite alphabets | Summability issues | Mauldin-Urbański theory |
| Higher dimensions | Geometric complexity | Higher-rank thermodynamics |

**Question:** Which extensions seem most promising/feasible to you?

**Specific Interest:** Can the methods be applied to:
- Limit sets of geometrically infinite Kleinian groups?
- Non-uniformly hyperbolic rational maps (complex)?
- Skew products over expanding maps?

---

## General Question for All Experts

### Question X: The "Meta-Question"
**What is the most significant gap or potential flaw in our overall approach that we should address before proceeding to complete proofs?**

We have:
- ✓ A consistent conceptual framework
- ✓ L1 rigorous proofs of main theorems
- ✓ Strong numerical evidence
- ✓ Parallel results in three domains

But we may be missing:
- ? Fundamental obstructions we haven't recognized
- ? Overlooked counterexamples
- ? Technical requirements beyond our expertise

**Your candid assessment would be invaluable.**

---

## Document Information

**Version:** 1.0  
**Last Updated:** February 2026  
**For:** Expert consultation preparation  
**Confidentiality:** Please do not distribute
