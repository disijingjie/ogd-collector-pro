# -*- coding: utf-8 -*-
"""
重建附录C-2和附录I的TOPSIS表格（基于真实数据）
删除内部说明文档
"""
import pandas as pd
import re

md_path = "docs/博士论文_最终定稿版_v10.md"
with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

changes = []

# 读取最新TOPSIS数据
df = pd.read_csv('data/verified_dataset/table_topsis_4e_final.csv')

# ========== 1. 重建附录C-2：中文TOPSIS详细得分 ==========
# 生成新表格
new_table_c2 = "**表C-2 TOPSIS评估各维度详细得分（23个平台）**\n\n"
new_table_c2 += "| 排名 | 省份 | 综合得分 | 供给保障(E1) | 平台服务(E2) | 数据质量(E3) | 利用效果(E4) | 公平性(E5) |\n"
new_table_c2 += "|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"

for _, row in df.iterrows():
    new_table_c2 += f"| {int(row['topsis_rank'])} | {row['name']} | {row['topsis_score']:.3f} | {row['E1']:.3f} | {row['E2']:.3f} | {row['E3']:.3f} | {row['E4']:.3f} | {row['E5']:.3f} |\n"

# 替换旧表格（从表C-2标题到下一个###之间）
old_c2_pattern = r'\*\*表C-2 TOPSIS评估各维度详细得分\*\*\n\n.*?\n\n### C\.3'
if re.search(old_c2_pattern, text, re.DOTALL):
    text = re.sub(old_c2_pattern, new_table_c2 + "\n\n### C.3", text, flags=re.DOTALL)
    changes.append("[必须] 附录C-2 TOPSIS表格已重建（23平台新数据）")
else:
    changes.append("[警告] 附录C-2旧表格未匹配")

# ========== 2. 重建附录I：英文TOPSIS排名 ==========
new_table_i = "**Table I-1 TOPSIS Performance Evaluation Raw Scores (23 Platforms)**\n\n"
new_table_i += "| Rank | Province | TOPSIS Score | Performance Tier | Advantage Dimension | Shortcoming Dimension |\n"
new_table_i += "|:---:|:---|:---:|:---|:---|:---|\n"

# 维度名称映射
dim_names = {'E1': 'Supply', 'E2': 'Service', 'E3': 'Quality', 'E4': 'Effect', 'E5': 'Equity'}

for _, row in df.iterrows():
    # 找出优势维度（得分最高的维度，满分1.0优先）
    e_vals = {'E1': row['E1'], 'E2': row['E2'], 'E3': row['E3'], 'E4': row['E4'], 'E5': row['E5']}
    max_e = max(e_vals.values())
    adv_dims = [dim_names[k] for k, v in e_vals.items() if v >= max_e - 0.01]
    adv_str = ', '.join(adv_dims) if adv_dims else 'Multiple'
    
    # 短板维度（得分最低的维度）
    min_e = min(e_vals.values())
    short_dims = [dim_names[k] for k, v in e_vals.items() if v <= min_e + 0.01]
    short_str = ', '.join(short_dims) if short_dims else 'Multiple'
    
    tier_en = "First Tier" if row['tier'] == '第一梯队' else ("Second Tier" if row['tier'] == '第二梯队' else "Third Tier")
    
    new_table_i += f"| {int(row['topsis_rank'])} | {row['province']} | {row['topsis_score']:.3f} | {tier_en} | {adv_str} | {short_str} |\n"

# 替换旧英文表格
old_i_pattern = r'\*\*Table I-1 TOPSIS Performance Evaluation Raw Scores \(22 Platforms\)\*\*\n\n.*?\n\n### I\.2'
if re.search(old_i_pattern, text, re.DOTALL):
    text = re.sub(old_i_pattern, new_table_i + "\n\n### I.2", text, flags=re.DOTALL)
    changes.append("[必须] 附录I TOPSIS英文表格已重建（23平台新数据）")
else:
    # 可能没有I.2，尝试匹配到文档末尾或其他模式
    old_i_pattern2 = r'\*\*Table I-1 TOPSIS Performance Evaluation Raw Scores \(22 Platforms\)\*\*\n\n.*?(?=\n## |\Z)'
    if re.search(old_i_pattern2, text, re.DOTALL):
        text = re.sub(old_i_pattern2, new_table_i, text, flags=re.DOTALL)
        changes.append("[必须] 附录I TOPSIS英文表格已重建（到文档末尾）")
    else:
        changes.append("[警告] 附录I旧表格未匹配")

# ========== 3. 删除内部说明文档 ==========
# 查找 "## 第三章 数据引用更新说明" 到下一个 "## 第" 或 "# 第" 之间的内容
old_note_pattern = r'## 第三章 数据引用更新说明\n\n.*?(?=\n## 第|\n# 第|\Z)'
if re.search(old_note_pattern, text, re.DOTALL):
    text = re.sub(old_note_pattern, '', text, flags=re.DOTALL)
    changes.append("[必须] 删除内部说明文档'第三章 数据引用更新说明'")
else:
    changes.append("[警告] 内部说明文档未匹配")

# 保存
with open(md_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"附录重建完成，共 {len(changes)} 处：")
for c in changes:
    print(f"  - {c}")
