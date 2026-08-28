from flask import Flask, render_template, request, redirect, session,url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from ai.skin_analyzer import analyze_skin
from dotenv import load_dotenv
import smtplib
import secrets
load_dotenv()

app = Flask(__name__)
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = os.getenv(
    "SECRET_KEY",
    "glowguide_secret_key"
)
def get_db_connection():
    conn = sqlite3.connect("glowguide.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_suitable_products(skin_type, sensitivity=None, concerns=None, source="ai"):

    if concerns is None:
        concerns = []

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM products
        WHERE ',' || LOWER(REPLACE(skin_types, ' ', '')) || ','
        LIKE ?
    """, (f"%,{skin_type.lower()},%",))

    all_products = cursor.fetchall()

    conn.close()

    suitable_products = []

    for product in all_products:

        product_sensitivity = [
            value.strip().lower()
            for value in product["sensitivity"].split(",")
        ]

        # AI recommendation
        if source == "ai":
            suitable_products.append(product)

        # Questionnaire recommendation
        elif sensitivity == "sensitive":

            if (
                "sensitive" in product_sensitivity
                or "somewhat_sensitive" in product_sensitivity
            ):
                suitable_products.append(product)

        elif sensitivity == "somewhat_sensitive":

            if (
                "sensitive" in product_sensitivity
                or "somewhat_sensitive" in product_sensitivity
            ):
                suitable_products.append(product)

        else:
            suitable_products.append(product)

    # --------------------------------
    # Concern score
    # --------------------------------

    scored_products = []

    for product in suitable_products:

        match_score = 0

        if source == "questionnaire" and product["concerns"]:

            product_concerns = [
                value.strip().lower()
                for value in product["concerns"].split(",")
            ]

            for concern in concerns:

                if concern.lower() in product_concerns:
                    match_score += 1

        scored_products.append(
            (product, match_score)
        )

    return scored_products

def send_otp_email(receiver_email, otp):

    subject = "GlowGuide - Password Reset OTP"

    message = f"""Subject: {subject}

Your GlowGuide password reset OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request a password reset, please ignore this email.
"""

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                MAIL_USERNAME,
                MAIL_PASSWORD
            )

            server.sendmail(
                MAIL_USERNAME,
                receiver_email,
                message
            )

        return True

    except Exception as e:

        print("Email sending error:", e)

        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            # Store user details in session
            session["user"] = user["fullname"]
            session["user_email"] = user["email"]
            session["role"] = user["role"]

            # Admin login
            if user["role"] == "admin":
                return redirect("/admin/dashboard")

            # Normal user login
            return redirect("/dashboard")

        else:
            error = "Incorrect email or password."

    return render_template(
        "login.html",
        error=error
    )

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    error = None
    success = None

    if request.method == "POST":

        email = request.form["email"].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if not user:

            error = "No account found with this email."

            return render_template(
                "forgot_password.html",
                error=error
            )

        # Generate 6-digit OTP
        otp = str(secrets.randbelow(900000) + 100000)

        # Store OTP temporarily in session
        session["reset_email"] = email
        session["reset_otp"] = otp

        # OTP expiry time
        import time
        session["reset_otp_expiry"] = time.time() + 300

        # Send OTP
        email_sent = send_otp_email(
            email,
            otp
        )

        if not email_sent:

            session.pop("reset_email", None)
            session.pop("reset_otp", None)
            session.pop("reset_otp_expiry", None)

            error = "Unable to send verification email. Please try again."

            return render_template(
                "forgot_password.html",
                error=error
            )

        return redirect(
            url_for("verify_otp")
        )

    return render_template(
        "forgot_password.html",
        error=error,
        success=success
    )

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if "reset_email" not in session:
        return redirect("/forgot-password")

    error = None

    if request.method == "POST":

        entered_otp = request.form["otp"].strip()

        stored_otp = session.get("reset_otp")
        expiry = session.get("reset_otp_expiry")

        # Check OTP expiry
        import time

        if not expiry or time.time() > expiry:

            error = "OTP has expired. Please request a new OTP."

            return render_template(
                "verify_otp.html",
                error=error
            )

        # Check OTP
        if entered_otp != stored_otp:

            error = "Incorrect OTP. Please try again."

            return render_template(
                "verify_otp.html",
                error=error
            )

        # OTP is correct
        session["otp_verified"] = True

        # Remove OTP after successful verification
        session.pop("reset_otp", None)
        session.pop("reset_otp_expiry", None)

        return redirect(
            url_for("reset_password")
        )

    return render_template(
        "verify_otp.html",
        error=error
    )

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "reset_email" not in session:
        return redirect("/forgot-password")

    if not session.get("otp_verified"):
        return redirect("/verify-otp")

    error = None

    if request.method == "POST":

        new_password = request.form["password"]

        if len(new_password) < 6:

            error = "Password must be at least 6 characters."

            return render_template(
                "reset_password.html",
                error=error
            )

        hashed_password = generate_password_hash(
            new_password
        )

        email = session["reset_email"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE email = ?
        """, (
            hashed_password,
            email
        ))

        conn.commit()
        conn.close()

        # Clear password reset session data
        session.pop("reset_email", None)
        session.pop("otp_verified", None)

        return redirect("/login")

    return render_template(
        "reset_password.html",
        error=error
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user" not in session:
        return redirect("/login")

    image_name = session.get("image_name")
    success = None

    if request.method == "POST":

        file = request.files.get("image")

        if file and file.filename != "":

            filename = secure_filename(file.filename)

            file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )

            # Replace the previous image
            session["image_name"] = filename

            image_name = filename
            success = "Image uploaded successfully!"

    return render_template(
        "upload.html",
        image_name=image_name,
        success=success
    )

