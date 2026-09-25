import sqlite3


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

conn = sqlite3.connect("glowguide.db")
cursor = conn.cursor()


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def add_recommendation(
    product_name,
    recommender_name,
    recommender_title,
    recommendation_reason,
    reference_title,
    reference_url
):
    """
    Add one recommendation/testing record for a product.

    A record is not inserted again when the same product and
    recommender_name already exist.
    """

    # Find product
    cursor.execute("""
        SELECT id
        FROM products
        WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
    """, (product_name,))

    product = cursor.fetchone()

    if not product:
        print("Product not found:", product_name)
        return

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

    if cursor.fetchone():
        print(
            "Already exists:",
            product_name,
            "-",
            recommender_name
        )
        return

    # Insert recommendation
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
        recommendation_reason,
        reference_title,
        reference_url
    ))

    print(
        "Added:",
        product_name,
        "-",
        recommender_name
    )


# ==========================================================
# 1. FACE WASH
# ==========================================================

face_wash_recommendations = [

    (
        "Foaming Facial Cleanser",
        "Dr. Gary Goldenberg, MD",
        "Dermatologist",
        "Listed among dermatologist-recommended face washes.",
        "MDedge - Dermatologists Weigh in on Face Washes",
        "https://www.mdedge.com/dermatology/article/100938/aesthetic-dermatology/cosmetic-corner-dermatologists-weigh-face-washes"
    ),

    (
        "Foaming Facial Cleanser",
        "Dr. Alecia Folkes",
        "Board-Certified Dermatologist",
        "Recommends this cleanser for patients with acne-prone or oily skin.",
        "CeraVe - Dr. Alecia Folkes",
        "https://www.cerave.com/authors/alecia-folkes"
    ),

    (
        "Gentle Skin Cleanser",
        "Dr. Husain",
        "Dermatologist",
        "Cetaphil's official product page features Dr. Husain discussing "
        "Gentle Skin Cleanser, including its niacinamide and glycerin "
        "formulation for cleansing while helping maintain skin hydration.",
        "Cetaphil - Gentle Skin Cleanser",
        "https://www.cetaphil.com/us/products/product-categories/all-cleansers/cetaphil-gentle-skin-cleanser/302990110227.html"
    ),

    (
        "Salicylic Acid LHA Cleanser",
        "Dermatologist Supervised",
        "Minimalist Safety Testing",
        "Minimalist states that the cleanser was evaluated for safety "
        "through patch testing under the supervision of a dermatologist. "
        "The product is intended for oily or combination, acne-prone skin.",
        "Minimalist - Salicylic Acid + LHA 2% Cleanser",
        "https://beminimalist.co/products/salicylic-lha-2-cleanser"
    ),

    (
        "2% Niacinamide Gentle Dry Skin Cleanser",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist and Clinical Study Investigators",
        "The cleanser underwent Primary Skin Irritation Testing on human "
        "subjects. The published certificate states that it was found "
        "dermatologically safe and non-irritant under direct dermatologist "
        "supervision.",
        "The Derma Co - Dermatological Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-2-niacinamide-gentle-skin-cleanser-patch-test-certificate"
    ),

    (
        "2% Niacinamide Oily Skin Cleanser",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist & Clinical Study Investigators",
        "The cleanser underwent Primary Skin Irritation Testing on human "
        "subjects under direct dermatologist supervision and was certified "
        "Dermatologically Safe for use and Non-Irritant.",
        "The Derma Co - Dermatological Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-2-niacinamide-oily-skin-cleanser-patch-test-certificate"
    ),

    (
        "Refreshing Facial Wash",
        "Dermatologically Tested",
        "Simple Skincare Clinical Product Evidence",
        "Simple states that Refreshing Facial Wash is dermatologically "
        "tested, hypoallergenic and non-comedogenic, and suitable for all "
        "skin types including sensitive skin.",
        "Simple - Refreshing Facial Wash",
        "https://www.simpleskincare.in/products/simple-kind-to-skin-refreshing-facial-wash-150ml"
    ),

    (
        "2% Sali-Cinamide Anti-Acne Face Wash",
        "Dermatologist Approved",
        "The Derma Co Official Dermatology Evidence",
        "The Derma Co states that this product is dermatologist-approved. "
        "It is formulated with 2% Salicylic Acid and 2% Niacinamide for "
        "acne-prone, oily and combination skin, helping control excess oil, "
        "unclog pores and reduce breakouts.",
        "The Derma Co - 2% Sali-Cinamide Anti-Acne Face Wash",
        "https://thedermaco.com/products/2-sali-cinamide-anti-acne-face-wash-with-2-salicylic-acid-2-niacinamide-200ml"
    ),

    (
        "Watermelon SuperGlow Facial Gel Cleanser",
        "Clinical & Dermatology Evidence",
        "Dot & Key Official Evidence",
        "Dot & Key reports clinically proven results for this cleanser. "
        "Its official product information describes a self-assessment "
        "study involving 36 subjects with oily skin, where 96% agreed "
        "that their skin appeared less oily from the first use. Dot & Key "
        "also includes this cleanser in its official guide to "
        "dermatologist-recommended face washes.",
        "Dot & Key - Watermelon SuperGlow Facial Gel Cleanser",
        "https://www.dotandkey.com/products/watermelon-vitamin-c-face-wash-gel-1"
    ),
]


