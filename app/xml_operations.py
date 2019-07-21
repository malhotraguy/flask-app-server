import os
import time
import xml.etree.ElementTree as ET
from xml.sax import make_parser, SAXParseException
from xml.sax.handler import ContentHandler
from flask import flash,get_flashed_messages


def get_links_count(file_path):
    try:
        tree = ET.parse(file_path)
    except ET.ParseError as pe:
        print(f"For File:{file_path} Error:{pe}")
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
            print(f"{file_path} is well-formed xml file")
        except SAXParseException as e:
            flash(message=str(e),category="error")
            error_type = str(e).split(sep=" ", maxsplit=1)[1]
            if error_type == "syntax error":
                os.remove(file_path)
                print(f"File: {file_path} Removed! because it is not xml file.")
            print(f"{e}")
    else:
        print(f"{file_path} doesnt exist.")


if __name__ == "__main__":
    #     calling main function
    file_path = "./po.txt"
    xml_validate(file_path)