@app.route("/analysis")
def analysis():

    if "user" not in session:
        return redirect("/login")

    image_name = session.get("image_name")

    if not image_name:
        return redirect("/upload")

    return render_template(
        "analysis.html",
        image_name=image_name
    )

@app.route("/analyze-skin", methods=["POST"])
def analyze_skin_route():

    if "user" not in session:
        return redirect("/login")

    image_name = session.get("image_name")

    if not image_name:
        return redirect("/upload")

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_name
    )

    # Run AI analysis
    results = analyze_skin(image_path)

    # Find the result with the highest confidence
    best_result = max(results, key=lambda x: x["score"])

    skin_type = best_result["label"].lower()

    # Store AI detected skin type for product recommendations
    session["ai_skin_type"] = skin_type
    session["recommendation_source"] = "ai"

    # Save AI analysis to history
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analysis_history
    (user_email, method, skin_type, confidence, image_name)
    VALUES (?, ?, ?, ?, ?)
    """, (
    session["user_email"],
    "AI Image",
    skin_type,
    best_result["score"],
    image_name
    ))

    conn.commit()
    conn.close()

    # Recommendations based on skin type
    recommendations = {
        "dry": [
            "Use a gentle, hydrating cleanser.",
            "Apply a moisturizer regularly.",
            "Avoid very hot water and harsh cleansers.",
            "Use sunscreen during the daytime."
        ],

        "oily": [
            "Use a gentle cleanser suitable for oily skin.",
            "Choose lightweight, non-comedogenic moisturizers.",
            "Avoid excessive washing, which can irritate the skin.",
            "Use sunscreen during the daytime."
        ],

        "normal": [
            "Use a gentle cleanser.",
            "Keep your skin moisturized.",
            "Use sunscreen during the daytime.",
            "Maintain a consistent skincare routine."
        ]
    }

    selected_recommendations = recommendations.get(
        skin_type,
        []
    )

    return render_template(
        "results.html",
        image_name=image_name,
        results=results,
        skin_type=skin_type,
        recommendations=selected_recommendations
    )
@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        # Get answers
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")

        q5 = request.form.get("q5")
        q6 = request.form.get("q6")
        q7 = request.form.get("q7")

        # Skin concern answers
        q8 = request.form.get("q8")
        q9 = request.form.get("q9")
        q10 = request.form.get("q10")


        # -----------------------------
        # Skin type scoring
        # -----------------------------

        scores = {
            "dry": 0,
            "oily": 0,
            "normal": 0,
            "combination": 0
        }

        for answer in [q1, q2, q3, q4]:

            if answer in scores:
                scores[answer] += 1


        # Find highest skin-type score
        skin_type = max(scores, key=scores.get)


        # -----------------------------
        # Sensitivity scoring
        # -----------------------------

        sensitivity_scores = {
            "not_sensitive": 0,
            "somewhat_sensitive": 0,
            "sensitive": 0
        }

        for answer in [q5, q6, q7]:

            if answer in sensitivity_scores:
                sensitivity_scores[answer] += 1


        # Find highest sensitivity score
        sensitivity = max(
            sensitivity_scores,
            key=sensitivity_scores.get
        )

        # -----------------------------
        # Skin concerns
        # -----------------------------

        concerns = []

        for answer in [q8, q9, q10]:
            if answer and answer not in concerns:
                concerns.append(answer)


        # -----------------------------
        # Recommendations
        # -----------------------------

        recommendations = {

            "dry": [
                "Use a gentle, hydrating cleanser.",
                "Apply moisturizer regularly.",
                "Avoid very hot water and harsh cleansers.",
                "Use sunscreen during the daytime."
            ],

            "oily": [
                "Use a gentle cleanser suitable for oily skin.",
                "Choose a lightweight, non-comedogenic moisturizer.",
                "Avoid excessive washing.",
                "Use sunscreen during the daytime."
            ],

            "normal": [
                "Use a gentle cleanser.",
                "Keep your skin moisturized.",
                "Use sunscreen during the daytime.",
                "Maintain a consistent skincare routine."
            ],

            "combination": [
                "Use a gentle cleanser suitable for combination skin.",
                "Use a lightweight moisturizer.",
                "Give extra attention to oily areas such as the T-zone.",
                "Avoid harsh products that can dry out other areas.",
                "Use sunscreen during the daytime."
            ]
        }


        selected_recommendations = recommendations.get(
            skin_type,
            []
        )


        # -----------------------------
        # Additional sensitive-skin advice
        # -----------------------------

        if sensitivity == "sensitive":

            selected_recommendations.extend([
                "Choose fragrance-free skincare products.",
                "Avoid harsh scrubs and irritating ingredients.",
                "Introduce new skincare products gradually."
            ])

        elif sensitivity == "somewhat_sensitive":

            selected_recommendations.extend([
                "Prefer gentle skincare products.",
                "Patch-test new products when possible."
            ])


        # Save questionnaire result in session
        session["questionnaire_skin_type"] = skin_type
        session["questionnaire_sensitivity"] = sensitivity
        session["questionnaire_concerns"] = concerns
        
        # Mark questionnaire as the current recommendation source
        session["recommendation_source"] = "questionnaire"


        # -----------------------------
        # Save result to history
        # -----------------------------

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO analysis_history
            (user_email, method, skin_type, confidence, image_name)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_email"],
            "Questionnaire",
            skin_type,
            None,
            None
        ))

        conn.commit()
        conn.close()


        # -----------------------------
        # Show result page
        # -----------------------------

        return render_template(
            "questionnaire_result.html",
            skin_type=skin_type,
            sensitivity=sensitivity,
            recommendations=selected_recommendations,
            scores=scores
        )


    return render_template("questionnaire.html")
    
@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analysis_history
        WHERE user_email = ?
        ORDER BY analysis_date DESC
    """, (session["user_email"],))

    history_records = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history_records=history_records
    )

