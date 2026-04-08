def test_register_new_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data

def test_login_user(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "securepassword"
        }
    )
    # Now login (OAuth2PasswordRequestForm expects username and password form fields)
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login User 2",
            "email": "login2@example.com",
            "password": "securepassword"
        }
    )
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login2@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 400
