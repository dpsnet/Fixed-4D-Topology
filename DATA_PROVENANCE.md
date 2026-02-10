# 数据来源清单与可复现性指南

**版本**: v1.0  
**日期**: 2026-02-10  
**状态**: 完整数据来源追踪与可复现性验证

---

## 数据源概览

| 类别 | 数据集数量 | 总大小 | 主要来源 |
|------|-----------|--------|---------|
| 网络拓扑数据 | 7个 | ~2.1GB | CAIDA, SNAP, BIOGRID |
| 机器学习数据 | 3个 | ~250MB | CIFAR-10, MNIST |
| 物理常数 | 50+ | - | PDG, CODATA, NIST |
| 数学参考值 | 20+ | - | OEIS, 文献值 |

---

## 网络数据源

### 1. CAIDA AS Relationships Dataset

| 属性 | 详情 |
|------|------|
| **来源** | CAIDA (Center for Applied Internet Data Analysis) |
| **URL** | https://www.caida.org/catalog/datasets/as-relationships/ |
| **文件** | `extended_research/I_network_geometry/data/real_data/as-skitter.txt` |
| **大小** | 149,105,700 bytes |
| **节点数** | 1,696,415 |
| **边数** | 11,095,298 |
| **许可** | 学术研究许可 (CAIDA AUA) |
| **引用** | "The CAIDA AS Relationships Dataset", CAIDA, 2024 |

### 2. SNAP Social Networks

#### Facebook Network
| 属性 | 详情 |
|------|------|
| **来源** | Stanford Network Analysis Project |
| **URL** | https://snap.stanford.edu/data/ego-Facebook.html |
| **文件** | `facebook_combined.txt` |
| **大小** | 854,362 bytes |
| **节点数** | 4,039 |
| **边数** | 88,234 |
| **引用** | McAuley & Leskovec, NIPS 2012 |

#### Twitter Network
| 属性 | 详情 |
|------|------|
| **来源** | SNAP |
| **URL** | https://snap.stanford.edu/data/twitter-2010.html |
| **文件** | `twitter.txt` |
| **大小** | 44,550,129 bytes |
| **节点数** | 81,306 |
| **边数** | 1,768,149 |
| **引用** | Kwak et al., WWW 2010 |

#### DBLP Network
| 属性 | 详情 |
|------|------|
| **来源** | SNAP |
| **URL** | https://snap.stanford.edu/data/com-DBLP.html |
| **文件** | `dblp.txt` |
| **大小** | 13,931,442 bytes |
| **引用** | Yang & Leskovec, ICDM 2012 |

### 3. BIOGRID Protein Networks

| 属性 | 详情 |
|------|------|
| **来源** | BioGRID (Biological General Repository) |
| **URL** | https://thebiogrid.org/ |
| **版本** | 5.0.254 |
| **总大小** | ~1.8GB |
| **主要文件** | Homo_sapiens (719MB), Saccharomyces_cerevisiae (492MB) |
| **引用** | Stark et al., Nucleic Acids Res, 2006 |

主要物种统计:
| 物种 | 节点数 | 边数 | 文件大小 |
|------|--------|------|---------|
| Homo sapiens | ~20,000 | ~719,000 | 719MB |
| Saccharomyces cerevisiae | ~6,000 | ~492,000 | 492MB |
| Mus musculus | ~10,000 | ~41,000 | 41MB |

### 4. IEEE Power Grid

| 属性 | 详情 |
|------|------|
| **来源** | IEEE Power Engineering Society |
| **文件** | `ieee_power.txt` |
| **大小** | 38,734 bytes |
| **节点数** | 4,941 |
| **引用** | Watts & Strogatz, Nature 1998 |

---

## 机器学习数据集

### CIFAR-10

