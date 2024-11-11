"""
Module to test the User model.
"""

import unittest
from pydantic import ValidationError
from skylock_cli.model.user import User


class TestUser(unittest.TestCase):
    """Test cases for the User model"""

    def test_user_creation(self):
        """Test the creation of a user"""
        user = User(username="testuser", password="password123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "password123")

    def test_user_creation_invalid_username(self):
        """Test the creation of a user with an invalid username"""
        with self.assertRaises(ValidationError):
            User(username=123, password="password123")

    def test_user_creation_invalid_password(self):
        """Test the creation of a user with an invalid password"""
        with self.assertRaises(ValidationError):
            User(username="testuser", password=123)

    def test_user_missing_username(self):
        """Test the creation of a user with a missing username"""
        with self.assertRaises(ValidationError):
            User(password="password123")

    def test_user_missing_password(self):
        """Test the creation of a user with a missing password"""
        with self.assertRaises(ValidationError):
            User(username="testuser")


if __name__ == "__main__":
    unittest.main()
