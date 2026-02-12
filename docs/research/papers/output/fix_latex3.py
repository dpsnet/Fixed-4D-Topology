#!/usr/bin/env python3
"""
Fix critical LaTeX syntax errors in preamble
"""

import re

# Read the file
with open('paper_fixed2.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting critical fixes...")

# Fix 1: Fix newtheorem definitions
content = content.replace('\\newtheorem{theorem{Theorem}[section]', 
                         '\\newtheorem{theorem}{Theorem}[section]')
print("Fix 1 applied: theorem definition")

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
print("Fix 2 applied: math operators")

# Fix 3: Fix }{
content = content.replace('\\Vol{Vol}', '\\Vol}{Vol}')
content = content.replace('\\Tr{Tr}', '\\Tr}{Tr}')
content = content.replace('\\Spec{Spec}', '\\Spec}{Spec}')
content = content.replace('\\dimH{dim_H}', '\\dimH}{dim_H}')
content = content.replace('\\Fix{Fix}', '\\Fix}{Fix}')
print("Fix 3 applied")

# Write the fixed file
with open('paper_fixed3.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed file written to: paper_fixed3.tex")
