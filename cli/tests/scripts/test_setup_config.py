"""
Test the setup_config script.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
from skylock_cli.scripts.setup_config import create_config_file, create_downloads_dir
from skylock_cli.config import EMPTY_CONTEXT


class TestCreateConfigFile(unittest.TestCase):
    """Test the create_config_file function."""

    @patch("skylock_cli.scripts.setup_config.CONFIG_DIR", "/tmp/test_skylock_config")
    @patch(
        "skylock_cli.scripts.setup_config.CONFIG_FILE_NAME", "test_skylock_config.json"
    )
    def test_create_config_file(self):
        """Test the create_config_file function."""

        # Call the function
        create_config_file()

        # Check if the directory was created
        config_dir_path = Path("/tmp/test_skylock_config")
        self.assertTrue(config_dir_path.exists())

        # Check if the file was created and written to
        config_file_path = config_dir_path / "test_skylock_config.json"
        self.assertTrue(config_file_path.exists())

        # Check the content written to the file
        with config_file_path.open("r", encoding="utf-8") as f:
            content = json.load(f)
            self.assertEqual(content, {"context": EMPTY_CONTEXT})

        # Clean up: delete the created file and directory
        config_file_path.unlink()  # Delete the file
        config_dir_path.rmdir()  # Delete the directory


class TestCreateDownloadsDir(unittest.TestCase):
    """Test the create_downloads_dir function."""

    @patch("skylock_cli.scripts.setup_config.DOWNLOADS_DIR", new_callable=MagicMock)
    def test_create_downloads_dir(self, mock_downloads_dir):
        """Test the create_downloads_dir function."""

        # Mock the exists method to return False
        mock_downloads_dir.exists.return_value = False

        # Call the function
        create_downloads_dir()

        # Check if mkdir was called with the correct arguments
        mock_downloads_dir.mkdir.assert_called_once_with(parents=True)

    @patch("skylock_cli.scripts.setup_config.DOWNLOADS_DIR", new_callable=MagicMock)
    def test_create_downloads_dir_already_exists(self, mock_downloads_dir):
        """Test the create_downloads_dir function when the directory already exists."""

        # Mock the exists method to return True
        mock_downloads_dir.exists.return_value = True

        # Call the function
        create_downloads_dir()

        # Check that mkdir was not called
        mock_downloads_dir.mkdir.assert_not_called()


if __name__ == "__main__":
    unittest.main()
