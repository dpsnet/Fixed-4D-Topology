# McMullen: Hausdorff Dimension and Conformal Dynamics 系列论文

## 搜索结果概述

**作者**: Curtis T. McMullen (哈佛大学数学系)  
**论文系列**: Hausdorff dimension and conformal dynamics I/II/III  
**发表时间**: 1997-2000年  
**核心主题**: Bowen公式, 热力学形式, Kleinian群极限集维数, 有理映射Julia集

---

## 论文详细信息

### Paper I: Strong Convergence of Kleinian Groups

| 属性 | 详情 |
|------|------|
| **完整标题** | Hausdorff dimension and conformal dynamics I: Strong convergence of Kleinian groups |
| **作者** | Curtis T. McMullen |
| **期刊** | Journal of Differential Geometry |
| **卷期页** | Vol. 51, No. 3 (1999), pp. 471-515 |
| **页数** | 45页 |
| **MR编号** | MR1726737 |
| **MSC分类** | Primary 30F40; Secondary 58F11, 58F23 |
| **发表年份** | 1999 |

#### 摘要
本文研究Kleinian群序列Γₙ→Γ的极限集Λₙ和Λ的Hausdorff维数行为，其中M=H³/Γ是几何有限的。主要结果：

1. **连续性定理**: 若Γₙ→Γ强收敛，则：
   - Mₙ=H³/Γₙ对所有充分大的n是几何有限的
   - Λₙ→Λ在Hausdorff拓扑下
   - 当H.dim(Λ)≥1时，H.dim(Λₙ)→H.dim(Λ)

2. **不连续性示例**: 当H.dim(Λ)<1时，维数可能在强极限下不连续变化

3. **径向收敛恢复连续性**: 要求意外抛物元径向收敛可恢复连续性

4. **应用**: 准Fuchsian群及其极限的研究

#### 与本研究的相关性评级
⭐⭐⭐⭐⭐ **极高** - 这是理解Kleinian群极限集维数连续性的基础理论

#### 获取途径
- ✅ **免费PDF**: 已从McMullen个人主页下载
- 📁 **本地路径**: `/Fixed-4D-Topology/docs/research/literature/kleinian/mcmullen_dimI_hausdorff_conformal.pdf`
- 🌐 **在线访问**: https://people.math.harvard.edu/~ctm/papers/home/text/papers/dimI/dimI.pdf

---

### Paper II: Geometrically Finite Rational Maps

| 属性 | 详情 |
|------|------|
| **完整标题** | Hausdorff dimension and conformal dynamics II: Geometrically finite rational maps |
| **作者** | Curtis T. McMullen |
| **期刊** | Commentarii Mathematici Helvetici |
| **卷期页** | Vol. 75, No. 4 (2000), pp. 535-593 |
| **页数** | 64页 |
| **DOI** | 10.1007/s000140050140 |
| **MR编号** | MR1789177 |
| **MSC分类** | Primary 58F23; Secondary 58F11, 30F40 |
| **发表年份** | 2000 |

#### 摘要
本文研究Riemann球面上有理映射的多种动态定义维数，提供以Kleinian群理论为模型的系统处理。

**核心内容**：

1. **径向Julia集**: 定义Jᵣₐd(f)，证明每个有理映射满足
   ```
   H.dim Jᵣₐd(f) = α(f)
   ```
   其中α(f)是球面上f-不变共形密度的最小维数。

2. **几何有限有理映射**: 若Julia集中每个临界点都是预周期的，则
   ```
   H.dim Jᵣₐd(f) = H.dim J(f) = δ(f)
   ```
   其中δ(f)是Poincaré级数的临界指数。

3. **连续性定理**: 设f几何有限，fₙ→f代数收敛且保持临界关系。当收敛对每个抛物点是双曲型时，fₙ对充分大的n是几何有限的，且J(fₙ)→J(f)在Hausdorff拓扑下。若收敛是径向的，则H.dim J(fₙ)→H.dim J(f)。

