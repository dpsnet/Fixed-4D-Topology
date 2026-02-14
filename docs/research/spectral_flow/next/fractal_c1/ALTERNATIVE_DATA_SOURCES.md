# 替代数据源搜索

## 现状
arXiv数据附件搜索效果不佳，转向其他策略

---

## 策略A：搜索已知开放数据集

### 1. Zenodo平台
**URL**: https://zenodo.org/

**搜索关键词**:
- "graphene Landau levels"
- "quantum well exciton spectroscopy"
- "semiconductor Rydberg exciton"

### 2. Figshare平台
**URL**: https://figshare.com/

**搜索关键词**:
- "exciton binding energy"
- "Landau level transition"

### 3. Kaggle数据集
**URL**: https://www.kaggle.com/datasets

**搜索关键词**:
- "condensed matter physics"
- "spectroscopy data"

### 4. NSF/DOE开放数据
- NSF PAR (Public Access Repository)
- DOE OSTI (Office of Scientific and Technical Information)

---

## 策略B：搜索包含数据表格的论文

### 具体目标论文类型

**类型1：Review文章**
- 通常包含汇总数据表
- 多个实验数据的比较

**类型2：学位论文（PhD Thesis）**
- 通常包含详细数据
- 附录中有原始数据表

**类型3：补充材料丰富的论文**
- Nature/Science子刊
- 通常有Supplementary Information with data tables

---

## 策略C：直接数值搜索

### Google搜索技巧

**搜索精确的数值表格**:
```
"n = 3" "10.2 meV" "Cu2O" exciton
"Landau level" "energy meV" "graphene" table
"quantum well" "5 nm" "binding energy" meV
```

**搜索PDF中的表格**:
```
filetype:pdf "Table 1" "exciton" "energy" "meV"
filetype:pdf "Fig." "Landau levels" "graphene" "energy"
```

---

## 策略D：联系数据存储库

### 1. NIST数据库
**URL**: https://www.nist.gov/pml/sensor-science/spectroscopy-databases

可能包含：
- 半导体光谱数据
- 能级参考数据

### 2. Springer Materials
**URL**: https://materials.springer.com/

可能包含：
- 材料属性数据库
- 激子参数

### 3. 材料项目（Materials Project）
**URL**: https://materialsproject.org/

包含：
- 计算材料数据
- 能带结构

---

## 策略E：直接构造合成数据

如果找不到合适的实验数据，可以考虑：

### 基于理论公式生成"模拟数据"
```python
# 使用已知物理参数生成
# 添加合理噪声
# 用于演示方法可行性
```

### 明确说明
在论文中注明：
> "While experimental data for graphene Landau levels with sufficient precision is currently being sought, we demonstrate the methodology using theoretically generated data based on the Dirac equation with added experimental noise (see Supplementary Material)."

---

## 推荐策略组合

### 短期（今天）
1. 搜索Review文章的数据表
2. 搜索PhD学位论文
3. 使用Google精确数值搜索

### 中期（本周）
1. 联系已找到论文的作者
2. 搜索Zenodo/Figshare
3. 探索NIST等数据库

### 备选
如果都找不到，使用策略E（合成数据）并明确说明

---

## 立即执行

让我尝试搜索Review文章和学位论文：
