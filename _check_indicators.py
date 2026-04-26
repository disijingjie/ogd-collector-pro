import csv

with open('data/verified_dataset/table_topsis_binary_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

indicators = ['has_https', 'has_search', 'has_download', 'has_api', 
              'has_visualization', 'has_update_info', 'has_metadata', 
              'has_feedback', 'has_register', 'has_preview', 'has_bulk_download']

print('=== Platform Indicator Values (0/1) ===')
print(f"{'Platform':12s} {'Score':>6s} " + " ".join([f"{ind[:4]:>4s}" for ind in indicators]))
print("-" * 75)

for r in sorted(rows, key=lambda x: float(x['topsis_score']), reverse=True):
    vals = [int(r[ind]) for ind in indicators]
    sum_vals = sum(vals)
    print(f"{r['name']:12s} {float(r['topsis_score']):>6.3f} " + " ".join([f"{v:>4d}" for v in vals]) + f"  sum={sum_vals}")

print()
print('=== Indicator Statistics ===')
for ind in indicators:
    ones = sum(int(r[ind]) for r in rows)
    print(f"{ind:25s}: {ones}/{len(rows)} platforms have it ({100*ones/len(rows):.1f}%)")
