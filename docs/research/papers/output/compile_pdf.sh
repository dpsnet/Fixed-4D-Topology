#!/bin/bash

# T3 Replacement Research Paper PDF Compilation Script
# Compiles the LaTeX source to generate PDF

set -e

echo "========================================="
echo "T3 Replacement Research Paper Compilation"
echo "========================================="
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex not found. Please install LaTeX."
    echo "Recommended: TeX Live (https://tug.org/texlive/)"
    exit 1
fi

# Check if bibtex is available
if ! command -v bibtex &> /dev/null; then
    echo "Warning: bibtex not found. Bibliography may not be processed correctly."
fi

echo "Compiling paper_final.tex..."
echo ""

# First compilation
pdflatex -interaction=nonstopmode -halt-on-error paper_final.tex || {
    echo "Error: First compilation failed"
    exit 1
}

# Process bibliography if .bib file exists
if [ -f "../references.bib" ]; then
    echo "Processing bibliography..."
    bibtex paper_final || echo "Warning: bibtex processing failed"
    
    # Second compilation (needed for bibliography)
    pdflatex -interaction=nonstopmode -halt-on-error paper_final.tex || {
        echo "Warning: Second compilation failed"
    }
fi

# Final compilation (for references)
pdflatex -interaction=nonstopmode -halt-on-error paper_final.tex || {
    echo "Warning: Final compilation failed"
}

# Check if PDF was generated
if [ -f "paper_final.pdf" ]; then
    echo ""
    echo "========================================="
    echo "✅ PDF Generated Successfully!"
    echo "========================================="
    echo "File: paper_final.pdf"
    ls -lh paper_final.pdf | awk '{print "Size: " $5}'
    pdfinfo paper_final.pdf 2>/dev/null | grep "Pages:" || echo "Pages: Check with pdfinfo"
    echo ""
    echo "Output location:"
    pwd
    echo "========================================="
else
    echo ""
    echo "Error: PDF generation failed"
    echo "Check paper_final.log for errors"
    exit 1
fi
