import json
import os
import unittest
from unittest.mock import patch, Mock

from brand_setup_tools.linkedin_id_and_posts_extractor.get_posts import (
    resolve_url,
    url_from_string,
    get_article_url,
    get_url_from_text_content,
    get_post_link_and_social_activity,
    print_linkedin_post_data,
    get_updates,
)

FILE_DIRECTORY = os.path.dirname(__file__)


class TestSuiteGetPosts(unittest.TestCase):
    def test_resolve_url(self):
        final_url = resolve_url(url_link="https://tinyurl.com/y22nomgc")
        self.assertEqual(
            final_url, "https://www.concured.com/blog/how-to-build-links-with-concured"
        )

    def test_url_from_string(self):
        resolved_urls_list = url_from_string(
            string="""BBC Children’s are now looking for an experienced Script Editor to join our team on a part - time basis, working on various drama and comedy productions.
                For more information and to apply, follow the link below:
                https://tinyurl.com/y22nomgc"""
        )
        self.assertEqual(
            resolved_urls_list,
            ["https://www.concured.com/blog/how-to-build-links-with-concured"],
        )

    def test_get_article_url(self):
        with open(
                f"{FILE_DIRECTORY}/get_posts_test_data/article_test_data.json"
        ) as article_file:
            article_items = json.load(article_file)
        url_1 = get_article_url(article_items[0])
        self.assertEqual(
            url_1,
            "https://www.concured.com/blog/how-to-transform-your-content-marketing-with-artificial-intelligence",
        )
        url_2 = get_article_url(article_items[1])
        self.assertEqual(
            url_2,
            "https://www.concured.com/blog/best-practices-for-a-successful-content-marketing-campaign",
        )

    def test_get_image_url(self):
        with open(
                f"{FILE_DIRECTORY}/get_posts_test_data/image_url_test_data.json"
        ) as image_file:
            image_item = json.load(image_file)
        url = get_url_from_text_content(image_item)
        self.assertEqual(
            url,
            "https://www2.deloitte.com/global/en/pages/about-deloitte/articles/covid-19/american-airlines-and-deloitte-partner-to-provide-40000-pieces-of-critical-personal-protective-equipment-to-frontline-health-care-heroes.html",
        )

    def test_get_video_url(self):
        with open(
                f"{FILE_DIRECTORY}/get_posts_test_data/video_url_test_data.json"
        ) as video_file:
            video_item = json.load(video_file)
        url = get_url_from_text_content(video_item)
        self.assertEqual(
            url,
            "https://www2.deloitte.com/global/en/pages/about-deloitte/articles/covid-19/covid-19"
            "--confronting-uncertainty-through---beyond-the-crisis-.html",
        )

    def test_get_post_link_and_social_activity(self):
        with open(
                f"{FILE_DIRECTORY}/get_posts_test_data/post_link_social_activity_test_data.json"
        ) as file:
            social_item = json.load(file)
        linkedin_post_link, likes = get_post_link_and_social_activity(social_item)
        self.assertIsInstance(linkedin_post_link, str)
        self.assertIsInstance(likes, int)
        self.assertEqual(
            linkedin_post_link,
            "https://www.linkedin.com/feed/update/urn:li:activity:6668958869974257664",
        )
        self.assertEqual(likes, 205)

    @patch("brand_setup_tools.linkedin_id_and_posts_extractor.get_posts.get_url")
    @patch(
        "brand_setup_tools.linkedin_id_and_posts_extractor.get_posts.get_post_link_and_social_activity"
    )
    def test_get_linkedin_post_data(
            self, mock_get_post_link_and_social_activity, mock_get_url
    ):
        mock_get_post_link_and_social_activity.return_value = (
            "https://www.linkedin.com/feed/update/urn:li:activity:6668958869974257664",
            205,
        )
        with open(
                f"{FILE_DIRECTORY}/get_posts_test_data/post_link_social_activity_test_data.json"
        ) as post_file:
            post_item = json.load(post_file)
        print_linkedin_post_data(item_number=0, item=post_item)
        mock_get_url.assert_called_once_with(item=post_item)
        mock_get_post_link_and_social_activity.assert_called_once_with(item=post_item)


class TestSuitePostsSetup(unittest.TestCase):
    @patch(
        "brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers.Linkedin"
    )
    def test_get_updates_empty_list(self, mock_Linkedin):
        mock_Linkedin.get_company_updates = Mock(return_value=[])
        company_updates = get_updates(linkedin_object=mock_Linkedin, company_name="1")
        self.assertEqual(company_updates, None)

    @patch(
        "brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers.Linkedin"
    )
    def test_get_updates_response_list(self, mock_Linkedin):
        mock_Linkedin.get_company_updates = Mock(
            return_value=[{"company activities": ["activities"]}]
        )
        company_updates = get_updates(
            linkedin_object=mock_Linkedin, company_name="good-company"
        )
        self.assertIsInstance(company_updates, list)
        self.assertEqual(company_updates, [{"company activities": ["activities"]}])

    @patch(
        "brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers.Linkedin"
    )
    def test_get_updates_keyerror(self, mock_Linkedin):
        mock_Linkedin.get_company_updates.side_effect = KeyError
        company_updates = get_updates(
            linkedin_object=mock_Linkedin, company_name="eeeeeeeeeee"
        )
        self.assertEqual(company_updates, None)
