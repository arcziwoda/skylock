"""This module contains the URL manager functions."""

from urllib.parse import urlparse
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.model.context import Context
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.exceptions.api_exceptions import InvalidURLError
from skylock_cli.config import LOCAL_HOST


def check_url(url: str) -> bool:
    """Validate the URL format."""
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise InvalidURLError(url)
    return True


def set_url(base_url: str | None) -> Context:
    """Set the URL of the SkyLock server."""
    if base_url is None:
        base_url = LOCAL_HOST
    with CLIExceptionHandler():
        check_url(base_url)
        context = ContextManager.get_context()
        context.base_url = base_url
        ContextManager.save_context(context)
    return context
