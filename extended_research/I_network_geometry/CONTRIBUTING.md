# 贡献指南

感谢您对**复杂网络有效维度**项目的兴趣！我们欢迎各种形式的贡献。

---

## 如何贡献

### 1. 报告问题 (Reporting Issues)

如果您发现bug或有改进建议：

1. 检查是否已有相关问题
2. 创建新issue，包含：
   - 问题描述
   - 复现步骤
   - 预期 vs 实际结果
   - 环境信息（Python版本、操作系统）

### 2. 提交代码 (Submitting Code)

#### 步骤

1. **Fork 仓库**
   ```bash
   git clone https://github.com/dpsnet/Fixed-4D-Topology.git
   cd Fixed-4D-Topology
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行修改**
   - 添加代码
   - 更新文档
   - 添加测试

4. **提交更改**
   ```bash
   git add .
   git commit -m "Add: 描述你的更改"
   git push origin feature/your-feature-name
   ```

5. **创建 Pull Request**
   - 描述更改内容
   - 说明解决的问题
   - 等待审核

### 3. 添加新数据集

如果您有新的网络数据集：

- 确保数据可公开使用
- 提供数据来源和引用
- 添加数据解析代码
- 更新文档

### 4. 改进文档

- 修正错别字
- 完善说明
- 添加示例
- 翻译

---

## 代码规范

### Python代码风格

- 使用清晰的变量名
- 添加docstring注释
- 每行不超过100字符
- 纯Python标准库，无外部依赖

### 示例

```python
def compute_box_dimension(graph, max_box=10):
    """
    Compute box-counting dimension of a network.
    
    Args:
        graph: Dict[int, Set[int]], adjacency list representation
        max_box: int, maximum box size
        
    Returns:
        float: estimated box dimension
    """
    # 实现代码
    pass
```

---

## 贡献类型

### 🐛 Bug修复
- 修复代码错误
- 改进算法稳定性
- 优化性能

### 💡 新功能
- 添加新的维度测量方法
- 支持更多网络类型
- 可视化改进

### 📊 新数据
- 添加公开网络数据集
- 提供数据预处理脚本
- 补充数据说明

### 📝 文档
- 改进README
- 添加教程
- 翻译文档

### 🎨 可视化
- 创建图表
- 改进结果展示
- 交互式可视化

---

## 审核流程

1. 提交Pull Request
2. 维护者审核代码
3. 讨论修改（如需）
4. 合并到主分支

---

## 行为准则

- 尊重所有贡献者
- 建设性反馈
- 专注于技术讨论
- 欢迎新手

---

## 联系方式

有问题？创建issue或联系：
- GitHub Issues: https://github.com/dpsnet/Fixed-4D-Topology/issues

---

感谢您的贡献！