@app.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "user" not in session:
        return redirect("/login")

    error = None
    success = None

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (session["user_email"],)
        )

        user = cursor.fetchone()

        # Check current password
        if not user or not check_password_hash(
            user["password"],
            current_password
        ):
            error = "Current password is incorrect."

        # Check new password length
        elif len(new_password) < 6:
            error = "New password must be at least 6 characters."

        # Check passwords match
        elif new_password != confirm_password:
            error = "New passwords do not match."

        else:

            hashed_password = generate_password_hash(new_password)

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE email = ?
                """,
                (
                    hashed_password,
                    session["user_email"]
                )
            )

            conn.commit()

            success = "Password changed successfully."

        conn.close()

    return render_template(
        "change_password.html",
        error=error,
        success=success
    )

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Total registered users
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role = 'user'
    """)
    total_users = cursor.fetchone()[0]

    # Total products
    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)
    total_products = cursor.fetchone()[0]

    # Total analyses
    cursor.execute("""
        SELECT COUNT(*)
        FROM analysis_history
    """)
    total_analyses = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_products=total_products,
        total_analyses=total_analyses
    )

@app.route("/admin/products")
def admin_products():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM products
        ORDER BY id DESC
    """)

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_products.html",
        products=products
    )

@app.route("/admin/products/add", methods=["GET", "POST"])
def admin_add_product():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    if request.method == "POST":

        name = request.form["name"].strip()
        brand = request.form["brand"].strip()
        category = request.form["category"]
        price = request.form["price"]

        skin_types = request.form.getlist("skin_types")
        sensitivity = request.form.getlist("sensitivity")
        concerns = request.form.getlist("concerns")

        description = request.form.get(
            "description", ""
        ).strip()

        product_link = request.form.get(
            "product_link", ""
        ).strip()

        # Convert checkbox lists to comma-separated strings
        skin_types_string = ",".join(skin_types)
        sensitivity_string = ",".join(sensitivity)
        concerns_string = ",".join(concerns)


        # ----------------------------
        # Product image
        # ----------------------------

        image = request.files.get("image")

        image_path = None

        if image and image.filename:

            filename = secure_filename(
                image.filename
            )

            product_folder = os.path.join(
                app.root_path,
                "static",
                "images",
                "products"
            )

            os.makedirs(
                product_folder,
                exist_ok=True
            )

            image.save(
                os.path.join(
                    product_folder,
                    filename
                )
            )

            image_path = (
                f"images/products/{filename}"
            )


        # ----------------------------
        # Save product
        # ----------------------------

        conn = get_db_connection()
        cursor = conn.cursor()

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
        """, (
            name,
            brand,
            category,
            price,
            skin_types_string,
            sensitivity_string,
            concerns_string,
            description,
            image_path,
            product_link
        ))

        conn.commit()
        conn.close()

        return redirect("/admin/products")


    return render_template(
        "admin_add_product.html"
    )

