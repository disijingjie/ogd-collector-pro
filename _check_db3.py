import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# Count records
cursor.execute("SELECT COUNT(*) FROM collection_records")
print(f"collection_records count: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM collection_tasks")
print(f"collection_tasks count: {cursor.fetchone()[0]}")

# Sample data
cursor.execute("SELECT platform_code, platform_name, dataset_count, status FROM collection_records LIMIT 5")
print("\nSample collection_records:")
for row in cursor.fetchall():
    print(f"  {row}")

conn.close()
