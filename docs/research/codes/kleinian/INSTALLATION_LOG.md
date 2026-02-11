# SnapPy 安装日志

**安装日期**: 2026-02-11  
**安装位置**: `/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/kleinian/`  
**Python版本**: 3.9.25  
**SnapPy版本**: 3.3

---

## 安装概述

SnapPy 是用于研究双曲3-流形和Kleinian群的Python包。本次安装使用pip完成，所有功能测试通过。

## 安装步骤

### 1. Python版本检查

```bash
$ python3 --version
Python 3.9.25
```

Python 3.9.25 满足 SnapPy 的 Python 3.8+ 要求。

### 2. SnapPy安装

```bash
$ pip3 install snappy
```

**安装的主要依赖包:**
- snappy-3.3
- snappy_manifolds-1.4
- spherogram-2.4.1
- cypari-2.5.6
- plink-2.4.8
- FXrays-1.3.6
- knot_floer_homology-1.2.2
- low_index-1.2.1
- ipython-8.18.1
- PyX-0.17
- networkx-3.2.1

### 3. 安装验证

```bash
$ python3 -c "import snappy; print(snappy.__version__)"
3.3
```

### 4. 功能测试

运行了完整的测试脚本 `snappy_test.py`，所有6项测试均通过:

| 测试项目 | 状态 |
|---------|------|
| Import | ✓ PASS |
| Manifold Creation | ✓ PASS |
| Hyperbolic Structure | ✓ PASS |
| Isometry Signature | ✓ PASS |
| Dirichlet Domain | ✓ PASS |
| Census Access | ✓ PASS |

## 核心功能验证

### 双曲3-流形操作

```python
import snappy

# 创建图形8纽结补空间
M = snappy.Manifold('4_1')
print(M.name())      # 4_1
print(M.volume())    # 2.029883...
print(M.num_cusps()) # 1
```

### Dirichlet域计算

```python
domain = M.dirichlet_domain()
print(domain.num_faces())    # 12
print(domain.num_vertices()) # 8
```

### 普查数据访问

```python
census = snappy.OrientableCuspedCensus
# 访问所有可定向有尖点的双曲3-流形
```

## 已知限制

1. **GUI不可用**: 由于系统无图形界面，tkinter相关的GUI功能不可用。这不会影响计算功能。

2. **数值格式化**: SnapPy内部使用特殊数值类型，需要使用 `float()` 转换后才能使用Python格式化字符串。

## 测试脚本

测试脚本位于: `/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/kleinian/snappy_test.py`

运行测试:
```bash
cd /mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/kleinian
python3 snappy_test.py
```

## 参考资源

- SnapPy官方文档: https://snappy.math.uic.edu/
- SnapPy GitHub: https://github.com/3-manifolds/SnapPy
- 双曲3-流形数据库: 已随SnapPy一同安装

## 结论

SnapPy 3.3 成功安装，所有核心功能正常工作，可用于研究双曲3-流形和Kleinian群。
