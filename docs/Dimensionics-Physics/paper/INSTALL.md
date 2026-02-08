# Installation Guide
## Dimensionics-Physics Paper

This guide explains how to set up your environment to compile and work with the Dimensionics-Physics paper.

---

## Prerequisites

### Required Software

1. **LaTeX Distribution**
   - TeX Live 2022 or later (recommended)
   - OR MiKTeX (Windows)
   - OR MacTeX (macOS)

2. **Python 3.8+** (for figure generation)
   - NumPy
   - Matplotlib

3. **Git** (for cloning repository)

---

## Step-by-Step Installation

### 1. Install LaTeX

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install texlive-full
# OR minimal installation:
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-science texlive-fonts-recommended
```

#### macOS
```bash
# Install MacTeX (full, ~4GB)
brew install --cask mactex

# OR install BasicTeX (minimal, ~90MB) + packages
brew install --cask basictex
tlmgr install amsmath amssymb amsthm mathtools booktabs hyperref cleveref
```

#### Windows
Download and install MiKTeX from: https://miktex.org/download

### 2. Install Python Dependencies

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install numpy matplotlib
```

### 3. Clone Repository

```bash
git clone https://github.com/dpsnet/Fixed-4D-Topology.git
cd Fixed-4D-Topology/docs/Dimensionics-Physics/paper
```

---

## Verification

### Test LaTeX Compilation

```bash
# Compile the paper
pdflatex Dimensionics_Physics.tex

# Check for errors
# If successful, Dimensionics_Physics.pdf will be generated
```

### Test Figure Generation

```bash
cd figures
python3 generate_figures.py

# Check that 7 PDF files are created
ls *.pdf
```

---

## Troubleshooting

### LaTeX Errors

**Error: File `xxx.sty' not found**
```bash
# Install missing package
# For TeX Live:
tlmgr install <package-name>

# For Ubuntu/Debian:
sudo apt-get install texlive-<package-collection>
```

**Error: ``! LaTeX Error: File `Dimensionics_Physics.aux' not found"``**
```bash
# Run pdflatex twice to resolve cross-references
pdflatex Dimensionics_Physics.tex
pdflatex Dimensionics_Physics.tex
```

### Python Errors

**Error: ``ModuleNotFoundError: No module named 'numpy'``**
```bash
pip install numpy matplotlib
```

**Error: Font issues in figures**
```python
# Add to generate_figures.py at the top:
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Serif'
```

---

## IDE Setup (Optional)

### VS Code

Recommended extensions:
- LaTeX Workshop (James Yu)
- Python
- Markdown All in One

Settings for LaTeX Workshop:
```json
{
  "latex-workshop.latex.recipes": [
    {
      "name": "pdflatex",
      "tools": ["pdflatex"]
    }
  ],
  "latex-workshop.latex.tools": [
    {
      "name": "pdflatex",
      "command": "pdflatex",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "%DOC%"
      ]
    }
  ]
}
```

### Overleaf

To work on Overleaf:
1. Download this repository as ZIP
2. Upload to Overleaf
3. Set main document to `Dimensionics_Physics.tex`

---

## Docker (Advanced)

For a reproducible environment:

```dockerfile
FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy matplotlib

WORKDIR /paper
COPY . .

CMD ["pdflatex", "Dimensionics_Physics.tex"]
```

Build and run:
```bash
docker build -t dimensionics-paper .
docker run -v $(pwd):/paper dimensionics-paper
```

---

## Next Steps

After successful installation:

1. **Read the paper**: `open Dimensionics_Physics.pdf`
2. **Check documentation**: See README.md
3. **Run validation**: `cd figures && python3 generate_figures.py`
4. **Start contributing**: See CONTRIBUTING.md

---

## Getting Help

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (if available)
2. Search existing [GitHub Issues](https://github.com/dpsnet/Fixed-4D-Topology/issues)
3. Open a new issue with:
   - Your operating system
   - LaTeX distribution and version
   - Error messages
   - Steps to reproduce

---

## Version Requirements

| Software | Minimum Version | Recommended |
|----------|----------------|-------------|
| TeX Live | 2020 | 2023+ |
| Python | 3.7 | 3.10+ |
| NumPy | 1.19 | 1.24+ |
| Matplotlib | 3.3 | 3.7+ |

---

**Installation Date**: February 2026  
**Last Updated**: February 2026
