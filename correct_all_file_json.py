import os

from app import app

from app.views import get_json_data, XML_UPLOADS, EXCLUDED_DISPLAY_FILES, get_file_detail, write_json
from app.xml_operations import LOGGER, xml_validate


def correct_all_file_json():
    """
    This route will render a template.
    If a query string comes into the URL, it will return a parsed
    dictionary of the query string keys & values, using request.args
    """
    if not os.path.isdir(app.config[XML_UPLOADS]):
        return """<h1>There is no output folder. Upload the files</h1>"""
    directory_list = os.listdir(app.config[XML_UPLOADS])
    number_of_xml_files = len(directory_list) - len(EXCLUDED_DISPLAY_FILES)

    LOGGER.info(f"Total number of xml files: {number_of_xml_files}")
    ip_data = get_json_data(f"{app.config[XML_UPLOADS]}/uploader_record.json")
    display_data = {}
    all_files_detail = get_json_data(f"{app.config[XML_UPLOADS]}/all_files_detail.json")
    for file_name in directory_list:
        LOGGER.info(f"working on file: {file_name}")
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


if __name__ == "__main__":
    correct_all_file_json()
