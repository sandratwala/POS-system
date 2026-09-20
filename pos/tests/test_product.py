def test_list_products_empty(client, auth_headers):
    response = client.get("/product/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_create_product_success(client, auth_headers):
    product_data = {
        "name": "Test Product",
        "price": 10.50,
        "quantity": 100
    }
    response = client.post("/product/", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == "10.50"
    assert data["quantity"] == 100
    assert "product_id" in data
    assert data["is_active"] == True


def test_create_product_missing_name(client, auth_headers):
    response = client.post("/product/", json={
        "price": 10.50,
        "quantity": 100
    }, headers=auth_headers)
    assert response.status_code == 422


def test_create_product_missing_price(client, auth_headers):
    response = client.post("/product/", json={
        "name": "Test Product",
        "quantity": 100
    }, headers=auth_headers)
    assert response.status_code == 422


def test_create_product_missing_quantity(client, auth_headers):
    response = client.post("/product/", json={
        "name": "Test Product",
        "price": 10.50
    }, headers=auth_headers)
    assert response.status_code == 422


def test_get_product_success(client, auth_headers):
    product_data = {
        "name": "Get Product",
        "price": 20.00,
        "quantity": 50
    }
    create_response = client.post("/product/", json=product_data, headers=auth_headers)
    product_id = create_response.json()["product_id"]
    
    response = client.get(f"/product/{product_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Get Product"
    assert data["product_id"] == product_id


def test_get_product_not_found(client, auth_headers):
    response = client.get("/product/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert response.status_code == 404


def test_update_product_success(client, auth_headers):
    product_data = {
        "name": "Original Product",
        "price": 10.00,
        "quantity": 10
    }
    create_response = client.post("/product/", json=product_data, headers=auth_headers)
    product_id = create_response.json()["product_id"]
    
    update_data = {
        "name": "Updated Product",
        "price": 15.00
    }
    response = client.put(f"/product/{product_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == "15.00"


def test_update_product_not_found(client, auth_headers):
    update_data = {
        "name": "Nonexistent"
    }
    response = client.put("/product/00000000-0000-0000-0000-000000000000", json=update_data, headers=auth_headers)
    assert response.status_code == 404


def test_delete_product_success(client, auth_headers):
    product_data = {
        "name": "To Delete",
        "price": 5.00,
        "quantity": 5
    }
    create_response = client.post("/product/", json=product_data, headers=auth_headers)
    product_id = create_response.json()["product_id"]
    
    response = client.delete(f"/product/{product_id}", headers=auth_headers)
    assert response.status_code == 204
    
    get_response = client.get(f"/product/{product_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_product_not_found(client, auth_headers):
    response = client.delete("/product/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert response.status_code == 404


def test_list_products_with_data(client, auth_headers):
    client.post("/product/", json={"name": "Prod1", "price": 10.00, "quantity": 10}, headers=auth_headers)
    client.post("/product/", json={"name": "Prod2", "price": 20.00, "quantity": 20}, headers=auth_headers)
    
    response = client.get("/product/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_product_without_auth(client):
    response = client.post("/product/", json={
        "name": "Test",
        "price": 10.00,
        "quantity": 10
    })
    assert response.status_code == 401