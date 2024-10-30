"""
User model class.
"""

from pydantic import BaseModel


class User(BaseModel):
    """
    Stores user information.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username: str
    password: str
