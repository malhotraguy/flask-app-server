import json
import os
from datetime import datetime

import pandas as pd
from flask import request, render_template, redirect, flash, url_for, abort, send_file
from flask_cors import CORS

from app import app
from app.xml_operations import (
    get_size,
    get_mod_date,
    get_links_count,
    xml_validate,
    get_logger,
)
from brand_setup_tools.linkedin_id_and_posts_extractor.get_posts import (
    get_updates,
    get_post_link_and_social_activity,
    get_url,
)
from brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_engagements import (
    get_engagements,
)
from brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_id import (
    get_linkedin_id,
)
from brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers import (
    get_company_name,
    get_linkedin_object,
)

CORS(app)

FILE_DIRECTORY = os.path.realpath(__file__)
PARENT_DIRECTORY_NAME = os.path.dirname(os.path.dirname(FILE_DIRECTORY))

XML_UPLOADS = "XML_UPLOADS"
ALLOWED_FILE_EXTENSIONS = "ALLOWED_FILE_EXTENSIONS"
EXCLUDED_DISPLAY_FILES = ["uploader_record.json", "all_files_detail.json"]
app.config[XML_UPLOADS] = f"{PARENT_DIRECTORY_NAME}/output"
app.config[ALLOWED_FILE_EXTENSIONS] = [".XML"]
LOGGER = get_logger(__name__)


def write_json(filepath, data={}):
    with open(filepath, "w+") as outfile:
        json.dump(data, outfile, indent=4)


def get_json_data(filepath=f"{app.config[XML_UPLOADS]}/uploader_record.json"):
    if not os.path.isfile(filepath):
        write_json(data={}, filepath=filepath)
    with open(filepath) as file:
        data = json.load(file)
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
    try:
        return send_file(f"{app.config[XML_UPLOADS]}/{file_name}")
    except FileNotFoundError:
        return f"<h1>File: {file_name} not found !!</h1>"


@app.route("/upload-xml", methods=["GET", "POST"])
def upload_xml():
    if request.method == "POST":
        if request.files:
            LOGGER.info(f"request.files={request.files}")
            file = request.files["file"]
            if file.filename == "":
                LOGGER.critical("No Filename")
                flash(message="No File Selected", category="error")
                return redirect(location=request.url, code=302)
            if not allowed_file(file.filename):
                flash(message="That file extension is not allowed", category="warning")
                return redirect(location=request.url, code=302)
            if not os.path.isdir(app.config[XML_UPLOADS]):
                os.mkdir(app.config[XML_UPLOADS], mode=0o777)
            file.save(f"{app.config[XML_UPLOADS]}/{file.filename}")
            xml_file_validated = xml_validate(
                f"{app.config[XML_UPLOADS]}/{file.filename}"
            )
            if xml_file_validated:
                ip_visitor = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
                uploader_record_data = get_json_data(
                    f"{app.config[XML_UPLOADS]}/uploader_record.json"
                )
                uploader_record_data[file.filename] = ip_visitor
                write_json(
                    data=uploader_record_data,
                    filepath=f"{app.config[XML_UPLOADS]}/uploader_record.json",
                )

                all_files_data = get_json_data(
                    f"{app.config[XML_UPLOADS]}/all_files_detail.json"
                )
                all_files_data[file.filename] = get_file_detail(
                    file_name=file.filename, ip_data=uploader_record_data
                )
                write_json(
                    filepath=f"{app.config[XML_UPLOADS]}/all_files_detail.json",
                    data=all_files_data,
                )
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
    number_of_xml_files = len(directory_list) - len(EXCLUDED_DISPLAY_FILES)
    if number_of_xml_files < 0:
        flash(
            message="""<h1>No file is uploaded to output yet</h1>""", category="error"
        )
        return """<h1>No file is uploaded to output yet</h1>"""
    LOGGER.info(f"Total number of xml files: {number_of_xml_files}")
    LOGGER.info("Reading upload_record.json")
    ip_data = get_json_data(f"{app.config[XML_UPLOADS]}/uploader_record.json")
    display_data = {}
    LOGGER.info("Reading all_files_detail.json")
    all_files_detail = get_json_data(f"{app.config[XML_UPLOADS]}/all_files_detail.json")
    for file_name in directory_list:
        if file_name in EXCLUDED_DISPLAY_FILES:
            continue
        file_detail = all_files_detail.get(file_name)
        if file_detail is None:
            LOGGER.info(f"No file detail for file: {file_name}")
            xml_file_validated = xml_validate(
                file_path=f"{app.config[XML_UPLOADS]}/{file_name}"
            )
            if not xml_file_validated:
                LOGGER.info(f"Removed the file: {file_name}")
                continue
            file_detail = get_file_detail(file_name=file_name, ip_data=ip_data)
            all_files_detail.update({file_name: file_detail})
            LOGGER.info(f"Added new detail in all_file_json for file: {file_name}")
        display_data.update({file_name: file_detail})
    write_json(
        filepath=f"{app.config[XML_UPLOADS]}/all_files_detail.json",
        data=all_files_detail,
    )
    return render_template("public/index.html", args=display_data)


