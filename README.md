# Dimensionics: Mathematical Core (T1-T4)

**English | [中文](README_zh.md)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18511249.svg)](https://doi.org/10.5281/zenodo.18511249)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-CORE%20FOUNDATION-blue.svg)]()

> **L1/L2 Strict Mathematical Foundation**: Cantor theory, Master equation, Convexity, Spectral geometry.

---

## ⚠️ Retraction Notice

**v3.0.0 has been RETRACTED** (Feb 11, 2026)

The previous release claimed:
- ❌ "Three Bridges eliminate phenomenological parameters" — **False**
- ❌ "C* = (Δλ/λ₁)·d_c·(1-d_c)·π/4" — **Incorrect** (predicts ~1.46 vs empirical ~0.21)
- ❌ "L1 rigorous proofs for bridges" — **Unproven**
- ❌ "100% first-principles unification" — **Not achieved**

**This release (v3.0.0-core)** contains only the mathematically rigorous core (T1-T4).

---

## Current Scope (L1/L2 Strict)

| Module | Direction | Strictness | Status |
|--------|-----------|------------|--------|
| **T1** | Cantor Dimension Approximation | L1-L2 | ✅ Complete |
| **T2** | Master Equation & Spectral PDE | L2 | ✅ Complete |
| **T3** | Convexity Analysis | L1 | ✅ Complete |
| **T4** | Algebraic Topology & Spectral Geometry | L2 | ✅ Complete |

**Total**: 4 core modules, 8+ theorems with proofs.

---

## Deleted Content (Not Meeting L1/L2)

| Content | Reason | Current Location |
|---------|--------|------------------|
| **Three Bridges (A,B,C)** | Formulas unproven, claims false | Removed |
| **H (Quantum Dimension)** | Numerical simulation only (L3) | Research plan only |
| **I (Network Geometry)** | Empirical analysis (L3) | Research plan only |
| **J (Random Fractals)** | Simulation only (L3) | Research plan only |
| **K (ML Dimension)** | Experimental (L3) | Research plan only |

**Standard**: L1/L2 or nothing.

---

## Installation

```bash
pip install dimensionics
```

## Usage

```python
from dimensionics import MasterEquation, CantorApproximation

# T2: Master equation
me = MasterEquation(alpha=0.5, beta=0.3)

# T1: Cantor approximation
cantor = CantorApproximation()
```

---

## Repository Structure

```
Fixed-4D-Topology/
├── src/dimensionics/           # Strict core (T1-T4)
│   ├── core/                   # T2-T3: Master equation, convexity
│   ├── number_theory/          # T1: Cantor theory
│   └── topology/               # T4: Spectral geometry
├── papers/                     # Core papers (T1-T10, A-G)
├── docs/theory/core/           # T1-T4 documentation
└── extended_research/          # H-K (research plans, not published theory)
```

---

## Version History

| Version | Date | Status | Content |
|---------|------|--------|---------|
| v2.1.0 | Feb 9, 2026 | ✅ Valid | 5 papers, T1-T10 + A-G foundation |
| **v3.0.0-core** | **Feb 11, 2026** | **✅ Current** | **T1-T4 strict core only** |
| v3.0.0 | Feb 10, 2026 | ❌ **RETRACTED** | False claims about bridges |

---

## Research Status

**Completed (L1/L2)**:
- ✅ T1: Cantor approximation theory
- ✅ T2: Master equation framework
- ✅ T3: Convexity analysis
- ✅ T4: Spectral geometry

**In Progress (Research Plans)**:
- 🟡 H-K: Extended directions (need L1/L2 strictification)
- 🟡 Three Bridges: Research hypotheses (need rigorous proof or refutation)

---

## Citation

```bibtex
@misc{dimensionics2026core,
  title={Dimensionics: Mathematical Core (T1-T4)},
  year={2026},
  version={3.0.0-core},
  doi={10.5281/zenodo.18511249},
  url={https://github.com/dpsnet/Fixed-4D-Topology}
}
```

---

**Standard**: Only content with complete mathematical proofs (L1/L2).
