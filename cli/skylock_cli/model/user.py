"""
User model class
"""

from typing import Optional
import json


class User:
    """
    Stores user information
    """

    def __init__(self, username: str, password: str, api_key: Optional[str] = None):
        """Initialize the User object"""
        self._username = username
        self._password = password
        self._api_key = api_key

    def __repr__(self) -> str:
        """Return a string representation of the User object"""
        return f"{__class__.__name__}({self._username}, {self._password}, {self._api_key})"

    def to_json(self) -> str:
        """Return the User object as a JSON string"""
        return json.dumps({"username": self._username, "password": self._password, "api_key": self._api_key})

    @classmethod
    def from_json(cls, json_data: str):
        """Create a User object from a JSON string"""
        data = json.loads(json_data)
        return cls(data["username"], data["password"], data["api_key"])

    def is_authenticated(self) -> bool:
        """Check if the user is authenticated"""
        return self._api_key is not None
