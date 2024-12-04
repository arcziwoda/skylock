"""
Module to test the ShareLink model.
"""

import unittest
from skylock_cli.model.share_link import ShareLink


class TestShareLink(unittest.TestCase):
    """
    Test cases for the ShareLink model.
    """

    def test_share_link_url(self):
        """
        Test the URL property of a ShareLink instance.
        """
        share_link = ShareLink(base_url="http://localhost:8000", location="/files/1")
        self.assertEqual(share_link.url, "http://localhost:8000/files/1")

    def test_share_link_url_with_trailing_slash(self):
        """
        Test the URL property of a ShareLink instance with a trailing slash in the base URL.
        """
        share_link = ShareLink(base_url="http://localhost:8000/", location="/files/1")
        self.assertEqual(share_link.url, "http://localhost:8000/files/1")

    def test_share_link_url_with_leading_slash(self):
        """
        Test the URL property of a ShareLink instance with a leading slash in the location.
        """
        share_link = ShareLink(base_url="http://localhost:8000", location="files/1")
        self.assertEqual(share_link.url, "http://localhost:8000/files/1")

    def test_share_link_url_with_slashes(self):
        """
        Test the URL property of a ShareLink instance with slashes in the base URL and location.
        """
        share_link = ShareLink(base_url="http://localhost:8000/", location="files/1")
        self.assertEqual(share_link.url, "http://localhost:8000/files/1")

    def test_share_link_url_with_query_string(self):
        """
        Test the URL property of a ShareLink instance with a query string in the location.
        """
        share_link = ShareLink(
            base_url="http://localhost:8000", location="/files/1?token=abc123"
        )
        self.assertEqual(share_link.url, "http://localhost:8000/files/1?token=abc123")

    def test_share_link_url_with_fragment(self):
        """
        Test the URL property of a ShareLink instance with a fragment in the location.
        """
        share_link = ShareLink(
            base_url="http://localhost:8000", location="/files/1#section"
        )
        self.assertEqual(share_link.url, "http://localhost:8000/files/1#section")

    def test_share_link_url_with_query_string_and_fragment(self):
        """
        Test the URL property of a ShareLink instance with a query string and fragment in the location.
        """
        share_link = ShareLink(
            base_url="http://localhost:8000", location="/files/1?token=abc123#section"
        )
        self.assertEqual(
            share_link.url, "http://localhost:8000/files/1?token=abc123#section"
        )


if __name__ == "__main__":
    unittest.main()
