import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()
cursor.execute("SELECT code, name, province FROM platforms WHERE tier='省级' ORDER BY code")
rows = cursor.fetchall()
print(f'省级平台总数: {len(rows)}')
for r in rows:
    print(f'  {r[0]:12s} {r[1]:10s} {r[2]}')
conn.close()
