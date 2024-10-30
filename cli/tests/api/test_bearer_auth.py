"""
Module to test the BearerAuth class
"""

from httpx import Request
from skylock_cli.model.token import Token
from skylock_cli.api.bearer_auth import BearerAuth


def test_bearer_auth():
    """Test the BearerAuth class"""
    mock_token = Token(access_token="mock_access_token", token_type="Bearer")

    auth = BearerAuth(token=mock_token)

    request = Request("GET", "http://test.com")

    auth_flow = auth.auth_flow(request)
    authenticated_request = next(auth_flow)

    assert authenticated_request.headers["Authorization"] == "Bearer mock_access_token"
