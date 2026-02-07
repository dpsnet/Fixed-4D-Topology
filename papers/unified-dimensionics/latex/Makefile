# Makefile for Dimensionics Paper
# Reviews in Mathematical Physics Submission
# Compatible with AlmaLinux 9 / TeX Live 2020

.PHONY: all clean pdf view

# Main document name
MAIN = main

# Default target: compile full PDF
all: pdf

# Compile PDF with bibliography
pdf:
	@echo "Compiling Dimensionics Paper..."
	@echo "Pass 1/3..."
	@pdflatex -interaction=nonstopmode $(MAIN).tex > /dev/null 2>&1
	@echo "Processing bibliography..."
	@bibtex $(MAIN) > /dev/null 2>&1
	@echo "Pass 2/3..."
	@pdflatex -interaction=nonstopmode $(MAIN).tex > /dev/null 2>&1
	@echo "Pass 3/3..."
	@pdflatex -interaction=nonstopmode $(MAIN).tex > /dev/null 2>&1
	@echo "✅ Compilation complete: $(MAIN).pdf"
	@ls -lh $(MAIN).pdf

# Quick compile (no bibliography)
quick:
	pdflatex $(MAIN).tex

# View the generated PDF (Linux)
view: pdf
	@echo "Opening PDF..."
	-evince $(MAIN).pdf 2>/dev/null || xdg-open $(MAIN).pdf 2>/dev/null || echo "PDF: $(MAIN).pdf"

# Clean auxiliary files
clean:
	@rm -f *.aux *.log *.out *.toc *.bbl *.blg
	@rm -f *.fdb_latexmk *.fls *.synctex.gz
	@rm -f chapters/*.aux
	@echo "Cleaned auxiliary files"

# Clean everything including PDF
distclean: clean
	@rm -f $(MAIN).pdf
	@echo "Cleaned all files"

# Check compilation log for issues
check:
	@echo "Checking for errors..."
	@grep -i "error" $(MAIN).log 2>/dev/null || echo "✓ No errors found"
	@echo "Checking for warnings..."
	@grep -i "warning" $(MAIN).log 2>/dev/null | head -5 || echo "✓ No warnings"

# Help
help:
	@echo "Dimensionics Paper - LaTeX Compilation"
	@echo "======================================"
	@echo ""
	@echo "Targets:"
	@echo "  make pdf       - Compile full PDF with bibliography"
	@echo "  make quick     - Quick compile (no bibliography)"
	@echo "  make view      - Compile and open PDF"
	@echo "  make clean     - Remove auxiliary files"
	@echo "  make distclean - Remove all generated files"
	@echo "  make check     - Check for errors/warnings"
	@echo "  make help      - Show this help"
	@echo ""
	@echo "Requirements: pdflatex, bibtex (TeX Live)"
