"""
将之前采集的数据导入到新系统数据库
"""
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

# 读取之前采集的数据
csv_path = Path(__file__).parent.parent / "三层架构采集结果_原始_20260422_214735.csv"
df = pd.read_csv(csv_path, encoding='utf-8-sig')

# 连接数据库
db_path = Path(__file__).parent / "data" / "ogd_database.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 先创建一个采集任务
cursor.execute("""
    INSERT INTO collection_tasks (task_name, task_type, status, total_count, completed_count, success_count, fail_count, started_at, completed_at, created_at)
    VALUES (?, ?, 'completed', ?, ?, ?, ?, ?, ?, ?)
""", (
    '三层架构完整采集_20260422',
    'full',
    len(df), len(df),
    len(df[df['status'] == 'available']),
    len(df[df['status'] != 'available']),
    '2026-04-22T21:47:00',
    '2026-04-22T21:49:00',
    '2026-04-22T21:47:00'
))
task_id = cursor.lastrowid

# 导入记录
for idx, row in df.iterrows():
    # 确定平台编码和名称
    code = row['city_code'] if pd.notna(row['city_code']) else row['province_code']
    name = row['city_name'] if pd.notna(row['city_name']) else row['province_name']
    
    # 查找platform_id
    cursor.execute("SELECT id FROM platforms WHERE code=?", (code,))
    result = cursor.fetchone()
    platform_id = result[0] if result else None
    
    # 确定状态
    status = 'available' if row['available'] == 1 else 'unavailable'
    
    if platform_id:
        cursor.execute("""
            INSERT INTO collection_records 
            (task_id, platform_id, platform_code, platform_name, tier, region, status, status_detail,
             response_time, has_https, has_search, has_download, has_api, has_register, has_preview,
             has_visualization, has_update_info, has_metadata, has_feedback,
             dataset_count, format_types, overall_score,
             http_status, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_id, platform_id, code, name, row['tier'], row['region'],
            status, str(row.get('error', ''))[:200],
            row.get('response_time', 0), row.get('has_https', 0), row.get('has_search', 0),
            row.get('has_download', 0), row.get('has_api', 0), row.get('has_registration', 0),
            row.get('has_preview', 0), row.get('has_visualization', 0),
            row.get('update_info', 0), 0, row.get('has_feedback', 0),
            row.get('dataset_count', 0), str(row.get('formats', '[]')),
            0,  # overall_score 需要后续计算
            None,
            row.get('collect_time', datetime.now().isoformat())
        ))

conn.commit()
conn.close()
print(f"[OK] 已导入 {len(df)} 条采集记录到任务 #{task_id}")
