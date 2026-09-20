def test_list_products(client, auth_headers):
    response = client.get("/product/", headers=auth_headers)
    assert response.status_code == 200


def test_create_product(client, auth_headers):
    product_data = {
        "name": "Milkit milk drink",
        "price": 100,
        "quantity": 5
    }
    response = client.post("/product/", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Milkit milk drink"


def test_update_product(client, auth_headers):
    product_data = {
        "name": "Milkit milk drink",
        "price": 100.00,
        "quantity": 5
    }
    response = client.post("/product/", json=product_data, headers=auth_headers)
    product_id = response.json()["product_id"]

    updated_product = {
        "name": "Milkit chocolate drink",
        "price": 120.00,
    }
    response = client.put(f"/product/{product_id}", json=updated_product, headers=auth_headers)
    assert response.json()["name"] == "Milkit chocolate drink"


def test_delete_product(client, auth_headers):
    product_data = {
        "name": "Milkit milk drink",
        "price": 100.00,
        "quantity": 5
    }
    response = client.post("/product/", json=product_data, headers=auth_headers)
    product_id = response.json()["product_id"]

    response = client.delete(f"/product/{product_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/product/{product_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_product_with_missing_name_returns_422(client, auth_headers):
    product_data = {
        "price": 100.00,
        "quantity": 5
    }
    response = client.post("/product/", json=product_data, headers=auth_headers)
    assert response.status_code == 422


def test_get_nonexistent_product_returns_404(client, auth_headers):
    response = client.get("/product/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert response.status_code == 404


def test_create_product_without_login_returns_401(client):
    product_data = {
        "name": "Milkit milk drink",
        "price": 100.00,
        "quantity": 5
    }
    response = client.post("/product/", json=product_data)
    assert response.status_code == 401
