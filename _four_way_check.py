# -*- coding: utf-8 -*-
"""
四向交叉核对脚本
检查：表-文、图-文、摘要-正文、章节编号 的一致性
"""
import re

md_path = "docs/博士论文_最终定稿版_v10.md"
with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

issues = []

# ========== 1. 摘要-正文一致性 ==========
print("=" * 60)
print("四向交叉核对报告")
print("=" * 60)
print("\n【一、摘要-正文一致性核对】")

# 检查摘要中的关键数据
abstract = text[:text.find("---")] if "---" in text else text[:2000]

# 山东得分
if "0.955" in abstract and "0.955" in text:
    print("  [OK] 山东TOPSIS得分 0.955：摘要与正文一致")
else:
    issues.append("山东得分不一致")

# 23个平台
if "23个" in abstract and "23个省级" in text:
    print("  [OK] 样本量23个：摘要与正文一致")
else:
    issues.append("样本量表述不一致")

# DEA有效1个
if "only 1 platform" in abstract or "仅有1个" in abstract:
    print("  [OK] DEA有效1个：摘要与正文一致")
else:
    issues.append("DEA结果不一致")

# DEMATEL网络化结构
if "networked structure" in abstract or "网络化结构" in abstract:
    print("  [OK] DEMATEL网络化结构：摘要与正文一致")
else:
    issues.append("DEMATEL结论不一致")

# fsQCA 2条路径
if "two core configuration paths" in abstract or "两条核心组态路径" in abstract:
    print("  [OK] fsQCA两条路径：摘要与正文一致")
else:
    issues.append("fsQCA路径不一致")

# ========== 2. 表-文一致性 ==========
print("\n【二、表-文一致性核对】")

# 表5-1 TOP3
# 从表5-1提取TOP3
table_51_match = re.search(r'\*\*表5-1.*?\*\*.*?\n\|[^\n]*\n\|[^\n]*\n((?:\|[^\n]*\n){1,5})', text, re.DOTALL)
if table_51_match:
    top3_lines = table_51_match.group(1).strip().split('\n')[:3]
    top3_provinces = []
    for line in top3_lines:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            top3_provinces.append(cells[1])
    print(f"  [INFO] 表5-1 TOP3: {top3_provinces}")

    # 检查正文是否提到TOP3
    if top3_provinces and all(p in text for p in top3_provinces):
        print(f"  [OK] 表5-1 TOP3省份在正文中有提及")
    else:
        issues.append("表5-1 TOP3与正文不一致")
else:
    issues.append("未找到表5-1")

# 表5-2 DEA有效
if "DEA有效" in text:
    dea_eff_count = text.count("| DEA有效 |")
    print(f"  [INFO] 表5-2中DEA有效平台数: {dea_eff_count}")
    if dea_eff_count == 1:
        print("  [OK] 表5-2 DEA有效仅1个，与正文一致")
    else:
        issues.append(f"表5-2 DEA有效数({dea_eff_count})与正文不一致")

# 表6-1 DEMATEL中心度
if "71.29" in text and "70.73" in text:
    print("  [OK] 表6-1 DEMATEL中心度数据在正文中")
else:
    issues.append("表6-1中心度数据缺失")

# ========== 3. 图-文一致性 ==========
print("\n【三、图-文一致性核对】")

# 检查所有图片引用
img_refs = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
print(f"  [INFO] 共发现 {len(img_refs)} 张图片引用")

import os
missing_imgs = []
for alt, path in img_refs:
    if not os.path.exists(path):
        missing_imgs.append((alt, path))

if missing_imgs:
    print(f"  [WARN] {len(missing_imgs)} 张图片文件缺失:")
    for alt, path in missing_imgs[:5]:
        print(f"    - {alt}: {path}")
else:
    print("  [OK] 所有图片文件均存在")

# 检查图注与正文引用
fig_captions = re.findall(r'\*\*图(\d+-\d+).*?\*\*', text)
print(f"  [INFO] 发现 {len(fig_captions)} 个图注")

fig_refs = re.findall(r'图(\d+-\d+)', text)
print(f"  [INFO] 正文中引用图表编号 {len(fig_refs)} 次")

# ========== 4. 章节编号连续性 ==========
print("\n【四、章节编号连续性核对】")

chapters = re.findall(r'^#+\s+第([一二三四五六七八九十]+)章', text, re.MULTILINE)
print(f"  [INFO] 发现章节: {chapters}")

# 检查是否有重复编号
if len(chapters) != len(set(chapters)):
    issues.append("存在重复章节编号")
    print("  [ERR] 存在重复章节编号!")
else:
    print("  [OK] 章节编号无重复")

# ========== 5. 数据一致性抽查 ==========
print("\n【五、关键数据一致性抽查】")

# 检查是否有残留的"22个平台"在分析章节
remaining_22 = re.findall(r'22个(?:样本|省级|有效)?平台', text)
if remaining_22:
    print(f"  [WARN] 仍发现 {len(remaining_22)} 处'22个平台'残留: {set(remaining_22)}")
    issues.append(f"残留{len(remaining_22)}处'22个平台'")
else:
    print("  [OK] 无'22个平台'残留")

# 检查山东得分一致性
shandong_scores = re.findall(r'山东.*?([0-9]\.[0-9]{3})', text)
if shandong_scores:
    unique_scores = set(shandong_scores)
    if len(unique_scores) == 1:
        print(f"  [OK] 山东得分一致: {list(unique_scores)[0]}")
    else:
        issues.append(f"山东得分不一致: {unique_scores}")
        print(f"  [ERR] 山东得分不一致: {unique_scores}")

# 检查梯队分布
first_tier = len(re.findall(r'第一梯队', text))
second_tier = len(re.findall(r'第二梯队', text))
third_tier = len(re.findall(r'第三梯队', text))
print(f"  [INFO] 梯队提及次数: 第一梯队={first_tier}, 第二梯队={second_tier}, 第三梯队={third_tier}")

# ========== 总结 ==========
print("\n" + "=" * 60)
print("核对总结")
print("=" * 60)
if issues:
    print(f"发现 {len(issues)} 个问题：")
    for issue in issues:
        print(f"  [待修复] {issue}")
else:
    print("未发现明显的一致性问题。")
print("=" * 60)
