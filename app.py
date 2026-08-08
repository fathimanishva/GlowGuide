from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from ai.skin_analyzer import analyze_skin

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = "glowguide_secret_key"

def get_db_connection():
    conn = sqlite3.connect("glowguide.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["fullname"]
            session["user_email"] = user["email"]
            return redirect("/dashboard")

        else:
            return "Invalid Email or Password!"

    return render_template("login.html")

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

        # Get answers from the questionnaire
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")

        scores = {
            "dry": 0,
            "oily": 0,
            "normal": 0,
            "combination": 0
        }

        # Add scores based on answers
        for answer in [q1, q2, q3, q4, q5]:

            if answer in scores:
                scores[answer] += 1

        # Find the highest-scoring skin type
        skin_type = max(scores, key=scores.get)

        # Save questionnaire result in session
        session["questionnaire_skin_type"] = skin_type

        # Save questionnaire result to history
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

        return render_template(
            "questionnaire_result.html",
            skin_type=skin_type,
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

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

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