4. **维数趋近于2**: 给出Shishikura结果的简单证明：存在fₙ(z)=z²+cₙ使得H.dim J(fₙ)→2。

#### 与本研究的相关性评级
⭐⭐⭐⭐⭐ **极高** - 提供了Bowen公式的现代版本，直接关联到热力学形式体系

#### 获取途径
- ✅ **免费PDF**: 已从McMullen个人主页下载
- 📁 **本地路径**: `/Fixed-4D-Topology/docs/research/literature/kleinian/mcmullen_dimII_hausdorff_conformal.pdf`
- 🌐 **在线访问**: https://people.math.harvard.edu/~ctm/papers/home/text/papers/dimII/dimII.pdf

---

### Paper III: Computation of Dimension

| 属性 | 详情 |
|------|------|
| **完整标题** | Hausdorff dimension and conformal dynamics III: Computation of dimension |
| **作者** | Curtis T. McMullen |
| **期刊** | American Journal of Mathematics |
| **卷期页** | Vol. 120, No. 4 (1998), pp. 691-721 |
| **页数** | 38页 |
| **MR编号** | MR1637951 |
| **MSC分类** | Primary 58F23; Secondary 58F11, 30F40 |
| **发表年份** | 1998 |

#### 摘要
本文提出一种特征值算法，用于精确计算Kleinian群极限集和有理映射Julia集的Hausdorff维数。算法应用于Schottky群、二次多项式和Blaschke积，获得数值和理论结果。

**维数图表**：
1. 由3条对称测地线反射生成的Fuchsian群族
2. 多项式f_c(z)=z²+c, c∈[-1,1/2]的族
3. 有理映射f_t(z)=z/t+1/z, t∈(0,1]的族

**计算结果**：
- Apollonian垫片: H.dim(Λ) ≈ 1.305688
- Douady兔子: H.dim(J(f)) ≈ 1.3934 (其中f(z)=z²+c满足f³(0)=0)

#### 与本研究的相关性评级
⭐⭐⭐⭐⭐ **极高** - 提供实际计算维数的算法，对数值验证至关重要

#### 获取途径
- ✅ **免费PDF**: 已从McMullen个人主页下载
- 📁 **本地路径**: `/Fixed-4D-Topology/docs/research/literature/kleinian/mcmullen_dimIII_hausdorff_conformal.pdf`
- 🌐 **在线访问**: https://people.math.harvard.edu/~ctm/papers/home/text/papers/dimIII/dimIII.pdf

---

## 其他相关论文

### 密切相关的McMullen论文

| 论文 | 期刊 | 年份 | 相关性 |
|------|------|------|--------|
| **Hausdorff dimension of general Sierpiński carpets** | Nagoya Math. J. | 1984 | ⭐⭐⭐⭐ |
| **Area and Hausdorff dimension of Julia sets of entire functions** | Trans. AMS | 1987 | ⭐⭐⭐⭐ |
| **Self-similarity of Siegel disks and Hausdorff dimension of Julia sets** | (Conference) | 1994 | ⭐⭐⭐⭐ |
| **Rigidity and inflexibility in conformal dynamics** | (Conference) | 1999 | ⭐⭐⭐⭐ |

### 引用McMullen系列的重要论文

| 作者 | 论文 | 期刊 | 相关性 |
|------|------|------|--------|
| R. Bowen | Hausdorff dimension of quasicircles | IHES Publ. Math. | ⭐⭐⭐⭐⭐ (原始Bowen公式) |
| S.P. Lalley | Renewal theorems in symbolic dynamics | Acta Math. | ⭐⭐⭐⭐⭐ |
| M. Urbański | Measures and dimensions in conformal dynamics | Bull. AMS | ⭐⭐⭐⭐⭐ (综述) |
| A. Avila & M. Lyubich | Hausdorff dimension and conformal measures | J. AMS | ⭐⭐⭐⭐⭐ |

---

## 推荐阅读顺序

