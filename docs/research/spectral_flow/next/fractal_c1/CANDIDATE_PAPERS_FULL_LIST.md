# 候选论文完整清单

**更新日期**: 2026-02-14  
**目标**: 收集3个系统的数据验证$c_1(d,w)$

---

## 系统1：石墨烯Landau能级（验证$c_1(2,1)=0.5$）

### 优先级A（已下载或高相关性）

| # | 论文 | 作者 | 年份 | 期刊 | 状态 | 备注 |
|---|------|------|------|------|------|------|
| 1 | Infrared Spectroscopy of Landau Levels of Graphene | Sadowski et al. | 2007 | PRL 98, 197403 | ✅ 已下载 | 单层石墨烯，半整数QHE |
| 2 | Infrared spectroscopy of Landau levels in graphene | Jiang et al. | 2007 | arXiv:cond-mat/0703822 | ⏳ 待下载 | 同组工作 |

### 优先级B（需要进一步评估）

| # | 论文 | 作者 | 年份 | 期刊 | 相关性 |
|---|------|------|------|------|--------|
| 3 | Electronic properties of graphene in strong magnetic field | Goerbig | 2011 | RMP 83, 1193 | ⭐⭐⭐⭐⭐ Review，可能有数据表 |
| 4 | Valley and Zeeman Splittings in Multilayer Epitaxial Graphene | Jiang et al. | 2019 | ACS Nano Lett | ⭐⭐⭐⭐ n=0→1跃迁分裂 |
| 5 | Infrared spectroscopy of phase transitions in lowest LL | - | 2024 | arXiv:2312.02489 | ⭐⭐⭐⭐ 双层石墨烯 |
| 6 | Landau level transition and magnetophonon resonance | - | 2023 | Physica B | ⭐⭐⭐ 理论分析 |

### 优先级C（备选）

| # | 论文 | 作者 | 年份 | 相关性 |
|---|------|------|------|--------|
| 7 | Magnetoabsorption study of Landau levels in graphite | - | 2009 | PRB | ⭐⭐⭐ 石墨（非石墨烯） |
| 8 | Landau Levels in Graphene (讲义) | - | - | IJS | ⭐⭐ 教学材料 |

---

## 系统2：GaAs量子阱（验证$c_1(2,0)=1.0$）

### 优先级A（厚度依赖关键）

| # | 论文 | 作者 | 年份 | 期刊 | 状态 | 备注 |
|---|------|------|------|------|------|------|
| 1 | Well-Width Dependence of the Exciton Lifetime | - | 2025 | - | ⏳ 待评估 | 厚度依赖研究 |
| 2 | light-hole exciton system in GaAs/AlGaAs QWs | - | 2022 | PRB 106, 085407 | ⏳ 待下载 | 不同阱宽的系统研究 |
| 3 | Quantitative measurements of many-body exciton dynamics | Smith | 2010 | PhD Thesis | ⏳ 待下载 | JILA博士论文，详细数据 |
| 4 | Excitons in GaAs quantum wells (讲义) | - | - | 中科院半导体所 | ⏳ 待评估 | 可能有参考数据 |

### 优先级B（理论/计算）

| # | 论文 | 作者 | 年份 | 相关性 |
|---|------|------|------|--------|
| 5 | Theoretical study of excitons in semiconductor quantum wires | Sidor | - | ⭐⭐⭐ 量子线（1D） |
| 6 | Resonant optical properties of AlGaAs/GaAs | - | 2017 | JAP | ⭐⭐⭐ 特定阱宽(10.4nm) |
| 7 | Refractive index change in GaAs-AlGaAs QWs | - | 2023 | PhD Thesis | ⭐⭐ 格拉斯哥大学 |

### 优先级C（历史数据）

| # | 论文 | 作者 | 年份 | 备注 |
|---|------|------|------|------|
| 8 | Well-width dependence of exciton binding energy | - | 1980s-90s | 经典文献，可能需要查找 |

---

## 系统3：全息对偶验证（备选）

### 拓扑绝缘体

| # | 论文 | 材料 | 相关性 |
|---|------|------|--------|
| 1 | Bi2Se3 bulk and surface states | Bi2Se3 | ⭐⭐⭐⭐ |
| 2 | Bi2Te3 optical properties | Bi2Te3 | ⭐⭐⭐⭐ |
| 3 | Topological insulator ARPES data | Various | ⭐⭐⭐ |

---

## 数据提取优先级

### 第一优先（本周完成）
1. **Sadowski 2007** (石墨烯) - 图1和图2
2. **Jiang 2007** (石墨烯) - 补充数据
3. **Goerbig 2011 Review** - Table II

### 第二优先（下周完成）
4. **PRB 106, 085407** (GaAs QW) - 厚度依赖数据
5. **Smith PhD Thesis** (GaAs QW) - 详细能级数据

### 第三优先（如有时间）
6. 其他备选论文

---

## 下载和提取计划

### 今日（2026-02-14）
- [x] 搜索并整理候选论文清单 ✅
- [ ] 下载高优先级论文（3-5篇）
- [ ] 使用WebPlotDigitizer提取Sadowski数据

### 明日（2026-02-15）
- [ ] 提取Jiang论文数据
- [ ] 查找Goerbig Review数据表
- [ ] 开始GaAs QW论文搜索

### 本周内
- [ ] 完成所有高优先级论文的数据提取
- [ ] 初步数据分析
- [ ] 验证$c_1$预测

---

## 数据提取模板

每个系统的数据记录格式：

```csv
system,material,d,w,n,energy_meV,error_meV,B_field_T,thickness_nm,temperature_K,source,doi
graphene,SLG,2,1,0,XX.X,0.X,18,,-,Sadowski2007,10.1103/...
graphene,SLG,2,1,1,XX.X,0.X,18,,-,Sadowski2007,10.1103/...
qwell,GaAs,2,0,1,XX.X,0.X,,5,4.2,Smith2010,...
qwell,GaAs,2,0,1,XX.X,0.X,,10,4.2,Smith2010,...
```

---

## 立即执行任务

1. **下载Jiang 2007 arXiv论文**
2. **下载Goerbig 2011 RMP Review**
3. **查找Goerbig论文的Table II**
4. **开始WebPlotDigitizer提取Sadowski数据**

---

**状态**: 候选论文清单完成  
**下一步**: 批量下载论文并提取数据
