import unittest

from brand_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers import (
    get_company_name,
)


class TestSuiteLinkedinId(unittest.TestCase):
    def test_company_name(self):
        name = get_company_name(input_string="bbc")
        self.assertEqual(name, "bbc")

    def test_company_name_with_full_url(self):
        name = get_company_name(input_string="https://www.linkedin.com/company/bbc/")
        self.assertEqual(name, "bbc")
