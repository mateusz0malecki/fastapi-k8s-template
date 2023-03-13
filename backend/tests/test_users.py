import pytest
from settings import get_settings

app_settings = get_settings()


@pytest.mark.xfail
def test_empty_db_users(client):
    response = client.get(f'{app_settings.root_path}/users')
    assert len(response.json()["records"]) > 0


def test_get_users_admin(client):
    data = {
        "email": "test@test.com",
        "password": "password123",
        "repeatPassword": "password123"
    }
    client.post(f'{app_settings.root_path}/register', json=data)
    response = client.get(f'{app_settings.root_path}/users')
    assert response.status_code == 200
    assert len(response.json()["records"]) == 1


def test_edit_admin_status(client):
    user_id = (client.get(f'{app_settings.root_path}/users')).json()["records"][0]["userId"]
    response = client.patch(f'{app_settings.root_path}/users/{user_id}/admin')
    assert response.status_code == 202
    assert response.json()["isAdmin"] is True


def test_deactivate_user(client):
    user_id = (client.get(f'{app_settings.root_path}/users')).json()["records"][0]["userId"]
    response = client.patch(f'{app_settings.root_path}/users/{user_id}/deactivate')
    assert response.status_code == 202
    assert response.json()["isActive"] is False
    assert response.json()["isAdmin"] is False
    assert response.json()["email"] == ""


def test_get_users(client, register_users):
    response = client.get(f'{app_settings.root_path}/users')
    assert response.status_code == 200
    assert len(response.json()["records"]) == 2


def test_get_myself(client):
    response = client.get(f'{app_settings.root_path}/users/me')
    assert response.status_code == 200
    assert response.json()["email"] == "email@email.com"
    assert response.json()["isAdmin"] is False


def test_edit_myself(client):
    data = {
        "password": "string123",
        "repeatPassword": "string123",
        "email": "user@example.com"
    }
    response = client.put(f'{app_settings.root_path}/users/me', json=data)
    assert response.status_code == 202
    assert response.json()["email"] == "user@example.com"


def test_edit_myself_fail(client):
    data = {
        # password do not match
        "password": "string123",
        "repeatPassword": "string1234"
    }
    response = client.put(f'{app_settings.root_path}/users/me', json=data)
    assert response.status_code == 422
    data = {
        # wrong password pattern
        "password": "string",
        "repeatPassword": "string"
    }
    response = client.put(f'{app_settings.root_path}/users/me', json=data)
    assert response.status_code == 422
    # wrong email pattern
    response = client.put(f'{app_settings.root_path}/users/me', json={"email": "example.com"})
    assert response.status_code == 422
    # wrong email pattern
    response = client.put(f'{app_settings.root_path}/users/me', json={"email": "user@example"})
    assert response.status_code == 422
