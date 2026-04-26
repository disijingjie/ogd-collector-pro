import csv

# Read TOPSIS data
with open('data/verified_dataset/table_topsis_binary_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    topsis_rows = list(csv.DictReader(f))

# Read DEA data
with open('data/verified_dataset/table_dea_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    dea_rows = list(csv.DictReader(f))

# Sort TOPSIS by score descending
topsis_sorted = sorted(topsis_rows, key=lambda r: float(r['topsis_score']), reverse=True)

# Sort DEA by efficiency descending
dea_sorted = sorted(dea_rows, key=lambda r: float(r['dea_efficiency']), reverse=True)

print('=== TOPSIS Ranking (from CSV) ===')
for i, r in enumerate(topsis_sorted):
    print(f"{i+1:2d}. {r['name']:10s}  score={float(r['topsis_score']):.3f}")

print()
print('=== DEA Ranking (from CSV) ===')
for i, r in enumerate(dea_sorted):
    print(f"{i+1:2d}. {r['name']:10s}  eff={float(r['dea_efficiency']):.3f}  years={r['operating_years']}  func={r['function_score']}")
