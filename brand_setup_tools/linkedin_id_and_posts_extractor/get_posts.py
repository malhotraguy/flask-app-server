import re
import sys
from pprint import pprint
from time import sleep

import requests
from requests.exceptions import SSLError, Timeout, ConnectionError
from urllib3.exceptions import MaxRetryError

from brand_setup_tools.linkedin_id_and_posts_extractor.constants import (
    SHAREUPDATE,
    SHAREIMAGE,
    SHAREARTICLE,
    SHAREVIDEO,
    HTML,
    VALUE,
    CONTENT,
    PERMALINK,
    SOCIAL_DETAIL,
    SOCIAL_COUNTS,
    NUM_LIKES,
    LINKID,
    UTM,
    EXIT,
    POSTS_MAX_RESULT,
    RESHAREUPDATE,
    EXTERNALVIDEO, DOCUMENTFEED,
)
from brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers import (
    get_linkedin_object,
    get_company_name, get_logger,
)

LOGGER = get_logger(__name__)


def refine_url(url):
    if HTML in url:
        url = url.split(HTML, 1)[0] + ".html"
        return url
    if LINKID in url:
        url = url.split(LINKID, 1)[0]
        return url
    if UTM in url:
        url = url.split(UTM, 1)[0]
        return url
    if "?id=" in url:
        url = url.split("?id=", 1)[0]
        return url
    return url


def resolve_url(url_link):
    try:
        get_response = requests.get(url=url_link, timeout=40)
    except (MaxRetryError, SSLError, Timeout, ConnectionError) as e:
        return f"Cant resolve url:{url_link} because of {e}"
    final_url = get_response.url
    final_url = refine_url(url=final_url)
    return final_url


def url_from_string(string):
    if not isinstance(string, str):
        raise Exception("Input to the url_from_string function is not a string!!")
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        string,
    )
    resolved_urls_list = [resolve_url(url) for url in urls]
    return resolved_urls_list


def get_article_url(item):
    action_target_url = item.get("navigationContext", {}).get("actionTarget")
    if action_target_url:
        return resolve_url(action_target_url)
    else:
        return None


def get_url_from_text_content(feed_item):
    string_value = feed_item.get("commentary", {}).get("text", {}).get("text")
    extracted_urls = []
    if string_value:
        extracted_urls = url_from_string(string_value)
        if len(extracted_urls) == 1 and isinstance(extracted_urls, list):
            extracted_urls = extracted_urls[0]
    return extracted_urls


def extract_url_from_components(shared_update):
    if CONTENT in shared_update:
        share_update_content = shared_update[CONTENT]
        share_update_content_key = list(share_update_content.keys())
        LOGGER.debug(share_update_content_key)
        if SHAREIMAGE in share_update_content:
            url = get_url_from_text_content(feed_item=shared_update)

        elif SHAREARTICLE in share_update_content:
            url = get_article_url(item=share_update_content[SHAREARTICLE])

        elif SHAREVIDEO in share_update_content:
            url = get_url_from_text_content(feed_item=shared_update)
        elif EXTERNALVIDEO in share_update_content:
            url = get_article_url(item=share_update_content[EXTERNALVIDEO])
        elif DOCUMENTFEED in share_update_content:
            url = get_article_url(item=share_update_content[DOCUMENTFEED])

        else:
            pprint(share_update_content)
            raise Exception("Type not defined by Tool")
        shared_url = refine_url(url=url)
        return shared_url


def get_url(item):
    if SHAREUPDATE in item.get(VALUE):
        shared_update = item.get(VALUE)[SHAREUPDATE]
        if CONTENT in shared_update:
            shared_url = extract_url_from_components(shared_update=shared_update)

        elif RESHAREUPDATE in shared_update:
            shared_url = extract_url_from_components(
                shared_update=shared_update[RESHAREUPDATE]
            )
        else:
            shared_url = get_url_from_text_content(feed_item=shared_update)
        return shared_url
    else:
        pprint(item)
        raise Exception("Not defined for this  type of Reshare by Tool")


def get_post_link_and_social_activity(item):
    linkedin_post_link = item.get(PERMALINK)
    total_social_activity_counts = (
        item.get(VALUE, {})
            .get(SHAREUPDATE, {})
            .get(SOCIAL_DETAIL, {})
            .get(SOCIAL_COUNTS, {})
    )
    likes = total_social_activity_counts.get(NUM_LIKES)
    return linkedin_post_link, likes


def print_linkedin_post_data(item_number, item):
    linkedin_post_link, total_likes = get_post_link_and_social_activity(item=item)
    LOGGER.info(f"{item_number})\n Linkedin Post link: {linkedin_post_link}")
    LOGGER.info(f" Total Likes={total_likes}")
    shared_url = get_url(item=item)
    LOGGER.info(f" Original Shared Url={shared_url}")


def get_updates(linkedin_object, company_name):
    try:
        updates = linkedin_object.get_company_updates(
            company_name, max_results=POSTS_MAX_RESULT, results=[]
        )
    except KeyError:
        LOGGER.warning(f"No posts has been retrieved for: {company_name}")
        return None
    if updates:
        return updates
    else:
        LOGGER.warning(f"No posts has been retrieved for: {company_name}")
        return None


def linkedin_posts_setup():
    linkedin_object = get_linkedin_object()
    user_input = input(
        "Enter the company universal name or urn id or linkedin profile url or type exit: "
    ).strip()
    if user_input == EXIT:
        sys.exit("Quiting the Tool!!")
    company_universal_name = get_company_name(user_input)
    LOGGER.debug("Looking for posts: ....")
    company_updates = get_updates(
        linkedin_object=linkedin_object, company_name=company_universal_name
    )
    if company_updates:
        LOGGER.debug("Fetched the posts and now printing them :")
        for update_number, update in enumerate(company_updates):
            print_linkedin_post_data(item_number=update_number, item=update)
        linkedin_posts_setup()


if __name__ == "__main__":
    linkedin_posts_setup()
