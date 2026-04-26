import csv

with open('data/verified_dataset/table_topsis_binary_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

print('Columns:', list(rows[0].keys()))
print()

# Sort by score descending
rows_sorted = sorted(rows, key=lambda r: float(r['topsis_score']), reverse=True)

print('=== TOPSIS Ranking with Dimension Scores ===')
for r in rows_sorted:
    dims = []
    for i in range(1, 6):
        k = f'E{i}_score'
        if k in r:
            dims.append(f'E{i}={float(r[k]):.2f}')
    dim_str = '  '.join(dims)
    rank_val = r.get('rank', r.get('topsis_rank', '?'))
    print(f"{r['name']:10s}  score={float(r['topsis_score']):.3f}  rank={rank_val}  {dim_str}")

print()
print('=== Score Distribution ===')
scores = [float(r['topsis_score']) for r in rows]
print(f'Max: {max(scores):.3f} ({rows_sorted[0]["name"]})')
print(f'Min: {min(scores):.3f} ({rows_sorted[-1]["name"]})')
print(f'Mean: {sum(scores)/len(scores):.3f}')
print(f'Median: {scores[len(scores)//2]:.3f}')

# Check if any platform has all E scores = 1
print()
print('=== Platforms with all dimension scores = 1.0 ===')
for r in rows:
    all_one = True
    for i in range(1, 6):
        k = f'E{i}_score'
        if k in r:
            if float(r[k]) < 0.99:
                all_one = False
                break
    if all_one:
        print(f"  {r['name']}: score={float(r['topsis_score']):.3f}")

# Check dimension ranges
print()
print('=== Dimension Score Ranges ===')
for i in range(1, 6):
    k = f'E{i}_score'
    if k in rows[0]:
        vals = [float(r[k]) for r in rows]
        print(f'E{i}: min={min(vals):.3f}, max={max(vals):.3f}, mean={sum(vals)/len(vals):.3f}')