@app.route("/admin/products/edit/<int:product_id>",
           methods=["GET", "POST"])
def admin_edit_product(product_id):

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get existing product
    cursor.execute("""
        SELECT *
        FROM products
        WHERE id = ?
    """, (product_id,))

    product = cursor.fetchone()

    if not product:
        conn.close()
        return redirect("/admin/products")


    # --------------------------------
    # Update product
    # --------------------------------

    if request.method == "POST":

        name = request.form["name"].strip()
        brand = request.form["brand"].strip()
        category = request.form["category"]
        price = request.form["price"]

        skin_types = request.form.getlist("skin_types")
        sensitivity = request.form.getlist("sensitivity")
        concerns = request.form.getlist("concerns")

        description = request.form.get(
            "description", ""
        ).strip()

        product_link = request.form.get(
            "product_link", ""
        ).strip()

        skin_types_string = ",".join(skin_types)
        sensitivity_string = ",".join(sensitivity)
        concerns_string = ",".join(concerns)


        # --------------------------------
        # Keep existing image by default
        # --------------------------------

        image_path = product["image"]

        new_image = request.files.get("image")

        if new_image and new_image.filename:

            filename = secure_filename(
                new_image.filename
            )

            product_folder = os.path.join(
                app.root_path,
                "static",
                "images",
                "products"
            )

            os.makedirs(
                product_folder,
                exist_ok=True
            )

            new_image.save(
                os.path.join(
                    product_folder,
                    filename
                )
            )

            image_path = (
                f"images/products/{filename}"
            )


        # --------------------------------
        # Update database
        # --------------------------------

        cursor.execute("""
            UPDATE products

            SET
                name = ?,
                brand = ?,
                category = ?,
                price = ?,
                skin_types = ?,
                sensitivity = ?,
                concerns = ?,
                description = ?,
                image = ?,
                product_link = ?

            WHERE id = ?
        """, (
            name,
            brand,
            category,
            price,
            skin_types_string,
            sensitivity_string,
            concerns_string,
            description,
            image_path,
            product_link,
            product_id
        ))

        conn.commit()
        conn.close()

        return redirect("/admin/products")


    conn.close()

    return render_template(
        "admin_edit_product.html",
        product=product
    )

@app.route("/admin/products/delete/<int:product_id>",
           methods=["POST"])