# ==========================================================
# 2. MOISTURIZER
# ==========================================================

moisturizer_recommendations = [

    (
        "PM Facial Moisturizing Lotion",
        "Dr. Heather Woolery-Lloyd, MD",
        "Board-Certified Dermatologist",
        "Dr. Heather Woolery-Lloyd specifically recommends CeraVe PM for "
        "oily, acne-prone patients and describes it as a lightweight "
        "moisturizer.",
        "CeraVe - Dr. Heather Woolery-Lloyd",
        "https://www.cerave.com/authors/heather-woolery-lloyd"
    ),

    (
        "Barrier Repair Moisturizer",
        "Dr. Nirupama Parwanda",
        "Dermatologist",
        "Dr. Nirupama Parwanda discusses and rates Dot & Key Barrier "
        "Repair Moisturizer in her dermatologist review of popular "
        "moisturizers. Dot & Key also reports clinical testing showing "
        "improvement in skin barrier and moisturization.",
        "Ask Dr Nirupama - Moisturiser Rating by a Dermatologist",
        "https://www.youtube.com/watch?v=u1ayFr6q3k0"
    ),

    (
        "Moisturising Cream",
        "Dermatologist Tested",
        "Cetaphil Clinical Evidence",
        "Cetaphil states that this moisturizer is dermatologist tested "
        "and clinically proven to be gentle on sensitive skin. It uses "
        "a dermatologist-backed blend of niacinamide, panthenol and "
        "glycerin.",
        "Cetaphil India - Moisturising Cream",
        "https://www.cetaphil.in/moisturizers/moisturising-cream/8906005273436.html"
    ),

    (
        "The Derma Co. 5% Nia-Ceramide Mattifying Moisturizer",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Consultant Dermatologist & Principal Investigator",
        "The moisturizer underwent Primary Skin Irritation Testing on "
        "human subjects under dermatologist supervision. The published "
        "certificate found the product dermatologically safe for use "
        "and non-irritant.",
        "The Derma Co - Dermatological Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-5-nia-ceramide-daily-hydrating-moisturizer-patch-test-certificate"
    ),

    (
        "Hydro Boost Water Gel",
        "Dr. Daniel Sugai",
        "Board-Certified Dermatologist",
        "Dr. Daniel Sugai specifically reviews and compares Neutrogena "
        "Hydro Boost Water Gel in his dermatologist skincare review.",
        "Dr. Daniel Sugai - Hydro Boost Water Gel Review",
        "https://www.youtube.com/watch?v=R3uKkMMM5VU"
    ),

    (
        "The Derma Co Ceramide + HA Intense Moisturizer Cream With Hyaluronic Acid",
        "Designed by Dermatologists",
        "The Derma Co Official Dermatology Evidence",
        "The Derma Co states that this moisturizer is designed by "
        "dermatologists. It combines ceramides and hyaluronic acid and "
        "is intended for intensive moisturization and supporting the "
        "skin moisture barrier.",
        "The Derma Co - Ceramide + HA Intense Daily Face Moisturizer",
        "https://thedermaco.com/products/ceramide-ha-intense-moisturizer"
    ),

    (
        "Watermelon Cooling Icy Gel Moisturizer",
        "Clinical Product Evidence",
        "Dot & Key Official Product Evidence",
        "Dot & Key identifies this as a lightweight cooling gel "
        "moisturizer for normal, oily and combination skin. The "
        "Watermelon range is presented with clinically proven results "
        "and the moisturizer contains ingredients including niacinamide, "
        "hyaluronic acid and watermelon extract.",
        "Dot & Key - Watermelon Cooling Icy Gel Moisturizer",
        "https://www.dotandkey.com/collections/moisturizers"
    ),

    (
        "Green Tea Mattifying Moisturizer",
        "Divya Agarwal",
        "Author - Plum Official Product Guide",
        "Divya Agarwal authored Plum's official guide specifically about "
        "Green Tea Mattifying Moisturizer. The guide explains how to use "
        "the product and discusses its suitability for combination, oily "
        "and acne-prone skin.",
        "Plum - How to Use Green Tea Mattifying Moisturizer",
        "https://plumgoodness.com/blogs/how-to-use/how-to-use-green-tea-mattifying-moisturizer"
    ),
]


