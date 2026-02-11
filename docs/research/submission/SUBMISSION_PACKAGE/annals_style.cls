% Annals of Mathematics Style File
% Based on amsart with Annals-specific modifications
% Version 1.0 - February 2026

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{annals_style}[2026/02/12 Annals of Mathematics Style]

% Base class
\LoadClass[11pt]{amsart}

% Required packages
\RequirePackage{amsmath,amssymb,amsthm}
\RequirePackage{mathtools}
\RequirePackage{mathrsfs}
\RequirePackage{geometry}
\RequirePackage{hyperref}
\RequirePackage{cleveref}
\RequirePackage{enumitem}
\RequirePackage{booktabs}
\RequirePackage{graphicx}

% Page geometry - Annals format
\geometry{
  letterpaper,
  margin=1.25in,
  headheight=12pt,
  footskip=30pt
}

% Theorem environments
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{conjecture}[theorem]{Conjecture}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{problem}[theorem]{Problem}

% Custom math operators
\DeclareMathOperator{\Vol}{Vol}
\DeclareMathOperator{\Tr}{Tr}
\DeclareMathOperator{\Spec}{Spec}
\DeclareMathOperator{\dimH}{dim_H}
\DeclareMathOperator{\Fix}{Fix}
\DeclareMathOperator{\Aut}{Aut}
\DeclareMathOperator{\Gal}{Gal}
\DeclareMathOperator{\Res}{Res}

% Hyphenation
\hyphenation{Kleinian Ber-ko-vich}

% Bibliography style
\bibliographystyle{amsalpha}

% Running heads
\pagestyle{headings}

% Section formatting
\renewcommand{\section}{%
  \@startsection{section}{1}{0mm}%
  {-\baselineskip}{0.5\baselineskip}%
  {\normalfont\large\bfseries}%
}

\renewcommand{\subsection}{%
  \@startsection{subsection}{2}{0mm}%
  {-\baselineskip}{0.25\baselineskip}%
  {\normalfont\normalsize\bfseries}%
}

% Title formatting
\renewcommand{\maketitle}{%
  \thispagestyle{plain}%
  \vspace*{0.5in}%
  \begin{center}%
    {\LARGE\bfseries\@title\par}%
    \vspace{0.5in}%
    {\large\scshape\@author\par}%
    \vspace{0.25in}%
    {\normalsize\@date\par}%
  \end{center}%
  \vspace{0.5in}%
}

% Abstract formatting
\renewenvironment{abstract}{%
  \begin{center}%
  \begin{minipage}{0.9\textwidth}%
  \small%
}{%
  \end{minipage}%
  \end{center}%
  \vspace{0.25in}%
}

% Keywords command
\newcommand{\keywords}[1]{%
  \vspace{0.25in}%
  \noindent\textbf{Keywords:} #1%
}

% MSC classes command
\newcommand{\msc}[1]{%
  \vspace{0.1in}%
  \noindent\textbf{MSC 2020:} #1%
}

% End of class file
\endinput
