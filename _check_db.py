import sqlite3

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# 查看所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print('Tables:', tables)

# 统计各表数据量
for t in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {t}')
        count = cursor.fetchone()[0]
        print(f'{t}: {count} rows')
    except Exception as e:
        print(f'{t}: ERROR - {e}')

# 查看每个表的结构和示例数据
for t in tables:
    try:
        cursor.execute(f'PRAGMA table_info({t})')
        cols = cursor.fetchall()
        print(f'\n{t} columns: {[c[1] for c in cols]}')
        cursor.execute(f'SELECT * FROM {t} LIMIT 1')
        row = cursor.fetchone()
        print(f'{t} sample: {row}')
    except Exception as e:
        print(f'{t} error: {e}')

conn.close()
