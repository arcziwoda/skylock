import pytest
from skylock.utils.path import UserPath


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


def test_get_folder_not_found(client):
    response = client.get("/folders/missing_folder")
    assert response.status_code == 404


def test_get_nested_folder(client, preconfigured_folders):
    response = client.get("/folders/folder1")
    assert response.status_code == 200
    assert len(response.json()["folders"]) == 2
    assert response.json()["folders"][0]["name"] == "subfolder1"
    assert response.json()["folders"][0]["path"] == "/folder1/subfolder1"
    assert response.json()["folders"][1]["name"] == "subfolder2"
    assert response.json()["folders"][1]["path"] == "/folder1/subfolder2"


# post methods
def test_create_folder_at_root_success(client):
    response = client.post("/folders/folder1/")
    assert response.status_code == 201


def test_create_folder_with_existing_name(client, preconfigured_folders):
    response = client.post("/folders/folder1/")
    assert response.status_code == 409


def test_create_subfolder_in_nonexistent_folder(client):
    response = client.post("/folders/folder1/subfolder1")
    assert response.status_code == 404


def test_create_nested_folder(client, preconfigured_folders):
    response = client.post("/folders/folder1/subfolder1/test_folder")
    assert response.status_code == 201


def test_create_folder_empty_path(client, preconfigured_folders):
    response = client.post("/folders")
    assert response.status_code == 400


# delete methods
def test_delete_folder(client, preconfigured_folders):
    response = client.delete("/folders/folder2")
    assert response.status_code == 204


def test_delete_folder_not_empty(client, preconfigured_folders):
    response = client.delete("/folders/folder1")
    assert response.status_code == 409


def test_delete_not_found(client):
    response = client.delete("/folders/invalid_folder")
    assert response.status_code == 404
