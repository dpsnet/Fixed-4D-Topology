# Dimensionics LaTeX Document

## Overview

This directory contains the LaTeX source files for the paper **"Dimensionics: A Unified Mathematical Theory of Dimension"** submitted to Reviews in Mathematical Physics.

## File Structure

```
.
├── main.tex              # Main document file
├── references.bib        # Bibliography database
├── Makefile              # Compilation automation
├── README.md             # This file
├── chapters/             # Chapter source files
│   ├── chapter1.tex      # Introduction
│   ├── chapter2.tex      # Mathematical Overview
│   ├── chapter3.tex      # Topological Dimension Theory
│   ├── chapter4.tex      # Analytic Theory (Sobolev Spaces)
│   ├── chapter5.tex      # Spectral Dimension Theory
│   ├── chapter6.tex      # Number-Theoretic Dimensions
│   ├── chapter7.tex      # The Unified Framework
│   ├── chapter8.tex      # Computational Complexity
│   ├── chapter9.tex      # Physical Applications
│   └── chapter10.tex     # Discussion and Conclusions
└── figures/              # TikZ figures
    ├── dimension_taxonomy.tex
    └── fusion_diagram.tex
```

## Compilation

### Requirements

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required packages: amsmath, amssymb, amsthm, mathtools, graphicx, booktabs, hyperref, cleveref, tikz, pgfplots, geometry, enumitem, xcolor

### Compilation Steps

#### Option 1: Using Makefile

```bash
# Full compilation with bibliography
make pdf

# Quick compilation (no bibliography)
make quick

# Clean auxiliary files
make clean
```

#### Option 2: Manual Compilation

```bash
# Standard compilation sequence
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

#### Option 3: Using latexmk (recommended)

```bash
latexmk -pdf main.tex
```

## Document Features

### Theorem Environments

The document defines the following theorem-like environments:

- `theorem` - Main theorems
- `lemma` - Lemmas
- `proposition` - Propositions
- `corollary` - Corollaries
- `conjecture` - Conjectures
- `definition` - Definitions
- `example` - Examples
- `remark` - Remarks

### Custom Commands

Mathematical shorthand commands:

- `\dH` - Hausdorff dimension ($d_H$)
- `\dB` - Box-counting dimension ($d_B$)
- `\ds` - Spectral dimension ($d_s$)
- `\deff` - Effective dimension ($d_{eff}$)
- `\C, \R, \N, \Z` - Number sets ($\mathbb{C}, \mathbb{R}, \mathbb{N}, \mathbb{Z}$)
- `\E` - Expectation ($\mathbb{E}$)

### Key Equations

The Master Equation (central to the paper):

```latex
\deff = \arg\min_{d \in \mathcal{D}} \left[ E(d) - T \cdot S(d) + \Lambda(d) \right]
```

## Submission Information

- **Journal**: Reviews in Mathematical Physics
- **Submission Date**: March 21, 2026
- **Word Count**: ~35,000 words
- **Estimated Pages**: 80-100 pages
- **MSC 2020**: 28A80, 35J20, 58J50, 81Q35, 11F11

## Citation Style

The document uses `alpha` bibliography style. Citations are numbered [AuthorYear] format.

Key references:
- [JW84] Jonsson-Wallin (Sobolev spaces on fractals)
- [Kig01] Kigami (Analysis on fractals)
- [Del74] Deligne (Modular forms)
- [RT06] Ryu-Takayanagi (Holographic entropy)

## Troubleshooting

### Compilation Errors

1. **Missing packages**: Ensure all required packages are installed
2. **Bibliography not showing**: Run `bibtex main` between pdflatex runs
3. **References showing as [?]**: Recompile multiple times

### Common Issues

- TikZ figures may require `shell-escape` flag if using externalization
- Cleveref package must be loaded after hyperref

## Contact

For questions about the LaTeX source, contact:
- A~G Research Team (Fundamental-Mathematics Project)
- Fixed-4D-Topology Team (Dynamic Spectral Dimension Framework)

---

*Last updated: February 7, 2026*