# ==========================================================
# 3. SERUM
# ==========================================================

serum_recommendations = [

    (
        "10% Glycolic Acid Face Serum",
        "Dr. Charu Sharma",
        "Head of Dermatology, CureSkin",
        "The ingredient profile and suitability of Dot & Key Watermelon "
        "& 10% Glycolic Serum were medically reviewed by Dr. Charu Sharma. "
        "The review evaluates key actives including glycolic acid, kojic "
        "acid, gluconolactone and allantoin.",
        "CureSkin - Watermelon & 10% Glycolic Serum",
        "https://cureskin.com/indianskincaredecoder/p/dotandkey-watermelon-10-glycolic-super-glow-serum-for-smooth-luminous-"
    ),

    (
        "Strawberry Bright Face Serum",
        "Dr. Charu Sharma",
        "Head of Dermatology, CureSkin",
        "The ingredients and suitability of Strawberry Bright 10% "
        "Niacinamide Face Serum were medically reviewed by Dr. Charu "
        "Sharma. The formula includes key ingredients such as 10% "
        "niacinamide, Vitamin B12, strawberry extract and hyaluronic acid.",
        "CureSkin - Strawberry Bright 10% Niacinamide Face Serum",
        "https://cureskin.com/indianskincaredecoder/p/dotandkey-10-niacinamide-strawberry-brightening-face-serum"
    ),

    (
        "10% Niacinamide Face Serum",
        "Dermatologist Supervised",
        "Minimalist Safety Testing",
        "Minimalist states that this serum was evaluated for safety "
        "through patch testing under the supervision of a dermatologist. "
        "The formula includes 10% niacinamide along with ingredients "
        "intended for oil balance and blemish-prone skin.",
        "Minimalist - Niacinamide 10% Face Serum",
        "https://beminimalist.co/products/niacinamide-10-with-matmarine"
    ),

    (
        "Salicylic Acid 2% Face Serum",
        "Dermatologist Supervised",
        "Minimalist Safety Testing",
        "Minimalist states that this serum was evaluated for safety "
        "through patch testing under the supervision of a dermatologist. "
        "Its 2% salicylic acid formulation is intended for concerns "
        "including acne, excess oil and blackheads.",
        "Minimalist - Salicylic Acid 2% Face Serum",
        "https://beminimalist.co/products/salicylic-acid-2"
    ),

    (
        "5% Niacinamide Face Serum",
        "Official Product Information",
        "Plum 5% Niacinamide & Rice Water Serum",
        "Plum identifies 5% niacinamide, rice water and an amino acid "
        "complex as key components of this beginner-friendly serum. "
        "The formula is intended to brighten skin, improve texture "
        "and support hydration.",
        "Plum - 5% Niacinamide & Rice Water Brightening Face Serum",
        "https://plumgoodness.com/products/niacinamide-face-serum-with-rice-water-amino-acid-vegan-30-ml"
    ),

    (
        "Niacinamide Face Serum with Rice Water",
        "Dr. Charu Sharma",
        "Head of Dermatology, CureSkin",
        "The listed ingredients and suitability of Plum 10% Niacinamide "
        "Face Serum with Rice Water were medically reviewed by "
        "Dr. Charu Sharma as part of CureSkin's ingredient analysis.",
        "CureSkin - Plum 10% Niacinamide Face Serum With Rice Water",
        "https://cureskin.com/indianskincaredecoder/p/tirabeauty-product-plum-10-niacinamide-face-serum-with-rice-water-clarity-b"
    ),

    (
        "10% Vitamin C Face Serum",
        "Dermatologically Tested",
        "The Derma Co Safety & Laboratory Testing",
        "The Derma Co publishes independent testing information for "
        "its 10% Vitamin C serum. The formulation contains 10% Vitamin C, "
        "5% niacinamide and hyaluronic acid, and the brand reports "
        "separate dermatological patch testing for skin tolerance.",
        "The Derma Co - 10% Vitamin C Face Serum",
        "https://thedermaco.com/products/10-vitamin-c-face-serum-with-niacinamide-hyaluronic-acid-for-skin-radiance-30ml"
    ),

    (
        "15% Vitamin C Face Serum",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist & Clinical Study Investigators",
        "The serum underwent Primary Skin Irritation Testing on human "
        "subjects under direct dermatologist supervision. The published "
        "certificate records the product as Dermatologically Safe for "
        "use and Non-Irritant.",
        "The Derma Co - 15% Vitamin C Face Serum Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-15-vitamin-c-face-serum-patch-test-certificate"
    ),

    (
        "2% Salicylic Acid Face Serum",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist & Clinical Study Investigators",
        "The serum underwent Primary Skin Irritation Testing on human "
        "subjects under direct dermatologist supervision. The published "
        "certificate records the product as Dermatologically Safe for "
        "use and Non-Irritant.",
        "The Derma Co - 2% Salicylic Acid Face Serum Patch Test Certificate",
        "https://thedermaco.com/pages/the-derma-co-2-salicylic-acid-face-serum-patch-test-certificate"
    ),

    (
        "10% Niacinamide + Zinc",
        "Dr. Jayashree Ramana",
        "Doctor & Skincare Reviewer",
        "Dr. Jayashree Ramana reviewed the Minimalist 10% Niacinamide "
        "+ Zinc serum and discussed the formulation and its use in "
        "skincare, particularly for concerns associated with oily "
        "and acne-prone skin.",
        "Minimalist 10% Niacinamide + Zinc Review - Dr. Jayashree Ramana",
        "https://www.youtube.com/watch?v=yLtGt3tM_K4"
    ),

    (
        "Hyaluronic Acid Serum",
        "Dr. Lisa Park",
        "Contributing Dermatologist",
        "Dr. Lisa Park reviewed The Ordinary Hyaluronic Acid 2% + B5 "
        "and identified it as a useful affordable hydrating serum, "
        "particularly for dry and dehydrated skin. The formula uses "
        "hyaluronic acid with vitamin B5 to support skin hydration.",
        "The Ordinary Hyaluronic Acid 2% + B5 Review",
        "https://www.insiderbeauty.com/reviews/the-ordinary/the-ordinary-hyaluronic-acid-2-b5"
    ),
]


