import pytest
from skylock.utils.path import UserPath
import pdb


@pytest.fixture
def preconfigured_folders(skylock, mock_user):
    user_path_folder1 = UserPath(path="folder1", owner=mock_user)
    user_path_folder2 = UserPath(path="folder2", owner=mock_user)
    user_path_subfolder1 = UserPath(path="folder1/subfolder1", owner=mock_user)
    user_path_subfolder2 = UserPath(path="folder1/subfolder2", owner=mock_user)

    skylock.create_folder_for_user(user_path_folder1)
    skylock.create_folder_for_user(user_path_folder2)
    skylock.create_folder_for_user(user_path_subfolder1)
    skylock.create_folder_for_user(user_path_subfolder2)


# get methods
def test_get_root_folder(client):
    response = client.get("/folders")
    assert response.status_code == 200


