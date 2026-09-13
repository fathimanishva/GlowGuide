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

# Remove duplicate recommendations
cursor.execute("""
    DELETE FROM product_recommendations
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM product_recommendations
        GROUP BY product_id, recommender_name
    )
""")

print("Duplicate recommendations removed.")

product_name = "2% Sali-Cinamide Anti-Acne Face Wash"
recommender_name = "Dermatologist Approved"

cursor.execute("""
    SELECT id
    FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    # Check before inserting
    cursor.execute("""
        SELECT id
        FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        product_id,
        recommender_name
    ))

    if not cursor.fetchone():

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
            "The Derma Co Official Dermatology Evidence",
            "The Derma Co states that this product is dermatologist-approved. "
            "It is formulated with 2% Salicylic Acid and 2% Niacinamide "
            "for acne-prone, oily and combination skin, helping control "
            "excess oil, unclog pores and reduce breakouts.",
            "The Derma Co - 2% Sali-Cinamide Anti-Acne Face Wash",
            "https://thedermaco.com/products/2-sali-cinamide-anti-acne-face-wash-with-2-salicylic-acid-2-niacinamide-200ml"
        ))

        print("Added:", product_name)

    else:
        print("Already exists:", product_name)

else:
    print("Product not found:", product_name)

# Dot & Key Watermelon SuperGlow Facial Gel Cleanser

product_name = "Watermelon SuperGlow Facial Gel Cleanser"
recommender_name = "Dermatologically Tested"

cursor.execute("""
    SELECT id
    FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    # Prevent duplicate recommendation
    cursor.execute("""
        SELECT id
        FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        product_id,
        recommender_name
    ))

    if not cursor.fetchone():

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
            "Product Testing Evidence",
            "The Watermelon SuperGlow Facial Gel Cleanser is listed as "
            "dermatologically tested. It is a gel cleanser formulated "
            "with ingredients including watermelon, cucumber and Vitamin C.",
            "Dot & Key - Watermelon SuperGlow Facial Gel Cleanser",
            "https://www.myntra.com/face-wash-and-cleanser/dot26key/dot--key-watermelon-super-glow-vitamin-c-face-wash-gel-for-oily-skin---120-ml/16549572/buy"
        ))

        print("Added:", product_name)

    else:
        print("Already exists:", product_name)

else:
    print("Product not found:", product_name)

# CeraVe PM Facial Moisturizing Lotion

product_name = "PM Facial Moisturizing Lotion"
recommender_name = "Dr. Heather Woolery-Lloyd, MD"

cursor.execute("""
    SELECT id
    FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    # Prevent duplicates
    cursor.execute("""
        SELECT id
        FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        product_id,
        recommender_name
    ))

    if not cursor.fetchone():

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
            "Board-Certified Dermatologist",
            "Dr. Heather Woolery-Lloyd specifically recommends "
            "CeraVe PM Facial Moisturizing Lotion for oily, "
            "acne-prone patients and describes it as a lightweight moisturizer.",
            "CeraVe - Dr. Heather Woolery-Lloyd",
            "https://www.cerave.com/authors/heather-woolery-lloyd"
        ))

        print("Added:", product_name)

    else:
        print("Already exists:", product_name)

else:
    print("Product not found:", product_name)

# ==========================================================
# MOISTURIZER RECOMMENDATIONS
# ==========================================================

moisturizer_recommendations = [

    # Dot & Key Barrier Repair Moisturizer
    (
        "Barrier Repair Moisturizer",
        "Dr. Nirupama Parwanda",
        "Dermatologist",
        "Dr. Nirupama Parwanda discusses and rates Dot & Key "
        "Barrier Repair Moisturizer in her dermatologist review "
        "of popular moisturizers. Dot & Key also reports clinical "
        "testing showing improvement in skin barrier and moisturization.",
        "Ask Dr Nirupama - Moisturiser Rating by a Dermatologist",
        "https://www.youtube.com/watch?v=u1ayFr6q3k0"
    ),

    # Cetaphil Moisturising Cream
    (
        "Moisturising Cream",
        "Dermatologist Tested",
        "Cetaphil Clinical Evidence",
        "Cetaphil states that this moisturizer is dermatologist "
        "tested and clinically proven to be gentle on sensitive skin. "
        "It uses a dermatologist-backed blend of niacinamide, "
        "panthenol and glycerin.",
        "Cetaphil India - Moisturising Cream",
        "https://www.cetaphil.in/moisturizers/moisturising-cream/8906005273436.html"
    ),

    # The Derma Co 5% Nia-Ceramide
    (
        "The Derma Co. 5% Nia-Ceramide Mattifying Moisturizer",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Consultant Dermatologist & Principal Investigator",
        "The moisturizer underwent Primary Skin Irritation Testing "
        "on human subjects under dermatologist supervision. "
        "The published certificate found the product dermatologically "
        "safe for use and non-irritant.",
        "The Derma Co - Dermatological Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-5-nia-ceramide-daily-hydrating-moisturizer-patch-test-certificate"
    )
]


