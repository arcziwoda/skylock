"""This module contains the test cases for the parse_path function from core.path_parser"""

import unittest
from pathlib import Path
from skylock_cli.core.path_parser import parse_path, is_directory
from skylock_cli.config import ROOT_PATH


class TestParsePath(unittest.TestCase):
    """Test cases for the parse_path function from core.path_parser"""

    def test_parse_path_absolute(self):
        """Test the case where the user input path is absolute"""
        cwd = Path("/home/user")
        user_input_path = Path("/etc/config")
        result = parse_path(cwd, user_input_path)
        self.assertEqual(result, Path("/etc/config"))

    def test_parse_path_relative(self):
        """Test the case where the user input path is relative"""
        cwd = Path("/home/user")
        user_input_path = Path("documents/file.txt")
        result = parse_path(cwd, user_input_path)
        result = Path(str(result).replace("/System/Volumes/Data", ""))
        self.assertEqual(result, Path("/home/user/documents/file.txt"))

    def test_parse_path_empty(self):
        """Test the case where the user input path is empty"""
        cwd = Path("/home/user")
        user_input_path = Path("")
        result = parse_path(cwd, user_input_path)
        self.assertEqual(result, cwd.resolve())

    def test_parse_path_special_characters(self):
        """Test the case where the user input path contains special characters"""
        cwd = Path("/home/user")
        user_input_path = Path("../etc/config")
        result = parse_path(cwd, user_input_path)
        result = Path(str(result).replace("/System/Volumes/Data", ""))
        self.assertEqual(result, Path("/home/etc/config"))

    def test_parse_path_with_spaces(self):
        """Test the case where the user input path contains spaces"""
        cwd = Path("/home/user")
        user_input_path = Path("documents/my file.txt")
        result = parse_path(cwd, user_input_path)
        result = Path(str(result).replace("/System/Volumes/Data", ""))
        self.assertEqual(result, Path("/home/user/documents/my file.txt"))

    def test_user_wants_to_go_back_beyond_root(self):
        """Test the case where the user wants to go back beyond the root directory"""
        cwd = ROOT_PATH
        user_input_path = Path("../../etc/config")
        result = parse_path(cwd, user_input_path)
        result = Path(str(result).replace("/private", ""))
        self.assertEqual(result, Path("/etc/config"))

    def test_parse_path_home_directory(self):
        """Test the case where the user wants to go to the home directory"""
        cwd = Path("/home/user")
        user_input_path = Path("~/documents/file.txt")
        result = parse_path(cwd, user_input_path)
        self.assertEqual(result, Path("/documents/file.txt"))

    def test_is_directory(self):
        """Test the case where the user input path is a directory"""
        path = "/home/user/documents/"
        result = is_directory(path)
        self.assertTrue(result)

    def test_is_not_directory(self):
        """Test the case where the user input path is not a directory"""
        path = "/home/user/documents/file"
        result = is_directory(path)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
