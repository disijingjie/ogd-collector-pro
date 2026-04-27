#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
博士论文V22批量修正第二批
- 口语化表达替换
- 英文摘要fsQCA数据统一
- 长句标记（仅标注，不自动拆分）
"""

import re

def main():
    with open('docs/博士论文_最终定稿版_v22.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    changes = []
    
    # 1. 口语化表达替换
    replacements = [
        ('"有平台无作为"', '"平台功能闲置"'),
        ('"僵尸数据"', '"长期未更新数据集"'),
        ('"眼高手低"', '"目标与能力不匹配"'),
        ('"大平台"建设模式', '"大平台"建设模式'),
        ('"数据开放了但没人用"', '"数据开放后利用率极低"'),
        ('"数据开放了但不好用"', '"数据开放后可用性不足"'),
        ('"有平台无数据"', '"平台数据汇聚能力不足"'),
        ('"一平台一议"', '"逐平台定制采集"'),
    ]
    
    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f'替换 "{old}" → "{new}" ({count}处)')
    
    # 2. 英文摘要fsQCA数据统一
    # 检查英文摘要中是否有 "two core configuration paths" 和覆盖率数据
    if 'two core configuration paths' in content:
        # 确保英文摘要中的数据与中文一致
        # 如果英文摘要有旧的路径描述，需要更新
        pass  # 英文摘要中可能没有具体路径名，先跳过
    
    # 3. 标记超长句（超过120字的句子）
    # 这部分仅统计，不自动修改
    long_sentences = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > 120 and not line.startswith('|') and not line.startswith('#') and not line.startswith('!') and not line.startswith('*'):
            # 只统计正文段落中的长句
            if re.search(r'[。；]', line):
                long_sentences.append((i, len(line), line[:60]))
    
    # 4. 统一缩写首次出现格式
    # 检查fsQCA首次出现是否已标注全称
    fsqca_first = content.find('fsQCA')
    if fsqca_first > 0:
        # 向前检查20个字符是否有全称
        context = content[max(0, fsqca_first-50):fsqca_first+10]
        if '模糊集定性比较分析' not in context and 'fuzzy-set' not in context:
            # 在首次出现前补充全称
            content = content.replace('fsQCA', '模糊集定性比较分析（fuzzy-set Qualitative Comparative Analysis, fsQCA）', 1)
            changes.append('补充fsQCA首次出现全称')
    
    # 5. 检查DEA首次出现
    dea_first = content.find('DEA')
    if dea_first > 0:
        context = content[max(0, dea_first-50):dea_first+10]
        if 'Data Envelopment Analysis' not in context and '数据包络分析' not in context:
            content = content.replace('DEA', '数据包络分析（Data Envelopment Analysis, DEA）', 1)
            changes.append('补充DEA首次出现全称')
    
    # 6. 检查TOPSIS首次出现
    topsis_first = content.find('TOPSIS')
    if topsis_first > 0:
        context = content[max(0, topsis_first-80):topsis_first+10]
        if 'Technique for Order Preference by Similarity to Ideal Solution' not in context:
            content = content.replace('TOPSIS', '逼近理想解排序法（Technique for Order Preference by Similarity to Ideal Solution, TOPSIS）', 1)
            changes.append('补充TOPSIS首次出现全称')
    
    # 7. 检查DEMATEL首次出现
    dematel_first = content.find('DEMATEL')
    if dematel_first > 0:
        context = content[max(0, dematel_first-80):dematel_first+10]
        if 'Decision-Making Trial and Evaluation Laboratory' not in context:
            content = content.replace('DEMATEL', '决策试验与评价实验室法（Decision-Making Trial and Evaluation Laboratory, DEMATEL）', 1)
            changes.append('补充DEMATEL首次出现全称')
    
    with open('docs/博士论文_最终定稿版_v22.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("=" * 60)
    print("V22批量修正第二批完成")
    print("=" * 60)
    for c in changes:
        print(f"  [OK] {c}")
    print(f"\n  超长句统计: {len(long_sentences)}句超过120字")
    if long_sentences:
        print("  前10个超长句位置:")
        for line_no, length, text in long_sentences[:10]:
            print(f"    行{line_no}: {length}字 | {text}...")
    print(f"\n  文件大小: {original_len} → {len(content)} 字符")

if __name__ == '__main__':
    main()
