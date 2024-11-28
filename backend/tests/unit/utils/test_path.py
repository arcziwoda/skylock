import pytest
from skylock.database.models import UserEntity
from skylock.utils.path import UserPath
from skylock.utils.exceptions import ForbiddenActionException, InvalidPathException


def test_user_path_initialization():
    user = UserEntity(id=1, username="testuser")
    path = "some/path"
    user_path = UserPath(path=path, owner=user)

    assert user_path.path == "some/path"
    assert user_path.owner == user
    assert user_path.root_folder_name == 1
    assert user_path.parts == ("some", "path")
    assert user_path.name == "path"


def test_user_path_root_folder_of_initialization():
    user = UserEntity(id=1, username="testuser")
    user_path = UserPath.root_folder_of(owner=user)

    assert user_path.is_root_folder() is True
    assert user_path.path == ""
    assert user_path.owner == user


def test_user_path_root_folder():
    user = UserEntity(id=1, username="testuser")
    path = ""
    user_path = UserPath(path=path, owner=user)

    assert user_path.is_root_folder() is True


def test_user_path_parent():
    user = UserEntity(id=1, username="testuser")
    path = "some/path"
    user_path = UserPath(path=path, owner=user)
    parent_path = user_path.parent

    assert parent_path.path == "some"
    assert parent_path.owner == user


def test_user_path_parent_root_folder():
    user = UserEntity(id=1, username="testuser")
    path = ""
    user_path = UserPath(path=path, owner=user)

    with pytest.raises(ForbiddenActionException):
        user_path.parent


def test_user_path_invalid_length():
    user = UserEntity(id=1, username="testuser")
    path = "a" * 256

    with pytest.raises(InvalidPathException):
        UserPath(path=path, owner=user)


def test_user_path_absolute_path():
    user = UserEntity(id=1, username="testuser")
    path = "/absolute/path"
    user_path = UserPath(path=path, owner=user)

    assert user_path.path == "absolute/path"


def test_user_path_proper_file_name():
    user = UserEntity(id=1, username="testuser")
    path = "file.txt"
    user_path = UserPath(path=path, owner=user)

    assert user_path.path == "file.txt"
