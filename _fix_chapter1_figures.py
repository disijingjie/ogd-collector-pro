"""
修复第一章中错误插入的其他章节图表
策略：
1. 从第一章移除图5-4、图7-1、图3-2、图7-2的描述
2. 在各自章节插入这些图表
3. 删除重复的图1-2
"""
import re

with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print(f"总行数: {len(lines)}")

# 找到需要删除的段落
# 1. 图5-4段落 (第44-53行, 0-indexed: 43-52)
# 2. 图7-1段落 (第54-61行, 0-indexed: 53-60)
# 3. 重复的图1-2 (第66-73行, 0-indexed: 65-72)
# 4. 图3-2段落 (第118-127行, 0-indexed: 117-126)
# 5. 图7-2段落 (第136-143行, 0-indexed: 135-142)

# 先打印这些行的内容确认
for i in [43, 53, 65, 117, 135]:
    print(f"\n行{i+1}: {lines[i][:80]}")

# 构建删除列表
delete_ranges = [
    (43, 53),   # 图5-4: 行44-54 ("不同类型平台在区域分布上..." 到 "...领先优势。")
    (53, 61),   # 图7-1: 行54-62 ("基于类型学分析..." 到 "...13%达到优化级或引领级。")
    (65, 73),   # 重复图1-2: 行66-74 (重复的图1-2图片+标题+来源+说明)
    (117, 127), # 图3-2: 行118-128 ("本研究采用AHP..." 到 "...授权运营成效(w=0.069)。")
    (135, 143), # 图7-2: 行136-144 ("针对不同类型平台..." 到 "...逐步改善基础条件。")
]

# 创建需要保留的行号
keep = set(range(len(lines)))
for start, end in delete_ranges:
    for i in range(start, end):
        keep.discard(i)

new_lines = [lines[i] for i in sorted(keep)]
print(f"\n删除后行数: {len(new_lines)}")
print(f"删除行数: {len(lines) - len(new_lines)}")

# 保存修改后的内容
with open('docs/博士论文_最终定稿版_v10.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("第一章清理完成")
