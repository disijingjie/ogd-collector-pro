#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
删除零引用参考文献（保留正文脚注编号不变）
"""

import re

def main():
    with open('docs/博士论文_最终定稿版_v22.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 扫描正文中所有脚注引用 [^N]
    footnote_refs = set(re.findall(r'\[\^(\d+)\]', content))
    used_nums = set(int(x) for x in footnote_refs)
    
    # 2. 找到参考文献列表
    ref_section_match = re.search(r'(# 参考文献)', content)
    if not ref_section_match:
        print("[ERROR] 未找到参考文献列表")
        return
    
    ref_start = ref_section_match.start()
    before_refs = content[:ref_start]
    ref_section = content[ref_start:]
    
    # 3. 提取并过滤参考文献条目
    # 参考文献条目格式: [N] 内容... （直到下一个[N]或文件结束）
    ref_pattern = r'^(\[(\d+)\]\s+.*?)(?=^\[\d+\]|\Z)'
    entries = re.findall(ref_pattern, ref_section, re.MULTILINE | re.DOTALL)
    
    # 保留被引用的条目
    kept_entries = []
    removed_count = 0
    for full_text, num_str in entries:
        num = int(num_str)
        if num in used_nums:
            kept_entries.append((num, full_text))
        else:
            removed_count += 1
    
    # 按原编号排序
    kept_entries.sort(key=lambda x: x[0])
    
    print(f"保留文献: {len(kept_entries)}篇")
    print(f"删除文献: {removed_count}篇")
    
    # 4. 重建参考文献部分
    # 保留标题和分节标题
    header_lines = []
    for line in ref_section.split('\n'):
        if line.startswith('#') or line.startswith('## '):
            header_lines.append(line)
        elif line.strip() == '':
            header_lines.append(line)
        else:
            break
    
    new_ref_section = '\n'.join(header_lines) + '\n\n'
    
    # 中文文献和英文文献分开处理
    # 简单处理：直接列出保留的文献，不区分中英文
    for num, entry in kept_entries:
        new_ref_section += entry + '\n'
    
    # 5. 合并
    new_content = before_refs + new_ref_section
    
    with open('docs/博士论文_最终定稿版_v22.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] 已保存。文件大小: {len(content)} → {len(new_content)} 字符")
    print(f"[说明] 正文脚注编号未改变，参考文献列表仅保留被引用的{len(kept_entries)}篇")

if __name__ == '__main__':
    main()
