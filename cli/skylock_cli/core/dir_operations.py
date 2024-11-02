"""
Module to handle logic for directory operations
"""

from pathlib import Path
from skylock_cli.api.dir_requests import send_mkdir_request, send_rmdir_request
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.core import path_parser, context_manager
from skylock_cli.exceptions.core_exceptions import NotADirectoryError


def create_directory(directory_path: str, parent: bool) -> Path:
    """Create a directory in the user's cwd"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        joind_path = path_parser.parse_path(current_context.cwd.path, Path(directory_path))
        send_mkdir_request(current_context.token, joind_path, parent)
    return joind_path


def remove_directory(directory_path: str, recursive: bool) -> Path:
    """Remove a directory"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        if not path_parser.is_directory(directory_path):
            raise NotADirectoryError(directory_path)

        joind_path = path_parser.parse_path(current_context.cwd.path, Path(directory_path))
        send_rmdir_request(current_context.token, joind_path, recursive)
    return joind_path
