import os
from xml.sax.handler import ContentHandler
from xml.sax import make_parser, SAXParseException


def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)

def xml_validate(filename):
    if os.path.isfile(filename):
        try:
            parsefile(filename)
            print(f"{filename} is well-formed xml file")
        except SAXParseException as e:
            error_type=str(e).split(sep=" ",maxsplit=1)[1]
            if error_type=="syntax error":
                os.remove(filename)
                print(f"File: {filename} Removed! because it is not xml file.")
            print(f"{e}")
    else:
        print(f"{filename} doesnt exist.")

if __name__ == "__main__":
    #     calling main function
    filename = "./po.txt"
    xml_validate(filename)