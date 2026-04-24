"""
整合最终完整论文V2（含真实计算结果的第五、六章）
"""
import os
from pathlib import Path

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def merge():
    print("=" * 80)
    print("整合最终完整论文V2")
    print("=" * 80)
    
    ch1 = read_file('docs/新论文_第一章_绪论.md')
    ch2 = read_file('docs/新论文_第二章_文献综述.md')
    ch3 = read_file('docs/新论文_第三章_理论基础与分析框架.md')
    ch4 = read_file('docs/新论文_第四章_研究设计与数据来源.md')
    ch4_real = read_file('docs/新论文_第四章_数据来源_真实数据版.md')
    ch5_real = read_file('docs/新论文_第五章_真实计算结果版.md')
    ch6_real = read_file('docs/新论文_第六章_真实计算结果版.md')
    ch7 = read_file('docs/新论文_第七章_问题诊断与对策建议.md')
    ch8 = read_file('docs/新论文_第八章_结论与展望.md')
    refs = read_file('docs/真实参考文献列表.md')
    
    # 替换第四章的数据来源部分
    ch4_parts = ch4.split('## 4.3')
    if len(ch4_parts) >= 2:
        rest = ch4_parts[1]
        next_section_idx = rest.find('\n## 4.4')
        if next_section_idx == -1:
            next_section_idx = rest.find('\n## 5.')
        if next_section_idx == -1:
            next_section_idx = len(rest)
        ch4_new = ch4_parts[0] + ch4_real + rest[next_section_idx:]
    else:
        ch4_new = ch4 + '\n\n' + ch4_real
    
    final = """# 中国省级政府数据开放平台数据利用绩效评估与提升路径研究

> 论文版本：V15-RealData（基于真实采集数据的重写版）
> 数据采集时间：2026年4月24日
> 验证编码：OGD-DS-V1-20260424_221138
> 数据来源：OGD-Collector Pro三层架构采集系统
> 代码仓库：https://github.com/disijingjie/ogd-collector-pro

---

"""
    
    chapters = [
        ('第一章 绪论', ch1),
        ('第二章 文献综述', ch2),
        ('第三章 理论基础与分析框架', ch3),
        ('第四章 研究设计与数据来源', ch4_new),
        ('第五章 绩效评估结果分析', ch5_real),
        ('第六章 影响因素与组态分析', ch6_real),
        ('第七章 问题诊断与对策建议', ch7),
        ('第八章 结论与展望', ch8),
        ('参考文献', refs),
    ]
    
    for title, content in chapters:
        final += '\n\n---\n\n# ' + title + '\n\n'
        final += content
        final += '\n\n'
    
    # 附录
    final += """

---

# 附录A：数据采集验证报告

## A.1 验证编码与元数据

- **验证编码**：OGD-DS-V1-20260424_221138
- **数据采集系统**：OGD-Collector Pro v1.0
- **采集时间**：2026年4月24日 18:23 - 22:06
- **采集环境**：Windows 10, Python 3.11, Requests 2.31.0
- **网络环境**：中国联通家庭宽带（北京IP段）
- **采集代码仓库**：https://github.com/disijingjie/ogd-collector-pro

## A.2 采集任务日志

| 任务ID | 任务名称 | 类型 | 状态 | 总平台数 | 成功数 | 失败数 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 省级平台全采 | provincial | completed | 31 | 18 | 13 |
| 2 | 省级平台补采 | provincial | completed | 13 | 4 | 9 |

## A.3 验证数据文件清单

所有验证后的数据文件保存在 `data/verified_dataset/` 目录：

- `verification_report_20260424_221138.json` —— 完整验证报告
- `table_topsis_binary_*.csv` —— TOPSIS排名表（11项指标版）
- `table_dea_*.csv` —— DEA效率分析表
- `dematel_results_*.json` —— DEMATEL分析结果
- `fsqca_results_*.json` —— fsQCA组态分析结果

## A.4 图表文件清单

基于真实数据生成的图表保存在 `static/charts/` 目录：

- `fig4_1_collection_status.png` —— 采集状态分布饼图
- `fig5_1_topsis_ranking.png` —— TOPSIS排名柱状图
- `fig5_2_region_comparison.png` —— 区域均值对比图
- `fig5_3_4e_radar.png` —— 4E维度雷达图

## A.5 数据使用声明

本研究采集的政府数据开放平台公开数据遵循各平台的开放许可协议。采集过程仅执行HTTP GET请求获取公开页面内容，未进行任何数据修改、删除或破坏性操作。所有采集数据仅用于学术研究目的。

"""
    
    output_path = 'docs/新论文_完整版_V15_真实数据.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final)
    
    chinese_chars = len([c for c in final if '\u4e00' <= c <= '\u9fff'])
    total_chars = len(final.replace('\n', '').replace(' ', ''))
    
    print("完整论文已保存:", output_path)
    print("中文字符数:", chinese_chars)
    print("总字符数:", total_chars)
    print("预估中文字数: 约%d字" % chinese_chars)
    print("距离15万字目标还差: 约%d字" % (150000 - chinese_chars))
    
    return output_path

if __name__ == '__main__':
    merge()
