# Makefile for arXiv paper
# Usage: make [target]

.PHONY: all clean pdf submit count check

# Default target: compile PDF
all: pdf

# Compile main PDF
pdf: main.tex macros/commands.tex sections/*.tex
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex
	@echo "=========================================="
	@echo "PDF generated: main.pdf"
	@echo "=========================================="

# Clean auxiliary files
clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg
	rm -f sections/*.aux
	rm -f macros/*.aux
	@echo "Cleaned auxiliary files"

# Deep clean (including PDF)
distclean: clean
	rm -f main.pdf
	@echo "Cleaned all generated files"

# Count words/lines
count:
	@echo "Word count (approximate):"
	@wc -w sections/*.tex main.tex | tail -1
	@echo ""
	@echo "Line count:"
	@wc -l sections/*.tex main.tex macros/*.tex | tail -1

# Check LaTeX syntax
check:
	@echo "Checking LaTeX syntax..."
	@pdflatex -interaction=nonstopmode -draftmode main.tex > /dev/null 2>&1 && echo "✓ Syntax OK" || echo "✗ Errors found"

# Create submission archive
submit: pdf
	@rm -f arxiv-submission.zip
	@zip -r arxiv-submission.zip \
		main.tex \
		macros/commands.tex \
		sections/*.tex \
		main.pdf \
		-x "*/.*" -x "*/__MACOSX/*"
	@echo "=========================================="
	@echo "Submission archive: arxiv-submission.zip"
	@echo "=========================================="

# Help
help:
	@echo "Available targets:"
	@echo "  make pdf     - Compile PDF (default)"
	@echo "  make clean   - Remove auxiliary files"
	@echo "  make count   - Count words and lines"
	@echo "  make check   - Check LaTeX syntax"
	@echo "  make submit  - Create arXiv submission zip"
	@echo "  make help    - Show this help"
