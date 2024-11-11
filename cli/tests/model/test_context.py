"""
Module to test the Context model.
"""

import unittest
from pathlib import Path
from skylock_cli.model.context import Context
from skylock_cli.model.token import Token
from skylock_cli.model.directory import Directory


class TestContext(unittest.TestCase):
    """
    Test cases for the Context model.
    """

    def test_context_creation(self):
        """
        Test the creation of a Context instance.
        """
        token = Token(access_token="test_token", token_type="Bearer")
        directory = Directory(path=Path("/home/user"), name="user")
        context = Context(token=token, cwd=directory)
        self.assertEqual(context.token, token)
        self.assertEqual(context.cwd, directory)

    def test_context_default_values(self):
        """
        Test the default values of a Context instance.
        """
        context = Context()
        self.assertIsNone(context.token)
        self.assertIsNone(context.cwd)


if __name__ == "__main__":
    unittest.main()
