"""
This module contains commands the user can run to interact with the SkyLock.
"""

from pathlib import Path
import typer
from art import text2art
from skylock_cli.core.auth import register_user, login_user
from skylock_cli.core.dir_operations import create_directory, remove_directory
from skylock_cli.core.file_operations import upload_file
from skylock_cli.core.nav import list_directory, change_directory, get_working_directory

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def register(username: str) -> None:
    """
    Register a new user in the SkyLock.

    Args:
        username (str): The username of the new user.

    Returns:
        None
    """
    password = typer.prompt("Password", hide_input=True)
    confirm_password = typer.prompt("Confirm password", hide_input=True)
    if password != confirm_password:
        typer.secho("Passwords do not match. Please try again.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    register_user(username, password)
    typer.secho("User registered successfully", fg=typer.colors.GREEN)


@app.command()
def login(username: str) -> None:
    """
    Login to the SkyLock.

    Args:
        username (str): The username of the user.

    Returns:
        None
    """
    password = typer.prompt("Password", hide_input=True)
    context = login_user(username, password)

    typer.secho("User logged in successfully", fg=typer.colors.GREEN)
    typer.secho("Hello, " + username, fg=typer.colors.GREEN)
    typer.secho("Welcome to our file hosting service", fg=typer.colors.BLUE, bold=True)
    typer.secho(text2art("SkyLock"), fg=typer.colors.BLUE)
    typer.secho(
        f"Your current working directory is: {context.cwd.path}",
        fg=typer.colors.BLUE,
    )


@app.command()
def mkdir(
    directory_path: Path,
    parent: bool = typer.Option(False, "-p", "--parent", help="Create parent directories as needed"),
) -> None:
    """
    Create a new directory in the SkyLock.

    Args:
        directory_path (Path): The path of the new directory.
        parent (bool): If True, create parent directories as needed.

    Returns:
        None
    """
    created_path = create_directory(directory_path, parent)

    cwd = get_working_directory()
    typer.secho(f"Current working directory: {cwd.path}", fg=typer.colors.BLUE)

    typer.secho(f"Directory {created_path} created successfully", fg=typer.colors.GREEN)


@app.command()
def rmdir(
    directory_path: str = typer.Argument(
        ...,
        help="Path to the directory to be removed. Must end with / as this command removes directories, not files.",
    ),
    recursive: bool = typer.Option(
        False,
        "-r",
        "--recursive",
        help="Remove directories and their contents recursively",
    ),
) -> None:
    """
    Remove a directory from the SkyLock.

    Args:
        directory_path (str): The path of the directory to remove.
        recursive (bool): If True, remove directories and their contents recursively.
    Returns:
        None
    """
    removed_path = remove_directory(directory_path, recursive)

    cwd = get_working_directory()
    typer.secho(f"Current working directory: {cwd.path}", fg=typer.colors.BLUE)

    typer.secho(f"Directory {removed_path} removed successfully", fg=typer.colors.GREEN)


@app.command()
def ls(directory_path: Path = typer.Argument(Path("."), help="The directory to list")) -> None:
    """
    List the contents of a directory.

    Args:
        directory_path (Path): The path of the directory to list.

    Returns:
        None
    """
    contents, path = list_directory(directory_path)

    typer.secho(f"Contents of {path}", fg=typer.colors.BLUE)

    for item in contents:
        typer.echo(typer.style(item.name, fg=item.color), nl=False)
        typer.echo("  ", nl=False)

    if contents:
        typer.echo()
    else:
        typer.secho("No contents in directory", fg=typer.colors.YELLOW)


@app.command()
def cd(directory_path: Path = typer.Argument(..., help="The directory to change to")) -> None:
    """
    Change the current working directory.

    Args:
        directory_path (Path): The path of the directory to change to.

    Returns:
        None
    """
    new_cwd = change_directory(directory_path)
    typer.secho(f"Changed directory to {new_cwd}", fg=typer.colors.GREEN)


@app.command()
def pwd() -> None:
    """
    Print the current working directory.

    Returns:
        None
    """
    cwd = get_working_directory()
    typer.secho(f"Current working directory: {cwd.path}", fg=typer.colors.BLUE)


@app.command()
def upload(
    file_path: Path,
    destination_path: Path = typer.Argument(Path("."), help="The destination path to upload the file to. Defaults to the current directory."),
) -> None:
    """
    Upload a file to the SkyLock.

    Args:
        file_path (Path): The path of the file to upload.
        destination_path (Path): The destination path to upload the file to. Defaults to the current directory.

    Returns:
        None
    """

    if not file_path.exists():
        typer.secho(f"File {file_path} does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not file_path.is_file():
        typer.secho(f"{file_path} is not a file.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    path = upload_file(file_path, destination_path)

    cwd = get_working_directory()
    typer.secho(f"Current working directory: {cwd.path}", fg=typer.colors.BLUE)

    typer.secho(f"File {file_path} uploaded to {path} successfully", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
