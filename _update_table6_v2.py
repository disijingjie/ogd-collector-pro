# -*- coding: utf-8 -*-
with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact text in the file
idx = content.find('表6-1展示了DEMATEL分析的中心度、原因度和因果分类结果。')
print('Found at index:', idx)

# Extract the exact text
if idx >= 0:
    # Find the end of the table section
    end_idx = content.find('基于中心度和原因度的综合分析', idx)
    print('End at index:', end_idx)
    actual_text = content[idx:end_idx]
    print('Actual text length:', len(actual_text))
    print('Actual text (first 500 chars):')
    print(repr(actual_text[:500]))
    print()
    print('Actual text (last 200 chars):')
    print(repr(actual_text[-200:]))
