# 格式转换指南

## Markdown → LaTeX 转换

### 推荐工具

**方案1: Pandoc (推荐)**
```bash
# 安装pandoc
# Ubuntu/Debian: sudo apt-get install pandoc
# Mac: brew install pandoc

# 基础转换
pandoc Manuscript.md -o manuscript.tex

# 使用Nature Physics模板
pandoc Manuscript.md -o manuscript.tex --template=nature-physics-template.tex

# 使用PRX模板
pandoc Manuscript.md -o manuscript.tex --template=prx-template.tex
```

**方案2: 手动转换**
- 复制Markdown内容到LaTeX模板
- 手动调整格式

---

## LaTeX 模板选择

### Nature Physics 模板

```latex
\documentclass{nature}
\title{Effective Dimensions of Complex Networks: A Large-Scale Empirical Study}
\author{Wang Bin}
\begin{document}
\maketitle
\begin{abstract}
[摘要内容]
\end{abstract}
\section{Introduction}
...
\end{document}
```

### PNAS 模板

```latex
\documentclass[9pt,twocolumn,twoside]{pnas-new}
\title{Effective Dimensions of Complex Networks}
\author{Wang Bin}
\begin{document}
\maketitle
\begin{abstract}
...
\end{abstract}
...
\end{document}
```

### PRX 模板

```latex
\documentclass[aps,prx,reprint]{revtex4-2}
\title{Effective Dimensions of Complex Networks}
\author{Wang Bin}
\begin{document}
\maketitle
\begin{abstract}
...
\end{abstract}
...
\end{document}
```

---

## 图表准备

### 图要求

**Nature Physics**
- 格式: EPS, TIFF, PDF
- 分辨率: 300 dpi (彩色), 600 dpi (黑白)
- 尺寸: 单栏 8.5 cm, 双栏 17.5 cm
- 字体: Arial 或 Helvetica

**PNAS**
- 格式: TIFF, EPS, PDF
- 分辨率: 300 dpi
- 尺寸: 单栏 8.6 cm, 双栏 17.8 cm

**PRX**
- 格式: EPS, PDF
- 分辨率: 300 dpi
- 建议: 矢量图优先

### 建议图表列表

**Figure 1**: 维度层次图 (7个网络的维度对比)
**Figure 2**: 聚类-维度关系散点图
**Figure 3**: 模拟vs真实对比图

---

## 快速转换步骤

### Step 1: 获取期刊模板
- Nature Physics: https://www.nature.com/nphys/for-authors/formatting-guide
- PNAS: https://www.pnas.org/authors/submission-information
- PRX: https://journals.aps.org/prx/authors

### Step 2: 内容迁移
1. 复制主标题
2. 复制作者信息
3. 复制摘要
4. 复制正文段落
5. 复制参考文献

### Step 3: 格式调整
- 调整标题层级 (\section, \subsection)
- 插入图表引用 (\ref{fig1})
- 添加数学公式 ($...$ 或 \[...\])
- 调整表格格式

### Step 4: 编译检查
```bash
# 编译LaTeX
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex

# 检查输出
open manuscript.pdf
```

---

## 常见格式问题

### 问题1: 特殊字符
- & → \&
- % → \%
- $ → \$
- # → \#
- _ → \_

### 问题2: 数学公式
```latex
% 行内公式
$d_{\text{eff}} = 2.4$

% 独立公式
$$d_B = -\frac{\Delta \log N_B}{\Delta \log l_B}$$

% 编号公式
\begin{equation}
d_B = -\frac{\Delta \log N_B}{\Delta \log l_B}
\end{equation}
```

### 问题3: 表格转换
```markdown
| A | B | C |
|---|---|---|
| 1 | 2 | 3 |
```

转换为:
```latex
\begin{table}
\centering
\begin{tabular}{ccc}
\hline
A & B & C \\
\hline
1 & 2 & 3 \\
\hline
\end{tabular}
\caption{Table caption.}
\label{tab1}
\end{table}
```

---

## 推荐工作流程

### 如果熟悉LaTeX
1. 下载期刊LaTeX模板
2. 复制粘贴内容
3. 手动调整格式
4. 编译检查

### 如果不熟悉LaTeX
1. 使用Word模板
2. 复制粘贴内容
3. 使用Word格式刷
4. 请他人协助检查

### 替代方案
使用Overleaf (在线LaTeX编辑器)
- https://www.overleaf.com
- 提供期刊模板
- 实时编译预览
- 协作编辑

---

## 最终检查清单

- [ ] 论文转换为期刊格式
- [ ] 图表符合分辨率要求
- [ ] 引用格式正确
- [ ] 字数符合限制
- [ ] 摘要长度合适
- [ ] 亮点数量正确
- [ ] 作者信息完整
- [ ] 无格式错误

---

*建议: 使用Overleaf在线编辑，可快速预览和调整格式*