@app.route("/linkedin_form")
def linkedin_form():
    return render_template("public/linkedin_form.html"), 200


@app.route("/id", methods=("POST", "GET"))
def id_html_table():
    start_time = datetime.now()
    try:
        linkedin_object = get_linkedin_object()
    except Exception as e:
        return render_template("public/error.html", error=e)
    company_identifier = request.form.get("company")
    company = get_company_name(input_string=company_identifier)
    df_ids = get_linkedin_id(company_name=company, linkedin_object=linkedin_object)
    if df_ids.empty:
        return f"No id fetched for :{company_identifier}"
    LOGGER.debug(f"Time taken to fetch the result= {datetime.now() - start_time}")
    return render_template(
        "public/simple.html",
        page_title=f"IDs for {company}",
        tables=[
            df_ids.to_html(
                classes=["table-bordered", "table-striped", "table-hover"],
                justify="initial",
                render_links=True,
                escape=False,
                float_format="{:,.0f}".format,
            )
        ],
        titles=df_ids.columns.values,
    )


@app.route("/ids_json", methods=("POST", "GET"))
def ids_json_response():
    try:
        linkedin_object = get_linkedin_object()
    except Exception as e:
        return render_template("public/error.html", error=e)
    company_identifier = request.args.get("company")
    company = get_company_name(input_string=company_identifier)
    df_ids = get_linkedin_id(company_name=company, linkedin_object=linkedin_object)
    ids_json = df_ids.to_json(orient="records")
    return ids_json


@app.route("/posts", methods=("POST", "GET"))
def posts_html_table():
    start_time = datetime.now()
    try:
        linkedin_object = get_linkedin_object()
    except Exception as e:
        return render_template("public/error.html", error=e)
    company_identifier = request.form.get("company")
    company = get_company_name(input_string=company_identifier)
    company_updates = get_updates(linkedin_object=linkedin_object, company_name=company)
    if not company_updates:
        return f"No post for :{company_identifier}"
    df_post = pd.DataFrame()
    for update in company_updates:
        linkedin_post_link, total_likes = get_post_link_and_social_activity(item=update)
        shared_url = get_url(item=update)
        df_post = df_post.append(
            {
                "LinkedIn Post Url": linkedin_post_link,
                "Total Likes": total_likes,
                "Shared Url": shared_url,
            },
            ignore_index=True,
        )
    LOGGER.debug(f"Time taken to fetch the result= {datetime.now() - start_time}")
    return render_template(
        "public/simple.html",
        page_title=f"Posts for {company}",
        tables=[
            df_post.to_html(
                classes=["table-bordered", "table-striped", "table-hover"],
                justify="initial",
                render_links=True,
                escape=False,
                float_format="{:,.0f}".format,
            )
        ],
        titles=df_post.columns.values,
    )


@app.route("/compare", methods=("POST", "GET"))
def compare_engagements():
    try:
        linkedin_object = get_linkedin_object()
    except Exception as e:
        return render_template("public/error.html", error=e)
    companies = request.form.get("company").split(",")
    LOGGER.info(companies)
    if type(companies) is not list or len(companies) == 0:
        abort(400, "Check the arguments passed with 'company' parameter of the URL")
    df_engagements = pd.DataFrame()
    for company in companies:
        total_posts, total_likes = get_engagements(linkedin_object, company)
        df_engagements = df_engagements.append(
            {
                "Company": company,
                "Total Posts": total_posts,
                "Total Likes": total_likes,
            },
            ignore_index=True,
        )
    if df_engagements.empty:
        return f"No engagements can be fetched for: {companies}"
    return render_template(
        "public/simple.html",
        page_title=f"Comparing Engagements",
        tables=[
            df_engagements.to_html(
                classes=["table-bordered", "table-striped", "table-hover"],
                justify="initial",
                render_links=True,
                escape=False,
                float_format="{:,.0f}".format,
            )
        ],
        titles=df_engagements.columns.values,
    )
