#!/usr/bin/env python3
"""
Comprehensive fix for LaTeX syntax errors
"""

import re

# Read the original file (not the partially fixed ones)
with open('paper_final.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting comprehensive fixes...")

# Fix 1: Fix newtheorem definitions that got corrupted
content = content.replace('\\newtheorem{theorem{Theorem}[section]', 
                         '\\newtheorem{theorem}{Theorem}[section]')

# Fix 2: Fix DeclareMathOperator definitions  
content = content.replace('\\DeclareMathOperator{\\Vol{Vol}', 
                         '\\DeclareMathOperator{\\Vol}{Vol}')
content = content.replace('\\DeclareMathOperator{\\Tr{Tr}', 
                         '\\DeclareMathOperator{\\Tr}{Tr}')
content = content.replace('\\DeclareMathOperator{\\Spec{Spec}', 
                         '\\DeclareMathOperator{\\Spec}{Spec}')
content = content.replace('\\DeclareMathOperator{\\dimH{dim_H}', 
                         '\\DeclareMathOperator{\\dimH}{dim_H}')
content = content.replace('\\DeclareMathOperator{\\Fix{Fix}', 
                         '\\DeclareMathOperator{\\Fix}{Fix}')
print("Preamble fixes applied")

# Fix 3: Fix $s^\textit{$ patterns -> $s^*$
content = content.replace('$s^\\textit{$', '$s^*$')
content = content.replace('$s^*}', '$s^*$')
print("s^* fixes applied")

# Fix 4: Fix }Let, }as, }and, }where patterns
content = content.replace('}Let', 'Let')
content = content.replace('}as', 'as')
content = content.replace('}and', 'and')
content = content.replace('}where', 'where')
print("Brace fixes applied")

# Fix 5: Fix orphaned \textit{ after text
content = content.replace('formula\\textit{', 'formula')
content = content.replace('given by\\textit{', 'given by')
content = content.replace('set.\\textit{', 'set.')
content = content.replace('equation\\textit{', 'equation')
content = content.replace('}\\textit{where', ' where')
content = content.replace('}\\textit{', ' ')
content = content.replace('\\textit{', '')  # Remove all remaining \textit{
print("\textit fixes applied")

# Fix 6: Fix reference patterns with }Title\textit{
# Change these to just Title,
lines = content.split('\n')
result_lines = []
for line in lines:
    # Fix patterns like: }Applications of...
    if line.strip().startswith('}') and len(line.strip()) > 1:
        next_char = line.strip()[1]
        if next_char.isupper() or next_char in 'ÀÉÈÊËÏÎÔÖÛÜÇ':
            line = line.replace('}', '', 1)
    result_lines.append(line)
content = '\n'.join(result_lines)
print("Reference title fixes applied")

# Fix 7: Fix specific math issues
# Fix \frac with wrong braces
content = content.replace('}){\\exp', '}}{\\exp')
content = content.replace('}){\\Gamma', '}}{\\Gamma')
content = content.replace('\\mathrm{Berk}$', '\\mathrm{Berk}}$')
print("Math fixes applied")

# Fix 8: Fix d\gamma_\mu issue
content = content.replace('\\frac{d\\gamma_\\textit{\\mu_{PS}{d\\mu_{PS}', 
                         '\\frac{d\\gamma_* \\mu_{PS}}{d\\mu_{PS}')
content = content.replace('\\frac{d\\gamma_{* \\mu_{PS}}{d\\mu_{PS}', 
                         '\\frac{d\\gamma_* \\mu_{PS}}{d\\mu_{PS}')
print("d\\gamma fixes applied")

# Fix 9: Fix remaining }{ patterns that shouldn't exist
# Be careful not to break valid }{ constructs
content = content.replace('}){(4\\pi', '}{(4\\pi')
content = content.replace('}{\\Gamma((1', '}}{\\Gamma((1')
print("Brace pair fixes applied")

# Fix 10: Remove orphaned closing braces at start of lines
lines = content.split('\n')
result_lines = []
for line in lines:
    stripped = line.lstrip()
    if stripped.startswith('}') and len(stripped) > 1 and stripped[1].isupper():
        line = line.replace('}', '', 1)
    result_lines.append(line)
content = '\n'.join(result_lines)
print("Orphaned brace fixes applied")

# Fix 11: Fix theorem statement braces
content = content.replace('\\textbf{Theorem A.} }', '\\textbf{Theorem A.} ')
content = content.replace('\\textbf{Theorem B.} }', '\\textbf{Theorem B.} ')
content = content.replace('Theorem A.} }', 'Theorem A.} ')
content = content.replace('Theorem B.} }', 'Theorem B.} ')
print("Theorem brace fixes applied")

# Fix 12: Fix specific line from original file
content = content.replace('\\frac{d\\gamma_\\textit{\\mu_{PS}}{d\\mu_{PS}',
                         '\\frac{d\\gamma_* \\mu_{PS}}{d\\mu_{PS}')
print("Final d\\gamma fix applied")

# Write the fixed file
with open('paper_final_fixed.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nFixed file written to: paper_final_fixed.tex")
print(f"File size: {len(content)} characters")
