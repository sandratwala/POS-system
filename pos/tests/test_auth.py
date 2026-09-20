def test_register_success(client):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "role": "cashier"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "user_id" in data
    assert "password" in data


def test_register_duplicate_username(client):
    user_data = {
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "password123",
        "first_name": "Dup",
        "last_name": "User",
        "role": "cashier"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_success(client):
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123",
        "first_name": "Login",
        "last_name": "User",
        "role": "cashier"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post("/auth/login", data={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_wrong_password(client):
    user_data = {
        "username": "wrongpass",
        "email": "wrong@example.com",
        "password": "correctpassword",
        "first_name": "Wrong",
        "last_name": "Pass",
        "role": "cashier"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/login", data={
        "username": "wrongpass",
        "password": "incorrectpassword"
    })
    assert response.status_code == 401