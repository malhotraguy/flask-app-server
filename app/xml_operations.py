import logging
import os
import sys
import time
from xml.sax import SAXParseException
from xml.sax.handler import ContentHandler

import defusedxml.ElementTree as ET
from defusedxml import defuse_stdlib
from defusedxml.sax import make_parser
from flask import flash

defuse_stdlib()  # Calling defusedxml.defuse_stdlib to patch known xml security vulnerabilities


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


def get_links_count(file_path):
    try:
        tree = ET.parse(file_path)
    except ET.ParseError as pe:
        LOGGER.warning(f"For File:{file_path} Error:{pe}")
        return f"{type(pe).__name__}: {str(pe)}"
    # get root element
    root = tree.getroot()
    return len(root)


def get_size(file_path):
    xml_file_size = os.path.getsize(file_path) / 1000
    return xml_file_size


def get_mod_date(file_path):
    mod_date = time.ctime(os.path.getmtime(file_path))
    return mod_date


def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)


def xml_validate(file_path):
    if os.path.isfile(file_path):
        try:
            parsefile(file_path)
            flash(message="File Uploaded successfully", category="info")
            return True
        except SAXParseException as e:
            flash(message=f"File removed because : {str(e)}", category="error")
            os.remove(file_path)
            return False
    else:
        LOGGER.warning(f"{file_path} doesnt exist.", file=sys.stderr)
        return False
