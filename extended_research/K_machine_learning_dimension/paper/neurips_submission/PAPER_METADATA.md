# NeurIPS 2026 Submission Metadata

## 基本信息

| 字段 | 内容 |
|------|------|
| **Title** | Neural Network Effective Dimension: A Geometric Framework for Understanding Generalization |
| **Track** | Main Conference (Algorithms) |
| **Paper Type** | Full Paper (8 pages) |
| **Anonymous Review** | No (Open Research Artifact) |

## 作者信息（已确认）

### 第一作者
- **Name**: Wang Bin (王斌)
- **Email**: wang.bin@foxmail.com
- **Role**: Independent Researcher (独立研究员)
- **Affiliation**: N/A (Independent)
- **Contribution**: Conceptualization, research direction, supervision

### 第二作者
- **Name**: Kimi 2.5 Agent
- **Role**: AI Research Assistant
- **Affiliation**: Moonshot AI
- **Contribution**: Mathematical derivation, software, writing, visualization

## 关键词（优化后）

**Primary Keywords**:
1. Effective dimension
2. Fisher information geometry
3. Neural network generalization
4. Over-parameterization

**Secondary Keywords**:
5. PAC-Bayesian bounds
6. Model complexity
7. Geometric deep learning
8. Cross-direction framework

## 摘要（250字限制）

```
We propose effective dimension (d_eff) as a fundamental measure of neural network 
complexity, grounded in Fisher information geometry. Our framework reveals that typical 
networks operate in a dramatically lower-dimensional parameter subspace than their 
nominal parameter count suggests. We prove (1) existence and uniqueness of d_eff, 
(2) dimension reduction theorems for over-parameterized regimes, and (3) PAC-Bayesian 
generalization bounds scaling as O(√(d_eff/n)) rather than O(√N/n). Through systematic 
experiments (E1-E6) across four research directions---neural networks (K), quantum 
systems (H), complex networks (I), and random fractals (J)---we validate that 
d_eff/N ≈ 20-28% across diverse architectures. The K-I correlation of 0.722 reveals 
deep geometric connections between neural networks and complex networks.
```

**字数**: 124 words (符合限制)

## 补充材料

### 代码提交
- **Repository**: https://github.com/dpsnet/Fixed-4D-Topology
- **Branch**: master
- **Path**: extended_research/K_machine_learning_dimension/
- **Docker**: Available (venv_pytorch/Dockerfile)

### 实验数据
- E1-E6 complete results in experiments/full/
- All figures in paper/figures/
- Data generation scripts in data/

### 伦理声明
- No human subjects
- No personal data
- Open source datasets only
- Transparent AI-assisted methodology

## 提交检查清单

- [x] Title (< 100 characters)
- [x] Abstract (< 250 words)
- [x] Keywords (4-8 terms)
- [x] Main paper (8 pages)
- [x] Bibliography (34 entries)
- [x] Author information confirmed
- [x] Code repository linked
- [x] Ethical considerations addressed

## 联系信息

**通讯作者**: Wang Bin (王斌)
**邮箱**: wang.bin@foxmail.com
**备用**: dpsnet@gmail.com

---

**最后更新**: 2026-02-09
**状态**: Ready for submission
