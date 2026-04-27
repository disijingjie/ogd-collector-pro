#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理零引用参考文献
正文引用格式: [^N]
参考文献格式: [N] 作者.标题...
"""

import re

def main():
    with open('docs/博士论文_最终定稿版_v22.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 扫描正文中所有脚注引用 [^N]
    footnote_refs = set(re.findall(r'\[\^(\d+)\]', content))
    print(f"正文中引用的脚注数量: {len(footnote_refs)}")
    if footnote_refs:
        print(f"引用编号范围: {min(int(x) for x in footnote_refs)} - {max(int(x) for x in footnote_refs)}")
    
    # 2. 找到参考文献列表的位置
    ref_section_match = re.search(r'(# 参考文献|## 参考文献)', content)
    if not ref_section_match:
        print("[ERROR] 未找到参考文献列表")
        return
    
    ref_start = ref_section_match.start()
    ref_section = content[ref_start:]
    
    # 3. 提取参考文献列表中的编号 [N]
    ref_entries = re.findall(r'^\[(\d+)\]\s+(.+?)(?=^\[\d+\]|\Z)', ref_section, re.MULTILINE | re.DOTALL)
    all_ref_nums = set(num for num, _ in ref_entries)
    print(f"参考文献列表总数: {len(all_ref_nums)}")
    
    if not all_ref_nums:
        print("[WARN] 未提取到参考文献，尝试备用正则")
        ref_entries = re.findall(r'\[(\d+)\]\s+([^\n]+)', ref_section)
        all_ref_nums = set(num for num, _ in ref_entries)
        print(f"备用正则提取: {len(all_ref_nums)}篇")
    
    if not all_ref_nums:
        print("[ERROR] 无法提取参考文献")
        return
    
    # 4. 找出未被引用的文献
    unused = sorted(int(x) for x in all_ref_nums - footnote_refs)
    used = sorted(int(x) for x in all_ref_nums & footnote_refs)
    
    print(f"\n被引用的文献: {len(used)}篇")
    print(f"未被引用的文献: {len(unused)}篇 ({len(unused)/len(all_ref_nums)*100:.1f}%)")
    
    if unused:
        print(f"\n未被引用的文献编号（前30个）:")
        for num in unused[:30]:
            entry_match = re.search(rf'\[{num}\]\s+([^\n]+)', ref_section)
            if entry_match:
                title = entry_match.group(1).strip()[:70]
                print(f"  [{num}] {title}")
        if len(unused) > 30:
            print(f"  ... 还有{len(unused)-30}篇未显示")
    
    # 5. 生成报告
    with open('docs/_零引用参考文献清单.md', 'w', encoding='utf-8') as f:
        f.write("# 零引用参考文献清理报告\n\n")
        f.write(f"- 参考文献总数: {len(all_ref_nums)}篇\n")
        f.write(f"- 被引用文献: {len(used)}篇\n")
        f.write(f"- 零引用文献: {len(unused)}篇 ({len(unused)/len(all_ref_nums)*100:.1f}%)\n\n")
        
        f.write(f"## 建议保留的文献（{len(used)}篇）\n\n")
        for num in used:
            entry_match = re.search(rf'\[{num}\]\s+([^\n]+)', ref_section)
            if entry_match:
                f.write(f"- [{num}] {entry_match.group(1).strip()}\n")
        
        f.write(f"\n## 建议删除的零引用文献（{len(unused)}篇）\n\n")
        for num in unused:
            entry_match = re.search(rf'\[{num}\]\s+([^\n]+)', ref_section)
            if entry_match:
                f.write(f"- [{num}] {entry_match.group(1).strip()}\n")
    
    print(f"\n[OK] 报告已保存: docs/_零引用参考文献清单.md")
    print(f"[建议] 删除{len(unused)}篇零引用文献，保留{len(used)}篇")

if __name__ == '__main__':
    main()
