from io import BytesIO
import pytest
from unittest.mock import patch
from skylock.utils.storage import (
    save_file_data,
    get_file_data,
    delete_file_data,
)


@pytest.fixture(autouse=True)
def patch_files_folder_disk_path(tmp_path):
    with patch("skylock.utils.storage.FILES_FOLDER_DISK_PATH", tmp_path):
        yield


def test_save_file_data_creates_file(tmp_path):
    data = BytesIO(b"test data")
    filename = "testfile.txt"
    save_file_data(data, filename)

    file_path = tmp_path / filename
    assert file_path.exists()
    assert file_path.read_bytes() == b"test data"


def test_save_file_data_raises_error_if_file_exists(tmp_path):
    data = BytesIO(b"test data")
    filename = "testfile.txt"
    (tmp_path / filename).write_bytes(b"existing data")

    with pytest.raises(ValueError, match="File of given path: .* already exists"):
        save_file_data(data, filename)


def test_get_file_data_returns_file_content(tmp_path):
    filename = "testfile.txt"
    expected_content = b"content data"
    (tmp_path / filename).write_bytes(expected_content)

    data = get_file_data(filename)
    assert data.read() == expected_content


def test_get_file_data_raises_error_if_file_not_found():
    filename = "nonexistentfile.txt"

    with pytest.raises(ValueError, match="File of given path: .* does not exist"):
        get_file_data(filename)


def test_delete_file_data_removes_file(tmp_path):
    filename = "testfile.txt"
    (tmp_path / filename).write_bytes(b"some data")

    delete_file_data(filename)
    assert not (tmp_path / filename).exists()


def test_delete_file_data_raises_error_if_file_not_found():
    filename = "nonexistentfile.txt"

    with pytest.raises(ValueError, match="File of given path: .* does not exist"):
        delete_file_data(filename)
