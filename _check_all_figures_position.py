"""
全面检查所有图表的位置和内容
"""
import re

with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到各章节位置
chapters = {}
for i, line in enumerate(lines, 1):
    m = re.match(r'#+\s*第([一二三四五六七八])章', line)
    if m:
        num = '一二三四五六七八'.index(m.group(1)) + 1
        chapters[num] = i

print("各章节起始行号:")
for k, v in sorted(chapters.items()):
    print(f"  第{k}章: 第{v}行")

# 检查每张图的位置
print("\n" + "="*70)
print("图表位置检查")
print("="*70)

for i, line in enumerate(lines, 1):
    m = re.search(r'!\[([^\]]*图(\d+)-(\d+)[^\]]*)\]', line)
    if m:
        caption = m.group(1)
        chap_num = int(m.group(2))
        fig_num = int(m.group(3))
        
        # 判断实际在哪一章
        actual_chap = 0
        for chap, start_line in sorted(chapters.items()):
            if i >= start_line:
                actual_chap = chap
        
        status = "正确" if actual_chap == chap_num else f"错误！在第{actual_chap}章"
        print(f"  图{chap_num}-{fig_num}: 第{i:5}行 | {status:15} | {caption[:40]}")

# 检查表的位置
print("\n" + "="*70)
print("表格位置检查")
print("="*70)

for i, line in enumerate(lines, 1):
    m = re.search(r'\*\*表(\d+)-(\d+)', line)
    if m:
        chap_num = int(m.group(1))
        actual_chap = 0
        for chap, start_line in sorted(chapters.items()):
            if i >= start_line:
                actual_chap = chap
        status = "正确" if actual_chap == chap_num else f"错误！在第{actual_chap}章"
        print(f"  表{chap_num}-{m.group(2)}: 第{i:5}行 | {status:15}")
