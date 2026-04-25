import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# Check distinct status values
cursor.execute("SELECT DISTINCT status FROM collection_records")
print("Distinct statuses:")
for row in cursor.fetchall():
    print(f"  {row[0]}")

# Count by status
cursor.execute("SELECT status, COUNT(*) FROM collection_records GROUP BY status")
print("\nCount by status:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Check provincial platforms
cursor.execute("""
SELECT p.code, p.name, cr.dataset_count, cr.status 
FROM platforms p 
LEFT JOIN collection_records cr ON p.code = cr.platform_code 
WHERE p.tier = '省级'
GROUP BY p.code
""")
print("\nProvincial platforms:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}, dataset_count={row[2]}, status={row[3]}")

conn.close()
