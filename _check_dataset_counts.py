import sqlite3
import json

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# Check database dataset counts
print('=== Database dataset_count ===')
cursor.execute("""
    SELECT p.code, p.name, cr.dataset_count, cr.status
    FROM platforms p
    LEFT JOIN (
        SELECT platform_code, MAX(id) as max_id 
        FROM collection_records 
        GROUP BY platform_code
    ) latest ON p.code = latest.platform_code
    LEFT JOIN collection_records cr ON latest.max_id = cr.id
    WHERE p.tier = '省级'
    ORDER BY cr.dataset_count DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]:12s} {row[1]:10s} datasets={row[2] or 0:>8,} status={row[3]}")

conn.close()

# Check v3 collection results
print()
print('=== V3 Collection Results ===')
try:
    with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
        v3 = json.load(f)
    for r in sorted(v3, key=lambda x: x.get('dataset_count') or 0, reverse=True):
        if r.get('status') == 'success':
            print(f"  {r['code']:12s} datasets={r.get('dataset_count') or 0:>8,}")
except FileNotFoundError:
    print("  v3_collection_results.json not found")

# Check if there's another data source
print()
print('=== Data directory files ===')
import os
for f in sorted(os.listdir('data')):
    if 'collect' in f.lower() or 'result' in f.lower():
        size = os.path.getsize(f'data/{f}')
        print(f"  {f:40s} {size:>10,} bytes")
