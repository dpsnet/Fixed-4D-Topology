# Zenodo DOI 生成状态

## Release v1.0.1 已发布

**Release URL**: https://github.com/dpsnet/Fixed-4D-Topology/releases/tag/v1.0.1

**发布状态**: ✅ 已发布 (2026-02-07 06:59 UTC+8)

## Zenodo 自动处理

Zenodo 现在会自动：
1. 检测到 GitHub Release v1.0.1
2. 创建代码存档
3. 生成永久 DOI

**预计时间**: 5-30 分钟

## 检查 DOI 状态

访问以下链接查看 DOI 是否已生成：

### 方法 1: GitHub 页面
https://github.com/dpsnet/Fixed-4D-Topology/releases/tag/v1.0.1

查看右侧是否有 "Zenodo DOI" 徽章

### 方法 2: Zenodo 页面
https://zenodo.org/account/settings/github/

查看 dpsnet/Fixed-4D-Topology 的最新存档

### 方法 3: Zenodo 搜索
https://zenodo.org/search?q=Fixed-4D-Topology

搜索项目名称

## 预期 DOI 格式

Zenodo 通常会生成类似以下的 DOI：
- `10.5281/zenodo.148xxxx` (新 DOI)
- 或者可能是 `10.5281/zenodo.8475` (如果与之前关联)

## DOI 生成后更新

一旦获得实际 DOI，更新以下文件：

1. **README.md** - 更新 DOI 徽章
2. **CITATION.cff** - 更新 DOI 字段
3. **papers/README.md** - 更新引用中的 DOI
4. **ZENODO_DOI.md** - 更新为实际 DOI

## 手动更新步骤

```bash
# 1. 获取实际 DOI 后，替换所有占位符
sed -i 's/10.5281\/zenodo.xxxxxxx/10.5281\/zenodo.实际DOI/g' README.md
sed -i 's/10.5281\/zenodo.xxxxxxx/10.5281\/zenodo.实际DOI/g' CITATION.cff
sed -i 's/10.5281\/zenodo.xxxxxxx/10.5281\/zenodo.实际DOI/g' papers/README.md

# 2. 提交更改
git add README.md CITATION.cff papers/README.md ZENODO_DOI.md
git commit -m "Update with actual Zenodo DOI: 10.5281/zenodo.xxxxx"
git push origin master
```

---

**最后更新**: 2026-02-07 06:59 UTC+8

**状态**: ⏳ 等待 Zenodo 处理
