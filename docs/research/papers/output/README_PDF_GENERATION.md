# PDF Generation Guide

## T3 Replacement Research Paper

This directory contains the LaTeX source files for the T3 replacement research paper.

### Files

| File | Description |
|------|-------------|
| `paper_final.tex` | Main LaTeX source (83 pages) |
| `paper_final.md` | Markdown version |
| `../references.bib` | BibTeX bibliography |
| `paper_statistics.json` | Paper statistics |

### Requirements

- **LaTeX Distribution**: TeX Live or MiKTeX
  - pdflatex
  - bibtex
- **Optional**: pdfinfo (for statistics)

### Method 1: Using Make (Recommended)

```bash
cd docs/research/papers/output

# Generate PDF
make

# Or explicitly
make pdf

# View PDF (Linux/macOS)
make view

# Clean auxiliary files
make clean

# Clean everything including PDF
make distclean
```

### Method 2: Using Compile Script

```bash
cd docs/research/papers/output

# Make script executable (first time)
chmod +x compile_pdf.sh

# Run compilation
./compile_pdf.sh
```

### Method 3: Manual Compilation

```bash
cd docs/research/papers/output

# Compile LaTeX
pdflatex paper_final.tex

# Process bibliography
bibtex paper_final

# Recompile (twice for references)
pdflatex paper_final.tex
pdflatex paper_final.tex
```

### Output

- **PDF File**: `paper_final.pdf`
- **Pages**: ~83 pages
- **Format**: Annals of Mathematics style

### Troubleshooting

**Error: pdflatex not found**
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS
brew install --cask mactex

# Windows
# Download and install MiKTeX from https://miktex.org/
```

**Error: Bibliography not processing**
- Ensure `../references.bib` exists
- Run `bibtex paper_final` manually

**Error: Missing packages**
- Install common LaTeX packages:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install texlive-latex-extra texlive-fonts-recommended
  ```

### Paper Details

- **Title**: Fractal Spectral Asymptotics and p-adic Thermodynamic Formalism
- **Status**: Research prototype (not submitted)
- **Strictness**: L1 proofs for two conjectures
- **Verification**: 671 cases (487 Kleinian + 184 p-adic)

### Citation

If you use this paper or code, please cite:

```bibtex
@misc{dimensionics2026t3replacement,
  title={T3 Replacement: Fractal Spectral Asymptotics and p-adic Thermodynamic Formalism},
  author={Wang Bin and Kimi AI Research Team},
  year={2026},
  url={https://github.com/dpsnet/Fixed-4D-Topology/tree/main/docs/research}
}
```
