import json
import os

from linkedin_api import Linkedin  # https://github.com/tomquirk/linkedin-api

from brand_setup_tools.linkedin_id_and_posts_extractor.constants import (
    COMPANY_URL_INITIAL,
)

FILE_DIRECTORY = os.path.dirname(__file__)


def get_key(filepath=f"{FILE_DIRECTORY}/credentials.json"):
    if os.path.isfile(filepath):
        credentials = json.load(open(filepath, "r"))
        return credentials["username"], credentials["password"]
    else:
        raise Exception(f"{filepath} doesnt exist")


def get_company_name(input_string):
    if COMPANY_URL_INITIAL in input_string:
        name = input_string.rsplit(COMPANY_URL_INITIAL)
        name = name[1].replace("/", "")
        return name
    return input_string


def get_linkedin_object():
    username, password = get_key()
    # Authenticate using any Linkedin account credentials
    linkedin_object = Linkedin(username=username, password=password)
    return linkedin_object