def admin_delete_product(product_id):

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    conn.commit()
    conn.close()

    return redirect("/admin/products")

@app.route("/admin/users")
def admin_users():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE role = 'user'
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_users.html",
        users=users
    )

@app.route("/admin/analyses")
def admin_analyses():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analysis_history
        ORDER BY analysis_date DESC
    """)

    analyses = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_analyses.html",
        analyses=analyses
    )

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get logged-in user's details
    cursor.execute(
        "SELECT fullname, email FROM users WHERE email = ?",
        (session["user_email"],)
    )

    user = cursor.fetchone()

    # Count user's analyses
    cursor.execute(
        "SELECT COUNT(*) FROM analysis_history WHERE user_email = ?",
        (session["user_email"],)
    )

    analysis_count = cursor.fetchone()[0]

    # Get latest analysis
    cursor.execute("""
        SELECT skin_type, method
        FROM analysis_history
        WHERE user_email = ?
        ORDER BY id DESC
        LIMIT 1
    """, (session["user_email"],))

    latest_analysis = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user,
        analysis_count=analysis_count,
        latest_analysis=latest_analysis
    )

@app.route("/recommendations")
def recommendations():

    if "user" not in session:
        return redirect("/login")

    # --------------------------------
    # Check recommendation source
    # --------------------------------

    source = session.get("recommendation_source")

    if source == "ai":

        # AI analysis provides skin type only
        skin_type = session.get("ai_skin_type")
        sensitivity = None
        concerns = []

    elif source == "questionnaire":

        # Questionnaire provides skin type,
        # sensitivity and concerns
        skin_type = session.get(
            "questionnaire_skin_type"
        )

        sensitivity = session.get(
            "questionnaire_sensitivity",
            "not_sensitive"
        )

        concerns = session.get(
            "questionnaire_concerns",
            []
        )

    else:
        return redirect("/dashboard")


    if not skin_type:
        return redirect("/dashboard")


    # --------------------------------
    # Get suitable products
    # --------------------------------

    scored_products = get_suitable_products(
        skin_type,
        sensitivity,
        concerns,
        source
    )


    # --------------------------------
    # Organize products by category
    # --------------------------------

    categories = [
        "Face Wash",
        "Toner",
        "Serum",
        "Moisturizer",
        "Sunscreen"
    ]

    categorized_products = {}


    for category in categories:

        category_products = [
            (product, score)
            for product, score in scored_products
            if product["category"].strip().lower()
            == category.lower()
        ]


        # Questionnaire:
        # Higher concern match first,
        # then lower price.
        #
        # AI:
        # Scores are 0,
        # so products are sorted by price.

        category_products.sort(
            key=lambda item: (
                -item[1],
                item[0]["price"]
            )
        )


        # Remove match score before
        # sending products to template

        category_products = [
            product
            for product, score in category_products
        ]


        if category_products:
            categorized_products[category] = (
                category_products
            )


    # --------------------------------
    # Count recommendations
    # --------------------------------

    total_products = len(scored_products)


    # --------------------------------
    # Save latest recommendations
    # --------------------------------

    # Save products in the same category/ranked
    # order shown on the recommendation page

    product_ids = []

    for category in categories:

        for product in categorized_products.get(
            category,
            []
        ):
            product_ids.append(
                str(product["id"])
            )


    product_ids_string = ",".join(product_ids)
    concerns_string = ",".join(concerns)


    conn = get_db_connection()
    cursor = conn.cursor()


    # Keep only latest saved recommendation
    cursor.execute("""
        DELETE FROM saved_recommendations
        WHERE user_email = ?
    """, (
        session["user_email"],
    ))


    cursor.execute("""
        INSERT INTO saved_recommendations
        (
            user_email,
            source,
            skin_type,
            sensitivity,
            concerns,
            product_ids
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session["user_email"],
        source,
        skin_type,
        sensitivity,
        concerns_string,
        product_ids_string
    ))


    conn.commit()
    conn.close()


    # --------------------------------
    # Show recommendation page
    # --------------------------------

    return render_template(
        "recommendations.html",
        categorized_products=categorized_products,
        skin_type=skin_type,
        sensitivity=sensitivity,
        concerns=concerns,
        total_products=total_products,
        source=source
    )

