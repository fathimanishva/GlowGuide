import sqlite3

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT id, name
    FROM products
    WHERE name LIKE ?
""", ("%Foaming Facial Cleanser%",))

products = cursor.fetchall()

print(products)

conn.close()