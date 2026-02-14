# 下一步快速启动指南

## 立即行动 (今天)

```bash
# 1. 创建综述论文专用目录
mkdir -p ~/research/unified-dimension-flow-review/{chapters,figures,data,references}

# 2. 初始化Git仓库
cd ~/research/unified-dimension-flow-review
git init
git remote add origin https://github.com/[your-username]/unified-dimension-flow-review.git

# 3. 创建基础文件
touch README.md
touch outline.md
touch chapter1-introduction.tex
```

## 本周任务清单

### 优先级1: 综述论文启动
- [ ] 安装/配置Zotero文献管理
- [ ] 创建文献库，导入现有论文
- [ ] 撰写详细大纲 (每个章节3-5页要点)
- [ ] 收集参考文献 (目标100+篇)
- [ ] 设计图表草图 (10+个)

### 优先级2: GR证明准备
- [ ] 复习热核理论教材
- [ ] 安装Mathematica试用版
- [ ] 下载相关论文 (10+篇)
- [ ] 编写计算脚本框架

### 优先级3: 实验合作
- [ ] 列出10个潜在合作实验室
- [ ] 撰写合作提案草稿
- [ ] 收集目标实验室联系方式

### 优先级4: LIGO学习
- [ ] 安装bilby: `pip install bilby`
- [ ] 完成bilby教程
- [ ] 下载GWOSC数据样本

## 关键时间节点

| 日期 | 事件 | 状态 |
|-----|------|------|
| 2月15日 | Cu₂O开源发布 | ⏰ 必须完成 |
| 2月28日 | 综述大纲v1.0 | 📋 目标 |
| 3月31日 | 综述初稿50% | 📋 目标 |
| 4月30日 | GR计算完成 | 📋 目标 |
| 6月30日 | 综述投稿RMP | 📋 目标 |

## 时间分配建议

```
每周40小时:
├── 综述论文:    20小时 (50%)
├── GR证明:      12小时 (30%)
├── GaAs联系:     6小时 (15%)
└── LIGO学习:     2小时 (5%)
```

## 资源链接

### 综述论文
- RMP投稿指南: https://journals.aps.org/rmp/authors
- 物理综述写作指南: [链接]

### GR证明
- Heat Kernel书籍: "Heat Kernels and Dirac Operators"
- Mathematica文档: https://reference.wolfram.com/

### GaAs实验
- MBE实验室列表: [待整理]
- 量子阱光谱教程: [待整理]

### LIGO分析
- bilby文档: https://lscsoft.docs.ligo.org/bilby/
- GWOSC数据: https://www.gw-openscience.org/

## 联系模板

### 实验合作邮件

```
Subject: Collaboration Proposal: Testing Dimension Flow in GaAs Quantum Wells

Dear Professor [Name],

I am writing to explore a potential collaboration on an exciting experimental 
test of dimension flow theory using GaAs quantum wells.

Our theoretical framework predicts that the effective dimension transitions 
from 3D to 2D as quantum well width decreases, with a universal parameter 
c₁ = 0.5 governing the crossover. This can be tested by measuring Rydberg 
exciton energy levels in quantum wells of varying widths (1-50 nm).

We provide:
- Complete theoretical framework
- Data analysis methodology
- WKB fitting procedures
- Co-authorship on resulting papers

What we need:
- High-quality GaAs/AlGaAs quantum well samples
- Low-temperature spectroscopy facility

Would you be interested in discussing this further?

Best regards,
Wang Bin
[contact info]
```

## 快速决策

**如果只能选一个方向？**
→ 综述论文 (RMP)

**如果有两个协作者？**
→ 综述 + GR证明并行

**如果实验合作失败？**
→ 转向WSe₂或MoS₂系统

**如果LIGO太复杂？**
→ 简化为方法论论文

## 成功检查点

### 2月底检查
- [ ] 综述大纲是否详细可行？
- [ ] 文献库是否>100篇？
- [ ] GR计算是否有初步结果？

### 3月底检查
- [ ] 综述是否完成50%？
- [ ] 是否有实验合作意向？
- [ ] bilby是否安装成功？

### 4月底检查
- [ ] 综述初稿是否完成？
- [ ] GR计算是否完成？
- [ ] 实验合作是否确定？

## 支持文档

| 文档 | 位置 | 用途 |
|-----|------|------|
| NEXT_STEPS_ACTION_PLAN.md | unified_theory/ | 详细计划 |
| PRIORITY_ROADMAP.md | unified_theory/ | 优先级 |
| OPEN_SOURCE_PUBLISHING_PLAN.md | unified_theory/ | 发布策略 |
| PROJECT_CONTEXT.md | unified_theory/ | 项目定位 |

## 一句话总结

> **优先写综述建权威，并行GR补数学，稳步推进实验，灵活处理LIGO。**

---

*快速指南版本*: v1.0  
*最后更新*: 2026-02-14  
*状态*: 立即可用
