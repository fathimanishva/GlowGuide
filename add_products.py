import sqlite3

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()

products = [
    # -------------------------
    # FACE WASH
    # -------------------------

    (
        "Gentle Skin Cleanser",
        "Cetaphil",
        "Face Wash",
        459,
        "dry,normal,sensitive",
        "sensitive",
        "dryness,sensitivity",
        "A gentle cleanser suitable for dry and sensitive skin.",
        None,
        "https://www.cetaphil.in/"
    ),

    (
        "Salicylic Acid LHA Cleanser",
        "Minimalist",
        "Face Wash",
        569,
        "oily,combination",
        "not_sensitive,somewhat_sensitive",
        "oil_control,pores",
        "A cleanser formulated for oily and combination skin.",
        None,
        "https://beminimalist.co/"
    ),

    (
        "Foaming Facial Cleanser",
        "CeraVe",
        "Face Wash",
        500,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control",
        "Foaming cleanser suitable for normal to oily skin.",
        None,
        "https://www.cerave.com/"
    ),

    (
        "Refreshing Facial Wash",
        "Simple",
        "Face Wash",
        350,
        "oily,combination,normal",
        "sensitive,somewhat_sensitive",
        "oil_control",
        "A simple daily cleanser for a fresh, clean feel.",
        None,
        "https://www.simple.co.uk/"
    ),

    # -------------------------
    # MOISTURIZER
    # -------------------------

    (
        "Hydro Boost Water Gel",
        "Neutrogena",
        "Moisturizer",
        750,
        "dry,normal,oily,combination",
        "normal,somewhat_sensitive",
        "dryness,dehydration",
        "Lightweight gel moisturizer focused on hydration.",
        None,
        "https://www.neutrogena.in/"
    ),

    (
        "Moisturising Cream",
        "Cetaphil",
        "Moisturizer",
        499,
        "dry,normal,sensitive",
        "sensitive",
        "dryness,sensitivity",
        "Moisturizer suitable for dry and sensitive skin.",
        None,
        "https://www.cetaphil.in/"
    ),

    (
        "Barrier Repair Moisturizer",
        "Dot & Key",
        "Moisturizer",
        895,
        "dry,normal,sensitive",
        "sensitive,somewhat_sensitive",
        "dryness,sensitivity",
        "Barrier-focused moisturizer for dry to sensitive skin.",
        None,
        "https://www.dotandkey.com/"
    ),

    (
        "Green Tea Mattifying Moisturizer",
        "Plum",
        "Moisturizer",
        395,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control",
        "Lightweight moisturizer for oily and combination skin.",
        None,
        "https://plumgoodness.com/"
    ),

    # -------------------------
    # SUNSCREEN
    # -------------------------

    (
        "Ultra Sheer SPF 50+",
        "Neutrogena",
        "Sunscreen",
        699,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "sun_protection",
        "Lightweight daily sunscreen.",
        None,
        "https://www.neutrogena.in/"
    ),

    (
        "Barrier Repair Sunscreen SPF 50+",
        "Dot & Key",
        "Sunscreen",
        505,
        "dry,normal,oily,combination",
        "sensitive,somewhat_sensitive",
        "sun_protection,dryness",
        "Daily sunscreen designed for broad skin-type compatibility.",
        None,
        "https://www.dotandkey.com/"
    ),

    (
        "Cica Calming Niacinamide Sunscreen",
        "Dot & Key",
        "Sunscreen",
        445,
        "oily,combination,normal",
        "sensitive,somewhat_sensitive",
        "sun_protection,oil_control",
        "Lightweight sunscreen with a calming-focused formula.",
        None,
        "https://www.dotandkey.com/"
    ),

    (
        "Rice Water Sheer Tinted Sunscreen",
        "Plum",
        "Sunscreen",
        449,
        "normal,dry,combination",
        "normal,somewhat_sensitive",
        "sun_protection",
        "Tinted sunscreen option for daily use.",
        None,
        "https://plumgoodness.com/"
    ),

    # -------------------------
    # SERUM
    # -------------------------

    (
        "10% Niacinamide Face Serum",
        "Minimalist",
        "Serum",
        599,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control,pores",
        "Niacinamide serum aimed at oil control and pore care.",
        None,
        "https://beminimalist.co/"
    ),

    (
        "Salicylic Acid 2% Face Serum",
        "Minimalist",
        "Serum",
        902,
        "oily,combination",
        "not_sensitive,somewhat_sensitive",
        "oil_control,pores",
        "Salicylic-acid serum intended for oily and combination skin.",
        None,
        "https://beminimalist.co/"
    ),

    (
        "5% Niacinamide Face Serum",
        "Plum",
        "Serum",
        509,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control,pores",
        "Niacinamide serum for everyday skincare routines.",
        None,
        "https://plumgoodness.com/"
    ),

    (
        "Niacinamide Face Serum with Rice Water",
        "Plum",
        "Serum",
        303,
        "normal,oily,combination",
        "normal,somewhat_sensitive",
        "oil_control,pores",
        "Lightweight serum for a simple skincare routine.",
        None,
        "https://plumgoodness.com/"
    ),

    (
        "Strawberry Bright Face Serum",
        "Dot & Key",
        "Serum",
        599,
        "normal,dry,combination",
        "normal,somewhat_sensitive",
        "dullness",
        "Brightening-focused facial serum.",
        None,
        "https://www.dotandkey.com/"
    ),

    # -------------------------
    # TONER
    # -------------------------

    (
        "PHA Face Toner",
        "Minimalist",
        "Toner",
        379,
        "normal,dry,combination",
        "normal,somewhat_sensitive",
        "texture,dullness",
        "Gentle exfoliating toner option.",
        None,
        "https://beminimalist.co/"
    ),

    (
        "Daily Hydrating Toner",
        "Plum",
        "Toner",
        450,
        "dry,normal,sensitive",
        "sensitive,somewhat_sensitive",
        "dryness,dehydration",
        "Hydrating toner for a gentle skincare routine.",
        None,
        "https://plumgoodness.com/"
    ),

    (
        "Niacinamide Face Toner",
        "Plum",
        "Toner",
        450,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control,pores",
        "Lightweight toner for oily and combination skin.",
        None,
        "https://plumgoodness.com/"
    )
]


# Prevent duplicate products
added = 0

for product in products:

    cursor.execute("""
        SELECT id
        FROM products
        WHERE name = ? AND brand = ?
    """, (product[0], product[1]))

    existing = cursor.fetchone()

    if existing:
        print(f"Already exists: {product[1]} - {product[0]}")
        continue

    cursor.execute("""
        INSERT INTO products
        (
            name,
            brand,
            category,
            price,
            skin_types,
            sensitivity,
            concerns,
            description,
            image,
            product_link
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, product)

    added += 1


conn.commit()

print(f"{added} new products added successfully!")

conn.close()