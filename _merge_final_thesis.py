"""
整合所有章节为最终完整论文
将真实数据版内容嵌入到对应位置
"""
import os
from pathlib import Path

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def merge_final_thesis():
    print("=" * 80)
    print("整合最终完整论文")
    print("=" * 80)
    
    # 读取各章
    ch1 = read_file('docs/新论文_第一章_绪论.md')
    ch2 = read_file('docs/新论文_第二章_文献综述.md')
    ch3 = read_file('docs/新论文_第三章_理论基础与分析框架.md')
    ch4 = read_file('docs/新论文_第四章_研究设计与数据来源.md')
    ch4_real = read_file('docs/新论文_第四章_数据来源_真实数据版.md')
    ch5 = read_file('docs/新论文_第五章_绩效评估结果分析.md')
    ch5_real = read_file('docs/新论文_第五章_真实数据评估结果.md')
    ch6 = read_file('docs/新论文_第六章_影响因素与组态分析.md')
    ch7 = read_file('docs/新论文_第七章_问题诊断与对策建议.md')
    ch8 = read_file('docs/新论文_第八章_结论与展望.md')
    refs = read_file('docs/真实参考文献列表.md')
    
    # 替换第四章的数据来源部分
    # 找到4.3节的位置，替换为真实数据版
    ch4_parts = ch4.split('## 4.3')
    if len(ch4_parts) >= 2:
        # 找到4.3之后的下一个##的位置
        rest = ch4_parts[1]
        next_section_idx = rest.find('\n## 4.4')
        if next_section_idx == -1:
            next_section_idx = rest.find('\n## 5.')
        if next_section_idx == -1:
            next_section_idx = len(rest)
        ch4_new = ch4_parts[0] + ch4_real + rest[next_section_idx:]
    else:
        ch4_new = ch4 + '\n\n' + ch4_real
    
    # 替换第五章的绩效评估部分
    # 将5.1节替换为真实数据版（保留5.2及以后作为补充分析）
    ch5_parts = ch5.split('## 5.1')
    if len(ch5_parts) >= 2:
        rest = ch5_parts[1]
        next_section_idx = rest.find('\n## 5.2')
        if next_section_idx == -1:
            next_section_idx = rest.find('\n## 6.')
        if next_section_idx == -1:
            next_section_idx = len(rest)
        ch5_new = ch5_parts[0] + ch5_real + '\n\n## 5.2' + rest[next_section_idx:]
    else:
        ch5_new = ch5_real + '\n\n' + ch5
    
    # 合并完整论文
    final = """# 中国省级政府数据开放平台数据利用绩效评估与提升路径研究

> 论文版本：基于真实采集数据的重写版（V15-RealData）
> 数据采集时间：2026年4月24日
> 验证编码：OGD-DS-V1-20260424_221138
> 数据来源：OGD-Collector Pro三层架构采集系统

---

"""
    
    chapters = [
        ('第一章 绪论', ch1),
        ('第二章 文献综述', ch2),
        ('第三章 理论基础与分析框架', ch3),
        ('第四章 研究设计与数据来源', ch4_new),
        ('第五章 绩效评估结果分析', ch5_new),
        ('第六章 影响因素与组态分析', ch6),
        ('第七章 问题诊断与对策建议', ch7),
        ('第八章 结论与展望', ch8),
        ('参考文献', refs),
    ]
    
    for title, content in chapters:
        final += '\n\n---\n\n# ' + title + '\n\n'
        final += content
        final += '\n\n'
    
    # 添加附录
    final += """

---

# 附录A：数据采集验证报告

本附录提供数据采集的完整验证信息，确保研究数据的可追溯性和可复现性。

## A.1 验证编码与元数据

- **验证编码**：OGD-DS-V1-20260424_221138
- **数据采集系统**：OGD-Collector Pro v1.0
- **采集时间**：2026年4月24日 18:23 - 22:06
- **采集环境**：Windows 10, Python 3.11, Requests 2.31.0
- **网络环境**：中国联通家庭宽带（北京IP段）
- **采集代码仓库**：https://github.com/disijingjie/ogd-collector-pro

## A.2 采集任务日志

| 任务ID | 任务名称 | 任务类型 | 状态 | 总平台数 | 成功数 | 失败数 | 开始时间 | 完成时间 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 省级平台全采 | provincial | completed | 31 | 18 | 13 | 2026-04-24T18:23 | 2026-04-24T19:59 |
| 2 | 省级平台补采 | provincial | completed | 13 | 4 | 9 | 2026-04-24T22:02 | 2026-04-24T22:06 |

## A.3 数据文件清单

验证后的数据文件保存在 `data/verified_dataset/` 目录：

- `verification_report_20260424_221138.json` —— 完整验证报告（JSON格式）
- `table1_collection_status_20260424_221037.csv` —— 采集状态表
- `table2_topsis_ranking_20260424_221037.csv` —— TOPSIS排名表

## A.4 图表文件清单

基于真实数据生成的图表保存在 `static/charts/` 目录：

- `fig4_1_collection_status.png` —— 采集状态分布饼图
- `fig5_1_topsis_ranking.png` —— TOPSIS排名柱状图
- `fig5_2_region_comparison.png` —— 区域均值对比图
- `fig5_3_4e_radar.png` —— 4E维度雷达图

## A.5 数据使用许可

本研究采集的政府数据开放平台公开数据遵循各平台的开放许可协议。采集过程仅执行HTTP GET请求获取公开页面内容，未进行任何数据修改、删除或破坏性操作。所有采集数据仅用于学术研究目的。

"""
    
    # 保存
    output_path = 'docs/新论文_完整版_真实数据.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final)
    
    # 统计字数
    chinese_chars = len([c for c in final if '\u4e00' <= c <= '\u9fff'])
    total_chars = len(final.replace('\n', '').replace(' ', ''))
    
    print("完整论文已保存:", output_path)
    print("中文字符数:", chinese_chars)
    print("总字符数:", total_chars)
    print("预估中文字数: 约%d字" % chinese_chars)
    
    return output_path

if __name__ == '__main__':
    merge_final_thesis()
