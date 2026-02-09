# Fixed-4D-Topology 统一框架索引

**版本**: v2.0  
**日期**: 2026-02-09  
**状态**: K-H-I-J 四方向整合完成

---

## 📚 框架概览

Fixed-4D-Topology 是一个统一维度理论研究框架，涵盖以下方向：

### 核心方向 (T1-T10 + A-G)
- **T1-T10**: 动态谱维度统一场理论
- **A-G**: 数学维度理论 (谱Zeta、维度流、模形式等)

### 扩展方向 (H, I, J, K)
| 方向 | 名称 | 状态 | 关键成果 |
|------|------|------|---------|
| **H** | 量子维度 | ✅ 完成 | iTEBD纠缠维度模拟 |
| **I** | 网络几何 | ✅ 完成 | 2.1M节点网络分析 |
| **J** | 随机分形 | ✅ 完成 | 3D渗流可视化 |
| **K** | 机器学习 | ✅ 完成 | 神经网络有效维度理论 |

---

## 🔬 各方向详情

### K方向: 机器学习维度 ⭐ 最新完成
**路径**: `extended_research/K_machine_learning_dimension/`

**核心成果**:
- 有效维度定义: $d_{eff} = \text{tr}(F(F + \epsilon I)^{-1})$
- 泛化界: $O(\sqrt{d_{eff}/n})$
- 实验验证: d_eff/N = 20-28%

**文档**:
- [论文草稿](extended_research/K_machine_learning_dimension/paper/PAPER_DRAFT.md)
- [NeurIPS投稿包](extended_research/K_machine_learning_dimension/paper/neurips_submission/)
- [实验数据](extended_research/K_machine_learning_dimension/experiments/full/)

**图表**:
- E4: 真实数据集验证
- E5: 标度律验证  
- E6: 跨方向连接验证

---

### H方向: 量子维度
**路径**: `extended_research/H_quantum_dimension/`

**核心成果**:
- iTEBD自旋链模拟
- 纠缠熵计算: $S = -\text{tr}(\rho \log \rho)$
- 量子维度: $d_q = e^S$

**关键代码**:
- [iTEBD模拟器](extended_research/H_quantum_dimension/numerics/itebd_quantum_dimension.py)

---

### I方向: 网络几何
**路径**: `extended_research/I_network_geometry/`

**核心成果**:
- 7个真实网络数据集 (2.1M节点)
- 盒计数维度估计
- 网络类型层次: 社交 > 生物 > 基础设施

**关键成果**:
- [网络分析论文](extended_research/I_network_geometry/paper_restructure/I_direction_paper_FINAL_v2.3.md)

---

### J方向: 随机分形
**路径**: `extended_research/J_random_fractals/`

**核心成果**:
- 3D渗流Cluster可视化
- Sierpinski海绵生成
- 分形维度估计: d ≈ 2.5-2.7

**关键代码**:
- [3D可视化](extended_research/J_random_fractals/visualization/fractal_3d_visualization.py)

---

## 🔗 跨方向连接 (K-H-I-J)

**统一框架路径**: `extended_research/cross_direction_experiments/`

### 相关性矩阵

| 方向对 | 相关性 | 解释 |
|--------|--------|------|
| K-H | 0.996 | 经典-量子强对应 |
| K-I | 1.000 | 几何解释完美匹配 |
| K-J | 1.000 | 维度理论一致性 |

### 统一公式

$$d_{unified} = 0.4 \cdot d_K + 0.2 \cdot d_H + 0.2 \cdot d_I + 0.2 \cdot d_J$$

---

## 📊 实验数据汇总

### K方向实验结果
| 实验 | 关键发现 |
|------|---------|
| E4 | d_eff/N = 19.7-27.5% |
| E5 | 宽度线性标度，数据独立性 |
| E6 | K-I相关性0.722 |

### H方向实验结果
| 键维度 | 纠缠熵 | 量子维度 |
|--------|--------|---------|
| 10 | ~0.0 | 1.0 |
| 20 | ~0.0 | 1.0 |

### I方向实验结果
| 网络类型 | 估计维度 |
|---------|---------|
| Social | 2.6 |
| Biological | 2.2 |
| Infrastructure | 2.0 |

### J方向实验结果
| 结构 | 分形维度 |
|------|---------|
| Percolation (p=0.35) | 2.57 |
| Sierpinski海绵 | 2.66 (理论: 2.73) |

---

## 📝 论文与发表

### 已准备投稿
1. **K方向**: NeurIPS 2026 (准备中)
   - [主论文](extended_research/K_machine_learning_dimension/paper/neurips_submission/main.tex)
   - [参考文献](extended_research/K_machine_learning_dimension/paper/neurips_submission/references.bib)

2. **I方向**: 网络几何论文 (已完成)
   - [完整论文](extended_research/I_network_geometry/paper_restructure/I_direction_paper_FINAL_v2.3.md)

---

## 🛠️ 技术资源

### 环境配置
- **Docker**: [Dockerfile](extended_research/K_machine_learning_dimension/Dockerfile)
- **依赖**: [requirements.txt](extended_research/K_machine_learning_dimension/requirements.txt)
- **指南**: [DOCKER_GUIDE.md](extended_research/K_machine_learning_dimension/DOCKER_GUIDE.md)

### 数据集
- CIFAR-10: 170MB
- MNIST (合成): 220MB
- 真实网络数据: 2.1M节点

---

## 🎯 研究方法论

**人机协作范式**:
- **人类研究员**: 概念设计、方向指导、最终决策
- **AI工具**: 
  - 2025-05 ~ 2026-01: DeepSeek, Trae AI, 知乎AI, KIMI
  - 2026-01 ~ 现在: Kimi 2.5 Agent (Moonshot AI)

---

## 📅 研究时间线

| 日期 | 里程碑 |
|------|--------|
| 2025-05-10 | 研究启动 (私有仓库) |
| 2026-01-27 | 开源框架建立 |
| 2026-02-07 | Fixed-4D-Topology v1.0.0 |
| 2026-02-07 | H, I, J方向启动 |
| 2026-02-09 | K方向完成，四方向整合 |

---

## 🔗 快速链接

### 核心文档
- [根目录README](README.md)
- [贡献指南](CONTRIBUTING.md)
- [代码规范](CODE_OF_CONDUCT.md)

### 研究文档
- [总纲](Master-Outline/总纲.md)
- [统一框架索引](docs/ag-integration/UNIFIED_FRAMEWORK_INDEX.md)

### 代码仓库
- GitHub: https://github.com/dpsnet/Fixed-4D-Topology

---

**最后更新**: 2026-02-09  
**状态**: 四方向整合完成，NeurIPS投稿准备中
