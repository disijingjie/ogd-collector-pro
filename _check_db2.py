import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# Check collection_records
cursor.execute("PRAGMA table_info(collection_records)")
print("collection_records columns:")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

# Check platforms
cursor.execute("PRAGMA table_info(platforms)")
print("\nplatforms columns:")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

# Check snapshots
cursor.execute("PRAGMA table_info(collection_snapshots)")
print("\ncollection_snapshots columns:")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

conn.close()
