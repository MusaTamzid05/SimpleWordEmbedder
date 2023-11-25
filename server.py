from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash
from flask import jsonify
from werkzeug.utils import secure_filename

from lib.word_genarator import WordGenerator
from lib.context import context

from datetime import datetime
import os
import threading

app = Flask(__name__)
app.secret_key = "this is the world best secret key"
CORPUS_UPLOAD_DIR = "corpus_data"

class TraningThread(threading.Thread):
    def __init__(self, corpus_name, epoch_count, model_name):
        super().__init__()
        self.corpus_path =  os.path.join(CORPUS_UPLOAD_DIR, corpus_name)
        self.epoch_count = epoch_count
        self.model_name = model_name

    def run(self):
        word_generator = WordGenerator()
        word_generator.init_train(
                corpus_path=self.corpus_path,
                word_count=1000
                )
        word_generator.train(epochs=self.epoch_count, model_name=self.model_name)

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


    corpus_files = os.listdir(CORPUS_UPLOAD_DIR)

    return render_template("home.html", corpus_files=corpus_files)


@app.route("/train", methods=["POST"])
def train():
    #TODO : Error checking
    post_data = request.json

    corpus_name = post_data["corpusName"]
    epoch_count = int(post_data["epochCount"]) 
    model_name = corpus_name + "_" +  str(datetime.now())
    model_name = model_name.replace(" ", "_")

    training_thread = TraningThread(
            model_name=model_name,
            corpus_name=corpus_name,
            epoch_count=epoch_count
            )

    training_thread.run()

    response = {}
    response["message"] = "Success"
    response["model_name"] = model_name

    return jsonify(response)


@app.route("/generate", methods=["GET"])
def generate():
    return render_template("generate.html")


@app.route("/current_model_info", methods=["GET"])
def get_current_info():
    global context
    response = [model_data for model_data in context.model_data]
    return jsonify(response)




    return render_template("generate.html")


