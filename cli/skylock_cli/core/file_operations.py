"""
Module to handle logic for file operations
"""

from pathlib import Path
import os
import tempfile
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.core import path_parser, context_manager
from skylock_cli.api.file_requests import send_upload_request, send_download_request
from skylock_cli.config import DOWNLOADS_DIR
from skylock_cli.scripts.setup_config import create_downloads_dir


def upload_file(real_file_path: Path, destination_path: Path) -> Path:
    """Upload a file"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        joind_path = path_parser.parse_path(current_context.cwd.path, destination_path)

        with open(real_file_path, "rb") as file:
            file_metadata = {
                "file_content": file,
                "file_name": real_file_path.name,
            }

            send_upload_request(current_context.token, joind_path, file_metadata)

    return joind_path


def download_file(virtual_file_path: Path) -> Path:
    """Download a file"""
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        joind_path = path_parser.parse_path(current_context.cwd.path, virtual_file_path)

        file_metadata = send_download_request(current_context.token, joind_path)
        file_name = file_metadata["file_name"]
        file_content = file_metadata["file_content"]

        if not DOWNLOADS_DIR.exists():
            create_downloads_dir()

        unique_file_path = _generate_unique_file_path(DOWNLOADS_DIR, file_name)

        with open(unique_file_path, "wb") as file:
            file.write(file_content)

    return unique_file_path


def _generate_unique_file_path(directory: Path, file_name: str) -> Path:
    """Generate a unique file path using tempfile.NamedTemporaryFile"""
    base_name, extension = os.path.splitext(file_name)
    with tempfile.NamedTemporaryFile(
        dir=directory, prefix=base_name, suffix=extension, delete=False
    ) as temp_file:
        unique_file_path = Path(temp_file.name)
    return unique_file_path
