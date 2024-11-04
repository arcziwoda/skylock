def test_create_folder_at_root(client):
    response = client.get('/folders/')
    assert response.status_code == 201
