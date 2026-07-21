from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello, GlowGuide!</h1><p>Your Flask app is working successfully.</p>"

if __name__ == "__main__":
    app.run(debug=True)