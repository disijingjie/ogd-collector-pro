#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
博士论文全文结构扫描器
识别章节混乱、图表错位、内容缺失等问题
"""

import re

def analyze_thesis(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    
    results = {
        'chapters': [],
        'sections': [],
        'figures': [],
        'tables': [],
        'issues': []
    }
    
    current_chapter = None
    current_chapter_num = 0
    
    for i, line in enumerate(lines, 1):
        # 识别章
        chapter_match = re.match(r'^# (第[一二三四五六七八]章.*?)$', line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            cn_nums = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8}
            for cn, num in cn_nums.items():
                if f'第{cn}章' in current_chapter:
                    current_chapter_num = num
                    break
            results['chapters'].append({'line': i, 'title': current_chapter, 'num': current_chapter_num})
            continue
        
        # 识别节 (### X.X)
        section_match = re.match(r'^(### (\d+\.\d+).*?)$', line)
        if section_match:
            section_title = section_match.group(1)
            section_num = section_match.group(2)
            section_main = int(section_num.split('.')[0])
            results['sections'].append({
                'line': i, 
                'title': section_title, 
                'num': section_num,
                'chapter': current_chapter_num
            })
            # 检查节编号是否与当前章匹配
            if current_chapter_num and section_main != current_chapter_num:
                results['issues'].append({
                    'type': '章节编号错位',
                    'line': i,
                    'detail': f'第{current_chapter_num}章中出现编号为{section_num}的节（应为{current_chapter_num}.X）',
                    'severity': '严重'
                })
            continue
        
        # 识别图
        fig_match = re.search(r'图(\d+)-(\d+)', line)
        if fig_match and ('**图' in line or '![图' in line or '从图' in line or '如图' in line):
            ch = int(fig_match.group(1))
            idx = int(fig_match.group(2))
            results['figures'].append({'line': i, 'chapter': ch, 'index': idx, 'text': line[:80]})
            if current_chapter_num and ch != current_chapter_num and '详见' not in line:
                results['issues'].append({
                    'type': '图表跨章引用',
                    'line': i,
                    'detail': f'第{current_chapter_num}章中引用了图{ch}-{idx}（可能错位）',
                    'severity': '警告'
                })
        
        # 识别表
        table_match = re.search(r'表(\d+)-(\d+)', line)
        if table_match and ('**表' in line or '如表' in line or '从表' in line):
            ch = int(table_match.group(1))
            idx = int(table_match.group(2))
            results['tables'].append({'line': i, 'chapter': ch, 'index': idx, 'text': line[:80]})
            if current_chapter_num and ch != current_chapter_num and '详见' not in line:
                results['issues'].append({
                    'type': '表格跨章引用',
                    'line': i,
                    'detail': f'第{current_chapter_num}章中引用了表{ch}-{idx}（可能错位）',
                    'severity': '警告'
                })
    
    # 统计每章图表数量
    chapter_fig_count = {}
    chapter_table_count = {}
    for fig in results['figures']:
        ch = fig['chapter']
        chapter_fig_count[ch] = chapter_fig_count.get(ch, 0) + 1
    for tbl in results['tables']:
        ch = tbl['chapter']
        chapter_table_count[ch] = chapter_table_count.get(ch, 0) + 1
    
    return results, chapter_fig_count, chapter_table_count

if __name__ == '__main__':
    filepath = 'docs/博士论文_最终定稿版_v23.md'
    results, fig_count, tbl_count = analyze_thesis(filepath)
    
    print("=" * 70)
    print("博士论文全文结构扫描报告")
    print("=" * 70)
    
    print("\n【一、章节结构】")
    for ch in results['chapters']:
        print(f"  第{ch['num']}章 | 行{ch['line']:>5} | {ch['title']}")
    
    print("\n【二、图表分布统计】")
    all_chapters = sorted(set(list(fig_count.keys()) + list(tbl_count.keys())))
    for ch in all_chapters:
        fc = fig_count.get(ch, 0)
        tc = tbl_count.get(ch, 0)
        print(f"  第{ch}章 | 图: {fc:>3}个 | 表: {tc:>3}个")
    
    print("\n【三、结构性问题】")
    severe = [i for i in results['issues'] if i['severity'] == '严重']
    warn = [i for i in results['issues'] if i['severity'] == '警告']
    
    print(f"  严重问题: {len(severe)}个")
    for i in severe:
        print(f"    [行{i['line']:>5}] {i['type']}: {i['detail']}")
    
    print(f"\n  警告问题: {len(warn)}个")
    for i in warn[:15]:
        print(f"    [行{i['line']:>5}] {i['type']}: {i['detail']}")
    if len(warn) > 15:
        print(f"    ... 还有{len(warn)-15}个警告未显示")
    
    print("\n【四、图表清单】")
    print("  图:")
    for fig in sorted(results['figures'], key=lambda x: (x['chapter'], x['index'])):
        print(f"    图{fig['chapter']}-{fig['index']} | 行{fig['line']:>5}")
    print("  表:")
    for tbl in sorted(results['tables'], key=lambda x: (x['chapter'], x['index'])):
        print(f"    表{tbl['chapter']}-{tbl['index']} | 行{tbl['line']:>5}")
