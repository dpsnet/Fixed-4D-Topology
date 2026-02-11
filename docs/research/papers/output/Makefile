# Makefile for T3 Replacement Research Paper

.PHONY: all clean pdf view

# Default target
all: pdf

# Compile PDF
pdf: paper_final.pdf

paper_final.pdf: paper_final.tex ../references.bib
	@echo "Compiling paper_final.tex..."
	pdflatex -interaction=nonstopmode -halt-on-error paper_final.tex
	-bibtex paper_final
	pdflatex -interaction=nonstopmode -halt-on-error paper_final.tex
	pdflatex -interaction=nonstopmode -halt-on-error paper_final.tex
	@echo "✅ PDF Generated: paper_final.pdf"

# View PDF (Linux)
view: paper_final.pdf
	xdg-open paper_final.pdf || open paper_final.pdf

# Clean auxiliary files
clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
	rm -f *.fdb_latexmk *.fls *.synctex.gz
	@echo "Cleaned auxiliary files"

# Clean everything including PDF
distclean: clean
	rm -f paper_final.pdf
	@echo "Cleaned all files including PDF"

# Check dependencies
check:
	@which pdflatex > /dev/null || (echo "Error: pdflatex not found" && exit 1)
	@which bibtex > /dev/null || echo "Warning: bibtex not found"
	@echo "✅ Dependencies OK"

# Generate statistics
stats: paper_final.pdf
	@echo "Paper Statistics:"
	@pdfinfo paper_final.pdf 2>/dev/null || echo "pdfinfo not available"
	@echo "File size: $$(ls -lh paper_final.pdf | awk '{print $$5}')"
