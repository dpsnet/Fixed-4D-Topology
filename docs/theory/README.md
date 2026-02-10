# Dimensionics Theory Documentation

This directory contains the organized theoretical framework of Dimensionics, structured by research directions and logical dependencies.

## Directory Structure

```
docs/theory/
├── README.md              # This file
├── core/                  # Core mathematical foundations (T1-T4)
│   ├── T1-cantor/         # Cantor dimension approximation
│   ├── T2-master-equation/# Master equation & spectral PDE
│   ├── T3-convexity/      # Convexity analysis & QFT
│   └── T4-topology/       # Algebraic topology & spectral geometry
│
├── extensions/            # Extended research directions (H-K)
│   ├── H-quantum/         # Quantum dimension (iTEBD)
│   ├── I-network/         # Network geometry
│   ├── J-fractal/         # Random fractals
│   └── K-ml/              # Machine learning effective dimension
│
├── bridges/               # Three Bridges (First-Principles Unification)
│   ├── A-critical-exponent/   # Bridge A: Critical exponent
│   ├── B-neural-network/      # Bridge B: Neural network weights
│   └── C-quantum/             # Bridge C: Quantum equivalence
│
└── foundations/           # Axiomatic foundations
    ├── axioms/            # Axioms A1-A9
    ├── theorems/          # Core theorems with proofs
    └── definitions/       # Key definitions
```

## Research Direction Mapping

| Direction | Code | Status | Bridge Connection |
|-----------|------|--------|-------------------|
| Cantor Approximation | T1 | ✅ Complete | Input to Bridge A |
| Master Equation | T2 | ✅ Complete | Foundation for all |
| Convexity Analysis | T3 | ✅ Complete | Constraint for Bridge B |
| Algebraic Topology | T4 | ✅ Complete | Foundation for Bridge C |
| Quantum Dimension | H | ✅ Complete | Connected to Bridge C |
| Network Geometry | I | ✅ Complete | Connected to Bridge B |
| Random Fractals | J | ✅ Complete | Validates Bridge A |
| ML Dimension | K | ✅ Complete | Applications of Bridge B |

## Three Bridges

| Bridge | Formula | Status |
|--------|---------|--------|
| **A** | C* ≈ 0.21 (empirical) | 🟡 Hypothesis - no strict derivation |
| **B** | w_i ∝ 1/|λ_i| at α+β=T/8 | ✅ Verified |
| **C** | H_NN = U·L·U† | ✅ Verified |

## Quick Navigation

- [Core Theory](core/) - Mathematical foundations
- [Extended Directions](extensions/) - Application domains
- [Three Bridges](bridges/) - First-principles unification
- [Axiomatic Foundations](foundations/) - Formal basis

---

*For execution status, see [Project Status](../../PROJECT_STATUS.md)*
