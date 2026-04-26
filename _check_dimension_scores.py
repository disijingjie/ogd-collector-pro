import sqlite3

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# Get platforms with valid dimension scores
cursor.execute("""
    SELECT p.code, p.name, p.province, p.region,
           cr.dataset_count, cr.app_count,
           cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4, cr.overall_score,
           cr.has_https, cr.has_search, cr.has_download, cr.has_api,
           cr.has_visualization, cr.has_update_info, cr.has_metadata, 
           cr.has_feedback, cr.has_register, cr.has_preview, cr.has_bulk_download
    FROM platforms p
    JOIN (
        SELECT platform_code, MAX(id) as max_id 
        FROM collection_records 
        WHERE score_c1 IS NOT NULL AND score_c1 > 0
        GROUP BY platform_code
    ) latest ON p.code = latest.platform_code
    JOIN collection_records cr ON latest.max_id = cr.id
    WHERE p.tier = '省级'
    ORDER BY cr.overall_score DESC
""")

rows = cursor.fetchall()
print(f'Platforms with dimension scores: {len(rows)}')
print()

print(f"{'Code':12s} {'Name':10s} {'Province':10s} {'Region':6s} {'Datasets':>10s} {'C1':>5s} {'C2':>5s} {'C3':>5s} {'C4':>5s} {'Overall':>7s}")
print("-" * 90)

for row in rows:
    code, name, province, region = row[0:4]
    dataset_count = row[4] or 0
    app_count = row[5] or 0
    c1, c2, c3, c4, overall = row[6:11]
    funcs = row[11:22]
    func_sum = sum(1 for f in funcs if f)
    
    print(f"{code:12s} {name:10s} {province:10s} {region:6s} {dataset_count:>10,} {c1:>5.2f} {c2:>5.2f} {c3:>5.2f} {c4:>5.2f} {overall:>7.3f}")

# Compare with the binary-only TOPSIS results
print()
print('=== Comparison: Dimension-based vs Binary-only TOPSIS ===')
import csv
with open('data/verified_dataset/table_topsis_binary_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    binary_rows = {r['code']: float(r['topsis_score']) for r in csv.DictReader(f)}

print(f"{'Code':12s} {'Name':10s} {'Dim-Overall':>12s} {'Binary-TOPSIS':>14s} {'Diff':>8s}")
print("-" * 60)
for row in rows:
    code = row[0]
    name = row[1]
    dim_overall = row[10] or 0
    binary_score = binary_rows.get(code, 0)
    diff = dim_overall - binary_score
    print(f"{code:12s} {name:10s} {dim_overall:>12.3f} {binary_score:>14.3f} {diff:>+8.3f}")

conn.close()
