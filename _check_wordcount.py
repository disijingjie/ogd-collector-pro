# -*- coding: utf-8 -*-
import os

files = [
    ('第一章原文', 'docs/新论文_第一章_绪论.md'),
    ('第二章扩充版', 'docs/chapter2_expanded_v2.md'),
    ('第三章扩充版', 'docs/chapter3_expanded_v2.md'),
    ('第四章', 'docs/chapter4_full_v2.md'),
    ('第五章', 'docs/chapter5_final_v2.md'),
    ('第六章', 'docs/chapter6_full.md'),
    ('第七章', 'docs/chapter7_full.md'),
    ('第八章', 'docs/chapter8_full.md'),
]

total = 0
for name, path in files:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        total += len(c)
        print(f'{name}: {len(c)} 字符')
    else:
        print(f'{name}: 文件不存在')

print(f'\n当前总计(1-8章): {total} 字符')
print(f'约 {total//10000}.{total%10000//1000} 万字')
print(f'距离15万字目标还差: {150000 - total} 字符')
