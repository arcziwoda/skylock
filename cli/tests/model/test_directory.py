# test_directory.py
"""
Module to test the Directory model.
"""

import unittest
from pathlib import Path
from typer.colors import MAGENTA
from skylock_cli.model.directory import Directory
from skylock_cli.config import ROOT_PATH


class TestDirectory(unittest.TestCase):
    """
    Test cases for the Directory model.
    """

    def test_directory_creation(self):
        """
        Test the creation of a Directory instance.
        """
        directory = Directory(path=Path("/home/user"), name="user")
        self.assertEqual(directory.path, Path("/home/user"))
        self.assertEqual(directory.name, "user/")
        self.assertEqual(directory.color, MAGENTA)

    def test_directory_default_path(self):
        """
        Test the default path of a Directory instance.
        """
        directory = Directory(name="root")
        self.assertEqual(directory.path, ROOT_PATH)

    def test_directory_default_color(self):
        """
        Test the default color of a Directory instance.
        """
        directory = Directory(path=Path("/home/user"), name="user")
        self.assertEqual(directory.color, MAGENTA)

    def test_directory_serialize_path(self):
        """
        Test the serialize_path method.
        """
        directory = Directory(path=Path("/home/user"), name="user")
        self.assertEqual(directory.serialize_path(directory.path), "/home/user")

    def test_directory_ensure_trailing_slash(self):
        """
        Test the ensure_trailing_slash validator.
        """
        directory = Directory(path=Path("/home/user"), name="user")
        self.assertEqual(directory.name, "user/")


if __name__ == "__main__":
    unittest.main()