# ==========================================================
# 4. SUNSCREEN
# ==========================================================

sunscreen_recommendations = [

    (
        "Ultra Sheer SPF 50+",
        "Official Product Information",
        "Neutrogena Sun Protection Information",
        "Neutrogena identifies Ultra Sheer Dry Touch Sunscreen as "
        "SPF 50+ PA++++ with broad UVA/UVB protection. The official "
        "product information describes it as suitable for sensitive, "
        "oily and acne-prone skin.",
        "Neutrogena - Ultra Sheer Dry Touch Sunscreen SPF 50+",
        "https://www.neutrogena.in/sun/ultra-sheer-sunscreen"
    ),

    (
        "Barrier Repair Sunscreen SPF 50+",
        "Independent SPF Testing",
        "Dot & Key In-Vivo Sunscreen Testing",
        "Dot & Key reports independent third-party in-vivo SPF testing "
        "for this sunscreen under international testing standards. "
        "The reported in-vivo SPF value is 51.62 with broad-spectrum "
        "protection.",
        "Dot & Key - Barrier Repair Sunscreen",
        "https://www.dotandkey.com/products/barrier-repair-sunscreen"
    ),

    (
        "Cica Calming Niacinamide Sunscreen",
        "Independent SPF Testing",
        "Dot & Key In-Vivo Sunscreen Testing",
        "Dot & Key reports independent third-party in-vivo SPF testing "
        "for its Cica + Niacinamide sunscreen. Testing reported an "
        "in-vivo SPF value of 51.54, PA++++ and broad-spectrum protection.",
        "Dot & Key - Cica + Niacinamide Sunscreen",
        "https://www.dotandkey.com/products/cica-calming-mattifying-sunscreen-spf-50-pa"
    ),

    (
        "Rice Water Sheer Tinted Sunscreen",
        "Independent Consumer Study",
        "Plum Clinical Results",
        "Plum reports an independent expert-graded consumer study for "
        "its Niacinamide & Rice Water Sheer-Tinted Sunscreen. The "
        "official product information also identifies it as SPF 50 "
        "PA++++ with broad-spectrum UVA and UVB protection.",
        "Plum - Niacinamide & Rice Water Sheer-Tinted Sunscreen",
        "https://plumgoodness.com/products/rice-water-3-niacinamide-sheer-tinted-sunscreen"
    ),

    (
        "1% Hyaluronic Sunscreen Aqua Gel SPF 50",
        "Dr. Bhagirath Patel, M.D., DVL & Dr. Parth Joshi",
        "Dermatologist & Clinical Study Investigators",
        "The sunscreen underwent Primary Skin Irritation Testing on "
        "human subjects under direct dermatologist supervision and "
        "was certified Dermatologically Safe for use and Non-Irritant. "
        "Separate standardized sunscreen efficacy testing reported "
        "in-vivo SPF 50.169 and PA++++.",
        "The Derma Co - 1% Hyaluronic Sunscreen Aqua Gel Testing",
        "https://thedermaco.com/pages/the-derma-co-1-hyaluronic-sunscreen-aqua-gel-patch-test-certificate"
    ),

    (
        "Watermelon Cooling Sunscreen SPF 50+",
        "Independent SPF Testing",
        "Dot & Key In-Vivo Sunscreen Testing",
        "Dot & Key reports independent third-party testing under "
        "international SPF testing standards. The Watermelon Cooling "
        "Sunscreen achieved an in-vivo SPF value of 63 with PA++++ "
        "and broad-spectrum protection.",
        "Dot & Key - Watermelon Cooling Sunscreen SPF 50+",
        "https://www.dotandkey.com/products/watermelon-cooling-spf-50-face-sunscreen"
    ),

    (
        "Moisturizing Sunscreen",
        "Official Product Information",
        "Cetaphil Sensitive Skin Sun Protection",
        "Cetaphil describes its SPF 50+ sunscreen as providing high "
        "UV protection with a lightweight formulation suitable for "
        "sensitive skin. The product is described as hypoallergenic, "
        "non-comedogenic and fragrance-free.",
        "Cetaphil - SPF 50+ Sunscreen",
        "https://www.cetaphil.in/sunscreens/cetaphil-spf-50%2B-sunscreen/3499320013192.html"
    ),

    (
        "SPF 50 Sunscreen",
        "In Vivo SPF Testing",
        "Fixderma Sunscreen Testing",
        "Fixderma identifies Shadow SPF 50+ Gel as an in-vivo tested "
        "broad-spectrum sunscreen. The formulation is designed to "
        "provide UVA and UVB protection and is intended for oily, "
        "acne-prone and sensitive skin.",
        "Fixderma - Shadow SPF 50+ Gel",
        "https://www.fixderma.com/products/shadow-sunscreen-for-oily-skin-spf-50-gel"
    ),
]


