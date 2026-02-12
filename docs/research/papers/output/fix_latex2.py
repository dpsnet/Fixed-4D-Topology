#!/usr/bin/env python3
"""
Additional fixes for LaTeX syntax errors
"""

import re

# Read the file
with open('paper_fixed.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting additional fixes...")

# Fix 1: Fix remaining $s^\textit{$ -> $s^*$
content = content.replace('$s^\\textit{$', '$s^*$')
print("Fix 1 applied")

# Fix 2: Fix \textit{ after formula, given by, set.
content = content.replace('formula\\textit{', 'formula')
content = content.replace('given by\\textit{', 'given by')
content = content.replace('set.\\textit{', 'set.')
content = content.replace('equation\\textit{', 'equation')
print("Fix 2 applied")

# Fix 3: Fix orphaned }{ patterns - these are likely errors
# Pattern: word}{ should be word}{ or word} {
content = content.replace('}){', '}{')
print("Fix 3 applied")

# Fix 4: Fix \frac{d\gamma_... issue
# Original: \frac{d\gamma_\textit{\mu_{PS}{d\mu_{PS}
# Should be: \frac{d\gamma_\mu_{PS}}{d\mu_{PS}}
content = content.replace('\\frac{d\\gamma_\\textit{\\mu_{PS}{d\\mu_{PS}', 
                         '\\frac{d\\gamma_* \\mu_{PS}}{d\\mu_{PS}')
print("Fix 4 applied")

# Fix 5: Fix remaining \textit{ issues in lines
lines = content.split('\n')
result_lines = []
for line in lines:
    # Remove standalone \textit{ at end of lines
    if line.rstrip().endswith('\\textit{'):
        line = line.rstrip()[:-8]  # Remove \textit{
    result_lines.append(line)
content = '\n'.join(result_lines)
print("Fix 5 applied")

# Fix 6: Fix specific patterns that look like this:
# }\textit{where -> where
content = content.replace('}\\textit{where', ' where')
content = content.replace('}\\textit{', ' ')
print("Fix 6 applied")

# Fix 7: Fix measure of the limit set.\textit{
content = content.replace('limit set.\\textit{', 'limit set.')
print("Fix 7 applied")

# Fix 8: Fix remaining }\textit{$s^ patterns
content = content.replace('}\\textit{$s^', '$s^')
print("Fix 8 applied")

# Fix 9: Fix orphaned closing braces that break math
# Look for }{ patterns that should be }{ or }{
content = content.replace(')}{', ')}{')
print("Fix 9 applied")

# Fix 10: Fix \gamma' formatting
content = content.replace("\\gamma'_{", "\\gamma'_{")
print("Fix 10 applied")

# Fix 11: Fix remaining brace issues in math
content = content.replace('^{\\Gamma', '^{\\Gamma}')
print("Fix 11 applied")

# Fix 12: Count and report remaining \textit{
remaining = content.count('\\textit{')
print(f"\nRemaining \\textit{{ occurrences: {remaining}")

# Write the fixed file
with open('paper_fixed2.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed file written to: paper_fixed2.tex")
