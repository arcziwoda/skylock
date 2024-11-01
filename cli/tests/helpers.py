"""Helper functions for tests."""

from unittest.mock import Mock


def mock_response_with_status(status_code, json_data=None):
    """Create a mock response object with a status code."""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data
    return mock_response
