# 石墨烯Landau能级数据搜索结果

**搜索日期**: 2026-02-14  
**目标**: 找到可用于提取$c_1(2,1) = 0.5$的实验数据

---

## 高优先级候选论文

### 1. Sadowski et al., PRL 98, 197403 (2007)
**文件**: `sadowski_2007_graphene_landau.pdf` (已下载, 313 KB)

**关键信息**:
- 单层石墨烯红外光谱
- Landau能级跃迁
- 半整数量子Hall效应
- **状态**: 待数据提取

### 2. Jiang et al., PRL 98, 197403 (2007) - 同组工作
**相关论文**:
- "Infrared Spectroscopy of Landau Levels of Graphene"
- 同一作者群，可能相关数据

### 3. Review: Goerbig, RMP 83, 1193 (2011)
**标题**: "Electronic properties of graphene in a strong magnetic field"

**关键信息**:
- Table II: Energy scales at different magnetic fields
- 可能包含汇总数据
- **状态**: 需要查找并评估

---

## 待评估论文清单

| # | 论文 | 年份 | 期刊 | 相关性 | 数据类型 |
|---|------|------|------|--------|----------|
| 1 | Sadowski et al. | 2007 | PRL | ⭐⭐⭐⭐⭐ | 原始光谱 |
| 2 | Review (Goerbig) | 2011 | RMP | ⭐⭐⭐⭐⭐ | 综述数据表 |
| 3 | Henriksen et al. | 2010 | PRL | ⭐⭐⭐⭐ | 高场Landau能级 |
| 4 | Deacon et al. | 2007 | PRL | ⭐⭐⭐⭐ | 跃迁能量 |
| 5 | Orlita et al. | 2008 | PRL | ⭐⭐⭐⭐ | 高能Landau能级 |

---

## 数据提取计划

### 今日任务（2026-02-14剩余时间）
1. **打开WebPlotDigitizer** (https://apps.automeris.io/wpd/)
2. **截图Sadowski论文中的关键图表**:
   - Fig. 1: 透射光谱（Landau能级跃迁）
   - Fig. 2: 跃迁能量随磁场变化
3. **提取数据点**:
   - 至少提取 n = 0, ±1, ±2, ±3 的能量
   - 记录磁场强度

### 预期提取的数据格式
```csv
n,energy_meV,magnetic_field_T,transition_type,source
0,0.0,18,L-1 to L0,Sadowski2007
1,XX.X,18,L0 to L1,Sadowski2007
2,XX.X,18,L1 to L2,Sadowski2007
...
```

---

## 关键物理

### 石墨烯Landau能级公式（相对论性）
$$E_n = \text{sgn}(n) \sqrt{2e\hbar v_F^2 B |n|}$$

其中：
- $v_F \approx 10^6$ m/s (费米速度)
- $B$：磁场强度
- $n$：Landau能级指数

### 分析策略
1. 提取不同$n$的跃迁能量
2. 拟合验证$\sqrt{B|n|}$依赖关系
3. 提取有效维度参数$c_1$
4. 验证$c_1(2,1) = 0.5$

---

## 下一步行动

**立即执行**:
1. 打开WebPlotDigitizer
2. 截图Sadowski论文的Fig. 1和Fig. 2
3. 开始数据提取
4. 记录提取的数据点

**预计时间**: 30-60分钟完成Sadowski论文的数据提取

---

**状态**: 准备开始数据提取  
**下一步**: WebPlotDigitizer操作
