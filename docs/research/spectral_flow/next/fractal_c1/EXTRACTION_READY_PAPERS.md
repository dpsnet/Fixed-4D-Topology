# 数据提取就绪论文清单

## 立即可提取（已下载，数据清晰）

### 1. 石墨烯Landau能级 - Sadowski et al. PRL 2007
**文件**: `sadowski_2007_graphene_landau.pdf` (313 KB)

**关键图表**:
- Fig. 1: 透射光谱（不同磁场下Landau能级跃迁）
- Fig. 2: 跃迁能量随磁场变化

**需要提取**:
- n = 0, ±1, ±2, ±3 Landau能级位置
- 不同磁场强度（B = 18 T等）
- 跃迁能量（meV）

**工具**: WebPlotDigitizer
**预计时间**: 30分钟

---

### 2. 石墨烯Landau能级 - Jiang et al. arXiv 2007
**文件**: `jiang_2007_graphene_landau_arxiv.pdf` (199 KB)

**内容**: 与Sadowski论文类似，可能有补充数据或不同视角

**需要提取**:
- 与Sadowski对比验证
- 可能的额外数据点

**工具**: WebPlotDigitizer
**预计时间**: 20分钟

---

### 3. GaAs量子阱 - PRB 2022
**文件**: `prb_2022_gaas_qw_excitons.pdf` (655 KB)

**标题**: "Light-hole exciton system in GaAs/AlGaAs quantum wells"

**关键内容**:
- 不同阱宽的研究（需要确认具体宽度）
- Light-hole和heavy-hole激子
- 激子束缚能数据

**需要提取**:
- 阱宽 vs 激子能量关系
- n = 1, 2, 3激子态
- 验证$c_1(2,0) = 1.0$

**工具**: WebPlotDigitizer
**预计时间**: 40分钟

---

### 4. GaAs量子阱理论 - Andlauer et al. 2010
**文件**: `andlauer_2010_gaas_qw.pdf` (957 KB)

**内容**: 理论计算，可能有系统性数据

**用途**: 与实验数据对比，验证理论一致性

---

## 数据提取计划

### 第一步：石墨烯数据（今天完成）

**任务**:
1. 打开 `sadowski_2007_graphene_landau.pdf`
2. 截图Fig. 1和Fig. 2
3. 使用WebPlotDigitizer提取数据点
4. 记录到CSV文件

**预期产出**:
```csv
system,n,B_field_T,energy_meV,source
graphene,0,18,XX.X,Sadowski2007
graphene,1,18,XX.X,Sadowski2007
graphene,2,18,XX.X,Sadowski2007
...
```

### 第二步：GaAs量子阱数据（明天完成）

**任务**:
1. 打开 `prb_2022_gaas_qw_excitons.pdf`
2. 寻找厚度依赖图表
3. 提取不同阱宽的激子数据
4. 记录到CSV文件

**预期产出**:
```csv
system,thickness_nm,n,energy_meV,source
qwell,5,1,XX.X,PRB2022
qwell,10,1,XX.X,PRB2022
qwell,20,1,XX.X,PRB2022
...
```

---

## 数据提取工具准备

### 已准备
- WebPlotDigitizer链接: https://apps.automeris.io/wpd/
- 使用指南: `WEBPLOTDIGITIZER_GUIDE.md`
- CSV模板: 已创建

### 需要您操作
1. **截图**: 从PDF截取清晰图表
2. **上传**: 到WebPlotDigitizer
3. **校准**: 设置坐标轴
4. **提取**: 点击数据点
5. **导出**: CSV格式

---

## 数据分析准备

提取数据后，使用以下代码分析：
- `analyze_cu2o_real_data.py` (修改版)
- 拟合三种模型
- 提取$c_1$参数
- 与理论比较

---

## 立即可执行

**现在可以开始**:
1. ✅ 打开Sadowski论文
2. ✅ 截图Fig. 1
3. ✅ 打开WebPlotDigitizer
4. ✅ 开始提取

**等待您提取数据后**，我将继续：
- 数据分析
- 拟合$c_1$
- 生成新图表
- 整合到论文

---

**状态**: 4篇论文就绪，等待数据提取  
**下一步**: 开始WebPlotDigitizer操作
