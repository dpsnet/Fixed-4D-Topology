#!/usr/bin/env python3
"""
Fix bibliography issues
"""

import re

# Read the file
with open('paper_final_fixed.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting bibliography fixes...")

# Fix 1: Remove } at start of reference lines
content = re.sub(r'^(\s*)\}([A-Z])', r'\1\2', content, flags=re.MULTILINE)
print("Fix 1 applied: removed } at start of reference lines")

# Fix 2: Convert \cite{key} Author, Title to \bibitem{key} Author, Title in ref sections
# But first, let's find all the reference sections and fix them
lines = content.split('\n')
result_lines = []
in_ref_section = False

for i, line in enumerate(lines):
    # Check if this looks like a reference entry with \cite
    if '\\cite{' in line and ('D. Sullivan' in line or 'Sapoval' in line or 'Gohberg' in line or 'Przytycki' in line or 'Rivera-Letelier' in line):
        # Convert \cite{key} to [key] format
        line = re.sub(r'\\cite\{([^}]+)\}', r'[\1]', line)
    result_lines.append(line)

content = '\n'.join(result_lines)
print("Fix 2 applied: converted \\cite to [] in references")

# Fix 3: Remove page count markers that look like content
content = re.sub(r'Section \d+ – Page count: approximately \d+ pages\*', '', content)
print("Fix 3 applied: removed page count markers")

# Write the fixed file
with open('paper_final_fixed2.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nFixed file written to: paper_final_fixed2.tex")
