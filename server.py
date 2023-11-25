from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/generate", methods=["GET"])
def generate():
    return render_template("generate.html")
