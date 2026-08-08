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

conn.commit()

print("Analysis history table is ready.")

conn.close()