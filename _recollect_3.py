"""重新采集北京、广东、安徽3个省级平台"""
import sqlite3
from collector_engine import CollectorEngine, create_collection_task
from models import get_db

# 创建专项采集任务
task_id = create_collection_task('省级平台补采-北京广东安徽', 'provincial')
print(f'创建任务ID: {task_id}')

engine = CollectorEngine(task_id=task_id, max_workers=1, delay=2)

# 只采集这3个平台
targets = ['北京市', '广东省', '安徽省']

conn = get_db()
cursor = conn.cursor()
placeholders = ','.join(['?' for _ in targets])
cursor.execute(f"SELECT * FROM platforms WHERE name IN ({placeholders}) AND tier='省级'", targets)
platforms = [dict(row) for row in cursor.fetchall()]
conn.close()

print(f'找到{len(platforms)}个平台')
for p in platforms:
    print(f'  {p["name"]}: {p["url"]}')

for p in platforms:
    print(f'\n>>> 开始采集: {p["name"]}')
    result = engine.collect_single(p)
    print(f'状态: {result["status"]}')
    print(f'详情: {result["status_detail"]}')
    print(f'数据集: {result["dataset_count"]}')
    print(f'功能: 搜索={result["has_search"]} 下载={result["has_download"]} API={result["has_api"]}')

print('\n=== 采集完成 ===')
print(f'成功: {engine.stats["success"]}, 失败: {engine.stats["failed"]}')
