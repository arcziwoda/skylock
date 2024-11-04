def test_create_folder_at_root(client_with_user):
    response = client_with_user.post('/folders/my_new_folder')
    assert response.status_code == 201
