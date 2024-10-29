"""
Module to handle logic for directory operations
"""

from pathlib import Path
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.api.http_client import send_mkdir_request
from skylock_cli.utils.api_exception_handler import APIExceptionHandler
from skylock_cli.core.path_parser import parse_path


def create_directory(directory_name: str) -> None:
    """Create a directory in the user's cwd"""
    current_context = ContextManager.get_context()
    directory_path = parse_path(current_context.user_dir.path, Path(directory_name))
    with APIExceptionHandler():
        send_mkdir_request(current_context.token, directory_path)
