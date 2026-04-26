# -*- coding: utf-8 -*-
with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('表6-1展示了DEMATEL分析的中心度、原因度和因果分类结果。')
end_idx = content.find('基于中心度和原因度的综合分析', idx)

old_text = content[idx:end_idx]
new_text = """表6-1展示了DEMATEL分析的中心度、原因度和因果分类结果。

**表6-1 DEMATEL因素中心度与因果分类结果**

| 排序 | 因素 | 代码 | 中心度(Mi) | 原因度(Ri-Ci) | 因果类型 | 政策含义 |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 1 | 供给保障 | C1 | 6.589 | +6.589 | 原因因素 | 制度供给是绩效改善的"第一推动力" |
| 2 | 利用效果 | C4 | 6.760 | -6.760 | 结果因素 | 利用效果是绩效的"最终体现" |
| 3 | 平台服务 | C2 | 4.634 | +0.683 | 原因因素 | 技术基础设施是"硬件支撑" |
| 4 | 数据质量 | C3 | 4.317 | -0.512 | 结果因素 | 质量保障是平台建设的"底线要求" |

*数据来源：DEMATEL计算结果，基于4个评估维度。中心度阈值=5.0。*
*注：原因度>0表示该因素主要影响其他因素；原因度<0表示该因素主要被其他因素影响。*

"""

content = content[:idx] + new_text + content[end_idx:]
with open('docs/博士论文_最终定稿版_v10.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('Table 6-1 updated successfully')
