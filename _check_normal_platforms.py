import sqlite3

conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

def fmt(v, w=8):
    if v is None:
        return 'None'.ljust(w)
    if isinstance(v, float):
        return f"{v:.2f}".ljust(w)
    return str(v).ljust(w)

# 只看每个平台最新的一条记录
cursor.execute("""
    SELECT cr.platform_code, cr.platform_name, cr.dataset_count, 
           cr.has_update_info, cr.has_metadata, cr.has_feedback,
           cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4,
           cr.collected_at
    FROM collection_records cr
    INNER JOIN (
        SELECT platform_code, MAX(collected_at) as max_at
        FROM collection_records
        WHERE tier='省级'
        GROUP BY platform_code
    ) latest ON cr.platform_code = latest.platform_code AND cr.collected_at = latest.max_at
    WHERE cr.tier='省级'
    ORDER BY cr.score_c3 DESC, cr.platform_code
""")
rows = cursor.fetchall()

print("=== 各省级平台最新采集记录 ===")
print(f"{'平台':<12} {'数据集':<10} {'更新':<6} {'元数据':<8} {'反馈':<6} {'C1':<8} {'C2':<8} {'C3':<8} {'C4':<8}")
for r in rows:
    print(f"{r[0]:<12} {fmt(r[2],10)} {fmt(r[3],6)} {fmt(r[4],8)} {fmt(r[5],6)} {fmt(r[6],8)} {fmt(r[7],8)} {fmt(r[8],8)} {fmt(r[9],8)}")

conn.close()