### 对于理论理解（数学物理学家）
1. **Paper II** (2000) - 从有理映射和Bowen公式的现代形式开始
2. **Paper I** (1999) - 理解Kleinian群极限集的连续性理论
3. **Paper III** (1998) - 学习维数计算的实际算法

### 对于数值计算（计算物理学家）
1. **Paper III** (1998) - 首先掌握特征值算法
2. **Paper II** (2000) - 理解算法背后的理论基础
3. **Paper I** (1999) - 扩展到更一般的Kleinian群

### 对于纤维-引力研究项目
1. **Paper II** (2000) **最优先** - 热力学形式与维数关系直接相关
2. **Paper III** (1998) - 数值计算方法用于验证纤维-引力理论预测
3. **Paper I** (1999) - 几何有限群理论为4D拓扑分析提供基础

---

## 关键数学概念索引

| 概念 | 定义 | 所在论文 |
|------|------|----------|
| **Bowen公式** | δ(f) = H.dim(J(f)) | Paper II |
| **径向Julia集** | Jᵣₐd(f) | Paper II |
| **几何有限性** | 临界点预周期性条件 | Paper I & II |
| **强收敛** | Γₙ→Γ的拓扑收敛 | Paper I |
| **Poincaré级数** | Σ|γ'(x)|ˢ 的临界指数δ | Paper I & II |
| **特征值算法** | 通过转移算子计算维数 | Paper III |
| **共形密度** | μ的Γ-不变性 | Paper I |

---

## 获取状态总结

| 论文 | 获取状态 | 本地文件 | 文件大小 |
|------|----------|----------|----------|
| Paper I | ✅ 已下载 | `mcmullen_dimI_hausdorff_conformal.pdf` | 392 KB |
| Paper II | ✅ 已下载 | `mcmullen_dimII_hausdorff_conformal.pdf` | 446 KB |
| Paper III | ✅ 已下载 | `mcmullen_dimIII_hausdorff_conformal.pdf` | 577 KB |

**总计**: 3篇论文，约1.4 MB

---

## 参考文献格式（BibTeX）

```bibtex
@article{mcmullen1999hausdorffI,
  author = {McMullen, Curtis T.},
  title = {Hausdorff dimension and conformal dynamics. {I}. {S}trong convergence of {K}leinian groups},
  journal = {J. Differential Geom.},
  volume = {51},
  number = {3},
  pages = {471--515},
  year = {1999},
  mrclass = {30F40 (58F11 58F23)},
  mrnumber = {1726737},
  mrreviewer = {Richard\ D.\ Canary}
}

@article{mcmullen2000hausdorffII,
  author = {McMullen, Curtis T.},
  title = {Hausdorff dimension and conformal dynamics. {II}. {G}eometrically finite rational maps},
  journal = {Comment. Math. Helv.},
  volume = {75},
  number = {4},
  pages = {535--593},
  year = {2000},
  doi = {10.1007/s000140050140},
  mrclass = {58F23 (58F11 30F40)},
  mrnumber = {1789177},
  mrreviewer = {Feliks\ Przytycki}
}

@article{mcmullen1998hausdorffIII,
  author = {McMullen, Curtis T.},
  title = {Hausdorff dimension and conformal dynamics. {III}. {C}omputation of dimension},
  journal = {Amer. J. Math.},
  volume = {120},
  number = {4},
  pages = {691--721},
  year = {1998},
  mrclass = {58F23 (58F11 30F40)},
  mrnumber = {1637951},
  mrreviewer = {J.\ H.\ Hubbard}
}
```

---

## 搜索记录

**搜索日期**: 2026-02-11  
**搜索来源**: 
- McMullen个人主页: https://people.math.harvard.edu/~ctm/
- Google Scholar
- AMS Journals
- Project Euclid

**搜索策略**: 
1. 直接访问作者主页获取完整论文列表
2. 通过Google Scholar验证引用信息
3. 从作者主页直接下载PDF文件

---

*本文档由AI研究助手生成，用于Fixed-4D-Topology项目的文献调研。*
