import json
import os
import unittest
from unittest.mock import patch, Mock

from constants import (
    SHAREUPDATE,
    SHAREIMAGE,
    SHAREARTICLE,
    SHAREVIDEO,
    SHARETEXT,
    SHAREFEED,
    SHARECOLLECTION,
    RESHARE,
)
from get_posts import (
    resolve_url,
    url_from_string,
    get_article_url,
    get_video_url,
    get_url_from_text_content,
    get_reshare_url,
    get_post_link_and_social_activity,
    print_linkedin_post_data,
    get_feed_topic_summary_url,
    get_url,
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
            FILE_DIRECTORY + "/get_posts_test_data" + "/article_test_data.json"
        ) as article_file:
            article_items = json.load(article_file)
        url_1 = get_article_url(article_items[0])
        self.assertEqual(
            url_1,
            "https://www.eventbrite.co.uk/e/do-you-want-to-help-buildthebbc-an-evening-of-tech"
            "-talks-networking-and-pizza-tickets-63047946104",
        )
        url_2 = get_article_url(article_items[1])
        self.assertEqual(
            url_2,
            "https://www2.deloitte.com/ca/en/pages/energy-and-resources/articles/future-mining"
            "-wearables-improve-safety.html",
        )

    def test_get_video_url(self):
        with open(
            FILE_DIRECTORY + "/get_posts_test_data" + "/video_url_test_data.json"
        ) as video_file:
            video_item = json.load(video_file)
        url = get_video_url(video_item)
        self.assertEqual(url, "https://www.youtube.com/watch?v=WC0wv8FBGUs")

    def test_get_image_url(self):
        with open(
            FILE_DIRECTORY + "/get_posts_test_data" + "/image_url_test_data.json"
        ) as image_file:
            image_item = json.load(image_file)
        url = get_url_from_text_content(image_item)
        self.assertEqual(
            url,
            [
                "https://www2.deloitte.com/ca/en/pages/financial-services/articles/payment"
                "-modernization.html"
            ],
        )

    def test_get_collection_url(self):
        with open(
            FILE_DIRECTORY + "/get_posts_test_data" + "/collection_url_test_data.json"
        ) as collection_file:
            collection_item = json.load(collection_file)
        url = get_url_from_text_content(collection_item)
        self.assertEqual(url, ["https://www.bbc.com/aboutthebbc/reports/policies/5050"])

    def test_get_text_url(self):
        with open(
            FILE_DIRECTORY + "/get_posts_test_data" + "/text_url_test_data.json"
        ) as text_file:
            text_item = json.load(text_file)
        url = get_url_from_text_content(text_item)
        self.assertEqual(
            url,
            [
                "https://www2.deloitte.com/ca/fr/pages/tax/articles/tax-technology-and-automation.html"
            ],
        )

    def test_get_feed_topic_summary_url(self):
        with open(
            FILE_DIRECTORY + "/get_posts_test_data" + "/feed_topic_url_test_data.json"
        ) as feed_topic_file:
            feed_topic_item = json.load(feed_topic_file)
        url = get_feed_topic_summary_url(feed_topic_item)
        self.assertEqual(
            url,
            "https://www.nytimes.com/guides/working-womans-handbook/overcome-impostor-syndrome",
        )

    def test_get_feed_topic_summary_url_with_none_response(self):
        url = get_feed_topic_summary_url({"feed_topic_item": []})
        self.assertEqual(url, None)

    @patch("get_posts.get_url")
    def test_get_reshare_url(self, mock_get_url):
        with open(
            FILE_DIRECTORY + "/get_posts_test_data" + "/reshare_url_test_data.json"
        ) as reshare_file:
            reshare_item = json.load(reshare_file)
        get_reshare_url(reshare_item)
        mock_get_url.assert_called_once()

    def test_get_post_link_and_social_activity(self):
        with open(
            FILE_DIRECTORY
            + "/get_posts_test_data"
            + "/post_link_social_activity_test_data.json"
        ) as file:
            social_item = json.load(file)
        linkedin_post_link, likes = get_post_link_and_social_activity(social_item)
        self.assertIsInstance(linkedin_post_link, str)
        self.assertIsInstance(likes, int)
        self.assertEqual(
            linkedin_post_link,
            "https://www.linkedin.com/feed/update/urn:li:activity:6570409121835814912",
        )
        self.assertEqual(likes, 3)

    @patch("get_posts.get_url")
    @patch("get_posts.get_post_link_and_social_activity")
    def test_get_linkedin_post_data(
        self, mock_get_post_link_and_social_activity, mock_get_url
    ):
        mock_get_post_link_and_social_activity.return_value = (
            "https://www.linkedin.com/feed/update/urn:li:activity"
            ":6570409121835814912",
            3,
        )
        with open(
            FILE_DIRECTORY
            + "/get_posts_test_data"
            + "/post_link_social_activity_test_data.json"
        ) as post_file:
            post_item = json.load(post_file)
        print_linkedin_post_data(item_number=0, item=post_item)

        mock_get_post_link_and_social_activity.assert_called_once_with(item=post_item)
        mock_get_url.assert_called_once_with(item=post_item)


