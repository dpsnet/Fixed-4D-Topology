# Code Organization Guide

This document clarifies the distinction between **production code** (PyPI package) and **research code** (theory validation).

## Two Types of Code

### 1. Production Code (`src/dimensionics/`)

**Purpose**: Stable, tested Python package for public use

**Location**:
```
src/dimensionics/
├── __init__.py
├── cli.py              # Command-line interface
├── core/               # Master equation, spectral dimension
├── number_theory/      # Cantor approximation
├── cosmology/          # Universe simulation
├── qft/                # Convexity analysis
├── topology/           # Algebraic topology
└── bridges/            # Three bridges (production version)
```

**Usage**:
```bash
pip install dimensionics
dimensionics-verify   # Verify all three bridges
dimensionics-demo     # Run demonstration
```

**Status**: 🟢 Production Ready

---

### 2. Research Code (`docs/theory/*/code/`)

**Purpose**: Theory development, verification, and exploration

**Location**:
```
docs/theory/
├── core/T1-cantor/code/           # Cantor theory development
├── core/T2-master-equation/code/  # Master equation solvers
├── bridges/A-critical-exponent/code/  # Bridge A proof
└── ...
```

**Characteristics**:
- Exploratory and experimental
- Contains proofs and validation scripts
- Organized by research direction
- May not have production-level testing

**Status**: 🟡 Research/Development

---

## Relationship

```
Research Code (docs/theory/)
        │
        │ Validation & Refinement
        ▼
Production Code (src/dimensionics/)
        │
        │ Packaging
        ▼
PyPI Release (pip install)
```

## When to Use Which

| Use Case | Use This | Location |
|----------|----------|----------|
| **Install & Use** | Production | `pip install dimensionics` |
| **Verify Bridges** | Production | `dimensionics-verify` |
| **Study Theory** | Research | `docs/theory/*/README.md` |
| **Understand Proof** | Research | `docs/theory/bridges/*/code/` |
| **Run Experiments** | Research | `docs/theory/extensions/*/code/` |
| **Development** | Research | Modify then migrate to production |

## Migration Flow

Research code that matures should be migrated to production:

```
docs/theory/core/T1-cantor/code/greedy_algorithm.py
                    │
                    │ Refactor, test, document
                    ▼
src/dimensionics/number_theory/cantor.py
```

---

**Summary**:
- `src/dimensionics/` - **Use this** for applications
- `docs/theory/*/code/` - **Study this** for understanding theory
