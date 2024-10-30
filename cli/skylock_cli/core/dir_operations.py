"""
Module to handle logic for directory operations
"""

from pathlib import Path
from skylock_cli.api.dir_requests import send_mkdir_request
from skylock_cli.utils.api_exception_handler import APIExceptionHandler
from skylock_cli.core import path_parser, context_manager


def create_directory(directory_name: str) -> Path:
    """Create a directory in the user's cwd"""
    current_context = context_manager.ContextManager.get_context()
    directory_path = path_parser.parse_path(
        current_context.user_dir.path, Path(directory_name)
    )
    with APIExceptionHandler():
        send_mkdir_request(current_context.token, directory_path)
    return directory_path
