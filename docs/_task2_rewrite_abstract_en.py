#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务2：重写英文摘要
位置：中文摘要之后
"""

with open('docs/博士论文_最终定稿版_v24.md','r',encoding='utf-8') as f:
    content = f.read()

# 新的英文摘要
new_abstract_en = '''**Abstract:** Open Government Data (OGD) is a critical component of digital government construction and a key pathway for unlocking data value in the era of data要素 marketization. However, existing evaluation systems suffer from a systemic bias of "emphasizing supply over effect"—over-focusing on "how many datasets were released" while neglecting "how much value data has generated"—forming the "Data Calibration Illusion"[^10] phenomenon identified in this study. Based on this core problem, this study constructs a 4E-based evaluation framework (Supply Assurance-Platform Service-Data Quality-Utilization Effect-Equity), comprising 5 first-level dimensions, 9 second-level dimensions, and 24 specific indicators.

This study adopts a multi-method integration approach: AHP-entropy weight combination for indicator weighting; TOPSIS for comprehensive performance evaluation of 23 provincial platforms; DEA-BCC for resource allocation efficiency assessment; DEMATEL for identifying key influencing factors and their causal relationships; fsQCA for revealing multiple equivalent configuration paths of high-performance platforms; and multi-period DID for evaluating the policy effect of "Data Twenty Articles." The findings reveal: (1) Significant performance differences among 23 platforms, with Shandong (0.955), Sichuan, and Liaoning ranking top three, exhibiting a "head concentration" pattern. (2) Only 1 platform (Shandong) is DEA-efficient, indicating that complete correspondence between high performance and high efficiency is extremely rare. (3) DEMATEL analysis reveals a networked structure where four dimensions are mutually causal without distinct cause-result hierarchy. (4) fsQCA reveals two core paths—"full-factor driven" (coverage 81%, suitable for resource-rich provinces) and "service-quality-effect driven" (coverage 19%, suitable for resource-constrained provinces). (5) The "Data Twenty Articles" policy has a significant positive effect on comprehensive performance (+0.043, p<0.01), but with dimensional differences and time lag characteristics.

The theoretical contributions of this study are: first, extending Institutional Isomorphism theory to the Chinese data要素 marketization context, revealing how coercive isomorphism (policy-driven), mimetic isomorphism (benchmark learning), and normative isomorphism (professional standards) shape platform convergence; second, proposing the "Data Calibration Illusion" concept, filling a theoretical gap in measurement bias research. The practical value lies in providing differentiated "configuration path-optimization strategy" matching for different platform types, directly translatable into policy references for the National Data Bureau.

**Keywords:** Open Government Data; Data Utilization Performance; 4E Framework; Data Calibration Illusion; Institutional Isomorphism; TOPSIS; DEA; DEMATEL; fsQCA; Multi-period DID; Optimization Path'''

# 找到英文摘要的开始和结束
old_abstract_en_start = content.find('**Abstract:**')
old_abstract_en_end = content.find('**Keywords:**', old_abstract_en_start)

if old_abstract_en_start != -1 and old_abstract_en_end != -1:
    # 找到关键词那一行的结束位置
    keyword_end = content.find('\n\n', old_abstract_en_end)
    if keyword_end == -1:
        keyword_end = content.find('\n---', old_abstract_en_end)
    
    # 替换英文摘要部分
    content = content[:old_abstract_en_start] + new_abstract_en + '\n\n' + content[keyword_end:]
    print("[+] 英文摘要已重写")
else:
    print("[!] 未找到旧英文摘要位置")

with open('docs/博士论文_最终定稿版_v24.md','w',encoding='utf-8') as f:
    f.write(content)

print(f"[+] 文件已保存，总字符数: {len(content):,}")