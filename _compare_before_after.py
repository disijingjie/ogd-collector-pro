import pandas as pd
from pathlib import Path

# 读取修复后的结果
new_df = pd.read_csv('data/verified_dataset/table_topsis_4e_final.csv', encoding='utf-8-sig')

# 读取修复前的结果（最后一个旧版本）
old_files = sorted(Path('data/verified_dataset').glob('table_topsis_4e_20260426_21*.csv'))
if old_files:
    old_df = pd.read_csv(old_files[-1], encoding='utf-8-sig')
else:
    old_df = pd.read_csv('data/verified_dataset/table_topsis_4e_20260426_213512.csv', encoding='utf-8-sig')

old_ranks = dict(zip(old_df['code'], old_df['topsis_rank']))
old_scores = dict(zip(old_df['code'], old_df['topsis_score']))
old_tiers = dict(zip(old_df['code'], old_df['tier']))

print("=" * 90)
print("修复前后排名对比")
print("=" * 90)
print(f"{'平台':<14} {'旧排名':<6} {'新排名':<6} {'变化':<6} {'旧得分':<8} {'新得分':<8} {'得分变化':<8} {'旧梯队':<8} {'新梯队':<8}")
print("-" * 90)

for _, row in new_df.iterrows():
    code = row['code']
    name = row['name']
    old_rank = old_ranks.get(code, '-')
    new_rank = row['topsis_rank']
    old_score = old_scores.get(code, 0)
    new_score = row['topsis_score']
    old_tier = old_tiers.get(code, '-')
    new_tier = row['tier']
    
    if old_rank != '-':
        rank_change = int(old_rank) - int(new_rank)
        score_change = new_score - old_score
        change_str = f"+{rank_change}" if rank_change > 0 else str(rank_change)
        print(f"{name:<14} {old_rank:<6} {new_rank:<6} {change_str:<6} {old_score:<8.4f} {new_score:<8.4f} {score_change:+.4f} {old_tier:<8} {new_tier:<8}")
    else:
        print(f"{name:<14} {'新':<6} {new_rank:<6} {'-':<6} {'-':<8} {new_score:<8.4f} {'-':<8} {'-':<8} {new_tier:<8}")

# 统计显著变化
print("\n" + "=" * 90)
print("显著变化统计")
print("=" * 90)

up_3 = 0
down_3 = 0
tier_change = 0

for _, row in new_df.iterrows():
    code = row['code']
    if code in old_ranks:
        rank_change = int(old_ranks[code]) - int(row['topsis_rank'])
        if rank_change >= 3:
            up_3 += 1
        elif rank_change <= -3:
            down_3 += 1
        if old_tiers.get(code) != row['tier']:
            tier_change += 1

print(f"排名上升≥3位: {up_3}个平台")
print(f"排名下降≥3位: {down_3}个平台")
print(f"梯队变化: {tier_change}个平台")
