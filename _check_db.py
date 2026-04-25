import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")
    
# Check collection_stats
cursor.execute("PRAGMA table_info(collection_stats)")
print("\ncollection_stats columns:")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")
    
conn.close()
