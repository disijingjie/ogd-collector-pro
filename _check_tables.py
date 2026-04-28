import sqlite3
conn = sqlite3.connect('data/ogd_database.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
for t in c.fetchall():
    print(t[0])
conn.close()
