# Docker 使用指南

本Docker环境确保K方向实验的可复现性。

## 快速开始

### 1. 构建镜像

```bash
docker build -t k-direction:latest .
```

或使用docker-compose:
```bash
docker-compose build
```

### 2. 运行实验

```bash
# 进入交互式容器
docker run -it -v $(pwd)/data:/workspace/data \
  -v $(pwd)/results:/workspace/results \
  k-direction:latest

# 在容器内运行实验
cd experiments/full
python3 e4_real_dataset_simulation.py
python3 e5_scaling_laws.py
python3 e6_cross_direction.py
```

### 3. 使用docker-compose

```bash
# 启动研究环境
docker-compose up -d k-direction-research
docker-compose exec k-direction-research bash

# 启动Jupyter
docker-compose up jupyter
# 访问 http://localhost:8888
```

## 目录结构

```
/workspace/
├── data/           # 数据集目录
├── experiments/    # 实验脚本
├── paper/          # 论文相关文件
├── results/        # 实验结果输出
└── code/           # 核心代码库
```

## 保存结果

容器内的`/workspace/results`目录会映射到主机的`./results`，实验结果会自动保存。

## 复现实验

```bash
# 完整复现
docker run -v $(pwd)/results:/workspace/results k-direction:latest \
  python3 experiments/full/run_all_full_experiments.py
```
