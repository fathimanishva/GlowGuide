import sqlite3

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

for user in users:
    print(user)

conn.close()