for item in moisturizer_recommendations:

    product_name = item[0]
    recommender_name = item[1]

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

    # Prevent duplicate recommendations
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
        print(
            "Already exists:",
            product_name,
            "-",
            recommender_name
        )
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
        item[2],
        item[3],
        item[4],
        item[5]
    ))

    print(
        "Added:",
        product_name,
        "-",
        recommender_name
    )

remaining_moisturizers = [

    # Neutrogena Hydro Boost Water Gel
    (
        "Hydro Boost Water Gel",
        "Dr. Daniel Sugai",
        "Board-Certified Dermatologist",
        "Dr. Daniel Sugai specifically reviews and compares "
        "Neutrogena Hydro Boost Water Gel in his dermatologist "
        "skincare review.",
        "Dr. Daniel Sugai - Hydro Boost Water Gel Review",
        "https://www.youtube.com/watch?v=R3uKkMMM5VU"
    ),

    # CeraVe PM Facial Moisturizing Lotion
    (
        "PM Facial Moisturizing Lotion",
        "Dr. Heather Woolery-Lloyd, MD",
        "Board-Certified Dermatologist",
        "Dr. Heather Woolery-Lloyd specifically recommends "
        "CeraVe PM for oily, acne-prone patients and describes "
        "it as a lightweight moisturizer.",
        "CeraVe - Dr. Heather Woolery-Lloyd",
        "https://www.cerave.com/authors/heather-woolery-lloyd"
    )
]


for item in remaining_moisturizers:

    product_name = item[0]
    recommender_name = item[1]

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

    # Prevent duplicates
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
        print("Already exists:", product_name)
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
        item[2],
        item[3],
        item[4],
        item[5]
    ))

    print("Added:", product_name, "-", recommender_name)

product_name = "The Derma Co Ceramide + HA Intense Moisturizer Cream With Hyaluronic Acid"
recommender_name = "Designed by Dermatologists"

cursor.execute("""
    SELECT id
    FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    cursor.execute("""
        SELECT id
        FROM product_recommendations
        WHERE product_id = ?
        AND recommender_name = ?
    """, (product_id, recommender_name))

    if not cursor.fetchone():

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
            "The Derma Co Official Dermatology Evidence",
            "The Derma Co states that this moisturizer is designed "
            "by dermatologists. It combines ceramides and hyaluronic "
            "acid and is intended for intensive moisturization and "
            "supporting the skin moisture barrier.",
            "The Derma Co - Ceramide + HA Intense Daily Face Moisturizer",
            "https://thedermaco.com/products/ceramide-ha-intense-moisturizer"
        ))

        print("Added:", product_name)

    else:
        print("Already exists:", product_name)

else:
    print("Product not found:", product_name)

last_moisturizers = [

    # Dot & Key Watermelon Cooling Icy Gel Moisturizer
    (
        "Watermelon Cooling Icy Gel Moisturizer",
        "Clinical Product Evidence",
        "Dot & Key Official Product Evidence",
        "Dot & Key identifies this as a lightweight cooling gel "
        "moisturizer for normal, oily and combination skin. "
        "The Watermelon range is presented with clinically proven "
        "results and the moisturizer contains ingredients including "
        "niacinamide, hyaluronic acid and watermelon extract.",
        "Dot & Key - Watermelon Cooling Icy Gel Moisturizer",
        "https://www.dotandkey.com/collections/moisturizers"
    )
]


for item in last_moisturizers:

    product_name = item[0]
    recommender_name = item[1]

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

    # Prevent duplicates
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
        print("Already exists:", product_name)
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
        item[2],
        item[3],
        item[4],
        item[5]
    ))

    print("Added:", product_name, "-", recommender_name)

# Update Plum Green Tea Mattifying Moisturizer evidence

product_name = "Green Tea Mattifying Moisturizer"

cursor.execute("""
    SELECT id
    FROM products
    WHERE name = ?
""", (product_name,))

product = cursor.fetchone()

if product:
    product_id = product[0]

    cursor.execute("""
        UPDATE product_recommendations
        SET recommender_name = ?,
            recommender_title = ?,
            recommendation_reason = ?,
            reference_title = ?,
            reference_url = ?
        WHERE product_id = ?
        AND recommender_name = ?
    """, (
        "Divya Agarwal",
        "Author - Plum Official Product Guide",
        "Divya Agarwal authored Plum's official guide specifically "
        "about Green Tea Mattifying Moisturizer. The guide explains "
        "how to use the product and discusses its suitability for "
        "combination, oily and acne-prone skin.",
        "Plum - How to Use Green Tea Mattifying Moisturizer",
        "https://plumgoodness.com/blogs/how-to-use/how-to-use-green-tea-mattifying-moisturizer",
        product_id,
        "Official Product Evidence"
    ))

    print("Updated Plum recommendation.")

else:
    print("Product not found:", product_name)

conn.commit()
conn.close()

print("Recommendations added successfully.")