from app import app

from flask import request, render_template
from flask_cors import CORS
import os
CORS(app)

@app.route('/')
def homepage():
    return """<h1>Hello world!</h1>"""
@app.route("/xml-file/<file_name>", methods=['GET'])
def xml(file_name):
    with open(f"./output/{file_name}") as file:
        content=file.read()
    return content
@app.route("/upload-image", methods=["GET","POST"])
def upload_image():

    if request.method == "POST":
        print("POST done")
        print(f"request.files={request.files}")

        if request.files:

            file = request.files["file"]

            print(file)
            if not os.path.isdir("./output"):
                os.mkdir("./output", mode=0o777)
            file.save("./output/"+file.filename)

            # return redirect(request.url)
            return '', 200

    elif request.method == "GET":
        print("GET done")


    # return render_template("upload_image.html"),200
    return '', 200

@app.route("/render-pages/")
def index():

    """
    This route will render a template.
    If a query string comes into the URL, it will return a parsed
    dictionary of the query string keys & values, using request.args
    """

    args = None

    if request.args:

        args = request.args

        return render_template("public/index.html", args=args)

    return render_template("public/index.html", args=args)