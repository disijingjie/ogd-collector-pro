import sqlite3

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print('Tables:', tables)

for table in tables:
    print()
    print(f'=== {table} ===')
    cursor.execute(f'PRAGMA table_info({table})')
    cols = cursor.fetchall()
    for col in cols:
        print(f'  {col[1]:30s} {col[2]}')

# Check platforms table data
cursor.execute("SELECT COUNT(*) FROM platforms")
print()
print(f"Total platforms: {cursor.fetchone()[0]}")

cursor.execute("SELECT code, name, province, region, launch_year, url FROM platforms WHERE tier='省级' LIMIT 5")
print()
print("Sample platforms:")
for row in cursor.fetchall():
    print(f"  {row}")

# Check collection_records
cursor.execute("SELECT COUNT(*) FROM collection_records")
print()
print(f"Total collection records: {cursor.fetchone()[0]}")

cursor.execute("PRAGMA table_info(collection_records)")
print()
print("Collection records columns:")
for col in cursor.fetchall():
    print(f"  {col[1]:30s} {col[2]}")

# Check latest records
cursor.execute("""
    SELECT platform_code, dataset_count, has_api, has_search, has_download, 
           has_visualization, has_update_info, has_metadata, has_feedback,
           has_register, has_preview, has_bulk_download, response_time
    FROM collection_records 
    WHERE id IN (SELECT MAX(id) FROM collection_records GROUP BY platform_code)
    AND dataset_count IS NOT NULL
    ORDER BY dataset_count DESC
    LIMIT 10
""")
print()
print("Latest records (top 10 by dataset_count):")
for row in cursor.fetchall():
    print(f"  {row[0]:10s} datasets={row[1]:>8,}  api={row[2]} search={row[3]} dl={row[4]} vis={row[5]} update={row[6]} meta={row[7]} fb={row[8]} reg={row[9]} prev={row[10]} bulk={row[11]} rt={row[12]}")

conn.close()
