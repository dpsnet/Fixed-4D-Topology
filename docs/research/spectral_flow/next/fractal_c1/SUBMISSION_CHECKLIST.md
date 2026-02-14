# PRL 投稿检查清单

## 投稿前必须完成

### 文档准备
- [x] 论文正文 (LaTeX源文件: `prl_paper.tex`)
- [x] 图表 (Figure 1, Figure 2)
- [x] 参考文献格式化
- [x] Cover Letter撰写
- [ ] 生成PDF文件
- [ ] 补充材料 (可选)

### 作者信息
- [ ] 确认所有作者名单
- [ ] 确认作者单位
- [ ] 确认通讯作者邮箱
- [ ] 获得所有作者同意

### 格式检查
- [ ] 字数限制 (~3500词，当前~2250词 ✅)
- [ ] 图表分辨率 (≥300 dpi)
- [ ] 参考文献格式 (PRL格式)
- [ ] PACS代码确认

---

## PACS 代码建议

| 代码 | 描述 | 适用性 |
|------|------|--------|
| 71.35.-y | Excitons and related phenomena | ✅ 主要 |
| 03.65.Sq | Semiclassical theories | ✅ 方法 |
| 04.60.-m | Quantum gravity | ✅ 理论联系 |
| 78.20.-e | Optical properties | ✅ 实验 |

---

## 投稿步骤

### 1. 准备PDF
```bash
# 如果有LaTeX环境
pdflatex prl_paper.tex
bibtex prl_paper
pdflatex prl_paper.tex
pdflatex prl_paper.tex

# 或使用Overleaf (在线LaTeX编辑器)
# https://www.overleaf.com/
```

### 2. 准备投稿文件
- `prl_paper.pdf` - 主论文
- `figure1_schematic.pdf` - 图1 (高质量)
- `figure2_data_analysis.pdf` - 图2 (高质量)
- `cover_letter.pdf` - Cover letter
- `supplementary_materials.pdf` - 补充材料 (可选)

### 3. PRL在线投稿
1. 访问: https://journals.aps.org/prl/
2. 注册/登录账号
3. 点击 "Submit a Manuscript"
4. 选择 "Physical Review Letters"
5. 按照向导上传文件

### 4. 填写信息
- 标题: "Experimental extraction of the dimension flow parameter from Rydberg excitons"
- 作者: [按顺序列出]
- 摘要: [复制自论文]
- PACS: 71.35.-y, 03.65.Sq, 04.60.-m, 78.20.-e
- 关键词: dimension flow, Rydberg excitons, quantum defect, effective dimension

### 5. 推荐审稿人
建议3-5位审稿人：
1. [Expert in Rydberg excitons] - [Institution] - [Email]
2. [Expert in quantum gravity/dimension] - [Institution] - [Email]
3. [Expert in semiconductor spectroscopy] - [Institution] - [Email]

### 6. 费用
- PRL发表费: ~$2700 (如果接受)
- 彩色图费: 通常免费(在线)
- 页面超限: PRL有严格页数限制，目前符合

---

## 投稿后流程

### 审稿周期
- 初审: 1-2周 (编辑决定是否送审)
- 外审: 4-6周
- 总周期: 6-8周

### 可能结果
1. **Accept** (罕见): 直接接受
2. **Minor revision**: 小修改后接受
3. **Major revision**: 大修改后重审
4. **Reject**: 拒稿，可转投PRB

### 备选方案
如果PRL拒稿或要求重大修改：
- **PRB Rapid Communication**: 快速发表，影响因子~3.7
- **New Journal of Physics**: 开放获取，影响因子~3.5
- **Scientific Reports**: Nature旗下，开放获取

---

## 补充材料建议

### 可包含内容
1. 完整数据表 (23个能级)
2. 详细拟合参数
3. 稳健性检验细节
4. 理论推导附录

### 格式
- 独立PDF文件
- 命名为 `supplementary_materials.pdf`
- 在正文中引用 "See Supplemental Material [25] for..."

---

## 数据可用性声明

PRL要求数据可用性声明。在论文末尾添加：

```
Data availability: The data used in this study are available 
in the Supplemental Material and from the corresponding author 
upon reasonable request.
```

---

## 最终检查

### 今天必须完成
- [ ] 编译生成PDF
- [ ] 检查PDF所有页面显示正常
- [ ] 核对作者信息和单位
- [ ] 确认图表清晰可读

### 明天投稿
- [ ] 上传所有文件到PRL系统
- [ ] 填写所有必填信息
- [ ] 确认Cover Letter已上传
- [ ] 提交并保存确认编号

---

## 联系方式

**PRL编辑部**: prl@aps.org  
**投稿帮助**: https://journals.aps.org/authors  

**紧急情况**：
- 投稿问题: authors@aps.org
- 技术问题: support@aps.org

---

## 时间表

| 日期 | 任务 | 状态 |
|------|------|------|
| 2026-02-13 | 论文完成 | ✅ |
| 2026-02-14 | 生成PDF | ⏳ |
| 2026-02-15 | 投稿PRL | ⏳ |
| 2026-04-15 | 预期初审结果 | ⏳ |

---

**准备好投稿了吗？** 确保所有检查项完成后，即可提交！
