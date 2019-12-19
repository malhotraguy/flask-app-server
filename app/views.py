import json
import os
import sys

from flask import request, render_template, redirect, flash, url_for
from flask_cors import CORS

from app import app
from app.xml_operations import get_size, get_mod_date, get_links_count, xml_validate

CORS(app)
XML_UPLOADS = "XML_UPLOADS"
ALLOWED_FILE_EXTENSIONS = "ALLOWED_FILE_EXTENSIONS"
EXCLUDED_DISPLAY_FILES = ["uploader_record.json", "all_files_detail.json"]
app.config[XML_UPLOADS] = "./output"
app.config[ALLOWED_FILE_EXTENSIONS] = [".XML"]


def write_json(filepath, data={}):
    with open(filepath, "w+") as outfile:
        json.dump(data, outfile)


def get_json_data(filepath=f"{app.config[XML_UPLOADS]}/uploader_record.json"):
    if not os.path.isfile(filepath):
        write_json(data={}, filepath=filepath)
    with open(filepath) as file:
        data = json.loads(file.read())
    return data


def allowed_file(filename):
    file_name, file_extension = os.path.splitext(filename)
    if file_extension.upper() in app.config[ALLOWED_FILE_EXTENSIONS]:
        return True
    else:
        return False


def get_file_detail(file_name, ip_data):
    file_detail = [
        get_size(file_path=f"{app.config[XML_UPLOADS]}/{file_name}"),
        f'http://{request.host}{url_for(endpoint="xml_display", file_name=file_name)}',
        get_mod_date(file_path=f"{app.config[XML_UPLOADS]}/{file_name}"),
        get_links_count(file_path=f"{app.config[XML_UPLOADS]}/{file_name}"),
        ip_data.get(file_name),
    ]
    return file_detail


@app.route("/", methods=["GET"])
def homepage():
    return """<h1>Hello Team!.The Server is running good.</h1>"""


@app.route("/xml-file/<file_name>", methods=["GET"])
def xml_display(file_name):
    with open(f"{app.config[XML_UPLOADS]}/{file_name}") as file:
        content = file.read()
    return content


@app.route("/upload-xml", methods=["GET", "POST"])
def upload_xml():
    if request.method == "POST":
        if request.files:
            print(f"request.files={request.files}")
            file = request.files["file"]
            if file.filename == "":
                print("No Filename", file=sys.stderr)
                flash(message="No File Selected", category="error")
                return redirect(location=request.url, code=302)
            if not allowed_file(file.filename):
                flash(message="That file extension is not allowed", category="warning")
                return redirect(location=request.url, code=302)
            if not os.path.isdir(app.config[XML_UPLOADS]):
                os.mkdir(app.config[XML_UPLOADS], mode=0o777)
            ip_visitor = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            uploader_record_data = get_json_data(
                f"{app.config[XML_UPLOADS]}/uploader_record.json"
            )
            uploader_record_data[file.filename] = ip_visitor
            write_json(
                data=uploader_record_data,
                filepath=f"{app.config[XML_UPLOADS]}/uploader_record.json",
            )
            file.save(f"{app.config[XML_UPLOADS]}/{file.filename}")
            xml_validate(f"{app.config[XML_UPLOADS]}/{file.filename}")
            return redirect(location=request.url, code=302)

    elif request.method == "GET":
        return render_template("public/upload_xml.html"), 200


@app.route("/render-pages/")
def render_all_pages():
    """
    This route will render a template.
    If a query string comes into the URL, it will return a parsed
    dictionary of the query string keys & values, using request.args
    """
    if not os.path.isdir(app.config[XML_UPLOADS]):
        return """<h1>There is no output folder. Upload the files</h1>"""
    directory_list = os.listdir(app.config[XML_UPLOADS])
    if len(directory_list) < 0:
        flash(
            message="""<h1>No file is uploaded to output yet</h1>""", category="error",
        )
        return """<h1>No file is uploaded to output yet</h1>"""
    ip_data = get_json_data(f"{app.config[XML_UPLOADS]}/uploader_record.json")
    display_data = {}
    all_files_detail = get_json_data(f"{app.config[XML_UPLOADS]}/all_files_detail.json")
    for file_name in directory_list:
        if file_name in EXCLUDED_DISPLAY_FILES:
            continue
        file_detail = all_files_detail.get(file_name)
        if file_detail is None:
            file_detail = get_file_detail(file_name=file_name, ip_data=ip_data)
            all_files_detail.update({file_name: file_detail})
        display_data.update({file_name: file_detail})
    write_json(
        filepath=f"{app.config[XML_UPLOADS]}/all_files_detail.json",
        data=all_files_detail,
    )
    return render_template("public/index.html", args=display_data)
