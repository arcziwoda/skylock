"""
Module to test the Token model.
"""

import unittest
from datetime import datetime, timedelta, timezone
import pytest
from jose import jwt
from skylock_cli.model.token import Token


@pytest.fixture
def valid_token_data():
    """
    Fixture for a valid token.
    """
    return {
        "access_token": jwt.encode(
            {"exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()},
            key="",
        ),
        "token_type": "Bearer",
    }


@pytest.fixture
def expired_token_data():
    """
    Fixture for an expired token.
    """
    return {
        "access_token": jwt.encode(
            {"exp": (datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()},
            key="",
        ),
        "token_type": "Bearer",
    }


@pytest.fixture
def invalid_token_data():
    """
    Fixture for an invalid token.
    """
    return {"access_token": "invalid.token", "token_type": "Bearer"}


class TestToken(unittest.TestCase):
    """
    Test cases for the Token model.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.valid_token_data = None
        self.expired_token_data = None
        self.invalid_token_data = None

    @pytest.fixture(autouse=True)
    def prepare_fixture(
        self, valid_token_data: dict, expired_token_data: dict, invalid_token_data: dict
    ):
        """Prepare the test fixture."""
        self.valid_token_data = valid_token_data
        self.expired_token_data = expired_token_data
        self.invalid_token_data = invalid_token_data

    def test_token_creation(self):
        """
        Test the creation of a Token instance.
        """
        token = Token(**self.valid_token_data)
        assert token.access_token == self.valid_token_data["access_token"]
        assert token.token_type == self.valid_token_data["token_type"]

    def test_token_is_valid(self):
        """
        Test the is_valid method for a valid token.
        """
        token = Token(**self.valid_token_data)
        assert token.is_valid()

    def test_token_is_invalid(self):
        """
        Test the is_valid method for an invalid token.
        """
        token = Token(**self.invalid_token_data)
        assert not token.is_valid()

    def test_token_is_expired(self):
        """
        Test the is_expired method for an expired token.
        """
        token = Token(**self.expired_token_data)
        assert token.is_expired()

    def test_token_is_not_expired(self):
        """
        Test the is_expired method for a valid token.
        """
        token = Token(**self.valid_token_data)
        assert not token.is_expired()


if __name__ == "__main__":
    unittest.main()
