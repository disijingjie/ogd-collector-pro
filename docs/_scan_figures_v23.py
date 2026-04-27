#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('docs/博士论文_最终定稿版_v23.md','r',encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
current_chapter = None
figures = {}
tables = {}

for line in lines:
    ch_match = re.match(r'^(#+) .*第([一二三四五六七八])章', line)
    if ch_match:
        current_chapter = ch_match.group(2)
        figures[current_chapter] = []
        tables[current_chapter] = []
    
    if current_chapter:
        fig_match = re.search(r'图([1-8])-(\d+)', line)
        if fig_match and '图' in line:
            fig_id = f'图{fig_match.group(1)}-{fig_match.group(2)}'
            if fig_id not in figures[current_chapter]:
                figures[current_chapter].append(fig_id)
        
        tab_match = re.search(r'表([1-8])-(\d+)', line)
        if tab_match and '表' in line:
            tab_id = f'表{tab_match.group(1)}-{tab_match.group(2)}'
            if tab_id not in tables[current_chapter]:
                tables[current_chapter].append(tab_id)

ch_names = {'一':'1','二':'2','三':'3','四':'4','五':'5','六':'6','七':'7','八':'8'}
print('=== 各章图表分布 ===')
for ch in ['一','二','三','四','五','六','七','八']:
    if ch in figures:
        print(f'第{ch_names[ch]}章: 图{len(figures[ch])}张 {sorted(figures[ch])}, 表{len(tables[ch])}张 {sorted(tables[ch])}')

print()
print('=== 缺失图表编号 ===')
for ch in ['一','二','三','四','五','六','七','八']:
    if ch not in figures:
        continue
    ch_num = ch_names[ch]
    fig_nums = sorted([int(re.search(r'-(\d+)',f).group(1)) for f in figures[ch]])
    tab_nums = sorted([int(re.search(r'-(\d+)',t).group(1)) for t in tables[ch]])
    
    if fig_nums:
        missing_figs = [i for i in range(1, max(fig_nums)+1) if i not in fig_nums]
        if missing_figs:
            print(f'第{ch_num}章缺图: {[f"图{ch_num}-{i}" for i in missing_figs]}')
    
    if tab_nums:
        missing_tabs = [i for i in range(1, max(tab_nums)+1) if i not in tab_nums]
        if missing_tabs:
            print(f'第{ch_num}章缺表: {[f"表{ch_num}-{i}" for i in missing_tabs]}')

print()
print('=== 总计 ===')
total_figs = sum(len(v) for v in figures.values())
total_tabs = sum(len(v) for v in tables.values())
print(f'全文: 图{total_figs}张, 表{total_tabs}张')
