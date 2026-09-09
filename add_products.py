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
    (
    "2% Sali-Cinamide Anti-Acne Face Wash",
    "The Derma Co",
    "Face Wash",
    349,
    "oily,combination,normal",
    "not_sensitive,somewhat_sensitive",
    "oil_control,pores",
    "Salicylic acid and niacinamide cleanser designed to control excess oil and unclog pores.",
    None,
    "https://thedermaco.com/"
    ),

    (
        "2% Niacinamide Gentle Dry Skin Cleanser",
        "The Derma Co",
        "Face Wash",
        299,
        "dry,normal,sensitive",
        "sensitive,somewhat_sensitive",
        "dryness,dehydration,sensitivity",
        "Gentle cleanser designed for dry skin with a hydration-focused formula.",
        None,
        "https://thedermaco.com/"
    ),

    (
        "Watermelon SuperGlow Facial Gel Cleanser",
        "Dot & Key",
        "Face Wash",
        295,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control,dullness",
        "Lightweight cleanser that helps remove excess oil without over-drying the skin.",
        None,
        "https://www.dotandkey.com/"
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
    (
    "5% Nia-Ceramide Daily Hydrating Moisturizer",
    "The Derma Co",
    "Moisturizer",
    399,
    "dry,normal,oily,combination",
    "normal,somewhat_sensitive",
    "dryness,dehydration",
    "Hydrating moisturizer containing niacinamide and ceramides to support the skin barrier.",
    None,
    "https://thedermaco.com/"
    ),

    (
        "Ceramide + HA Intense Daily Face Moisturizer",
        "The Derma Co",
        "Moisturizer",
        349,
        "dry,normal,sensitive",
        "sensitive,somewhat_sensitive",
        "dryness,dehydration,sensitivity",
        "Ceramide and hyaluronic acid moisturizer designed for dry and dehydrated skin.",
        None,
        "https://thedermaco.com/"
    ),

    (
        "Watermelon Cooling Icy Gel Moisturizer",
        "Dot & Key",
        "Moisturizer",
        495,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control,dehydration",
        "Lightweight gel moisturizer that provides hydration without a heavy feel.",
        None,
        "https://www.dotandkey.com/"
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
    (
    "1% Hyaluronic Sunscreen Aqua Gel SPF 50",
    "The Derma Co",
    "Sunscreen",
    499,
    "dry,normal,oily,combination",
    "normal,somewhat_sensitive",
    "sun_protection,dehydration",
    "Lightweight SPF 50 sunscreen with hyaluronic acid for daily sun protection.",
    None,
    "https://thedermaco.com/"
    ),

    (
        "Watermelon Cooling Sunscreen SPF 50+",
        "Dot & Key",
        "Sunscreen",
        495,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "sun_protection,oil_control",
        "Lightweight sunscreen designed for oily, combination and normal skin.",
        None,
        "https://www.dotandkey.com/"
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
    (
    "10% Vitamin C Face Serum",
    "The Derma Co",
    "Serum",
    599,
    "normal,dry,combination,oily",
    "normal,somewhat_sensitive",
    "dullness",
    "Vitamin C serum designed to improve dull-looking and uneven skin.",
    None,
    "https://thedermaco.com/"
    ),

    (
        "15% Vitamin C Face Serum",
        "The Derma Co",
        "Serum",
        649,
        "normal,dry,combination,oily",
        "not_sensitive,somewhat_sensitive",
        "dullness",
        "Brightening serum formulated with vitamin C and supporting hydrating ingredients.",
        None,
        "https://thedermaco.com/"
    ),

    (
        "2% Salicylic Acid Face Serum",
        "The Derma Co",
        "Serum",
        499,
        "oily,combination",
        "not_sensitive,somewhat_sensitive",
        "oil_control,pores",
        "Salicylic acid serum designed to help unclog pores and manage excess oil.",
        None,
        "https://thedermaco.com/"
    ),

    (
        "10% Glycolic Acid Face Serum",
        "Dot & Key",
        "Serum",
        599,
        "oily,combination,normal",
        "not_sensitive",
        "texture,dullness,pores",
        "Exfoliating serum designed to improve skin texture and dullness.",
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
    ),
    (
    "Rice Water Probiotics Toner",
    "Dot & Key",
    "Toner",
    395,
    "dry,normal,combination,sensitive",
    "sensitive,somewhat_sensitive",
    "dryness,dehydration,dullness",
    "Hydrating toner designed to support smoother and more hydrated skin.",
    None,
    "https://www.dotandkey.com/"
    ),

    (
        "Watermelon SuperGlow Pore Tightening Toner",
        "Dot & Key",
        "Toner",
        395,
        "oily,combination,normal",
        "normal,somewhat_sensitive",
        "oil_control,pores",
        "Lightweight toner aimed at controlling excess oil and improving the appearance of pores.",
        None,
        "https://www.dotandkey.com/"
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
cursor.execute("SELECT COUNT(*) FROM products")
total = cursor.fetchone()[0]

print("Total products in database:", total)

conn.close()