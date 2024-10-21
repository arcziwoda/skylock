"""
Why should i write module docstrings on a pydantic class? pylint :[
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents an authentication token returned from the API.

    Attributes:
        access_token (str): The token used for authenticated requests.
        token_type (str): The type of the token, typically 'Bearer'.
    """

    access_token: str
    token_type: str
