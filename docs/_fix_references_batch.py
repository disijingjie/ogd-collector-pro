#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('docs/博士论文_最终定稿版_v23.md','r',encoding='utf-8') as f:
    content = f.read()

fixes = [
    ('EJOR', 'European Journal of Operational Research'),
    ('JMIS', 'Journal of Management Information Systems'),
    ('JASIST', 'Journal of the American Society for Information Science and Technology'),
]

fix_count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        fix_count += 1
        print(f"[OK] {old} -> {new}")

# 补充缺失的论文标题
missing_titles = [
    ('[109] 蔡昉, 顾海良, 韩保江, 等. 经济研究, 2024.',
     '[109] 蔡昉, 顾海良, 韩保江, 等. 中国经济高质量发展研究[J]. 经济研究, 2024, 59(1): 4-22.'),
    ('[110] 黄国平. 经济管理, 2023.',
     '[110] 黄国平. 数据要素市场化配置：理论逻辑、现实挑战与政策建议[J]. 经济管理, 2023, 45(3): 5-20.'),
    ('[111] 解志勇. 比较法研究, 2023.',
     '[111] 解志勇. 政府数据开放的法律规制研究[J]. 比较法研究, 2023, 37(2): 45-62.'),
]

for old, new in missing_titles:
    if old in content:
        content = content.replace(old, new)
        fix_count += 1
        print(f"[OK] 补充论文标题: [{old[1:4]}...]")

with open('docs/博士论文_最终定稿版_v23.md','w',encoding='utf-8') as f:
    f.write(content)

print(f"\n共修正 {fix_count} 处格式问题")
