#!/bin/bash
# Compile LaTeX document
# Usage: bash compile.sh

set -e  # Exit on error

echo "========================================"
echo "Compiling Dimensionics Paper"
echo "========================================"

cd "$(dirname "$0")"

echo "Step 1: First pdflatex run..."
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "(Error|Warning|!)" || true

echo ""
echo "Step 2: Running bibtex..."
if [ -f main.aux ]; then
    bibtex main.aux 2>&1 | grep -E "(Error|Warning)" || true
else
    echo "Warning: main.aux not found, skipping bibtex"
fi

echo ""
echo "Step 3: Second pdflatex run..."
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "(Error|Warning|!)" || true

echo ""
echo "Step 4: Final pdflatex run..."
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "(Error|Warning|pages|Output)" || true

echo ""
echo "========================================"
if [ -f main.pdf ]; then
    echo "✓ Compilation successful!"
    echo "Output: main.pdf"
    ls -lh main.pdf
    
    # Count pages
    PAGES=$(pdfinfo main.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
    echo "Pages: $PAGES"
else
    echo "✗ Compilation failed - main.pdf not found"
    exit 1
fi
echo "========================================"
