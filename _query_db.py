import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

# 查看所有平台的层级分布
cursor.execute("SELECT tier, COUNT(*) FROM platforms GROUP BY tier")
print("=== 平台层级分布 ===")
for row in cursor.fetchall():
    print("  %s: %d" % row)

# 查看省级平台的code和url
cursor.execute("SELECT code, name, url FROM platforms WHERE tier='省级' ORDER BY code")
print()
print("=== 省级平台列表 ===")
for row in cursor.fetchall():
    print("  %-15s | %s" % (row[0], row[2]))

# 查看副省级和地市级的
cursor.execute("SELECT code, name, tier, url FROM platforms WHERE tier != '省级' ORDER BY code")
print()
print("=== 非省级平台列表 ===")
for row in cursor.fetchall():
    print("  %-15s | %-10s | %s" % (row[0], row[2], row[3]))

conn.close()
