MOCK_USERNAME = "mockuser"
MOCK_PASSWORD = "mockpasswd"


def test_create_folder_at_root(client, token):
    response = client.post(
        "/folders/bla/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201


def test_get_root_folder(client, token):
    response = client.get("/folders", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
