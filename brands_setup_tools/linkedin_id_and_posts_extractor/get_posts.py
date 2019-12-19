import re
import sys
from datetime import datetime
from pprint import pprint

import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError

from brands_setup_tools.linkedin_id_and_posts_extractor.constants import (
    SHAREUPDATE,
    SHAREIMAGE,
    SHAREARTICLE,
    SHAREVIDEO,
    SHARETEXT,
    SHAREFEED,
    SHARECOLLECTION,
    RESHARE,
    SHAREFEED_HYPERLINK,
    ARTICLE,
    URL,
    RESOLVED_URL,
    HTML,
    VALUES,
    TEXT,
    VALUE,
    ATTRIBUTES,
    SUMMARY,
    ORIGINAL_UPDATE,
    CONTENT,
    PERMALINK,
    SOCIAL_DETAIL,
    SOCIAL_COUNTS,
    NUM_LIKES,
    TYPE,
    LINKID,
    UTM,
    EXIT)
# from linkedin_tool_helpers import get_company_name, get_linkedin_object
from brands_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers import get_linkedin_object, \
    get_company_name


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
    return url


def resolve_url(url_link):
    try:
        get_response = requests.get(url=url_link)
    except MaxRetryError:
        return f"Cant resolve url:{url_link} because of MaxRetryError"
    except SSLError:
        return f"Cant resolve url:{url_link} because of SSLError"
    final_url = get_response.url
    final_url = refine_url(url=final_url)
    return final_url


def url_from_string(string):
    if type(string) is not str:
        raise Exception("Input to the url_from_string function is not a string!!")
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        string,
    )
    resolved_urls_list = [resolve_url(url) for url in urls]
    if not resolved_urls_list:
        return None
    return resolved_urls_list


def get_article_url(item):
    if ARTICLE in item.get(ARTICLE, {}):
        if URL in item[ARTICLE][ARTICLE]:
            return item[ARTICLE][ARTICLE][URL]
    else:
        if RESOLVED_URL in item:
            print(f"resolvedUrl={item[RESOLVED_URL]}")
        if URL in item:
            print(f"url in post={item[URL]}")
            return resolve_url(item[URL])


def get_video_url(item):
    if ARTICLE not in item.get(ARTICLE, {}):
        print("url not present")
        pprint(item)
        return None
    if URL in item[ARTICLE][ARTICLE]:
        return item[ARTICLE][ARTICLE][URL]


def get_url_from_text_content(item):
    if VALUES not in item.get(TEXT, {}):
        return None
    values = item[TEXT][VALUES]
    extracted_urls = []
    for string_value in values:
        url_list = url_from_string(string_value.get(VALUE))
        if url_list:
            extracted_urls.extend(url_list)
    if len(extracted_urls) == 1 and type(extracted_urls) == list:
        extracted_urls = extracted_urls[0]
    return extracted_urls


def get_feed_topic_summary_url(item):
    if ATTRIBUTES not in item.get(SUMMARY, {}):
        return None
    for attribute in item[SUMMARY][ATTRIBUTES]:
        if SHAREFEED_HYPERLINK in attribute.get(TYPE, {}):
            return attribute[TYPE][SHAREFEED_HYPERLINK].get(URL)


def get_reshare_url(item):
    if ORIGINAL_UPDATE in item:
        print("=" * 30, "Reshare", "=" * 30)
        get_url(item=item[ORIGINAL_UPDATE])
        print("=" * 70)
    else:
        pprint(item)


def get_url(item):
    if SHAREUPDATE in item.get(VALUE):
        if CONTENT not in item.get(VALUE)[SHAREUPDATE]:
            pprint(item.get(VALUE)[SHAREUPDATE])
            raise Exception(
                "content keyword is missing in item.get('value')['com.linkedin.voyager.feed.ShareUpdate']"
            )
        share_update_content = item.get(VALUE)[SHAREUPDATE][CONTENT]
        # keys_list = [key for key in share_update_content]
        # print(keys_list)
        if SHAREIMAGE in share_update_content:
            url = get_url_from_text_content(item=share_update_content[SHAREIMAGE])

        elif SHAREARTICLE in share_update_content:
            url = get_article_url(item=share_update_content[SHAREARTICLE])

        elif SHAREVIDEO in share_update_content:
            url = get_video_url(item=share_update_content[SHAREVIDEO])

        elif SHARETEXT in share_update_content:
            url = get_url_from_text_content(item=share_update_content[SHARETEXT])

        elif SHAREFEED in share_update_content:
            url = get_feed_topic_summary_url(item=share_update_content[SHAREFEED])

        elif SHARECOLLECTION in share_update_content:
            url = get_url_from_text_content(item=share_update_content[SHARECOLLECTION])
        else:
            pprint(share_update_content)
            raise Exception("Type not defined by Tool")
        shared_url = refine_url(url=url)
        print(f" Original Shared Url={shared_url}")
        return shared_url

    elif RESHARE in item.get(VALUE):
        get_reshare_url(item=item.get(VALUE)[RESHARE])
    else:
        pprint(item)
        raise Exception("Not defined for this  type of Reshare by Tool")


def get_post_link_and_social_activity(item):
    linkedin_post_link = item.get(PERMALINK)
    total_social_activity_counts = item.get(SOCIAL_DETAIL, {}).get(SOCIAL_COUNTS, {})
    likes = total_social_activity_counts.get(NUM_LIKES)
    return linkedin_post_link, likes


def print_linkedin_post_data(item_number, item):
    linkedin_post_link, total_likes = get_post_link_and_social_activity(item=item)
    print("-" * 150)
    print(f"{item_number})\n Linkedin Post link: {linkedin_post_link}")
    print(f" Total Likes={total_likes}")
    get_url(item=item)


def get_updates(linkedin_object, company_name):
    try:
        updates = linkedin_object.get_company_updates(company_name, results=[])
    except KeyError:
        print(f"No posts has been retrieved for: {company_name}")
        print("=" * 160)
        return None
    if updates:
        return updates
    else:
        print(f"No posts has been retrieved for: {company_name}")
        print("=" * 160)
        return None


def linkedin_posts_setup():
    start_time = datetime.now()
    linkedin_object = get_linkedin_object()
    print("=" * 160)
    user_input = input(
        "Enter the company universal name or urn id or linkedin profile url or type exit: "
    ).strip()
    if user_input == EXIT:
        sys.exit("Quiting the Tool!!")
    company_universal_name = get_company_name(user_input)
    print("Looking for posts: ....")
    company_updates = get_updates(
        linkedin_object=linkedin_object, company_name=company_universal_name
    )
    if company_updates:
        print("Fetched the posts and now printing them :")
        for update_number, update in enumerate(company_updates):
            print_linkedin_post_data(item_number=update_number, item=update)
        print(f"Total Time={datetime.now() - start_time}")
        linkedin_posts_setup()


if __name__ == "__main__":
    linkedin_posts_setup()
