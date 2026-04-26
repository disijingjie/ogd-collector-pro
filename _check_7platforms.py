import sqlite3
import json

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# 查看collection_records表结构
cursor.execute("PRAGMA table_info(collection_records)")
cols = cursor.fetchall()

out_lines = []
out_lines.append('=== collection_records 字段 ===')
for c in cols:
    out_lines.append(f"  {c[1]} ({c[2]})")

out_lines.append('')

# 查看7个score_c3=0的平台记录
platforms = ['guangdong', 'jiangsu', 'guizhou', 'jiangxi', 'fujian', 'shanghai', 'anhui']
for code in platforms:
    cursor.execute("SELECT * FROM collection_records WHERE platform_code=? ORDER BY collected_at DESC LIMIT 1", (code,))
    row = cursor.fetchone()
    if row:
        out_lines.append(f'=== {code} ===')
        for i, col in enumerate(cols):
            val = row[i]
            if val is not None and str(val) != '':
                out_lines.append(f'  {col[1]}: {val}')
    else:
        out_lines.append(f'=== {code} === 无记录')
    out_lines.append('')

conn.close()

with open('_check_7platforms_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print('结果已写入 _check_7platforms_result.txt')
