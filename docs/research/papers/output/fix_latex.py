#!/usr/bin/env python3
"""
Fix LaTeX syntax errors in paper_final.tex
"""

import re

# Read the file
with open('paper_final.tex', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting fixes...")

# Fix 1: Fix $s^\textit{$ patterns -> $s^*$
content = re.sub(r'\$s\^\\\\textit\{\$', '$s^*$', content)
print("Fix 1 applied: $s^\\textit{$ -> $s^*$")

# Fix 2: Fix $s^*} patterns in various contexts
content = re.sub(r'\$s\^\*\}', '$s^*$', content)
print("Fix 2 applied: $s^*} -> $s^*$")

# Fix 3: Fix }Let -> Let (remove extra braces before Let)
content = re.sub(r'\}Let', 'Let', content)
print("Fix 3 applied: }Let -> Let")

# Fix 4: Fix formula\textit{ -> formula (remove spurious \textit{ after formulas)
content = re.sub(r'formula\\\\textit\{', 'formula', content)
print("Fix 4 applied: formula\\textit{ -> formula")

# Fix 5: Fix set.\textit{ -> set. (remove spurious \textit{)
content = re.sub(r'set\.\\\\textit\{', 'set.', content)
print("Fix 5 applied: set.\\textit{ -> set.")

# Fix 6: Fix given by\textit{ -> given by
content = re.sub(r'given by\\\\textit\{', 'given by', content)
print("Fix 6 applied: given by\\textit{ -> given by")

# Fix 7: Fix }as -> as (remove extra brace before as)
content = re.sub(r'\}as', 'as', content)
print("Fix 7 applied: }as -> as")

# Fix 8: Fix }and -> and
content = re.sub(r'\}and', 'and', content)
print("Fix 8 applied: }and -> and")

# Fix 9: Fix }where -> where
content = re.sub(r'\}where', 'where', content)
print("Fix 9 applied: }where -> where")

# Fix 10: Fix \textit{ at the end of lines (unclosed)
content = re.sub(r'\\\\textit\{\s*$', '', content, flags=re.MULTILINE)
print("Fix 10 applied: orphaned \\textit{ at EOL")

# Fix 11-44: Fix }Title patterns in references
reference_fixes = [
    (r'\}Applications', 'Applications'),
    (r'\}Hyperbolic', 'Hyperbolic'),
    (r'\}Dynamics', 'Dynamics'),
    (r'\}Distribution', 'Distribution'),
    (r'\}Spectral', 'Spectral'),
    (r'\}Equilibrium', 'Equilibrium'),
    (r'\}Hausdorff', 'Hausdorff'),
    (r'\}Some', 'Some'),
    (r'\}Generalizations', 'Generalizations'),
    (r'\}Equidistribution', 'Equidistribution'),
    (r'\}Th', 'Th'),  # Théorème
    (r'\}Dynamique', 'Dynamique'),
    (r'\}Espace', 'Espace'),
    (r'\}Patterson', 'Patterson'),
    (r'\}The Laplace', 'The Laplace'),
    (r'\}Asymptotics', 'Asymptotics'),
    (r'\}Classical', 'Classical'),
    (r'\}Thermodynamic', 'Thermodynamic'),
    (r'\}Harmonic', 'Harmonic'),
    (r'\}Repellers', 'Repellers'),
    (r'\}The Arithmetic', 'The Arithmetic'),
    (r'\}Dimension', 'Dimension'),
    (r'\}Geometric', 'Geometric'),
    (r'\}The density', 'The density'),
    (r'\}p-adic', 'p-adic'),
    (r'\}Patterson-Sullivan', 'Patterson-Sullivan'),
    (r'\}The', 'The'),
    (r'\}Lectures', 'Lectures'),
]

for pattern, replacement in reference_fixes:
    content = re.sub(pattern, replacement, content)
print("Fix 11-44 applied: reference title fixes")

# Fix 45: Fix d\gamma_\textit{\mu issue
# Use raw string for replacement to avoid \g issues
content = re.sub(r'd\\\\gamma_\\\\textit\{', r'd\\gamma_{', content)
print("Fix 45 applied: d\\gamma_\\textit{ -> d\\gamma{")

# Fix 46: Fix math inside \textit (shouldn't happen)
content = re.sub(r'\\\\textit\{\$([^$]+)\$\}', r'$\1$', content)
print("Fix 46 applied: \\textit{$...$} -> $")

# Fix 47: Fix }\textit{ patterns -> just the text
content = re.sub(r'\}\\\\textit\{', '', content)
print("Fix 47 applied: }\\textit{ -> ''")

# Fix 48: Fix orphaned } before text in references
content = re.sub(r'\}([A-Z][a-z]+)', r'\1', content)
print("Fix 48 applied: }Word -> Word")

# Fix 49: Fix specific theorem statement issues
content = re.sub(r'Theorem A\.\}\}', 'Theorem A.}', content)
content = re.sub(r'Theorem B\.\}\}', 'Theorem B.}', content)
print("Fix 49 applied: Theorem statement braces")

# Fix 50: Clean up any remaining }{ patterns
content = re.sub(r'\}\{', '{', content)
print("Fix 50 applied: }{ -> {")

# Fix 51: Fix remaining \textit{ in bibliography
# Pattern: Author, }Title\textit{, -> Author, Title,
def fix_bib_title(match):
    before = match.group(1)
    title = match.group(2)
    return f"{before}{title},"

content = re.sub(r'([,\s])\}([^,]+)\\\\textit\{,', fix_bib_title, content)
print("Fix 51 applied: bibliography title formatting")

# Fix 52: Fix remaining \textit{ in references with different pattern
# Pattern: word\textit{ -> word
content = re.sub(r'([a-z])\\\\textit\{', r'\1', content)
print("Fix 52 applied: word\\textit{ -> word")

# Fix 53: Remove orphaned \textit{ at start of lines
content = re.sub(r'^\\\\textit\{', '', content, flags=re.MULTILINE)
print("Fix 53 applied: ^\\textit{ -> ''")

# Fix 54: Fix double closing braces where not needed
content = re.sub(r'\}\}', '}', content)
print("Fix 54 applied: }} -> }")

# Fix 55: Fix specific issue with mu_{PS}
content = re.sub(r'\{\\\\mu\}\{d\\\\mu\}', r'{\\mu}{d\\mu}', content)
print("Fix 55 applied: mu formatting")

# Fix 56: Fix gamma' formatting
content = re.sub(r'\\\\gamma\'_\{', r'\\gamma\'_{', content)
print("Fix 56 applied: gamma' formatting")

# Fix 57: Fix orphaned closing braces at start of lines
lines = content.split('\n')
result_lines = []
for line in lines:
    # Check if line starts with } followed by text
    if line.startswith('}') and len(line) > 1 and line[1].isalpha():
        line = line[1:]
    result_lines.append(line)
content = '\n'.join(result_lines)
print("Fix 57 applied: }Text at line start -> Text")

print("\nChecking for remaining issues...")

# Count remaining issues
remaining_issues = []
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '\\textit{' in line:
        open_braces = line.count('{')
        close_braces = line.count('}')
        if open_braces != close_braces:
            remaining_issues.append((i, line.strip()[:100]))

if remaining_issues:
    print(f"Found {len(remaining_issues)} lines with potential brace issues:")
    for line_num, line_text in remaining_issues[:10]:
        print(f"  Line {line_num}: {line_text}")
else:
    print("No obvious brace issues found!")

# Check for orphaned }
orphaned_braces = []
for i, line in enumerate(lines, 1):
    if line.strip().startswith('}') and len(line.strip()) > 1 and line.strip()[1].isupper():
        orphaned_braces.append((i, line.strip()[:80]))

if orphaned_braces:
    print(f"\nFound {len(orphaned_braces)} lines with orphaned }} at start:")
    for line_num, line_text in orphaned_braces[:10]:
        print(f"  Line {line_num}: {line_text}")

# Write the fixed file
with open('paper_fixed.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFixed file written to: paper_fixed.tex")
print(f"File size: {len(content)} characters")
