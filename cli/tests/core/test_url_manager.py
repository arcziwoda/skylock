"""
Module to test the URLManager
"""

import unittest
from unittest.mock import patch
from io import StringIO
from click import exceptions
from skylock_cli.core.url_manager import check_url, set_url
from skylock_cli.exceptions.api_exceptions import InvalidURLError
from tests.helpers import mock_test_context


class TestURLManager(unittest.TestCase):
    """Test cases for the URLManager"""

    def test_check_url_valid(self):
        """Test check_url with a valid URL"""
        valid_url = "http://example.com"
        self.assertTrue(check_url(valid_url))

    def test_check_url_invalid_no_scheme(self):
        """Test check_url with a URL missing the scheme"""
        invalid_url = "example.com"
        with self.assertRaises(InvalidURLError) as context:
            check_url(invalid_url)
        self.assertEqual(
            str(context.exception),
            f"Invalid URL: `{invalid_url}`. Please provide a valid URL.",
        )

    def test_check_url_invalid_no_netloc(self):
        """Test check_url with a URL missing the netloc"""
        invalid_url = "http://"
        with self.assertRaises(InvalidURLError) as context:
            check_url(invalid_url)
        self.assertEqual(
            str(context.exception),
            f"Invalid URL: `{invalid_url}`. Please provide a valid URL.",
        )

    def test_check_url_invalid_empty(self):
        """Test check_url with an empty URL"""
        invalid_url = ""
        with self.assertRaises(InvalidURLError) as context:
            check_url(invalid_url)
        self.assertEqual(
            str(context.exception),
            f"Invalid URL: `{invalid_url}`. Please provide a valid URL.",
        )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.save_context",
        return_value=None,
    )
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    def test_set_url_success(self, _mock_get_context, _mock_save_context):
        """Test set_url with a valid URL"""
        base_url = "http://example.com"
        context = set_url(base_url)
        self.assertEqual(context.base_url, base_url)

    @patch(
        "skylock_cli.core.context_manager.ContextManager.save_context",
        return_value=None,
    )
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    def test_set_url_default(self, _mock_get_context, _mock_save_context):
        """Test set_url with the default URL"""
        context = set_url(None)
        self.assertEqual(context.base_url, "http://localhost:8000")

    def test_set_url_invalid(self):
        """Test set_url with an invalid URL"""
        invalid_url = "example.com"
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                set_url(invalid_url)

            self.assertIn(
                f"Invalid URL: `{invalid_url}`. Please provide a valid URL.",
                mock_stderr.getvalue(),
            )

    def test_set_url_invalid_empty(self):
        """Test set_url with an empty URL"""
        empty_url = ""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                set_url(empty_url)

            self.assertIn(
                f"Invalid URL: `{empty_url}`. Please provide a valid URL.",
                mock_stderr.getvalue(),
            )

    def test_set_url_invalid_no_scheme(self):
        """Test set_url with a URL missing the scheme"""
        invalid_url = "example.com"
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                set_url(invalid_url)

            self.assertIn(
                f"Invalid URL: `{invalid_url}`. Please provide a valid URL.",
                mock_stderr.getvalue(),
            )

    def test_set_url_invalid_no_netloc(self):
        """Test set_url with a URL missing the netloc"""
        invalid_url = "http://"
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                set_url(invalid_url)

            self.assertIn(
                f"Invalid URL: `{invalid_url}`. Please provide a valid URL.",
                mock_stderr.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
