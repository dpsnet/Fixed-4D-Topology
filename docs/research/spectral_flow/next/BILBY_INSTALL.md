# Bilby + 维度流动 安装说明

## 依赖安装

```bash
# 安装Bilby
pip install bilby

# 安装GWOSC数据获取工具
pip install gwosc

# 安装gwpy (可选)
pip install gwpy
```

## 使用步骤

1. 复制插件文件
   ```bash
   cp bilby_dimflow_plugin.py /path/to/your/analysis/
   ```

2. 在分析脚本中导入
   ```python
   from bilby_dimflow_plugin import DimFlowAnalysis
   ```

3. 运行分析
   ```python
   python bilby_example_gw150914.py
   ```

## 注意事项

- 完整分析需要GWOSC数据下载
- 贝叶斯推断需要较长时间 (小时级)
- 建议先在简单注入测试上验证
