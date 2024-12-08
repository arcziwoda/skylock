import pathlib
import shutil
from io import BytesIO


FILES_FOLDER_DISK_PATH = "./data/files"


def save_file_data(data: bytes, filename: str):
    folder = create_files_folder_if_non_existent()

    path = folder / filename

    if path.exists():
        raise ValueError(f"File of given path: {path} already exists")

    with path.open("wb") as buffer:
        shutil.copyfileobj(BytesIO(data), buffer)


def get_file_data(filename: str) -> bytes:
    folder = create_files_folder_if_non_existent()

    path = folder / filename

    if not path.exists():
        raise ValueError(f"File of given path: {path} does not exist")

    return path.read_bytes()


def delete_file_data(filename: str):
    folder = create_files_folder_if_non_existent()

    path = folder / filename

    if not path.exists():
        raise ValueError(f"File of given path: {path} does not exist")

    path.unlink()


def create_files_folder_if_non_existent() -> pathlib.Path:
    folder = pathlib.Path(FILES_FOLDER_DISK_PATH)
    folder.mkdir(parents=True, exist_ok=True)
    return folder
