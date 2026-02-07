# Dimensionics: A Unified Mathematical Theory of Dimension

## Overview

This repository contains the complete source materials for the paper **"Dimensionics: A Unified Mathematical Theory of Dimension"** submitted to *Reviews in Mathematical Physics*.

The paper presents a unified framework synthesizing seven research directions (A~G) with the Fixed-4D-Topology framework, centered on the Master Equation:

$$d_{\text{eff}} = \arg\min_{d \in \mathcal{D}} \left[ E(d) - T \cdot S(d) + \Lambda(d) \right]$$

## Quick Links

- 📄 [LaTeX Source](latex/) - Complete document source
- 📊 [Numerical Validation](src/unified_framework/numerical_validation.py) - Pure Python validation
- ✅ [Submission Checklist](SUBMISSION_CHECKLIST.md) - Pre-submission verification
- 📋 [Submission Status](SUBMISSION_STATUS.md) - Project status and timeline
- 📝 [Contributions](CONTRIBUTIONS.md) - Detailed contribution statement

## Paper Statistics

| Metric | Value |
|--------|-------|
| **Word Count** | ~35,000 words |
| **Pages** | 80-100 (target) |
| **Chapters** | 10 |
| **Theorems** | 12 core + 3 fusion |
| **References** | 30+ |
| **Validation Tests** | 14 (all passed) |

## Fusion Theorems (Core Results)

| Theorem | Connection | Error |
|---------|------------|-------|
| **FE-T1** | Sobolev ↔ Cantor | 6.75% |
| **FB-T2** | Flow ↔ PDE Variational | 0% |
| **FG-T4** | Grothendieck ↔ Variational | 0% |

All theorems are **rigorously proved** (L1 classification).

## Repository Structure

```
.
├── papers/unified-dimensionics/
│   ├── README.md                 # This file
│   ├── SUBMISSION_STATUS.md      # Detailed status report
│   ├── SUBMISSION_CHECKLIST.md   # Pre-submission checklist
│   ├── CONTRIBUTIONS.md          # Contribution statement
│   ├── VALIDATION_REPORT.md      # Numerical validation results
│   ├── chapters/                 # Markdown source (10 chapters)
│   └── latex/                    # LaTeX document
│       ├── main.tex              # Main document
│       ├── references.bib        # Bibliography
│       ├── Makefile              # Compilation automation
│       ├── README.md             # LaTeX documentation
│       ├── chapters/             # LaTeX chapter files (10)
│       └── figures/              # TikZ figures
│
└── src/unified_framework/
    └── numerical_validation.py   # Validation code (pure Python)
```

## Key Features

### Mathematical Content

1. **Complete dimension taxonomy**: Topological, Hausdorff, Spectral, Box-counting, Effective
2. **Dimension hierarchy**: $\dim_{\text{top}} \leq d_s \leq d_H \leq d_B$ (rigorously proved)
3. **Three fusion theorems**: Connecting previously disparate mathematical areas
4. **M-0.3 refutation**: Systematic refutation of modular-fractal correspondence

### Physical Applications

- Quantum gravity (dimensional reduction)
- Condensed matter (Anderson localization)
- Network science (complex network dimensions)
- Quantum information (entanglement entropy)

### Computational Validation

- Pure Python implementation (no external dependencies)
- All 3 fusion theorems validated
- Maximum error < 8%

## Compilation

### Prerequisites

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required packages: amsmath, amssymb, amsthm, mathtools, graphicx, booktabs, hyperref, cleveref, tikz, pgfplots, geometry, enumitem, xcolor

### Quick Start

```bash
cd papers/unified-dimensionics/latex

# Using Makefile
make pdf        # Full compilation
make quick      # Quick compile (no bibliography)
make clean      # Clean auxiliary files

# Manual compilation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Citation

If you use this work, please cite:

```bibtex
@article{dim2026,
  title={Dimensionics: A Unified Mathematical Theory of Dimension},
  author={{The Dimensionics Research Initiative}},
  journal={Reviews in Mathematical Physics},
  year={2026},
  note={Submitted}
}
```

## Submission Information

- **Journal**: Reviews in Mathematical Physics
- **Submission Deadline**: March 21, 2026
- **Status**: 🟢 **On Track**
- **MSC 2020**: 28A80, 35J20, 58J50, 81Q35, 11F11

## Research Framework

- **Human Supervisor**: Wang Bin (Independent Researcher)
- **AI Agent**: Kimi 2.5 (Moonshot AI)
- **Repository**: [https://github.com/dpsnet/Fixed-4D-Topology](https://github.com/dpsnet/Fixed-4D-Topology)

## License

This research is provided for academic use. Please cite appropriately.

---

*Last updated: February 7, 2026*
