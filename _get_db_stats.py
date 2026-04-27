import sqlite3, json
conn = sqlite3.connect('data/ogd_database.db')
c = conn.cursor()

# 先看所有表
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in c.fetchall()]
print('Tables:', tables)

# 获取platforms表结构
c.execute("PRAGMA table_info(platforms)")
plat_cols = [col[1] for col in c.fetchall()]
print('Platforms columns:', plat_cols)

# 1. 平台统计
c.execute("SELECT COUNT(DISTINCT province) FROM platforms")
provinces = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM platforms")
platforms = c.fetchone()[0]

# 找数据集表名
dataset_table = 'datasets' if 'datasets' in tables else ('dataset' if 'dataset' in tables else tables[0] if tables else None)
print('Dataset table:', dataset_table)

if dataset_table and dataset_table != 'platforms':
    c.execute(f"SELECT COUNT(*) FROM {dataset_table}")
    datasets = c.fetchone()[0]
    
    # 2. 数据集按格式统计
    c.execute(f"SELECT format, COUNT(*) FROM {dataset_table} WHERE format IS NOT NULL GROUP BY format ORDER BY COUNT(*) DESC")
    formats = c.fetchall()
    
    # 3. 数据集按标签统计
    c.execute(f"SELECT tag, COUNT(*) FROM {dataset_table} WHERE tag IS NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 10")
    tags = c.fetchall()
    
    # 5. 数据集时间范围
    c.execute(f"SELECT MIN(update_time), MAX(update_time) FROM {dataset_table} WHERE update_time IS NOT NULL")
    time_range = c.fetchone()
    
    # 6. 数据集按省份统计
    c.execute(f"SELECT p.province, COUNT(*) FROM {dataset_table} d JOIN platforms p ON d.platform_id = p.id GROUP BY p.province ORDER BY COUNT(*) DESC LIMIT 15")
    prov_counts = c.fetchall()
    
    # 7. 数据集按部门统计
    c.execute(f"SELECT department, COUNT(*) FROM {dataset_table} WHERE department IS NOT NULL AND department != '' GROUP BY department ORDER BY COUNT(*) DESC LIMIT 10")
    dept_counts = c.fetchall()
else:
    datasets = 0
    formats = []
    tags = []
    time_range = (None, None)
    prov_counts = []
    dept_counts = []

# 4. 平台列表（含URL）
c.execute("SELECT name, url, province FROM platforms ORDER BY province, name")
plat_list = c.fetchall()

# 8. 查看platforms表所有列
c.execute("PRAGMA table_info(platforms)")
plat_cols_full = c.fetchall()
print('Platforms full schema:', plat_cols_full)

conn.close()

print('---STATS---')
print(f'provinces={provinces}')
print(f'platforms={platforms}')
print(f'datasets={datasets}')
print(f'time_range={time_range}')
print('---FORMATS---')
for f in formats: print(f'{f[0]}:{f[1]}')
print('---TAGS---')
for t in tags: print(f'{t[0]}:{t[1]}')
print('---PLATFORMS---')
for p in plat_list: print(f'{p[0]}|{p[1]}|{p[2]}')
print('---PROV_COUNTS---')
for p in prov_counts: print(f'{p[0]}:{p[1]}')
print('---DEPT_COUNTS---')
for d in dept_counts: print(f'{d[0]}:{d[1]}')
