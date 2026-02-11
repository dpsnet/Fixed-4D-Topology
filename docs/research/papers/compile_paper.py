#!/usr/bin/env python3
"""
Annals of Mathematics Paper Compilation Script
===============================================

This script compiles the paper sections into a complete document,
generates LaTeX version, and performs validation checks.

Usage:
    python compile_paper.py [--format {markdown,latex,pdf}] [--output OUTPUT]

Author: Research Team
Date: February 2026
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Configuration
SECTIONS_DIR = Path(__file__).parent / "sections"
OUTPUT_DIR = Path(__file__).parent / "output"

SECTIONS = [
    "01_INTRODUCTION.md",
    "02_PRELIMINARIES.md",
    "03_TRACE_FORMULA_PROOF.md",
    "04_GIBBS_MEASURE_PROOF.md",
]

METADATA = {
    "title": "Fractal Spectral Asymptotics and p-adic Thermodynamic Formalism: "
             "A Unified Framework for Kleinian Groups and Non-Archimedean Dynamics",
    "authors": [
        "Research Team"
    ],
    "date": "February 2026",
    "journal": "Annals of Mathematics",
    "msc_classes": ["37F30", "37D35", "11F72", "28A80", "37P50", "58J50"],
}


class PaperCompiler:
    """Compiles paper sections into complete documents."""
    
    def __init__(self):
        self.sections_content = {}
        self.citations = set()
        self.theorems = []
        self.errors = []
        self.warnings = []
    
    def load_sections(self):
        """Load all section files."""
        print("Loading section files...")
        
        for section_file in SECTIONS:
            section_path = SECTIONS_DIR / section_file
            if not section_path.exists():
                self.errors.append(f"Missing section file: {section_file}")
                continue
            
            with open(section_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.sections_content[section_file] = content
                print(f"  ✓ Loaded {section_file} ({len(content)} chars)")
        
        if self.errors:
            print(f"\nErrors: {len(self.errors)}")
            for error in self.errors:
                print(f"  ✗ {error}")
            return False
        
        return True
    
    def validate_content(self):
        """Validate content consistency."""
        print("\nValidating content...")
        
        # Check for theorem numbering consistency
        theorem_pattern = r'\*\*Theorem\s+([0-9.]+)\.\*\*'
        
        for section_file, content in self.sections_content.items():
            theorems = re.findall(theorem_pattern, content)
            for thm in theorems:
                self.theorems.append((section_file, thm))
        
        # Check for citation consistency
        citation_pattern = r'\[([A-Z][a-z]+\d{2,4}(?:,\s*\w+)?)\]'
        
        for content in self.sections_content.values():
            cites = re.findall(citation_pattern, content)
            self.citations.update(cites)
        
        print(f"  ✓ Found {len(self.theorems)} theorems")
        print(f"  ✓ Found {len(self.citations)} unique citations")
        
        # Check for common issues
        self._check_common_issues()
        
        return len(self.errors) == 0
    
    def _check_common_issues(self):
        """Check for common formatting issues."""
        issues = []
        
        for section_file, content in self.sections_content.items():
            # Check for unclosed math
            math_inline = content.count('$')
            if math_inline % 2 != 0:
                issues.append(f"{section_file}: Unmatched inline math delimiters")
            
            # Check for unclosed display math
            display_math = content.count('$$')
            if display_math % 2 != 0:
                issues.append(f"{section_file}: Unmatched display math delimiters")
            
            # Check for broken references
            broken_refs = re.findall(r'\[\s*\?\s*\]', content)
            if broken_refs:
                issues.append(f"{section_file}: {len(broken_refs)} broken references")
            
            # Check for TODO markers
            todos = re.findall(r'TODO|FIXME|XXX', content, re.IGNORECASE)
            if todos:
                self.warnings.append(f"{section_file}: {len(todos)} TODO markers")
        
        if issues:
            for issue in issues:
                self.errors.append(issue)
    
    def generate_markdown(self):
        """Generate complete markdown document."""
        print("\nGenerating Markdown...")
        
        lines = []
        
        # Header
        lines.extend([
            f"# {METADATA['title']}",
            "",
            "## Authors",
            "",
        ])
        for author in METADATA['authors']:
            lines.append(f"- {author}")
        
        lines.extend([
            "",
            f"**Date:** {METADATA['date']}",
            f"**Target Journal:** {METADATA['journal']}",
            "",
            "**MSC Classification:** " + ", ".join(METADATA['msc_classes']),
            "",
            "---",
            "",
        ])
        
        # Abstract placeholder
        lines.extend([
            "## Abstract",
            "",
            "We establish a unified framework connecting fractal spectral theory with p-adic thermodynamic "
            "formalism. Our main results include: (1) a fractal Weyl law for Kleinian groups relating "
            "Laplacian eigenvalue asymptotics to the Hausdorff dimension of limit sets, and (2) a p-adic "
            "Bowen formula characterizing the dimension of p-adic Julia sets via topological pressure. "
            "These theorems reveal deep structural parallels between Archimedean and non-Archimedean "
            "dynamical systems. We provide rigorous proofs, numerical verification for over 1,000 test "
            "cases, and applications to arithmetic geometry and quantum chaos.",
            "",
            "---",
            "",
        ])
        
        # Sections
        for section_file in SECTIONS:
            if section_file in self.sections_content:
                content = self.sections_content[section_file]
                # Remove the first h1 heading as it's in the title
                content = re.sub(r'^#\s+.*\n+', '', content)
                lines.append(content)
                lines.extend(["", "---", ""])
        
        # References section placeholder
        lines.extend([
            "# References",
            "",
            f"Total citations: {len(self.citations)}",
            "",
            "[References to be compiled from individual sections]",
            "",
        ])
        
        return "\n".join(lines)
    
    def generate_latex(self):
        """Generate LaTeX document."""
        print("Generating LaTeX...")
        
        lines = []
        
        # Preamble
        lines.extend([
            r"\documentclass[11pt]{amsart}",
            r"",
            r"% Packages",
            r"\usepackage{amsmath,amssymb,amsthm}",
            r"\usepackage{mathtools}",
            r"\usepackage{mathrsfs}",
            r"\usepackage{geometry}",
            r"\usepackage{hyperref}",
            r"\usepackage{cleveref}",
            r"",
            r"% Page geometry",
            r"\geometry{letterpaper, margin=1in}",
            r"",
            r"% Theorem environments",
            r"\theoremstyle{plain}",
            r"\newtheorem{theorem}{Theorem}[section]",
            r"\newtheorem{lemma}[theorem]{Lemma}",
            r"\newtheorem{proposition}[theorem]{Proposition}",
            r"\newtheorem{corollary}[theorem]{Corollary}",
            r"",
            r"\theoremstyle{definition}",
            r"\newtheorem{definition}[theorem]{Definition}",
            r"\newtheorem{example}[theorem]{Example}",
            r"\newtheorem{remark}[theorem]{Remark}",
            r"",
            r"% Math operators",
            r"\DeclareMathOperator{\Vol}{Vol}",
            r"\DeclareMathOperator{\Tr}{Tr}",
            r"\DeclareMathOperator{\Spec}{Spec}",
            r"\DeclareMathOperator{\dimH}{dim_H}",
            r"\DeclareMathOperator{\Fix}{Fix}",
            r"",
            r"% Title information",
            rf"\title{{{METADATA['title']}}}",
            rf"\author{{{METADATA['authors'][0]}}}",
            rf"\date{{{METADATA['date']}}}",
            r"",
            r"\begin{document}",
            r"",
            r"\maketitle",
            r"",
            r"\begin{abstract}",
            r"We establish a unified framework connecting fractal spectral theory with p-adic thermodynamic "
            r"formalism. Our main results include: (1) a fractal Weyl law for Kleinian groups relating "
            r"Laplacian eigenvalue asymptotics to the Hausdorff dimension of limit sets, and (2) a p-adic "
            r"Bowen formula characterizing the dimension of p-adic Julia sets via topological pressure. "
            r"These theorems reveal deep structural parallels between Archimedean and non-Archimedean "
            r"dynamical systems. We provide rigorous proofs, numerical verification for over 1,000 test "
            r"cases, and applications to arithmetic geometry and quantum chaos.",
            r"\end{abstract}",
            r"",
            r"\maketitle",
            r"",
        ])
        
        # Convert sections
        for section_file in SECTIONS:
            if section_file in self.sections_content:
                content = self.sections_content[section_file]
                latex_content = self._markdown_to_latex(content)
                lines.append(latex_content)
                lines.append("")
        
        # End document
        lines.extend([
            r"\begin{thebibliography}{99}",
            r"",
            r"% Bibliography to be completed",
            r"",
            r"\end{thebibliography}",
            r"",
            r"\end{document}",
        ])
        
        return "\n".join(lines)
    
    def _markdown_to_latex(self, content):
        """Convert Markdown content to LaTeX."""
        # Remove YAML frontmatter if present
        content = re.sub(r'^---\s*\n.*?---\s*\n', '', content, flags=re.DOTALL)
        
        # Convert section headers
        content = re.sub(r'^#\s+(.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^##\s+(.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^###\s+(.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        
        # Convert bold and italic
        content = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\\textbf{\\textit{\1}}', content)
        content = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', content)
        
        # Convert display math
        content = re.sub(r'\$\$\s*\n?([^$]+)\n?\$\$', r'\\[\1\\]', content)
        
        # Convert inline math (preserve existing $)
        # content = re.sub(r'(?<!\$)\$([^$]+)\$(?!\$)', r'$\1$', content)
        
        # Convert theorem environments
        content = re.sub(
            r'\*\*Theorem\s+([0-9.]+)\s*\(([^(]+)\)\.?\*\*',
            r'\\begin{theorem}[\2]',
            content
        )
        content = re.sub(r'\*\*Theorem\s+([0-9.]+)\.?\*\*', r'\\begin{theorem}', content)
        content = re.sub(r'\*\*Lemma\s+([0-9.]+)\.?\*\*', r'\\begin{lemma}', content)
        content = re.sub(r'\*\*Proposition\s+([0-9.]+)\.?\*\*', r'\\begin{proposition}', content)
        content = re.sub(r'\*\*Corollary\s+([0-9.]+)\.?\*\*', r'\\begin{corollary}', content)
        content = re.sub(r'\*\*Definition\s+([0-9.]+)\.?\*\*', r'\\begin{definition}', content)
        
        # Close environments (simplified - would need proper nesting)
        content = re.sub(r'\$\\square\$', r'\\end{proof}', content)
        
        # Convert citations
        content = re.sub(r'\[([A-Z][a-z]+\d{2,4})\]', r'\\cite{\1}', content)
        
        # Convert lists
        content = re.sub(r'^\s*-\s+(.+)$', r'\\item \1', content, flags=re.MULTILINE)
        
        # Wrap itemize environments
        lines = content.split('\n')
        result = []
        in_itemize = False
        
        for line in lines:
            if line.strip().startswith('\\item') and not in_itemize:
                result.append('\\begin{itemize}')
                in_itemize = True
            elif not line.strip().startswith('\\item') and in_itemize and line.strip():
                result.append('\\end{itemize}')
                in_itemize = False
            result.append(line)
        
        if in_itemize:
            result.append('\\end{itemize}')
        
        content = '\n'.join(result)
        
        # Remove horizontal rules
        content = re.sub(r'\n---\s*\n', r'\n\n', content)
        
        # Escape special characters
        content = content.replace('&', r'\&')
        content = content.replace('%', r'\%')
        
        return content
    
    def save_output(self, content, filename, format_type):
        """Save output file."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        output_path = OUTPUT_DIR / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Saved: {output_path}")
        return output_path
    
    def compile_pdf(self, latex_path):
        """Compile LaTeX to PDF if pdflatex is available."""
        print("\nAttempting PDF compilation...")
        
        # Check for pdflatex
        import shutil
        if not shutil.which('pdflatex'):
            print("  ✗ pdflatex not found. Skipping PDF generation.")
            return None
        
        try:
            import subprocess
            
            # Run pdflatex twice for references
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-output-directory', str(OUTPUT_DIR), str(latex_path)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    print(f"  ✗ pdflatex failed (run {i+1})")
                    print(result.stderr[:500])
                    return None
            
            pdf_path = latex_path.with_suffix('.pdf')
            if pdf_path.exists():
                print(f"  ✓ Generated PDF: {pdf_path}")
                return pdf_path
            
        except subprocess.TimeoutExpired:
            print("  ✗ pdflatex timed out")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        return None
    
    def generate_summary(self):
        """Generate compilation summary."""
        summary = []
        
        summary.append("=" * 60)
        summary.append("COMPILATION SUMMARY")
        summary.append("=" * 60)
        summary.append("")
        summary.append(f"Title: {METADATA['title']}")
        summary.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        summary.append("Sections Compiled:")
        for section in SECTIONS:
            status = "✓" if section in self.sections_content else "✗"
            summary.append(f"  {status} {section}")
        summary.append("")
        summary.append(f"Total Theorems: {len(self.theorems)}")
        summary.append(f"Total Citations: {len(self.citations)}")
        summary.append("")
        
        if self.errors:
            summary.append(f"Errors: {len(self.errors)}")
            for error in self.errors:
                summary.append(f"  ✗ {error}")
            summary.append("")
        
        if self.warnings:
            summary.append(f"Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                summary.append(f"  ⚠ {warning}")
            summary.append("")
        
        summary.append("=" * 60)
        
        return "\n".join(summary)


def main():
    parser = argparse.ArgumentParser(
        description="Compile Annals of Mathematics paper sections"
    )
    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'latex', 'pdf', 'all'],
        default='all',
        help='Output format (default: all)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory (default: ./output)'
    )
    parser.add_argument(
        '--validate-only', '-v',
        action='store_true',
        help='Only validate, do not generate output'
    )
    
    args = parser.parse_args()
    
    if args.output:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output)
    
    compiler = PaperCompiler()
    
    # Load sections
    if not compiler.load_sections():
        print("\nFailed to load all sections.")
        sys.exit(1)
    
    # Validate content
    if not compiler.validate_content():
        print("\nValidation failed with errors.")
        for error in compiler.errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    
    if args.validate_only:
        print(compiler.generate_summary())
        sys.exit(0)
    
    # Generate outputs
    outputs = []
    
    if args.format in ('markdown', 'all'):
        md_content = compiler.generate_markdown()
        md_path = compiler.save_output(md_content, 'paper.md', 'markdown')
        outputs.append(md_path)
    
    if args.format in ('latex', 'pdf', 'all'):
        latex_content = compiler.generate_latex()
        latex_path = compiler.save_output(latex_content, 'paper.tex', 'latex')
        outputs.append(latex_path)
        
        if args.format in ('pdf', 'all'):
            pdf_path = compiler.compile_pdf(latex_path)
            if pdf_path:
                outputs.append(pdf_path)
    
    # Print summary
    print(compiler.generate_summary())
    print(f"\nOutput files:")
    for output in outputs:
        if output:
            print(f"  - {output}")
    
    print("\n✓ Compilation complete!")


if __name__ == '__main__':
    main()
