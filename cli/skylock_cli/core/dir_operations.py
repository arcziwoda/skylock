"""
Module to handle logic for directory operations
"""

from pathlib import Path
from skylock_cli.api.dir_requests import send_mkdir_request, send_rmdir_request
from skylock_cli.core.nav import change_directory
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.core import path_parser, context_manager
from skylock_cli.exceptions.core_exceptions import (
    NotADirectoryError,
    RootDirectoryError,
)
from skylock_cli.config import ROOT_PATH


def create_directory(directory_path: Path, parent: bool) -> Path:
    """Create a directory"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        joind_path = path_parser.parse_path(current_context.cwd.path, directory_path)
        send_mkdir_request(current_context.token, joind_path, parent)
    return joind_path


def remove_directory(directory_path: str, recursive: bool) -> Path:
    """Remove a directory"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        if not path_parser.is_directory(directory_path):
            raise NotADirectoryError(directory_path)

        joind_path = path_parser.parse_path(
            current_context.cwd.path, Path(directory_path)
        )

        if joind_path == ROOT_PATH:
            raise RootDirectoryError()

        send_rmdir_request(current_context.token, joind_path, recursive)

        if current_context.cwd.path.is_relative_to(joind_path):
            change_directory(str(joind_path.parent))

    return joind_path
