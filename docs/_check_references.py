#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 7714-2015 参考文献格式检查与修正
"""

import re

with open('docs/博士论文_最终定稿版_v23.md','r',encoding='utf-8') as f:
    content = f.read()

# 提取参考文献部分
ref_start = content.find('# 参考文献')
if ref_start == -1:
    print("未找到参考文献部分")
    exit(1)

ref_section = content[ref_start:]

# 提取每条参考文献
ref_lines = re.findall(r'^\[(\d+)\] (.+)$', ref_section, re.MULTILINE)

issues = []
auto_fixes = []

for num, text in ref_lines:
    text = text.strip()
    issue_list = []

    # 检查1: 是否有文献类型标识
    has_type = bool(re.search(r'\[[JMDRGSNEB/OLZ]+\]', text))
    if not has_type:
        issue_list.append("缺少文献类型标识")

    # 检查2: [Z] 标识不规范
    if '[Z]' in text:
        issue_list.append("[Z]非标准文献类型标识")
        # 自动修正: 政策法规用[A]或[EB/OL]
        if '.gov.cn' in text or 'xinhuanet' in text or 'http' in text:
            auto_fixes.append((f'[{num}] {text}', f'[{num}] {text.replace("[Z]", "[EB/OL]")}'))
        else:
            auto_fixes.append((f'[{num}] {text}', f'[{num}] {text.replace("[Z]", "[A]")}'))

    # 检查3: 中文文献只有期刊名无标题（如"蔡昉. 经济研究, 2024."）
    if re.search(r'[\u4e00-\u9fff]', text) and '[J]' in text:
        # 检查是否有"题名[J]"格式
        if not re.search(r'[\u4e00-\u9fff][^\[。]*\[J\]', text):
            issue_list.append("期刊论文可能缺少题名")

    # 检查4: 英文作者名格式
    if not re.search(r'[\u4e00-\u9fff]', text):
        # 检查是否全大写
        authors_part = text.split('.')[0] if '.' in text else text.split('[')[0]
        if re.search(r'[A-Z]{3,}', authors_part):
            # 全大写姓是OK的，但名也全大写就不对
            pass
        # 检查大小写混用（如Wirtz B W）
        if re.search(r'\b[A-Z][a-z]+ [A-Z] [A-Z]\b', authors_part):
            issue_list.append("英文作者名大小写格式不规范")

    # 检查5: 期刊缩写不规范
    journal_abbrs = ['EJOR', 'JMIS', 'JASIST']
    for abbr in journal_abbrs:
        if abbr in text:
            issue_list.append(f"期刊缩写'{abbr}'不规范，应写全称")

    # 检查6: 缺少页码的期刊论文
    if '[J]' in text and not re.search(r':\s*\d+[-–—]\d+', text):
        # 有些在线优先出版可能没有页码，暂时不报错
        pass

    # 检查7: 网络文献缺少访问日期
    if '[EB/OL]' in text and not re.search(r'\[\d{4}-\d{2}-\d{2}\]', text):
        issue_list.append("网络文献可能缺少访问日期")

    if issue_list:
        issues.append({'num': num, 'text': text[:100], 'issues': issue_list})

print(f"参考文献总数: {len(ref_lines)}")
print(f"问题文献数: {len(issues)}")
print(f"可自动修正: {len(auto_fixes)}")

print("\n=== 问题详情 ===")
for item in issues[:30]:
    print(f"\n[{item['num']}] {item['text']}")
    for iss in item['issues']:
        print(f"   -> {iss}")

# 执行自动修正
fix_count = 0
for old, new in auto_fixes:
    if old in content:
        content = content.replace(old, new)
        fix_count += 1

if fix_count > 0:
    with open('docs/博士论文_最终定稿版_v23.md','w',encoding='utf-8') as f:
        f.write(content)
    print(f"\n已自动修正 {fix_count} 条参考文献格式")
else:
    print("\n无需要自动修正的格式问题")

# 输出修正建议报告
report = []
report.append("# 参考文献GB/T 7714-2015格式检查报告\n")
report.append(f"检查时间: 2026-04-27\n")
report.append(f"参考文献总数: {len(ref_lines)}\n")
report.append(f"问题文献数: {len(issues)}\n")
report.append(f"自动修正: {fix_count}条\n\n")
report.append("## 需手动修正的问题\n\n")

for item in issues:
    if item['num'] not in [a[0].split(']')[0][1:] for a in auto_fixes]:
        report.append(f"**[{item['num']}]** {item['text']}\n")
        for iss in item['issues']:
            report.append(f"- {iss}\n")
        report.append("\n")

with open('docs/_参考文献格式检查报告.md','w',encoding='utf-8') as f:
    f.writelines(report)

print("检查报告已保存: docs/_参考文献格式检查报告.md")
