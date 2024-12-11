import pytest
import uuid
from skylock.utils.storage import FileStorageService
from skylock.database.models import FileEntity, FolderEntity, UserEntity


@pytest.fixture
def temp_storage_service(tmp_path):
    return FileStorageService(storage_path=tmp_path)


@pytest.fixture
def test_user():
    return UserEntity(id=str(uuid.uuid4()), username="test_user", password="password")


@pytest.fixture
def test_folder(test_user):
    return FolderEntity(id=str(uuid.uuid4()), name="test_folder", owner=test_user)


@pytest.fixture
def test_file(test_folder, test_user):
    """Fixture to create a test file entity."""
    return FileEntity(
        id=str(uuid.uuid4()), name="test_file.txt", folder=test_folder, owner=test_user
    )


def test_save_file(temp_storage_service, test_file):
    """Test saving a file to storage."""
    data = b"This is test file content"

    temp_storage_service.save_file(data, test_file)

    expected_path = temp_storage_service.storage_path / test_file.id
    assert expected_path.exists()
    assert expected_path.read_bytes() == data


def test_get_file(temp_storage_service, test_file):
    data = b"This is test file content"

    temp_storage_service.save_file(data, test_file)

    file_stream = temp_storage_service.get_file(test_file)
    assert file_stream.read() == data


def test_delete_file(temp_storage_service, test_file):
    data = b"This is test file content"

    temp_storage_service.save_file(data, test_file)

    temp_storage_service.delete_file(test_file)

    expected_path = temp_storage_service.storage_path / test_file.id
    assert not expected_path.exists()


def test_save_existing_file_raises_error(temp_storage_service, test_file):
    """Test saving a file with the same name raises an error."""
    data = b"This is test file content"

    temp_storage_service.save_file(data, test_file)

    with pytest.raises(ValueError, match="File of given path: .* already exists"):
        temp_storage_service.save_file(data, test_file)


def test_get_nonexistent_file_raises_error(temp_storage_service, test_file):
    """Test retrieving a nonexistent file raises an error."""
    with pytest.raises(ValueError, match="File of given path: .* does not exist"):
        temp_storage_service.get_file(test_file)


def test_delete_nonexistent_file_raises_error(temp_storage_service, test_file):
    """Test deleting a nonexistent file raises an error."""
    with pytest.raises(ValueError, match="File of given path: .* does not exist"):
        temp_storage_service.delete_file(test_file)