class TestSuiteGetUrl(unittest.TestCase):
    @patch("get_posts.get_url_from_text_content")
    def test_image(self, mock_get_url_from_text_content):
        with open(FILE_DIRECTORY + "/get_url_test_data" + "/Image.json") as image_file:
            image_item = json.load(image_file)
        get_url(image_item)
        mock_get_url_from_text_content.assert_called_once_with(
            item=image_item.get("value")[SHAREUPDATE]["content"][SHAREIMAGE]
        )

    @patch("get_posts.get_article_url")
    def test_article(self, mock_get_article_url):
        with open(
            FILE_DIRECTORY + "/get_url_test_data" + "/Article.json"
        ) as article_file:
            article_item = json.load(article_file)
        get_url(article_item)
        mock_get_article_url.assert_called_once_with(
            item=article_item.get("value")[SHAREUPDATE]["content"][SHAREARTICLE]
        )

    @patch("get_posts.get_video_url")
    def test_video(self, mock_get_video_url):
        with open(FILE_DIRECTORY + "/get_url_test_data" + "/Video.json") as video_file:
            video_item = json.load(video_file)
        get_url(video_item)
        mock_get_video_url.assert_called_once_with(
            item=video_item.get("value")[SHAREUPDATE]["content"][SHAREVIDEO]
        )

    @patch("get_posts.get_url_from_text_content")
    def test_text(self, mock_get_url_from_text_content):
        with open(FILE_DIRECTORY + "/get_url_test_data" + "/Text.json") as text_file:
            text_item = json.load(text_file)
        get_url(text_item)
        mock_get_url_from_text_content.assert_called_once_with(
            item=text_item.get("value")[SHAREUPDATE]["content"][SHARETEXT]
        )

    @patch("get_posts.get_feed_topic_summary_url")
    def test_feed_topic(self, mock_get_feed_topic_summary_url):
        with open(
            FILE_DIRECTORY + "/get_url_test_data" + "/FeedTopic.json"
        ) as feed_topic_file:
            feed_topic_item = json.load(feed_topic_file)
        get_url(feed_topic_item)
        mock_get_feed_topic_summary_url.assert_called_once_with(
            item=feed_topic_item.get("value")[SHAREUPDATE]["content"][SHAREFEED]
        )

    @patch("get_posts.get_url_from_text_content")
    def test_collection(self, mock_get_url_from_text_content):
        with open(
            FILE_DIRECTORY + "/get_url_test_data" + "/Collection.json"
        ) as collection_file:
            collection_item = json.load(collection_file)
        get_url(collection_item)
        mock_get_url_from_text_content.assert_called_once_with(
            item=collection_item.get("value")[SHAREUPDATE]["content"][SHARECOLLECTION]
        )

    @patch("get_posts.get_reshare_url")
    def test_reshare(self, mock_get_reshare_url):
        with open(
            FILE_DIRECTORY + "/get_url_test_data" + "/Reshare.json"
        ) as reshare_file:
            reshare_item = json.load(reshare_file)
        get_url(reshare_item)
        mock_get_reshare_url.assert_called_once_with(
            item=reshare_item.get("value")[RESHARE]
        )


class TestSuitePostsSetup(unittest.TestCase):
    @patch("get_posts.Linkedin")
    def test_get_updates_empty_list(self, mock_Linkedin):
        mock_Linkedin.get_company_updates = Mock(return_value=[])
        company_updates = get_updates(linkedin_object=mock_Linkedin, company_name="1")
        self.assertEqual(company_updates, None)

    @patch("get_posts.Linkedin")
    def test_get_updates_response_list(self, mock_Linkedin):
        mock_Linkedin.get_company_updates = Mock(
            return_value=[{"company activities": ["activities"]}]
        )
        company_updates = get_updates(
            linkedin_object=mock_Linkedin, company_name="good-company"
        )
        self.assertIsInstance(company_updates, list)
        self.assertEqual(company_updates, [{"company activities": ["activities"]}])

    @patch("get_posts.Linkedin")
    def test_get_updates_keyerror(self, mock_Linkedin):
        mock_Linkedin.get_company_updates.side_effect = KeyError
        company_updates = get_updates(
            linkedin_object=mock_Linkedin, company_name="eeeeeeeeeee"
        )
        self.assertEqual(company_updates, None)
