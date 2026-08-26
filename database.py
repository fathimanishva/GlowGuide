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


cursor.execute("""
    UPDATE products
    SET image = ?
    WHERE name = ?
""", (
    "images/products/cetaphil_gentle_cleanser.jpg",
    "Gentle Skin Cleanser"
))

conn.commit()

print("Cetaphil image updated successfully!")


# Update image paths for the next 3 products

image_updates = {
    "Salicylic Acid LHA Cleanser":
        "images/products/minimalist_salicylic_cleanser.jpg",

    "Foaming Facial Cleanser":
        "images/products/cerave_foaming_cleanser.jpg",

    "Refreshing Facial Wash":
        "images/products/simple_refreshing_wash.jpg"
}

for product_name, image_path in image_updates.items():

    cursor.execute("""
        UPDATE products
        SET image = ?
        WHERE name = ?
    """, (image_path, product_name))

conn.commit()

print("3 product image paths updated!")

image_updates = {
    "Hydro Boost Water Gel":
        "images/products/neutrogena_hydro_boost.jpg",

    "Moisturising Cream":
        "images/products/cetaphil_moisturising_cream.jpg",

    "Barrier Repair Moisturizer":
        "images/products/dot_key_barrier_repair.jpg",

    "Green Tea Mattifying Moisturizer":
        "images/products/plum_green_tea_moisturizer.jpg"
}

for product_name, image_path in image_updates.items():

    cursor.execute("""
        UPDATE products
        SET image = ?
        WHERE name = ?
    """, (image_path, product_name))

conn.commit()

print("4 moisturizer image paths updated!")

image_updates = {
    "Ultra Sheer SPF 50+":
        "images/products/neutrogena_ultra_sheer.jpg",

    "Barrier Repair Sunscreen SPF 50+":
        "images/products/dot_key_barrier_sunscreen.jpg",

    "Cica Calming Niacinamide Sunscreen":
        "images/products/dot_key_cica_sunscreen.jpg",

    "Rice Water Sheer Tinted Sunscreen":
        "images/products/plum_rice_sunscreen.jpg"
}

for product_name, image_path in image_updates.items():

    cursor.execute("""
        UPDATE products
        SET image = ?
        WHERE name = ?
    """, (image_path, product_name))

conn.commit()

print("4 sunscreen image paths updated!")

# Update image paths for existing serum products

image_updates = {
    "10% Niacinamide Face Serum":
        "images/products/minimalist_niacinamide_10.jpg",

    "Salicylic Acid 2% Face Serum":
        "images/products/minimalist_salicylic_serum.jpg",

    "5% Niacinamide Face Serum":
        "images/products/plum_niacinamide_5.jpg",

    "Niacinamide Face Serum with Rice Water":
        "images/products/plum_rice_serum.jpg",

    "Strawberry Bright Face Serum":
        "images/products/dot_key_strawberry_serum.jpg"
}

for product_name, image_path in image_updates.items():

    cursor.execute("""
        UPDATE products
        SET image = ?
        WHERE name = ?
    """, (image_path, product_name))

conn.commit()

print("5 serum image paths updated!")

# Update image paths for existing toner products

image_updates = {
    "PHA Face Toner":
        "images/products/minimalist_pha_toner.jpg",

    "Daily Hydrating Toner":
        "images/products/plum_hydrating_toner.jpg",

    "Niacinamide Face Toner":
        "images/products/plum_niacinamide_toner.jpg"
}

for product_name, image_path in image_updates.items():

    cursor.execute("""
        UPDATE products
        SET image = ?
        WHERE name = ?
    """, (image_path, product_name))

conn.commit()

print("3 toner image paths updated!")

conn.close()