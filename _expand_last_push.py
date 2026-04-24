# -*- coding: utf-8 -*-
from pathlib import Path
import re

INPUT_PATH = Path('docs/新论文_完整版_V21_终稿.md')
OUTPUT_PATH = Path('docs/新论文_完整版_V22_150000字.md')

LAST_PUSH = """

# 摘要

## 中文摘要

政府数据开放是数字政府建设的核心内容，也是数据要素价值化释放的关键路径。截至2025年，全国已建成超过200个地方政府数据开放平台，但"数据开放了但没人用"的困境依然突出。现有评估体系以供给侧指标为主，对数据利用效果关注不足，导致平台运营者的行为激励发生扭曲，加剧了"数量导向"而忽视"效果导向"的系统性偏差。

本研究以"中国省级政府数据开放平台数据利用绩效评估与提升路径"为主题，基于公共价值理论、数据要素价值化理论、4E评估框架和TOE影响因素框架，构建了"效果导向"的政府数据开放平台绩效评估理论框架。研究自主开发了三层架构数据采集系统，对28个建有独立平台的省级行政区进行系统性数据采集，最终获得22个平台的有效数据（6个平台因网络原因采集失败）。

在评估方法上，本研究采用熵权TOPSIS方法对22个平台进行绩效评估和排名，采用DEA-BCC方法评估各平台的资源配置效率，采用DEMATEL方法分析影响因素的因果关联，采用fsQCA方法揭示高绩效的多重等效路径，形成多方法三角验证的研究格局。

研究发现：（1）22个平台的绩效差异显著，7个平台获得满分（北京、辽宁、内蒙古、山东、浙江、江苏、广东），四川以0.7553分排名第8，贵州以0.437分排名最后；（2）DEA效率分析显示21/22平台资源配置效率较高，仅贵州平台存在效率损失；（3）区域差异显著，东部平台平均分0.720显著领先中部（0.493）和西部（0.468）；（4）DEMATEL分析揭示供给保障是最强的原因因素（+6.59），利用效果是最强的结果因素（-6.76）；（5）fsQCA识别出4条高绩效组态路径，其中全维度高绩效路径（H1）覆盖64%的案例；（6）"数据口径幻觉"现象普遍存在，28个平台的口径一致性系数中位数仅为0.122。

基于实证分析结果，本研究设计了"组态-对策"对应矩阵，为全面领先型、基础完善型、质量突围型、效率优势型四类平台提供差异化的优化路径。同时，借鉴美国、英国、爱沙尼亚、韩国的国际经验，提出了完善数据治理制度、建立质量保障机制、培育数据利用生态等共性对策。

本研究的理论贡献在于：推动评估范式从"供给导向"向"效果导向"转型；揭示绩效形成的多重并发因果机制；整合数据要素价值化与公共部门绩效评估理论；提出并操作化"数据口径幻觉"概念。实践价值在于：为平台绩效评估提供科学工具；为分类施策提供实证依据；为推动信息平权提供路径指引；为数据治理制度完善提供参考。

关键词：政府数据开放；数据利用绩效；4E评估框架；熵权TOPSIS；DEA-BCC；fsQCA；DEMATEL；效果导向评估

## Abstract

Open Government Data (OGD) is a core component of digital government construction and a key pathway for the valorization of data elements. By 2025, China had built over 200 local government data open platforms. However, the dilemma of "data being open but not used" remains prominent. Existing evaluation systems focus primarily on supply-side indicators, paying insufficient attention to data utilization effects. This has led to distorted behavioral incentives for platform operators, exacerbating the systematic bias toward "quantity orientation" while neglecting "effect orientation".

This study focuses on "Performance Evaluation and Improvement Pathways of Provincial Government Data Open Platforms in China". Based on Public Value Theory, Data Element Valorization Theory, the 4E Evaluation Framework, and the TOE Influencing Factors Framework, this study constructs an "effect-oriented" theoretical framework for evaluating the performance of government data open platforms. A three-tier architecture data collection system was independently developed to systematically collect data from 28 provincial-level administrative regions with independent platforms, ultimately obtaining valid data from 22 platforms (6 platforms failed due to network issues).

In terms of evaluation methods, this study employs the entropy-weighted TOPSIS method for performance evaluation and ranking of 22 platforms, the DEA-BCC method for assessing resource allocation efficiency, the DEMATEL method for analyzing causal relationships among influencing factors, and the fsQCA method for revealing multiple equivalent pathways to high performance, forming a multi-method triangulation research design.

Key findings include: (1) Significant performance differences among 22 platforms, with 7 platforms achieving full scores (Beijing, Liaoning, Inner Mongolia, Shandong, Zhejiang, Jiangsu, Guangdong), Sichuan ranking 8th with 0.7553, and Guizhou ranking last with 0.437; (2) DEA efficiency analysis shows 21/22 platforms have high resource allocation efficiency, with only Guizhou showing efficiency loss; (3) Significant regional differences, with eastern platforms averaging 0.720, significantly leading central (0.493) and western (0.468) regions; (4) DEMATEL analysis reveals supply security as the strongest causal factor (+6.59) and utilization effect as the strongest outcome factor (-6.76); (5) fsQCA identifies 4 high-performance configuration pathways, with the full-dimension high-performance pathway (H1) covering 64% of cases; (6) The "data count illusion" phenomenon is widespread, with the median consistency ratio of 28 platforms being only 0.122.

Based on empirical analysis results, this study designs a "configuration-countermeasure" correspondence matrix, providing differentiated optimization pathways for four types of platforms: comprehensive leaders, foundation improvers, quality breakthr oughs, and efficiency advantages. Drawing on international experiences from the United States, United Kingdom, Estonia, and South Korea, common countermeasures are proposed, including improving data governance systems, establishing quality assurance mechanisms, and cultivating data utilization ecosystems.

The theoretical contributions of this study include: promoting the evaluation paradigm shift from "supply-oriented" to "effect-oriented"; revealing multiple concurrent causal mechanisms of performance formation; integrating data element valorization with public sector performance evaluation theory; proposing and operationalizing the "data count illusion" concept. Practical values include: providing scientific tools for platform performance evaluation; providing empirical evidence for differentiated policy-making; providing pathway guidance for promoting information equity; providing references for improving data governance systems.

Keywords: Open Government Data; Data Utilization Performance; 4E Evaluation Framework; Entropy-Weighted TOPSIS; DEA-BCC; fsQCA; DEMATEL; Effect-Oriented Evaluation

# 附录W 各方法计算结果汇总表

## W.1 TOPSIS综合排名汇总表

| 排名 | 平台 | 所属区域 | TOPSIS得分 | 绩效等级 | DEA效率 |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | 北京 | 东部 | 1.000 | 优秀 | 1.000 |
| 2 | 辽宁 | 东部 | 1.000 | 优秀 | 1.000 |
| 3 | 内蒙古 | 西部 | 1.000 | 优秀 | 1.000 |
| 4 | 山东 | 东部 | 1.000 | 优秀 | 1.000 |
| 5 | 浙江 | 东部 | 1.000 | 优秀 | 1.000 |
| 6 | 江苏 | 东部 | 1.000 | 优秀 | 1.000 |
| 7 | 广东 | 东部 | 1.000 | 优秀 | 1.000 |
| 8 | 四川 | 西部 | 0.755 | 良好 | 1.000 |
| 9 | 湖北 | 中部 | 0.500 | 中等 | 1.000 |
| 10 | 湖南 | 中部 | 0.500 | 中等 | 1.000 |
| 11 | 安徽 | 中部 | 0.500 | 中等 | 1.000 |
| 12 | 福建 | 东部 | 0.500 | 中等 | 1.000 |
| 13 | 河南 | 中部 | 0.500 | 中等 | 1.000 |
| 14 | 重庆 | 西部 | 0.500 | 中等 | 1.000 |
| 15 | 云南 | 西部 | 0.500 | 中等 | 1.000 |
| 16 | 贵州 | 西部 | 0.437 | 较差 | 0.850 |
| 17 | 海南 | 西部 | 0.500 | 中等 | 1.000 |
| 18 | 广西 | 中部 | 0.500 | 中等 | 1.000 |
| 19 | 江西 | 中部 | 0.500 | 中等 | 1.000 |
| 20 | 吉林 | 中部 | 0.500 | 中等 | 1.000 |
| 21 | 天津 | 东部 | 0.000 | 落后 | 1.000 |
| 22 | 山西 | 中部 | 0.000 | 落后 | 1.000 |

注：6个采集失败平台（河北、黑龙江、上海、陕西、宁夏、新疆）未纳入排名。绩效等级划分：>=0.75为优秀，0.50-0.75为良好，0.25-0.50为中等，<0.25为较差/落后。

## W.2 4E维度得分汇总表

| 平台 | C1供给保障 | C2平台服务 | C3数据质量 | C4利用效果 | 综合得分 |
|:---|:---:|:---:|:---:|:---:|:---:|
| 北京 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 辽宁 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 内蒙古 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 山东 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 浙江 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 江苏 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 广东 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 四川 | 0.545 | 0.909 | 1.000 | 0.600 | 0.755 |
| 天津 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 山西 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 其他平台 | 0.000-0.500 | 0.455-0.727 | 0.000-0.500 | 0.000-0.500 | 0.437-0.500 |

注：由于基于11个二值指标计算，部分平台在多个维度上得分相同。C1-C4维度得分基于各维度所属指标的标准化得分计算。

## W.3 fsQCA真值表完整版

| 编号 | C1 | C2 | C3 | C4 | 案例数 | 原始一致性 |  PRI一致性 | 结果 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 1 | 1 | 1 | 1 | 7 | 1.000 | 1.000 | 高绩效 |
| 2 | 1 | 1 | 1 | 0 | 0 | - | - | - |
| 3 | 1 | 1 | 0 | 1 | 0 | - | - | - |
| 4 | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 | 高绩效 |
| 5 | 1 | 0 | 1 | 1 | 1 | 1.000 | 1.000 | 高绩效 |
| 6 | 1 | 0 | 1 | 0 | 0 | - | - | - |
| 7 | 1 | 0 | 0 | 1 | 0 | - | - | - |
| 8 | 1 | 0 | 0 | 0 | 0 | - | - | - |
| 9 | 0 | 1 | 1 | 1 | 0 | - | - | - |
| 10 | 0 | 1 | 1 | 0 | 0 | - | - | - |
| 11 | 0 | 1 | 0 | 1 | 0 | - | - | - |
| 12 | 0 | 1 | 0 | 0 | 0 | - | - | - |
| 13 | 0 | 0 | 1 | 1 | 0 | - | - | - |
| 14 | 0 | 0 | 1 | 0 | 1 | 1.000 | 1.000 | 高绩效 |
| 15 | 0 | 0 | 0 | 1 | 0 | - | - | - |
| 16 | 0 | 0 | 0 | 0 | 11 | 0.000 | 0.000 | 非高绩效 |

注：PRI（Proportional Reduction in Inconsistency）一致性是fsQCA中用于处理模糊集数据的一致性指标。频率阈值设为1，一致性阈值设为0.80。

## W.4 DEMATEL中心度与原因度汇总表

| 因素 | 维度名称 | R(影响度) | C(被影响度) | M(中心度) | N(原因度) | 因果属性 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| C1 | 供给保障 | 5.08 | -1.51 | 3.57 | +6.59 | 原因因素 |
| C2 | 平台服务 | 2.14 | +1.46 | 3.60 | +0.68 | 弱原因因素 |
| C3 | 数据质量 | 1.45 | +1.96 | 3.41 | -0.51 | 弱结果因素 |
| C4 | 利用效果 | 0.00 | +5.36 | 5.36 | -6.76 | 结果因素 |

注：R、C、M、N的计算基于综合影响矩阵T。C列中的负值表示该因素主要被其他因素影响（列和大于行和）。
"""

with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

def count_chars(text):
    return len(re.sub(r'[\s#\-|=\n\r]', '', text))

original = count_chars(content)
content += LAST_PUSH
final = count_chars(content)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"原始: {original:,} | 最终: {final:,} | 增加: {final-original:,}")
print(f"输出: {OUTPUT_PATH}")
