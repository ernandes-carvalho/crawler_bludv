import sqlite3
import json

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("""
select id, nome, link, img, data from link_filmes
""")

data = c.fetchall()
print(json.dumps(data, indent=4))
# for row in c.fetchall():
#    print(row)


conn.close()
