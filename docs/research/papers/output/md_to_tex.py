#!/usr/bin/env python3
"""
Convert Markdown to clean LaTeX
"""

import re

# Read the markdown file
with open('paper_final.md', 'r', encoding='utf-8') as f:
    content = f.read()

print("Converting Markdown to LaTeX...")

# LaTeX preamble
preamble = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{mathtools}
\usepackage{mathrsfs}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{array}
\usepackage{longtable}
\usepackage{listings}
\usepackage{xcolor}

\geometry{left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{remark}[theorem]{Remark}

\DeclareMathOperator{\Vol}{Vol}
\DeclareMathOperator{\Tr}{Tr}
\DeclareMathOperator{\Spec}{Spec}
\DeclareMathOperator{\dimH}{dim_H}
\DeclareMathOperator{\Fix}{Fix}

\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    backgroundcolor=\color{gray!10},
    keywordstyle=\color{blue},
    commentstyle=\color{green!60!black}
}

\title{Fractal Spectral Asymptotics and p-adic Thermodynamic Formalism\\
\large A Unified Framework for Kleinian Groups and Non-Archimedean Dynamics}
\author{Research Team}
\date{February 2026}

\begin{document}

\maketitle

\begin{abstract}
'''

# Extract abstract
abstract_match = re.search(r'## Abstract\s*\n\s*\n(.*?)(?=\n---|\n##)', content, re.DOTALL)
if abstract_match:
    abstract = abstract_match.group(1).strip()
else:
    abstract = "We establish a unified framework connecting fractal spectral theory with p-adic thermodynamic formalism."

# Convert markdown to LaTeX
def convert_markdown_to_latex(text):
    # Remove YAML frontmatter if present
    text = re.sub(r'^---\s*\n.*?---\s*\n', '', text, flags=re.DOTALL)
    
    # Convert headers
    text = re.sub(r'^# (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)
    
    # Convert bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    
    # Convert italic
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    
    # Convert code blocks
    text = re.sub(r'```python\s*\n(.*?)```', r'\\begin{lstlisting}[language=Python]\n\1\\end{lstlisting}', text, flags=re.DOTALL)
    text = re.sub(r'```\s*\n(.*?)```', r'\\begin{lstlisting}\n\1\\end{lstlisting}', text, flags=re.DOTALL)
    
    # Convert inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    
    # Convert display math (already in $$)
    # Keep as is
    
    # Convert links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', text)
    
    # Convert horizontal rules
    text = re.sub(r'^---+$', r'\\hrule', text, flags=re.MULTILINE)
    
    # Convert bullet lists
    lines = text.split('\n')
    result = []
    in_list = False
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                result.append('\\begin{itemize}')
                in_list = True
            item_text = line.strip()[2:]
            result.append(f'\\item {item_text}')
        elif in_list and line.strip() and not line.strip().startswith('- ') and not line.strip().startswith('* '):
            result.append('\\end{itemize}')
            in_list = False
            result.append(line)
        else:
            result.append(line)
    if in_list:
        result.append('\\end{itemize}')
    text = '\n'.join(result)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

# Convert the content
latex_content = convert_markdown_to_latex(content)

# Remove the abstract section from content (we'll add it separately)
latex_content = re.sub(r'## Authors.*?## Abstract.*?\n\s*\n', '', latex_content, flags=re.DOTALL)
latex_content = re.sub(r'---\s*\n', '', latex_content)

# Combine everything
full_latex = preamble + abstract + r'''
\end{abstract}

''' + latex_content + r'''

\end{document}
'''

# Clean up any remaining issues
full_latex = full_latex.replace('\\textbf{', '\\textbf{')
full_latex = re.sub(r'\\textbf\{([^}]+)\\textbf\{', r'\\textbf{\1', full_latex)

# Fix double subsections in headers
full_latex = re.sub(r'\\subsection\{\\subsection\{([^}]+)\}\}', r'\\subsection{\1}', full_latex)

# Write the output
with open('paper_from_md.tex', 'w', encoding='utf-8') as f:
    f.write(full_latex)

print(f"LaTeX file written to: paper_from_md.tex")
print(f"File size: {len(full_latex)} characters")
