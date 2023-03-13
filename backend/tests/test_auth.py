from settings import get_settings

app_settings = get_settings()


def test_register(client):
    data = {
        "email": "email@email.com",
        "password": "password123",
        "repeatPassword": "password123"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "email@email.com"


def test_login(client):
    response = client.post(
        f'{app_settings.root_path}/login',
        data={
            "username": "email@email.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert len(response.json()["access_token"]) == 137


def test_login_fail(client):
    response = client.post(
        f'{app_settings.root_path}/login',
        data={
            "username": "error@error.com",
            "password": "error123"
        }
    )
    assert response.status_code == 401


def test_register_fail(client):
    data = {
        # lacking "repeatPassword"
        "email": "email@email.com",
        "password": "password123"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 422
    data = {
        # using already used email
        "email": "email@email.com",
        "password": "password123",
        "repeatPassword": "password123"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 400
    data = {
        # password without any number
        "email": "email@email.com",
        "password": "password",
        "repeatPassword": "password"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 422
    data = {
        # password without any letter
        "email": "email@email.com",
        "password": "123456789",
        "repeatPassword": "123456789"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 422
    data = {
        # wrong email pattern
        "email": "email.com",
        "password": "string123",
        "repeatPassword": "string123"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 422
    data = {
        # wrong email pattern
        "email": "email@email",
        "password": "string123",
        "repeatPassword": "string123"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 422
    data = {
        # password do not match
        "email": "test@email.com",
        "password": "string123",
        "repeatPassword": "string1234"
    }
    response = client.post(f'{app_settings.root_path}/register', json=data)
    assert response.status_code == 422
