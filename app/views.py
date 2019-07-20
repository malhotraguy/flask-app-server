import os


from flask import request, render_template, redirect, abort, flash, url_for
from flask_cors import CORS

from app import app
from app import xml_operations

CORS(app)
app.config['XML_UPLOADS'] = "./output"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["XML"]


def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/", methods=["GET"])
def homepage():
    return """<h1>Hello Team!.The Server is running good.</h1>"""


@app.route("/xml-file/<file_name>", methods=["GET"])
def xml_display(file_name):
    with open(f"{app.config['XML_UPLOADS']}/{file_name}") as file:
        content = file.read()
    return content


@app.route("/upload-xml", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        print("POST done")

        if request.files:
            print(f"request.files={request.files}")
            file = request.files["file"]

            if file.filename == "":
                print("No Filename")
                # return "No Filename", 400
                abort(400)
            if allowed_file(file.filename):

                print(file)
                if not os.path.isdir(app.config['XML_UPLOADS']):
                    os.mkdir(app.config['XML_UPLOADS'], mode=0o777)
                ip_visitor = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                print(f"IP Address of the Visitor:{ip_visitor}")
                file.save(f"{app.config['XML_UPLOADS']}/{file.filename}")
                flash(message="File Uploaded successfully")
                xml_operations.xml_validate(f"{app.config['XML_UPLOADS']}/{file.filename}")
                print(
                    f"size of received  file in Kb=",
                    os.path.getsize(f"{app.config['XML_UPLOADS']}/{file.filename}"),
                )
                return redirect(location=request.url, code=302)
            else:
                print("That file extension is not allowed")
                return "That file extension is not allowed", 400

    elif request.method == "GET":
        print("GET done")

    return render_template("public/upload_xml.html"), 200
    # return '', 200


@app.route("/render-pages/")
def string():
    """
    This route will render a template.
    If a query string comes into the URL, it will return a parsed
    dictionary of the query string keys & values, using request.args
    """
    if os.path.isdir(app.config['XML_UPLOADS']):
        directory_list = os.listdir(app.config['XML_UPLOADS'])
        if len(directory_list) > 0:
            lis_dict = {
                file_name: [xml_operations.get_size(file_path=f"{app.config['XML_UPLOADS']}/{file_name}"),
                            f'http://{request.host}{url_for(endpoint="xml_display", file_name=file_name)}',
                            xml_operations.get_mod_date(file_path=f"{app.config['XML_UPLOADS']}/{file_name}"),
                            xml_operations.get_links_count(file_path=f"{app.config['XML_UPLOADS']}/{file_name}")]
                for file_name in directory_list
            }
            print(lis_dict)
            args = lis_dict

            return render_template("public/index.html", args=args)
        else:
            return """<h1>No file is uploaded to output yet</h1>"""
    else:
        return """<h1>There is no output folder. Upload the files</h1>"""
