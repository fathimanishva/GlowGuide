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

app.secret_key = "glowguide_secret_key"

def get_db_connection():
    conn = sqlite3.connect("glowguide.db")
    conn.row_factory = sqlite3.Row
    return conn

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

        if user and check_password_hash(user["password"], password):

            session["user"] = user["fullname"]
            session["user_email"] = user["email"]

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

    skin_type = session.get("questionnaire_skin_type")
    sensitivity = session.get(
        "questionnaire_sensitivity",
        "not_sensitive"
    )

    if not skin_type:
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    # --------------------------------
    # Get products matching skin type
    # --------------------------------

    cursor.execute("""
        SELECT *
        FROM products
        WHERE ',' || LOWER(REPLACE(skin_types, ' ', '')) || ','
        LIKE ?
    """, (f"%,{skin_type.lower()},%",))

    all_products = cursor.fetchall()

    conn.close()

    # --------------------------------
    # Filter according to sensitivity
    # --------------------------------

    suitable_products = []

    for product in all_products:

        # Convert database value into a clean list
        product_sensitivity = [
            value.strip().lower()
            for value in product["sensitivity"].split(",")
        ]

        # Sensitive users
        if sensitivity == "sensitive":

            if (
                "sensitive" in product_sensitivity
                or "somewhat_sensitive" in product_sensitivity
            ):
                suitable_products.append(product)

        # Somewhat sensitive users
        elif sensitivity == "somewhat_sensitive":

            if (
                "sensitive" in product_sensitivity
                or "somewhat_sensitive" in product_sensitivity
                or "not_sensitive" in product_sensitivity
            ):
                suitable_products.append(product)

        # Non-sensitive users
        else:

            suitable_products.append(product)

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
            product
            for product in suitable_products
            if product["category"].strip().lower() == category.lower()
        ]

        # Sort products by price
        category_products.sort(
            key=lambda product: product["price"]
        )

        # Only add categories that have products
        if category_products:
            categorized_products[category] = category_products

    # --------------------------------
    # Count recommendations
    # --------------------------------

    total_products = len(suitable_products)

    return render_template(
        "recommendations.html",
        categorized_products=categorized_products,
        skin_type=skin_type,
        sensitivity=sensitivity,
        total_products=total_products
    )
@app.route("/logout")
def logout():
    session.pop("user", None)
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

        return "Registration Successful!"

    return render_template("register.html")     

if __name__ == '__main__':
    app.run(debug=True)