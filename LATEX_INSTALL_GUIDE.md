# LaTeX Installation Guide for Dimensionics

**System**: AlmaLinux 9.5 (RHEL/CentOS compatible)  
**Purpose**: Compile Dimensionics paper for Reviews in Mathematical Physics

---

## Quick Start

```bash
cd /mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories

# 1. Install LaTeX
sudo ./install_latex.sh

# 2. Test compilation
./test_latex.sh
```

---

## Manual Installation

If the script doesn't work, install manually:

```bash
# Update system
sudo dnf update -y

# Install TeX Live with required packages
sudo dnf install -y texlive-scheme-medium \
    texlive-cleveref \
    texlive-mathtools \
    texlive-booktabs \
    texlive-enumitem \
    texlive-xcolor \
    texlive-pgfplots \
    texlive-bibtex \
    texlive-amsfonts \
    texlive-hyperref \
    texlive-geometry
```

---

## Package Requirements

Dimensionics paper requires these LaTeX packages:

| Package | Purpose | Status |
|---------|---------|--------|
| amsmath | Mathematical typesetting | ✅ Essential |
| amssymb | Math symbols | ✅ Essential |
| amsthm | Theorem environments | ✅ Essential |
| mathtools | Math enhancements | ✅ Essential |
| cleveref | Smart cross-references | ✅ Essential |
| booktabs | Professional tables | ✅ Essential |
| tikz | Graphics | ✅ Essential |
| pgfplots | Plots | ✅ Optional |
| hyperref | PDF links | ✅ Recommended |
| enumitem | List customization | ✅ Essential |
| xcolor | Colors | ✅ Essential |
| geometry | Page layout | ✅ Essential |

---

## Installation Size

| Scheme | Size | Recommendation |
|--------|------|----------------|
| `scheme-minimal` | ~200MB | ❌ Too minimal |
| `scheme-medium` | ~500MB | ✅ Recommended |
| `scheme-full` | ~4GB | ✅ Complete |

---

## Compilation

### Method 1: Using Makefile

```bash
cd Fixed-4D-Topology/papers/unified-dimensionics/latex

make pdf        # Full compilation with bibliography
make quick      # Fast compile (no bibliography)
make clean      # Clean auxiliary files
```

### Method 2: Manual Compilation

```bash
cd Fixed-4D-Topology/papers/unified-dimensionics/latex

# Standard 3-pass compilation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Method 3: Using latexmk

```bash
latexmk -pdf main.tex
```

---

## Troubleshooting

### Issue: Package not found

```bash
# Find which package provides a file
sudo dnf provides '*/cleveref.sty'

# Install specific package
sudo dnf install texlive-cleveref
```

### Issue: pdflatex not in PATH

```bash
# Find pdflatex location
find /usr -name pdflatex 2>/dev/null

# Add to PATH if needed
export PATH=$PATH:/usr/bin
```

### Issue: Bibliography not processing

```bash
# Ensure bibtex is installed
which bibtex

# Run manually
bibtex main
```

### Issue: Font problems

```bash
# Install additional fonts
sudo dnf install texlive-fonts-recommended texlive-fonts-extra
```

---

## Alternative: Docker

If system installation fails, use Docker:

```bash
# Run LaTeX in Docker
docker run --rm -v $(pwd):/workdir texlive/texlive:latest \
    pdflatex -output-directory=/workdir main.tex
```

---

## Verification Checklist

After installation, verify:

- [ ] `pdflatex --version` works
- [ ] `bibtex --version` works
- [ ] `kpsewhich amsmath.sty` returns path
- [ ] Compilation produces PDF
- [ ] PDF contains all 10 chapters
- [ ] Bibliography appears at end
- [ ] No missing font warnings

---

## Support Files

| File | Description |
|------|-------------|
| `install_latex.sh` | Automated installation script |
| `test_latex.sh` | Compilation test script |
| `latex/Makefile` | Compilation automation |

---

## Expected Output

Successful compilation produces:

```
main.pdf          (final document, ~80-100 pages)
main.aux          (auxiliary file)
main.bbl          (bibliography)
main.toc          (table of contents)
main.out          (PDF outlines)
```

---

## Resources

- **CTAN**: https://www.ctan.org/
- **TeX Live**: https://tug.org/texlive/
- **Dimensionics Paper**: See `papers/unified-dimensionics/`

---

*Last updated: February 7, 2026*
