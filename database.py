import sqlite3

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()


# --------------------------------
# Create analysis history table
# --------------------------------

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


# --------------------------------
# Create products table
# --------------------------------

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


# --------------------------------
# Add concerns column if missing
# --------------------------------

try:

    cursor.execute("""
        ALTER TABLE products
        ADD COLUMN concerns TEXT
    """)

    print("Concerns column added.")

except sqlite3.OperationalError:

    print("Concerns column already exists.")

# --------------------------------
# Add role column to users
# --------------------------------

try:
    cursor.execute("""
        ALTER TABLE users
        ADD COLUMN role TEXT DEFAULT 'user'
    """)

    print("Role column added.")

except sqlite3.OperationalError:
    print("Role column already exists.")



# --------------------------------
# Saved recommendations
# --------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT NOT NULL,
    skin_type TEXT NOT NULL,
    sensitivity TEXT,
    concerns TEXT,
    product_ids TEXT
)
""")


# --------------------------------
# Saved routines
# --------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT NOT NULL,
    skin_type TEXT NOT NULL,
    sensitivity TEXT,
    concerns TEXT,
    morning_product_ids TEXT,
    night_product_ids TEXT
)
""")


# --------------------------------
# Save database changes
# --------------------------------

# Add recommended_by column to products table
try:
    cursor.execute("""
        ALTER TABLE products
        ADD COLUMN recommended_by TEXT
    """)
    print("recommended_by column added.")
except sqlite3.OperationalError:
    print("recommended_by column already exists.")


# Add reference column to products table
try:
    cursor.execute("""
        ALTER TABLE products
        ADD COLUMN reference TEXT
    """)
    print("reference column added.")
except sqlite3.OperationalError:
    print("reference column already exists.")


# Create product reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS product_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_email TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    review_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

# Create product recommendations table
cursor.execute("""
CREATE TABLE IF NOT EXISTS product_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    recommender_name TEXT NOT NULL,
    recommender_title TEXT,
    recommendation_reason TEXT,
    reference_title TEXT,
    reference_url TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

print("Product recommendations table is ready.")



conn.commit()

print("Analysis history table is ready.")
print("Products table is ready.")
print("Product reviews table is ready.")

conn.close()