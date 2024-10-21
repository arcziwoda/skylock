"""
User model class
"""

from pydantic import BaseModel


class User(BaseModel):
    """
    Stores user information
    """

    username: str
    password: str
