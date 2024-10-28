"""Helper functions for tests."""

from unittest.mock import Mock


def mock_response_with_status(status_code):
    """Create a mock response object with a status code."""
    mock_response = Mock()
    mock_response.status_code = status_code
    return mock_response
