from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.secret_key = "this is the world best secret key"

CORPUS_UPLOAD_DIR = "corpus_data"
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename.endswith("txt") == False:
            flash("Only txt file are allowed")

        else:
            filename = secure_filename(uploaded_file.filename)
            upload_dir_path = os.path.join(os.getcwd(), CORPUS_UPLOAD_DIR)

            if os.path.isdir(upload_dir_path) == False:
                os.mkdir(upload_dir_path)


            uploaded_file.save(
                    os.path.join(upload_dir_path, filename)
                    )
            flash(f"{filename} uploaded")





        return redirect(url_for("home"))





    return render_template("home.html")


@app.route("/generate", methods=["GET"])
def generate():
    return render_template("generate.html")