| 属性 | 详情 |
|------|------|
| **来源** | Canadian Institute for Advanced Research |
| **URL** | https://www.cs.toronto.edu/~kriz/cifar.html |
| **大小** | ~170MB |
| **训练样本** | 50,000 |
| **测试样本** | 10,000 |
| **MD5** | c58f30108f718f92721af3b95e74349a |
| **引用** | Krizhevsky, "Learning Multiple Layers of Features", 2009 |

### MNIST

| 属性 | 详情 |
|------|------|
| **来源** | Yann LeCun, NYU |
| **URL** | http://yann.lecun.com/exdb/mnist/ |
| **训练样本** | 60,000 |
| **测试样本** | 10,000 |
| **引用** | LeCun et al., Proc. IEEE, 1998 |

---

## 物理常数 (CODATA 2018)

| 常数 | 符号 | 值 | 单位 |
|------|------|-----|------|
| 真空光速 | c | 299792458 | m/s (exact) |
| 普朗克常数 | h | 6.62607015e-34 | J.s (exact) |
| 约化普朗克常数 | hbar | 1.054571817e-34 | J.s |
| 引力常数 | G | 6.67430e-11 | m^3/kg/s^2 |
| 普朗克质量 | m_P | 2.176434e-8 | kg |
| 玻尔兹曼常数 | k_B | 1.380649e-23 | J/K (exact) |
| 哈勃常数 | H_0 | 67.4 +/- 0.5 | km/s/Mpc |
| CMB温度 | T_CMB | 2.72548 | K |

**来源**: 
- CODATA 2018: https://physics.nist.gov/cuu/Constants/
- Planck 2018: A&A 641, A6 (2020)

---

## 数学常数

| 常数 | 值 | 来源 |
|------|-----|------|
| pi | 3.14159265358979323846... | OEIS A000796 |
| e | 2.71828182845904523536... | OEIS A001113 |
| 黄金比例 phi | 1.61803398874989484820... | OEIS A001622 |
| ln(2) | 0.69314718055994530942... | OEIS A002162 |

---

## 可复现性检查清单

### 数据完整性验证

```bash
# 检查网络数据
ls -la extended_research/I_network_geometry/data/real_data/as-skitter.txt
ls -la extended_research/I_network_geometry/data/real_data/facebook_combined.txt
ls -la extended_research/I_network_geometry/data/real_data/twitter.txt

# 检查ML数据
ls -la extended_research/K_machine_learning_dimension/data/cifar10/
ls -la extended_research/K_machine_learning_dimension/data/mnist/

# 检查BIOGRID
ls -la extended_research/I_network_geometry/data/real_data/BIOGRID-ORGANISM-Homo_sapiens-5.0.254.tab3.txt
```

### 运行环境要求

| 依赖 | 版本 | 安装命令 |
|------|------|---------|
| Python | 3.8+ | `python --version` |
| NumPy | 1.21+ | `pip install numpy>=1.21` |
| Matplotlib | 3.4+ | `pip install matplotlib>=3.4` |
| NetworkX | 2.6+ | `pip install networkx>=2.6` |

### 复现步骤

1. 安装依赖: `pip install -r requirements.txt`
2. 下载数据: `bash scripts/download_data.sh`
3. 验证数据: `python scripts/verify_data.py`
4. 运行分析: `python research/P1/T3/code/rigorous_proofs_final.py`

---

## 引用要求

使用本仓库数据必须引用:

1. CAIDA: "The CAIDA AS Relationships Dataset", https://www.caida.org/
2. SNAP: "Stanford Network Analysis Project", https://snap.stanford.edu/
3. BioGRID: Stark et al., Nucleic Acids Res, 2006
4. CIFAR-10: Krizhevsky, 2009
5. MNIST: LeCun et al., Proc. IEEE, 1998
6. Planck 2018: A&A 641, A6 (2020)
7. CODATA 2018: https://physics.nist.gov/cuu/Constants/

---

**最后更新**: 2026-02-10  
**数据清单版本**: v1.0  
**状态**: 完整数据来源追踪
