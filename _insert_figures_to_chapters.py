"""
将图插入到各自章节的正确位置
"""
import re

with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 更新已有图片的路径为v6
path_updates = [
    ('static/v3_chart_46_architecture.png', 'static/thesis_charts_v6/图3-1.png'),
    ('static/v3_chart_24_workflow.png', 'static/thesis_charts_v6/图4-1.png'),
    ('static/thesis_08_dea_topsis_scatter.png', 'static/thesis_charts_v6/图5-3.png'),
    ('static/v3_chart_48_swot.png', 'static/thesis_charts_v6/图7-2.png'),
    ('static/v3_chart_53_strategy_roadmap.png', 'static/thesis_charts_v6/图7-3.png'),
    ('static/thesis_01_platform_types.png', 'static/thesis_charts_v6/图1-2.png'),
    ('static/v3_chart_31_international.png', 'static/thesis_charts_v6/图1-3.png'),
    ('static/thesis_03_topsis.png', 'static/thesis_charts_v6/图3-2.png'),
    ('static/thesis_04_region_comparison.png', 'static/thesis_charts_v6/图5-4.png'),
    ('static/thesis_05_dematel.png', 'static/thesis_charts_v6/图6-1.png'),
    ('static/thesis_05_dematel_causal.png', 'static/thesis_charts_v6/图6-2.png'),
    ('static/thesis_06_fsqca.png', 'static/thesis_charts_v6/图6-3.png'),
    ('static/v3_chart_51_dematel_sensitivity.png', 'static/thesis_charts_v6/图6-4.png'),
    ('static/v3_chart_52_fsqca_robustness.png', 'static/thesis_charts_v6/图6-5.png'),
    ('static/v3_chart_45_maturity_model.png', 'static/thesis_charts_v6/图7-1.png'),
    ('static/thesis_07_histogram.png', 'static/thesis_charts_v6/图1-3.png'),
    ('static/thesis_02_datasets.png', 'static/thesis_charts_v6/图4-2.png'),
]

for old_path, new_path in path_updates:
    content = content.replace(old_path, new_path)

print(f"路径更新完成，共更新 {len(path_updates)} 处")

# 2. 在第三章插入图3-2（在图3-1之后）
fig3_2_insert = """

本研究采用AHP-熵权组合赋权法确定各指标权重，兼顾主观经验与客观信息。图3-2展示了24个指标的最终权重分布。

![图3-2 4E评估指标权重分布](static/thesis_charts_v6/图3-2.png)

**图3-2 4E评估指标权重分布**

*数据来源：AHP-熵权组合赋权计算结果*

图3-2的权重分布揭示了4E评估体系的核心价值取向。权重最高的五个指标依次为：应用成果数量（w=0.089）、API调用深度（w=0.082）、数据更新及时性（w=0.076）、数据格式标准化（w=0.072）和授权运营成效（w=0.069）。

"""

# 在图3-1说明之后插入
marker_3_2 = "第三层为指标层，每个一级维度下设2-3个二级维度，每个二级维度下设2-4个具体测量指标。"
if marker_3_2 in content and "图3-2" not in content:
    content = content.replace(marker_3_2, marker_3_2 + fig3_2_insert)
    print("图3-2 已插入第三章")
else:
    print("图3-2 插入跳过（已存在或标记未找到）")

# 3. 在第五章插入图5-4（在5.5节类型学分析处）
fig5_4_insert = """

不同类型平台在区域分布上呈现出明显的空间集聚特征。图5-4展示了四大类型平台的区域分布和绩效差异。

![图5-4 四大类型平台的区域分布](static/thesis_charts_v6/图5-4.png)

**图5-4 四大类型平台的区域分布**

*数据来源：TOPSIS和DEA计算结果，2025年*

图5-4的区域分析揭示了数据开放平台绩效的空间不均衡性。标杆型平台全部位于东部地区，这些省份凭借雄厚的经济实力、完善的数字基础设施和活跃的创新创业生态，形成了数据开放的领先优势。

"""

# 在第五章类型学分析占位符处插入
marker_5_4 = "[类型学分析将在子代理完成后更新]"
if marker_5_4 in content:
    content = content.replace(marker_5_4, fig5_4_insert)
    print("图5-4 已插入第五章")
else:
    print("图5-4 插入跳过（标记未找到）")

# 4. 在第七章插入图7-1（在7.1节之后、7.2节之前）
fig7_1_insert = """

基于类型学分析和组态分析结果，本研究构建了政府数据开放平台成熟度模型。图7-1展示了平台从"基础级"到"引领级"的五级成熟度演进路径。

![图7-1 政府数据开放平台成熟度模型](static/thesis_charts_v6/图7-1.png)

**图7-1 政府数据开放平台成熟度模型**

如图7-1所示，政府数据开放平台的成熟度分为五个等级：基础级（Level 1）以数据目录发布为核心功能；发展级（Level 2）引入API接口和数据可视化功能；规范级（Level 3）建立数据质量保障体系和用户反馈机制；优化级（Level 4）形成数据利用生态；引领级（Level 5）实现数据要素价值化。23个样本平台中，约61%处于基础级或发展级，约26%处于规范级，仅约13%达到优化级或引领级。

"""

# 在7.1.3节之后、7.2节之前插入
marker_7_1 = '**西部地区的"贵阳模式"**具有启示意义。贵州省凭借大数据综合试验区的政策优势，实现了"后发赶超"。这表明在开放政府数据领域，制度创新和政策支持可以弥补经济基础的不足。'
if marker_7_1 in content and "图7-1" not in content.split("### 7.2")[1] if "### 7.2" in content else True:
    content = content.replace(marker_7_1, marker_7_1 + fig7_1_insert)
    print("图7-1 已插入第七章")
else:
    print("图7-1 插入跳过（已存在或标记未找到）")

# 5. 在第七章插入图7-2（在7.3节开头）
fig7_2_insert = """

针对不同类型平台的差异化特征，本研究构建了"类型-策略"对应矩阵。图7-2展示了四大类型平台的核心短板和优化路径。

![图7-2 差异化优化策略矩阵](static/thesis_charts_v6/图7-2.png)

**图7-2 差异化优化策略矩阵**

图7-2的SWOT分析矩阵为不同类型平台提供了差异化的优化策略。标杆型平台（SO策略）应发挥优势、抓住机遇，重点推进数据要素价值化和授权运营创新；潜力型平台（WO策略）应克服劣势、抓住机遇，重点优化资源配置效率；节约型平台（ST策略）应发挥优势、规避威胁，适度增加资源投入；困境型平台（WT策略）应克服劣势、规避威胁，通过外部支援和系统帮扶逐步改善基础条件。

"""

# 在7.3节第一个标题之后插入
marker_7_2 = "### 7.3 基于 fsQCA 组态路径的差异化提升策略"
if marker_7_2 in content:
    # 找到第一个7.3的位置（避免重复插入到第二个7.3）
    idx = content.find(marker_7_2)
    if idx != -1 and content.find("图7-2", idx, idx+500) == -1:
        content = content[:idx+len(marker_7_2)] + fig7_2_insert + content[idx+len(marker_7_2):]
        print("图7-2 已插入第七章")
    else:
        print("图7-2 插入跳过（已存在）")
else:
    print("图7-2 插入跳过（标记未找到）")

# 保存修改后的内容
with open('docs/博士论文_最终定稿版_v10.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n所有图表插入完成")
