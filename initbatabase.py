import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('CREATE TABLE accounts(email, login, password)')
conn.commit()
conn.close()