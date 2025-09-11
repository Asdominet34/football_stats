import sqlite3

conn = sqlite3.connect("calcetto_stats.db")
c = conn.cursor()

c.execute("PRAGMA table_info(Partite)")
schema = c.fetchall()

for col in schema:
    print(col)
