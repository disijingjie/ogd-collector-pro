import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
c = conn.cursor()

for table in ['collection_logs', 'data_provenance', 'collection_records', 'collection_tasks', 'collection_snapshots']:
    c.execute(f"PRAGMA table_info({table})")
    cols = [col[1] for col in c.fetchall()]
    print(f"{table}: {cols}")
    c.execute(f"SELECT * FROM {table} LIMIT 1")
    row = c.fetchone()
    if row:
        safe_row = []
        for v in row:
            if isinstance(v, str):
                safe_row.append(v.encode('ascii','replace').decode('ascii'))
            else:
                safe_row.append(v)
        print(f"  sample: {safe_row}")
    print()

conn.close()