@app.route("/saved-recommendations")
def saved_recommendations():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM saved_recommendations
        WHERE user_email = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (
        session["user_email"],
    ))

    saved = cursor.fetchone()

    if not saved:
        conn.close()
        return redirect("/dashboard")

    product_ids = []

    if saved["product_ids"]:
        product_ids = [
            int(product_id)
            for product_id in saved["product_ids"].split(",")
        ]

    products = []

    if product_ids:

        placeholders = ",".join(
            ["?"] * len(product_ids)
        )

        cursor.execute(
            f"""
            SELECT *
            FROM products
            WHERE id IN ({placeholders})
            """,
            product_ids
        )

        products = cursor.fetchall()

    conn.close()


    # Organize products by category

    categories = [
        "Face Wash",
        "Toner",
        "Serum",
        "Moisturizer",
        "Sunscreen"
    ]

    categorized_products = {}

    for category in categories:

        category_products = [
            product
            for product in products
            if product["category"].strip().lower()
            == category.lower()
        ]

        if category_products:
            categorized_products[category] = (
                category_products
            )


    return render_template(
        "saved_recommendations.html",
        categorized_products=categorized_products,
        skin_type=saved["skin_type"],
        sensitivity=saved["sensitivity"],
        source=saved["source"]
    )

@app.route("/routine")
def routine():

    if "user" not in session:
        return redirect("/login")

    source = session.get("recommendation_source")

    if source == "ai":

        skin_type = session.get("ai_skin_type")
        sensitivity = None
        concerns = []

    elif source == "questionnaire":

        skin_type = session.get("questionnaire_skin_type")

        sensitivity = session.get(
            "questionnaire_sensitivity",
            "not_sensitive"
        )

        concerns = session.get(
            "questionnaire_concerns",
            []
        )

    else:
        return redirect("/dashboard")

    if not skin_type:
        return redirect("/dashboard")


    # Get suitable products
    scored_products = get_suitable_products(
        skin_type,
        sensitivity,
        concerns,
        source
    )


    # Sort by concern match first,
    # then by lower price
    scored_products.sort(
        key=lambda item: (
            -item[1],
            item[0]["price"]
        )
    )


    # --------------------------------
    # Select one product per category
    # --------------------------------

    selected_products = {}

    categories = [
        "Face Wash",
        "Toner",
        "Serum",
        "Moisturizer",
        "Sunscreen"
    ]

    for category in categories:

        for product, score in scored_products:

            if (
                product["category"].strip().lower()
                == category.lower()
            ):

                selected_products[category] = product
                break


    # --------------------------------
    # Morning routine
    # --------------------------------

    morning_routine = [
        {
            "step": 1,
            "category": "Face Wash",
            "product": selected_products.get("Face Wash"),
            "instruction":
                "Use first to gently cleanse your face, then rinse."
        },
        {
            "step": 2,
            "category": "Toner",
            "product": selected_products.get("Toner"),
            "instruction":
                "Apply after cleansing."
        },
        {
            "step": 3,
            "category": "Serum",
            "product": selected_products.get("Serum"),
            "instruction":
                "Apply after toner and allow it to absorb."
        },
        {
            "step": 4,
            "category": "Moisturizer",
            "product": selected_products.get("Moisturizer"),
            "instruction":
                "Apply after serum to keep your skin moisturized."
        },
        {
            "step": 5,
            "category": "Sunscreen",
            "product": selected_products.get("Sunscreen"),
            "instruction":
                "Use as the final step of your morning routine."
        }
    ]


    # --------------------------------
    # Night routine
    # --------------------------------

    night_routine = [
        {
            "step": 1,
            "category": "Face Wash",
            "product": selected_products.get("Face Wash"),
            "instruction":
                "Cleanse your face gently and rinse."
        },
        {
            "step": 2,
            "category": "Toner",
            "product": selected_products.get("Toner"),
            "instruction":
                "Apply after cleansing."
        },
        {
            "step": 3,
            "category": "Serum",
            "product": selected_products.get("Serum"),
            "instruction":
                "Apply after toner and allow it to absorb."
        },
        {
            "step": 4,
            "category": "Moisturizer",
            "product": selected_products.get("Moisturizer"),
            "instruction":
                "Use as the final step of your night routine."
        }
    ]

    # --------------------------------
    # Save latest routine
    # --------------------------------

    morning_product_ids = [
        str(item["product"]["id"])
        for item in morning_routine
        if item["product"]
    ]

    night_product_ids = [
        str(item["product"]["id"])
        for item in night_routine
        if item["product"]
    ]

    morning_ids_string = ",".join(morning_product_ids)
    night_ids_string = ",".join(night_product_ids)
    concerns_string = ",".join(concerns)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Keep only the latest saved routine
    cursor.execute("""
        DELETE FROM saved_routines
        WHERE user_email = ?
    """, (
        session["user_email"],
    ))

    cursor.execute("""
        INSERT INTO saved_routines
        (
            user_email,
            source,
            skin_type,
            sensitivity,
            concerns,
            morning_product_ids,
            night_product_ids
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session["user_email"],
        source,
        skin_type,
        sensitivity,
        concerns_string,
        morning_ids_string,
        night_ids_string
    ))

    conn.commit()
    conn.close()


    return render_template(
        "routine.html",
        skin_type=skin_type,
        sensitivity=sensitivity,
        source=source,
        morning_routine=morning_routine,
        night_routine=night_routine
    )

@app.route("/saved-routine")
def saved_routine():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get latest saved routine
    cursor.execute("""
        SELECT *
        FROM saved_routines
        WHERE user_email = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (
        session["user_email"],
    ))

    saved = cursor.fetchone()

    if not saved:
        conn.close()
        return redirect("/dashboard")


    # --------------------------------
    # Convert stored IDs into lists
    # --------------------------------

    morning_ids = []

    if saved["morning_product_ids"]:
        morning_ids = [
            int(product_id)
            for product_id
            in saved["morning_product_ids"].split(",")
        ]

    night_ids = []

    if saved["night_product_ids"]:
        night_ids = [
            int(product_id)
            for product_id
            in saved["night_product_ids"].split(",")
        ]


    # --------------------------------
    # Function to get products
    # in the same saved order
    # --------------------------------

    def get_products_by_ids(product_ids):

        if not product_ids:
            return []

        placeholders = ",".join(
            ["?"] * len(product_ids)
        )

        cursor.execute(
            f"""
            SELECT *
            FROM products
            WHERE id IN ({placeholders})
            """,
            product_ids
        )

        products = cursor.fetchall()

        product_map = {
            product["id"]: product
            for product in products
        }

        return [
            product_map[product_id]
            for product_id in product_ids
            if product_id in product_map
        ]


    morning_products = get_products_by_ids(
        morning_ids
    )

    night_products = get_products_by_ids(
        night_ids
    )

    conn.close()


    # --------------------------------
    # Instructions
    # --------------------------------

    instructions = {
        "Face Wash":
            "Use first to gently cleanse your face, then rinse.",

        "Toner":
            "Apply after cleansing.",

        "Serum":
            "Apply after toner and allow it to absorb.",

        "Moisturizer":
            "Apply after serum to keep your skin moisturized.",

        "Sunscreen":
            "Use as the final step of your morning routine."
    }


    # --------------------------------
    # Build morning routine
    # --------------------------------

    morning_routine = []

    for step, product in enumerate(
        morning_products,
        start=1
    ):

        morning_routine.append({
            "step": step,
            "category": product["category"],
            "product": product,
            "instruction": instructions.get(
                product["category"],
                "Use as directed."
            )
        })


    # --------------------------------
    # Build night routine
    # --------------------------------

    night_routine = []

    for step, product in enumerate(
        night_products,
        start=1
    ):

        instruction = instructions.get(
            product["category"],
            "Use as directed."
        )

        if product["category"] == "Moisturizer":
            instruction = (
                "Use as the final step of your night routine."
            )

        night_routine.append({
            "step": step,
            "category": product["category"],
            "product": product,
            "instruction": instruction
        })


    return render_template(
        "saved_routine.html",
        skin_type=saved["skin_type"],
        sensitivity=saved["sensitivity"],
        source=saved["source"],
        morning_routine=morning_routine,
        night_routine=night_routine
    )
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Email already registered!"

        # Insert new user
        cursor.execute(
            "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
            (fullname, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")     

if __name__ == '__main__':
    app.run(debug=True)