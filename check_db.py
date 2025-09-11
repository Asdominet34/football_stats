import sqlite3

conn = sqlite3.connect("calcetto_stats.db")
c = conn.cursor()

c.execute("PRAGMA table_info(Giocatori)")
print("Schema della tabella Giocatori:")
for col in c.fetchall():
    print(col)

conn.close()