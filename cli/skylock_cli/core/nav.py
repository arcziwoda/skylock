"""
Module for navigating the file system.
"""

from pathlib import Path
from typing import List, Tuple
from pydantic import TypeAdapter
from skylock_cli.core import context_manager, path_parser
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.api.nav_requests import send_ls_request
from skylock_cli.model import directory, file


def list_directory(
    directory_path: str,
) -> Tuple[List[file.File], List[directory.Directory]]:
    """
    List the contents of a directory.
    """
    current_context = context_manager.ContextManager.get_context()
    with CLIExceptionHandler():
        joind_path = path_parser.parse_path(
            current_context.user_dir.path, Path(directory_path)
        )
        response = send_ls_request(current_context.token, joind_path)
        files = TypeAdapter(List[file.File]).validate_python(response["files"])
        directories = TypeAdapter(List[directory.Directory]).validate_python(
            response["folders"]
        )
    return sorted(files + directories, key=lambda x: x.name)
