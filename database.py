import sqlite3

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()

# Check existing users
cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

for user in users:
    print(user)


# Create analysis history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method TEXT NOT NULL,
    skin_type TEXT NOT NULL,
    confidence REAL,
    image_name TEXT
)
""")

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    skin_types TEXT NOT NULL,
    sensitivity TEXT NOT NULL,
    description TEXT,
    image TEXT,
    product_link TEXT
)
""")

# Add concerns column to products table if it doesn't exist
try:
    cursor.execute("""
        ALTER TABLE products ADD COLUMN concerns TEXT
    """)
    print("Concerns column added.")
except sqlite3.OperationalError:
    print("Concerns column already exists.")


conn.commit()

print("Analysis history table is ready.")
print("Products table is ready.")

conn.close()