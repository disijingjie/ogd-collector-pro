#!/usr/bin/env python3
"""
修复脚本：移除参考文献列表和附录中的脚注标记
"""

import re

INPUT_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\docs\博士论文_最终定稿版_v20.md"
OUTPUT_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\docs\博士论文_最终定稿版_v20_fixed.md"

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 找到参考文献部分的起始位置
    ref_start = text.find('# 参考文献')
    if ref_start == -1:
        ref_start = text.find('## 参考文献')
    
    if ref_start == -1:
        print("未找到参考文献部分")
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(text)
        return
    
    # 分割：正文部分 + 参考文献及之后部分
    body = text[:ref_start]
    ref_section = text[ref_start:]
    
    # 在参考文献部分移除所有 [^数字] 脚注标记
    # 但要注意保留 [数字] 的引用编号（如 [1], [2]）
    # 所以只移除 [^数字] 格式的
    ref_section_cleaned = re.sub(r'\[\^\d+\]', '', ref_section)
    
    # 合并
    new_text = body + ref_section_cleaned
    
    # 统计信息
    body_footnotes = len(re.findall(r'\[\^\d+\]', body))
    removed = len(re.findall(r'\[\^\d+\]', ref_section))
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(new_text)
    
    print(f"✅ 修复完成")
    print(f"   正文脚注保留: {body_footnotes} 个")
    print(f"   参考文献/附录脚注移除: {removed} 个")
    print(f"   输出文件: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
