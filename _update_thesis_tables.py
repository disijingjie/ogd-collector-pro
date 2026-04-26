#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新论文中的表5-1和表5-2
"""
import csv
import json

# 读取TOPSIS数据
topsis_rows = []
with open('data/verified_dataset/table_topsis_4e_final.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for r in reader:
        # 只取前22个有数据的平台（排除河北、西藏等8个无数据平台）
        code = r['code']
        # 排除8个无数据平台
        if code in ['hebei', 'xizang', 'shaanxi', 'gansu', 'qinghai', 'ningxia', 'xinjiang', 'heilongjiang']:
            continue
        topsis_rows.append(r)

# 读取DEA数据
dea_rows = []
with open('data/verified_dataset/table_dea_4e_final.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for r in reader:
        code = r['code']
        if code in ['hebei', 'xizang', 'shaanxi', 'gansu', 'qinghai', 'ningxia', 'xinjiang', 'heilongjiang']:
            continue
        dea_rows.append(r)

# 维度名称映射
dim_names = {'E1': '供给保障', 'E2': '平台服务', 'E3': '数据质量', 'E4': '利用效果', 'E5': '公平性'}

def get_advantage_shortcoming(row):
    """计算优势维度和短板维度"""
    dims = {}
    for k in ['E1', 'E2', 'E3', 'E4', 'E5']:
        try:
            dims[k] = float(row[k])
        except:
            dims[k] = 0.0
    max_dim = max(dims, key=dims.get)
    min_dim = min(dims, key=dims.get)
    
    # 如果有多个相同的最大值/最小值，列出所有
    max_val = dims[max_dim]
    min_val = dims[min_dim]
    adv = [dim_names[k] for k, v in dims.items() if abs(v - max_val) < 0.001]
    shc = [dim_names[k] for k, v in dims.items() if abs(v - min_val) < 0.001]
    
    return '、'.join(adv), '、'.join(shc)

# 生成表5-1
print("=== 表5-1 22个样本平台TOPSIS绩效评估结果 ===")
print()
print("| 排名 | 省份 | TOPSIS得分 | 绩效梯队 | 优势维度 | 短板维度 |")
print("|:---:|:---|:---:|:---|:---|:---|")
for i, r in enumerate(topsis_rows, 1):
    adv, shc = get_advantage_shortcoming(r)
    score = float(r['topsis_score'])
    print(f"| {i} | {r['province']} | {score:.3f} | {r['tier']} | {adv} | {shc} |")
print()
print("*数据来源：OGD-Collector Pro采集系统 + 4E-TOPSIS计算，2026-04-26。*")
print()

# 计算梯队统计
tier2 = [float(r['topsis_score']) for r in topsis_rows if r['tier'] == '第二梯队']
tier3 = [float(r['topsis_score']) for r in topsis_rows if r['tier'] == '第三梯队']
print(f"第二梯队均值: {sum(tier2)/len(tier2):.3f}, 数量: {len(tier2)}")
print(f"第三梯队均值: {sum(tier3)/len(tier3):.3f}, 数量: {len(tier3)}")
print(f"绩效断层: {float(topsis_rows[0]['topsis_score']) - float(topsis_rows[1]['topsis_score']):.3f}")
print()

# 生成表5-2
print("=== 表5-2 22个省级平台DEA-BCC效率评价结果 ===")
print()
print("| 排名 | 省份 | 效率值(TE) | 运营年限 | 功能完善度 | 效率类型 |")
print("|:---:|:---|:---:|:---:|:---:|:---:")
for i, r in enumerate(dea_rows, 1):
    eff = float(r['dea_efficiency'])
    eff_type = "DEA有效" if eff >= 0.999 else "非DEA有效"
    func = float(r['E2_func'])
    print(f"| {i} | {r['province']} | {eff:.3f} | {r['operating_years']} | {func:.2f} | {eff_type} |")
print()
print("*数据来源：OGD-Collector Pro采集系统 + DEA-BCC计算，2026-04-26。*")
