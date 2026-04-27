# Kimi任务指令：图1-2修复 + 第二章新增图表

## 任务背景
博士论文V20版本已生成，但存在两个问题：
1. 图1-2（省级政府数据开放平台类型分布）中文字显示为方框（字体缺失/编码问题）
2. 第二章（文献综述）完全没有图表，内容单薄

## 任务一：修复图1-2

### 问题描述
当前图1-2路径：`static/thesis_charts_v6/图1-2.png`
问题：饼图中中文标签显示为方框（□□□□），百分比和数字正常显示

### 数据
23个有效样本平台的类型分布：
- 综合型平台：10个（43.5%）——东部沿海省份为主
- 主题型平台：8个（34.8%）——中部省份为主
- 基础型平台：5个（21.7%）——西部省份为主

### 要求
1. 使用matplotlib重新生成饼图
2. **必须解决中文显示问题**：使用系统自带中文字体（如SimHei、Microsoft YaHei）或指定字体路径
3. 配色使用论文统一配色方案：
   - 综合型：#2E5BFF（蓝色）
   - 主题型：#FF6B35（橙色）
   - 基础型：#00C9A7（绿色）
4. 包含：标题、图例、百分比标注、数量标注
5. 输出尺寸：10x8英寸，300dpi
6. 保存路径：`static/thesis_charts_v6/图1-2.png`（覆盖原文件）

### 参考代码框架
```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 数据
labels = ['综合型平台\n(10个)', '主题型平台\n(8个)', '基础型平台\n(5个)']
sizes = [10, 8, 5]
colors = ['#2E5BFF', '#FF6B35', '#00C9A7']
explode = (0.02, 0.02, 0.02)

fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                   autopct='%1.1f%%', startangle=90, textprops={'fontsize': 14})
ax.set_title('图1-2 省级政府数据开放平台类型分布', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('static/thesis_charts_v6/图1-2.png', dpi=300, bbox_inches='tight')
plt.close()
```

## 任务二：第二章新增图表

### 要求
在第二章新增以下6张图表，保存到 `static/thesis_charts_v6/` 目录：

#### 图2-1：OGD研究文献年度发表量趋势图（2010-2024）
- 类型：折线图+柱状图组合
- 数据（估算，基于CNKI和Web of Science趋势）：
  | 年份 | 中文文献 | 英文文献 |
  |------|----------|----------|
  | 2010 | 5 | 12 |
  | 2012 | 15 | 28 |
  | 2014 | 35 | 55 |
  | 2016 | 68 | 92 |
  | 2018 | 120 | 145 |
  | 2020 | 185 | 198 |
  | 2022 | 220 | 235 |
  | 2024 | 180 | 210 |
- 配色：中文#2E5BFF，英文#FF6B35
- 标注关键政策节点（2015大数据纲要、2022数据二十条）

#### 图2-2：国内外OGD评估工具核心维度对比雷达图
- 类型：雷达图
- 维度：数据供给、平台服务、数据质量、利用效果、制度保障、用户参与
- 数据：
  - 国际工具均值（ODB/OURdata/GODI）：[85, 60, 50, 40, 70, 30]
  - 国内工具均值（开放数林/复旦指数）：[90, 75, 65, 50, 80, 45]
  - 4E框架：        [95, 90, 90, 95, 85, 70]
- 配色：国际#888888，国内#2E5BFF，4E#FF6B35

#### 图2-3：评估方法三代演进时间轴
- 类型：水平时间轴图
- 三代划分：
  - 第一代（2010-2015）：供给导向——GODI、早期指数
  - 第二代（2015-2020）：质量导向——ODB、OURdata、开放数林
  - 第三代（2020-至今）：效果导向——4E框架、生态系统评估
- 每个节点标注代表性工具和核心特征

#### 图2-4：TOE框架三层面因素分解图
- 类型：三层架构图（可用matplotlib的矩形+箭头）
- 技术层面：平台技术、数据标准、API开放度
- 组织层面：部门配合、制度保障、人员能力
- 环境层面：市场需求、政策支持、竞争压力
- 顶层：TOE框架 → 数据开放绩效

#### 图2-5：公共价值三角模型与4E映射图
- 类型：三角形+箭头映射图
- 三角三个顶点：合法性支持、运营能力、公共价值创造
- 分别映射到：E1供给保障、E2+E3平台服务+数据质量、E4利用效果

#### 图2-6：本研究技术路线图
- 类型：流程图（从左到右）
- 阶段：数据采集 → 指标构建 → 权重确定 → 综合评价 → 效率分析 → 因果识别 → 组态分析 → 政策评估
- 对应方法：OGD-Collector → 4E框架 → AHP-熵权 → TOPSIS → DEA → DEMATEL → fsQCA → DID

### 统一格式要求
1. 所有图表尺寸：10x8英寸（流程图可适当加宽）
2. 分辨率：300dpi
3. 中文字体：SimHei/Microsoft YaHei（必须正确显示）
4. 标题格式："图2-X 标题内容"，16号字加粗
5. 图例：12号字
6. 保存格式：PNG

### 输出清单
修复后需确认以下文件存在：
- [ ] static/thesis_charts_v6/图1-2.png（修复）
- [ ] static/thesis_charts_v6/图2-1.png（新增）
- [ ] static/thesis_charts_v6/图2-2.png（新增）
- [ ] static/thesis_charts_v6/图2-3.png（新增）
- [ ] static/thesis_charts_v6/图2-4.png（新增）
- [ ] static/thesis_charts_v6/图2-5.png（新增）
- [ ] static/thesis_charts_v6/图2-6.png（新增）

### 注意事项
1. 如果系统没有SimHei字体，请尝试以下备选：
   - Windows: `C:/Windows/Fonts/simhei.ttf`
   - 备选字体：'Microsoft YaHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei'
2. 如果所有中文字体都不可用，请使用英文标签 + 在论文正文中解释
3. 每个图表生成后请立即检查中文显示是否正常
4. 完成后在论文V20的第二章对应位置插入图片引用代码：
   ```markdown
   ![图2-X 标题](static/thesis_charts_v6/图2-X.png)
   
   **图2-X 标题**
   
   *数据来源：作者整理*
   ```
