import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()
conn.commit()
conn.close()

