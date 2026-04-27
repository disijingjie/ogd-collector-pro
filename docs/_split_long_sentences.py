#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检测并拆分超长句（>100字）
"""

import re

with open('docs/博士论文_最终定稿版_v23.md','r',encoding='utf-8') as f:
    content = f.read()

# 分割成段落
paragraphs = content.split('\n')

# 检测超长句
long_sentences = []
for pi, para in enumerate(paragraphs):
    if not para.strip() or para.strip().startswith('#') or para.strip().startswith('|') or para.strip().startswith('!'):
        continue
    if para.strip().startswith('*') and para.strip().endswith('*'):
        continue

    # 按句号、问号、感叹号分割句子
    sentences = re.split(r'([。！？])', para)
    current = ''
    for s in sentences:
        current += s
        if s in '。！？':
            # 计算中文字符数
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', current))
            if chinese_chars > 100:
                long_sentences.append({
                    'para_idx': pi,
                    'text': current,
                    'chars': chinese_chars
                })
            current = ''

print(f"检测到 {len(long_sentences)} 句超长句（>100字）")
print(f"\n前20句示例：")
for i, s in enumerate(long_sentences[:20]):
    preview = s['text'][:80] + "..." if len(s['text']) > 80 else s['text']
    print(f"  {i+1}. [{s['chars']}字] {preview}")

# 自动拆分策略：对有明显拆分标记的句子进行处理
split_count = 0
replacements = []

for s in long_sentences[:80]:  # 先处理前80句
    text = s['text']

    # 策略1: "一方面...另一方面..." 拆分为两句
    if '一方面' in text and '另一方面' in text:
        new_text = text.replace('，另一方面', '。另一方面')
        replacements.append((text, new_text))
        split_count += 1
        continue

    # 策略2: "首先...其次...再次...最后..." 拆分
    if '首先' in text and ('其次' in text or '再次' in text or '最后' in text):
        new_text = text
        for marker in ['，其次', '，再次', '，最后']:
            new_text = new_text.replace(marker, '。' + marker[1:])
        if new_text != text:
            replacements.append((text, new_text))
            split_count += 1
            continue

    # 策略3: 包含多个"；"的长句，将分号改为句号
    if text.count('；') >= 2 and len(re.findall(r'[\u4e00-\u9fff]', text)) > 120:
        new_text = text.replace('；', '。')
        replacements.append((text, new_text))
        split_count += 1
        continue

    # 策略4: "从...视角" + "从...视角" 结构拆分
    pattern = r'(从\w+视角[^。]{10,50}?)，(从\w+视角)'
    if re.search(pattern, text):
        new_text = re.sub(pattern, r'\1。\2', text)
        if new_text != text:
            replacements.append((text, new_text))
            split_count += 1
            continue

    # 策略5: 超长句中有"；"，拆分第一个分号
    if '；' in text and len(re.findall(r'[\u4e00-\u9fff]', text)) > 110:
        new_text = text.replace('；', '。', 1)
        replacements.append((text, new_text))
        split_count += 1
        continue

print(f"\n可自动拆分: {split_count} 句")

# 执行替换
for old, new in replacements:
    content = content.replace(old, new, 1)

with open('docs/博士论文_最终定稿版_v23.md','w',encoding='utf-8') as f:
    f.write(content)

print(f"\n已执行拆分替换，文件已保存")
print(f"文件大小: {len(content):,} 字符")

# 重新统计
long_sentences_after = []
for pi, para in enumerate(content.split('\n')):
    if not para.strip() or para.strip().startswith('#') or para.strip().startswith('|') or para.strip().startswith('!'):
        continue
    sentences = re.split(r'([。！？])', para)
    current = ''
    for s in sentences:
        current += s
        if s in '。！？':
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', current))
            if chinese_chars > 100:
                long_sentences_after.append(current)
            current = ''

print(f"\n拆分后剩余超长句: {len(long_sentences_after)} 句")
