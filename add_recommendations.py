import sqlite3

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()

# CeraVe Foaming Facial Cleanser
product_id = 12

recommendations = [
    (
        product_id,
        "Dr. Gary Goldenberg, MD",
        "Dermatologist",
        "Listed among dermatologist-recommended face washes.",
        "MDedge - Dermatologists Weigh in on Face Washes",
        "https://www.mdedge.com/dermatology/article/100938/aesthetic-dermatology/cosmetic-corner-dermatologists-weigh-face-washes"
    ),

    (
        product_id,
        "Dr. Alecia Folkes",
        "Board-Certified Dermatologist",
        "Recommends this cleanser for patients with acne-prone or oily skin.",
        "CeraVe - Dr. Alecia Folkes",
        "https://www.cerave.com/authors/alecia-folkes"
    )
]


for recommendation in recommendations:

    # Prevent duplicate recommendations
    cursor.execute("""
        SELECT id
        FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        recommendation[0],
        recommendation[1]
    ))

    existing = cursor.fetchone()

    if existing:
        print("Already exists:", recommendation[1])
        continue

    cursor.execute("""
        INSERT INTO product_recommendations
        (
            product_id,
            recommender_name,
            recommender_title,
            recommendation_reason,
            reference_title,
            reference_url
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, recommendation)

    print("Added:", recommendation[1])

# ------------------------------------------------
# ADDITIONAL FACE WASH EVIDENCE
# ------------------------------------------------

recommendations = [

    # Cetaphil Gentle Skin Cleanser
    (
        "Gentle Skin Cleanser",
        "Dermatologist Tested",
        "Cetaphil Clinical Product Evidence",
        "Cetaphil states that Gentle Skin Cleanser is dermatologist tested and clinically proven to be gentle on sensitive skin. It is intended for normal-to-dry skin and uses a dermatologist-backed blend of niacinamide, panthenol and glycerin.",
        "Cetaphil - Gentle Skin Cleanser",
        "https://www.cetaphil.com/us/products/product-categories/all-cleansers/cetaphil-gentle-skin-cleanser/302990110227.html"
    ),

    # Minimalist Salicylic Acid + LHA Cleanser
    (
        "Salicylic Acid LHA Cleanser",
        "Dermatologist Supervised",
        "Minimalist Safety Testing",
        "Minimalist states that the cleanser was evaluated for safety through patch testing under the supervision of a dermatologist. The product is intended for oily or combination, acne-prone skin.",
        "Minimalist - Salicylic Acid + LHA 2% Cleanser",
        "https://beminimalist.co/products/salicylic-lha-2-cleanser"
    ),

    # The Derma Co Niacinamide Gentle Cleanser
    (
        "2% Niacinamide Gentle Dry Skin Cleanser",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist and Clinical Study Investigators",
        "The cleanser underwent Primary Skin Irritation Testing on human subjects. The published certificate states that it was found dermatologically safe and non-irritant under direct dermatologist supervision.",
        "The Derma Co - Dermatological Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-2-niacinamide-gentle-skin-cleanser-patch-test-certificate"
    ),

    # Simple Refreshing Facial Wash
    (
        "Refreshing Facial Wash",
        "Dermatologically Tested",
        "Simple Skincare Clinical Product Evidence",
        "Simple states that Refreshing Facial Wash is dermatologically tested, hypoallergenic and non-comedogenic, and suitable for all skin types including sensitive skin.",
        "Simple - Refreshing Facial Wash",
        "https://www.simpleskincare.in/products/simple-kind-to-skin-refreshing-facial-wash-150ml"
    )
]

for item in recommendations:

    product_name = item[0]

    cursor.execute("""
        SELECT id
        FROM products
        WHERE name = ?
    """, (product_name,))

    product = cursor.fetchone()

    if not product:
        print("Product not found:", product_name)
        continue

    product_id = product[0]

    recommender_name = item[1]
    recommender_title = item[2]
    reason = item[3]
    reference_title = item[4]
    reference_url = item[5]

    # Avoid duplicates
    cursor.execute("""
        SELECT id
        FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        product_id,
        recommender_name
    ))

    if cursor.fetchone():
        print("Already exists:", product_name, "-", recommender_name)
        continue

    cursor.execute("""
        INSERT INTO product_recommendations
        (
            product_id,
            recommender_name,
            recommender_title,
            recommendation_reason,
            reference_title,
            reference_url
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        recommender_name,
        recommender_title,
        reason,
        reference_title,
        reference_url
    ))

    print("Added:", product_name, "-", recommender_name)

# The Derma Co 2% Niacinamide Oily Skin Cleanser
product_name = "2% Niacinamide Oily Skin Cleanser"

cursor.execute("""
    SELECT id FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    cursor.execute("""
        INSERT INTO product_recommendations
        (
            product_id,
            recommender_name,
            recommender_title,
            recommendation_reason,
            reference_title,
            reference_url
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist & Clinical Study Investigators",
        "The cleanser underwent Primary Skin Irritation Testing on human subjects under direct dermatologist supervision and was certified Dermatologically Safe for use and Non-Irritant.",
        "The Derma Co - Dermatological Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-2-niacinamide-oily-skin-cleanser-patch-test-certificate"
    ))

    print("Added:", product_name)
else:
    print("Product not found:", product_name)

product_name = "Gentle Skin Cleanser"

cursor.execute("""
    SELECT id FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    # Remove the older generic Cetaphil entry
    cursor.execute("""
        DELETE FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        product_id,
        "Dermatologist Tested"
    ))

    # Add named dermatologist entry
    cursor.execute("""
        INSERT INTO product_recommendations
        (
            product_id,
            recommender_name,
            recommender_title,
            recommendation_reason,
            reference_title,
            reference_url
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        "Dr. Husain",
        "Dermatologist",
        "Cetaphil's official product page features Dr. Husain discussing Gentle Skin Cleanser, including its niacinamide and glycerin formulation for cleansing while helping maintain skin hydration.",
        "Cetaphil - Gentle Skin Cleanser",
        "https://www.cetaphil.com/us/products/product-categories/all-cleansers/cetaphil-gentle-skin-cleanser/302990110227.html"
    ))

    print("Updated:", product_name)
else:
    print("Product not found:", product_name)


conn.commit()
conn.close()

print("Recommendations added successfully.")