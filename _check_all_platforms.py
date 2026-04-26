import sqlite3

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# Get all provincial platforms with their latest data
cursor.execute("""
    SELECT 
        p.code, p.name, p.province, p.region, p.launch_year,
        cr.dataset_count, cr.has_https, cr.has_search, cr.has_download, 
        cr.has_api, cr.has_visualization, cr.has_update_info, cr.has_metadata, 
        cr.has_feedback, cr.has_register, cr.has_preview, cr.has_bulk_download,
        cr.response_time, cr.app_count, cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4,
        cr.status, cr.status_detail
    FROM platforms p
    LEFT JOIN (
        SELECT platform_code, MAX(id) as max_id 
        FROM collection_records 
        GROUP BY platform_code
    ) latest ON p.code = latest.platform_code
    LEFT JOIN collection_records cr ON latest.max_id = cr.id
    WHERE p.tier = '省级'
    ORDER BY p.code
""")

rows = cursor.fetchall()
print(f'Total provincial platforms: {len(rows)}')
print()

print(f"{'Code':12s} {'Name':10s} {'Status':10s} {'Datasets':>10s} {'App':>5s} {'C1':>5s} {'C2':>5s} {'C3':>5s} {'C4':>5s} {'Overall':>7s} {'Func':>5s}")
print("-" * 100)

for row in rows:
    code, name, province, region, launch_year = row[0:5]
    dataset_count = row[5] or 0
    funcs = row[6:17]  # has_https to has_bulk_download
    func_sum = sum(1 for f in funcs if f)
    response_time = row[17] or 0
    app_count = row[18] or 0
    c1, c2, c3, c4 = row[19:23]
    status = row[23] or 'N/A'
    status_detail = row[24] or ''
    
    overall = row[22] if row[22] else 0
    
    print(f"{code:12s} {name:10s} {status:10s} {dataset_count:>10,} {app_count:>5} {c1 or 0:>5.2f} {c2 or 0:>5.2f} {c3 or 0:>5.2f} {c4 or 0:>5.2f} {overall:>7.3f} {func_sum:>5d}")

# Check which platforms have score_c1-c4 values
print()
print('=== Platforms with dimension scores (score_c1-c4) ===')
cursor.execute("""
    SELECT p.code, p.name, cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4, cr.overall_score
    FROM platforms p
    JOIN collection_records cr ON p.id = cr.platform_id
    WHERE p.tier = '省级' AND cr.score_c1 IS NOT NULL
    ORDER BY cr.overall_score DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]:12s} {row[1]:10s} C1={row[2]:.3f} C2={row[3]:.3f} C3={row[4]:.3f} C4={row[5]:.3f} Overall={row[6]:.3f}")

conn.close()
