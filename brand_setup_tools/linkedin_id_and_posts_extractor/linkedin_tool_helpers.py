import json
import logging
import os

from linkedin_api import Linkedin  # https://github.com/tomquirk/linkedin-api
from linkedin_api.client import ChallengeException

from brand_setup_tools.linkedin_id_and_posts_extractor.constants import (
    COMPANY_URL_INITIAL,
)

FILE_DIRECTORY = os.path.dirname(__file__)


def get_logger(name):
    """
    Function to initialize the logger
    :param name: Name of the module in which logger has to be initialized
    :return:
    """
    # Gets or creates a logger
    logger = logging.getLogger(name)

    # set log level
    logger.setLevel(logging.DEBUG)

    # define  handler and set formatter
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s-[%(filename)s:%(lineno)d]:%(message)s"
    )
    stream_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(stream_handler)
    return logger


LOGGER = get_logger(__name__)


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
    try:
        LOGGER.debug("Authenticating the Linkedin Client Object using cached cookies")
        linkedin_object = Linkedin(
            username=username, password=password, refresh_cookies=False
        )
    except ChallengeException:
        LOGGER.debug(
            "Authenticating the Linkedin Client Object after refreshing cookies"
        )
        linkedin_object = Linkedin(
            username=username, password=password, refresh_cookies=True
        )

    return linkedin_object