# ==========================================================
# 5. TONER
# ==========================================================

toner_recommendations = [

    (
        "Cerasense Milky Toner",
        "Independent Clinical Testing",
        "Clinically Tested Formula",
        "The CeraSense Milky Toner was clinically tested at independent, "
        "expert-graded labs. Testing reported support for skin barrier "
        "health and 72-hour moisturization.",
        "Plum - CeraSense Milky Toner",
        "https://plumgoodness.com/products/plum-cerasense-milky-toner-with-acai-1-nmf"
    ),

    (
        "Daily Niacinamide Toner",
        "Dermatologically Tested",
        "Niacinamide & Rice Water Toner",
        "The Plum niacinamide and rice water toner range is described "
        "as dermat-tested and alcohol-free, with niacinamide used for "
        "pore appearance, uneven tone and skin texture.",
        "Plum - 3% Niacinamide & Rice Water Toner",
        "https://plumgoodness.com/products/3-niacinamide-rice-water-toner-for-bright-skin80ml"
    ),

    (
        "PHA Face Toner",
        "Dermatologist-Supervised Testing",
        "Safety Patch Tested",
        "Minimalist states that the Polyhydroxy Acid 3% Face Toner was "
        "evaluated for safety through patch testing under the supervision "
        "of a dermatologist.",
        "Minimalist - Polyhydroxy Acid (PHA) 3% Face Toner",
        "https://beminimalist.co/products/pha-3-biotic-toner"
    ),

    (
        "Daily Hydrating Toner",
        "Ingredient & Formulation Information",
        "Bulgarian Valley Rose Water Toner",
        "The formula contains hydrating and soothing ingredients including "
        "rose water and hyaluronic acid and is designed to support skin "
        "hydration.",
        "Plum - Bulgarian Valley Rose Water Toner",
        "https://plumgoodness.com/products/bulgarian-valley-rose-water-toner-150-ml"
    ),

    (
        "Niacinamide Face Toner",
        "Dermatologically Tested",
        "3% Niacinamide & Rice Water Toner",
        "Plum identifies its 3% Niacinamide & Rice Water Toner as "
        "dermat-tested. The formula is designed to refine the appearance "
        "of pores, brighten skin and improve skin texture.",
        "Plum - 3% Niacinamide & Rice Water Toner",
        "https://plumgoodness.com/products/plum-niacinamide-toner-with-rice-water"
    ),

    (
        "Rice Water Probiotics Toner",
        "Ingredient & Formulation Information",
        "Blueberry Hydrate Barrier Repair Rice Water Toner",
        "Dot & Key describes this toner as a hydrating barrier-support "
        "formula containing probiotics and rice water. Probiotics are "
        "included to support the skin microbiome and barrier, while rice "
        "water is included for its soothing properties.",
        "Dot & Key - Blueberry Hydrate Barrier Repair Rice Water Toner",
        "https://www.dotandkey.com/products/rice-water-probiotics-hydrating-toner-alcohol-free-new"
    ),

    (
        "Watermelon SuperGlow Pore Tightening Toner",
        "Product Testing",
        "Self-Assessment Study",
        "Dot & Key reports product testing based on a self-assessment "
        "study. The toner is designed to help manage excess oil and "
        "improve the appearance of pores.",
        "Dot & Key - Watermelon SuperGlow Pore Tightening Toner",
        "https://www.dotandkey.com/products/watermelon-superglow-pore-tightening-toner"
    ),
]


# ==========================================================
# INSERT ALL RECOMMENDATIONS
# ==========================================================

categories = [
    ("FACE WASH", face_wash_recommendations),
    ("MOISTURIZER", moisturizer_recommendations),
    ("SERUM", serum_recommendations),
    ("SUNSCREEN", sunscreen_recommendations),
    ("TONER", toner_recommendations),
]


for category_name, recommendations in categories:

    print(f"\n--- {category_name} ---")

    for recommendation in recommendations:

        add_recommendation(*recommendation)


# ==========================================================
# REMOVE ANY OLD DUPLICATES ALREADY IN DATABASE
# ==========================================================

cursor.execute("""
    DELETE FROM product_recommendations
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM product_recommendations
        GROUP BY product_id, recommender_name
    )
""")


# ==========================================================
# SAVE AND CLOSE
# ==========================================================

conn.commit()
conn.close()

print("\nRecommendations added successfully.")