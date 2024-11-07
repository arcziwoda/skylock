"""
Test cases for the functions from core.file_operations
"""

import unittest
from unittest.mock import patch
from pathlib import Path
from skylock_cli.core.file_operations import _generate_unique_file_path


class TestGenerateUniqueFilePath(unittest.TestCase):
    """
    Test cases for the _generate_unique_file_path function
    """

    @patch("skylock_cli.core.file_operations.tempfile.NamedTemporaryFile")
    def test_generate_unique_file_path(self, mock_tempfile):
        """
        Test the _generate_unique_file_path function
        """
        mock_tempfile.return_value.__enter__.return_value.name = "/mocked/path/file.txt"
        directory = Path("/mocked/path")
        file_name = "file.txt"

        result = _generate_unique_file_path(directory, file_name)

        self.assertEqual(result, Path("/mocked/path/file.txt"))
        mock_tempfile.assert_called_once_with(dir=directory, prefix="file", suffix=".txt", delete=False)

    @patch("skylock_cli.core.file_operations.tempfile.NamedTemporaryFile")
    def test_generate_unique_file_path_with_different_extension(self, mock_tempfile):
        """
        Test the _generate_unique_file_path function with a different file extension
        """
        mock_tempfile.return_value.__enter__.return_value.name = "/mocked/path/file.pdf"
        directory = Path("/mocked/path")
        file_name = "file.pdf"

        result = _generate_unique_file_path(directory, file_name)

        self.assertEqual(result, Path("/mocked/path/file.pdf"))
        mock_tempfile.assert_called_once_with(dir=directory, prefix="file", suffix=".pdf", delete=False)

    @patch("skylock_cli.core.file_operations.tempfile.NamedTemporaryFile")
    def test_generate_unique_file_path_with_no_extension(self, mock_tempfile):
        """
        Test the _generate_unique_file_path function with no file extension
        """
        mock_tempfile.return_value.__enter__.return_value.name = "/mocked/path/file"
        directory = Path("/mocked/path")
        file_name = "file"

        result = _generate_unique_file_path(directory, file_name)

        self.assertEqual(result, Path("/mocked/path/file"))
        mock_tempfile.assert_called_once_with(dir=directory, prefix="file", suffix="", delete=False)


if __name__ == "__main__":
    unittest.main()
