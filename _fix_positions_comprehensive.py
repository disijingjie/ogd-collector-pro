"""
综合修复图表位置问题
策略：
1. 从第1章删除图6-3和图6-1
2. 从第4章删除图6-2和图5-3
3. 在第六章/第五章正确位置插入
"""

with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"总行数: {len(lines)}")

# 找到各章节起始行（0-indexed）
chap_starts = {}
for i, line in enumerate(lines):
    import re
    m = re.match(r'#+\s*第([一二三四五六七八])章', line)
    if m:
        num = '一二三四五六七八'.index(m.group(1)) + 1
        chap_starts[num] = i

print("章节起始行:", chap_starts)

# 需要删除的块（0-indexed行号）
# 图6-3: 行126-135 (0-indexed 125-134)
# 图6-1: 行142-151 (0-indexed 141-150)
# 图6-2: 行1056-1065 (0-indexed 1055-1064)
# 图5-3: 行1068-1077 (0-indexed 1067-1076)

delete_ranges = [
    (125, 135),   # 图6-3 在第1章
    (141, 151),   # 图6-1 在第1章
    (1055, 1065), # 图6-2 在第4章
    (1067, 1077), # 图5-3 在第4章
]

# 创建保留的行
keep = set(range(len(lines)))
for start, end in delete_ranges:
    for i in range(start, end):
        keep.discard(i)

new_lines = [lines[i] for i in sorted(keep)]
print(f"删除后行数: {len(new_lines)}")
print(f"删除行数: {len(lines) - len(new_lines)}")

# 保存
with open('docs/博士论文_最终定稿版_v10.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("\n错误位置已清理")
