"""
Module to handle logic for file operations
"""

from pathlib import Path
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.core import path_parser, context_manager
from skylock_cli.api.file_requests import send_upload_request


def upload_file(real_file_path: Path, destination_path: Path) -> Path:
    """Upload a file"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        joind_path = path_parser.parse_path(current_context.cwd.path, destination_path)
        send_upload_request(current_context.token, joind_path, real_file_path)
    return joind_path
