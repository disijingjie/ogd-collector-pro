import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()
cursor.execute('''
    SELECT p.code, p.name, cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4, cr.dataset_count, cr.app_count,
           cr.has_https, cr.has_search, cr.has_download, cr.has_api, cr.has_visualization, 
           cr.has_update_info, cr.has_metadata, cr.has_feedback, cr.has_register, cr.has_preview, cr.has_bulk_download,
           cr.response_time, p.launch_year
    FROM platforms p
    LEFT JOIN (
        SELECT platform_code, MAX(id) as max_id 
        FROM collection_records 
        GROUP BY platform_code
    ) latest ON p.code = latest.platform_code
    LEFT JOIN collection_records cr ON latest.max_id = cr.id
    WHERE p.tier = '省级'
    ORDER BY p.code
''')
rows = cursor.fetchall()
print(f'平台数: {len(rows)}')
print('code          name       c1    c2    c3    c4  datasets  apps  funcs  response launch')
for r in rows:
    code, name, c1, c2, c3, c4, dc, ac = r[0:8]
    funcs = r[8:18]
    rt = r[18]
    ly = r[19]
    func_sum = sum(1 for f in funcs if f)
    print(f'{code:12s} {name:8s} {c1 or 0:>5.2f} {c2 or 0:>5.2f} {c3 or 0:>5.2f} {c4 or 0:>5.2f} {dc or 0:>8} {ac or 0:>5} {func_sum:>2}/10  {rt or 0:>6}ms {ly or "N/A"}')
conn.close()
