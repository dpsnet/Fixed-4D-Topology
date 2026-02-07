# 参考文献与数据来源引用

## 真实数据集引用

### 1. Internet AS拓扑

**来源**: CAIDA (The Center for Applied Internet Data Analysis)  
**数据集**: AS-Skitter  
**引用**:
```
Leskovec J, Kleinberg J, Faloutsos C. Graphs over Time: Densification Laws, 
Shrinking Diameters and Possible Explanations. ACM SIGKDD 2005.
```
**链接**: http://www.caida.org/tools/measurement/skitter/  
**许可**: 公开学术使用

---

### 2. DBLP学术合作网络

**来源**: SNAP Stanford  
**数据集**: DBLP Computer Science Bibliography  
**引用**:
```
Yang J, Leskovec J. Defining and Evaluating Network Communities based on 
Ground-truth. ICDM 2012.
```
**链接**: https://snap.stanford.edu/data/com-DBLP.html  
**许可**: 公开学术使用

---

### 3. Yeast PPI生物网络 ⭐

**来源**: BioGRID (Biological General Repository for Interaction Datasets)  
**数据集**: Saccharomyces cerevisiae S288c (Release 5.0.254)  
**引用**:
```
Stark C, Breitkreutz BJ, Reguly T, Boucher L, Breitkreutz A, Tyers M. 
BioGRID: A General Repository for Interaction Datasets. 
Nucleic Acids Res. Jan 1, 2006; 34:D535-9.
```
**链接**: https://downloads.thebiogrid.org/  
**许可**: MIT License (100% freely available to both academic and commercial users)  
**数据使用声明**: Provided WITHOUT ANY WARRANTY

---

### 4. Facebook社交网络

**来源**: SNAP Stanford  
**数据集**: Facebook Combined (ego networks)  
**引用**:
```
McAuley JJ, Leskovec J. Learning to Discover Social Circles in Ego Networks. 
NIPS 2012.
```
**链接**: https://snap.stanford.edu/data/egonets-Facebook.html  
**许可**: 公开学术使用

---

### 5. Twitter社交网络

**来源**: SNAP Stanford  
**数据集**: Twitter Combined (ego networks)  
**引用**:
```
McAuley JJ, Leskovec J. Learning to Discover Social Circles in Ego Networks. 
NIPS 2012.
```
**链接**: https://snap.stanford.edu/data/egonets-Twitter.html  
**许可**: 公开学术使用

---

### 6. IEEE Power Grid电网 ⭐

**来源**: IEEE / University of Washington  
**数据集**: IEEE 118 Bus Test Case  
**引用**:
```
IEEE 118 Bus Test Case. Power Systems Test Case Archive.
University of Washington, Electrical Engineering.
```
**链接**: https://www2.ee.washington.edu/research/pstca/  
**许可**: 公开学术使用 (标准测试案例)

---

### 7. Email机构通信网络

**来源**: SNAP Stanford  
**数据集**: email-Eu-core  
**引用**:
```
Leskovec J, Kleinberg J, Faloutsos C. Graph Evolution: Densification and 
Shrinking Diameters. ACM TKDD 2007.
```
**链接**: https://snap.stanford.edu/data/email-Eu-core.html  
**许可**: 公开学术使用

---

## 工具与软件引用

### 分析工具
- Python 3.x (标准库)
- 自编分析脚本 (见代码仓库)

### 网络数据源汇总平台
- **SNAP**: Stanford Network Analysis Project (https://snap.stanford.edu/)
- **BioGRID**: Biological General Repository for Interaction Datasets (https://thebiogrid.org/)
- **CAIDA**: Center for Applied Internet Data Analysis (https://www.caida.org/)
- **IEEE**: Power Systems Test Case Archive (https://www2.ee.washington.edu/research/pstca/)

---

## 许可声明汇总

| 数据集 | 许可类型 | 商业使用 | 引用要求 |
|-------|---------|---------|---------|
| Internet AS | 公开学术 | 需授权 | 是 |
| DBLP | 公开学术 | 允许 | 是 |
| Yeast PPI | **MIT License** | **允许** | **是** |
| Facebook | 公开学术 | 需授权 | 是 |
| Twitter | 公开学术 | 需授权 | 是 |
| Power Grid | 公开学术 | 允许 | 建议 |
| Email | 公开学术 | 需授权 | 是 |

**特别注意**: BioGRID数据采用MIT License，100%免费提供给学术和商业用户，但需提供引用。

---

## 建议论文引用格式

在论文的"Data Availability"或"Methods"部分添加：

```
All network datasets used in this study are publicly available:
- Internet AS topology: CAIDA AS-Skitter dataset [Leskovec et al., 2005]
- Academic collaboration: DBLP dataset from SNAP [Yang & Leskovec, 2012]
- Protein interactions: BioGRID yeast PPI dataset (Release 5.0.254) 
  [Stark et al., 2006], available under MIT License
- Social networks: Facebook and Twitter datasets from SNAP 
  [McAuley & Leskovec, 2012]
- Power grid: IEEE 118 Bus Test Case
- Communication network: email-Eu-core from SNAP [Leskovec et al., 2007]
```

---

*文档生成*: 2026-02-07  
*数据集版本*: BioGRID 5.0.254, SNAP 最新版, CAIDA 历史数据
