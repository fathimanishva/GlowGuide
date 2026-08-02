from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

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
            session["user"] = user["email"]
            return redirect("/dashboard")

        else:
            return "Invalid Email or Password!"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return f"Welcome {session['user']}!"

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