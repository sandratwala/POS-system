import uuid

MOCK_CUSTOMER_ID = "db2d18e3b51743ffb55256285759cd9a"
MOCK_USER_ID = "a1b2c3d4e5f67a8b9c0d1e2f3a4b5c6d"

def test_list_sales_empty(client):
    response = client.get("/sale/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_sale_success(client):
    sale_data = {
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00,
        "tax_amount": 10.00,
        "total_amount": 110.00,
        "status": "completed"
    }
    response = client.post("/sale/", json=sale_data)
    assert response.status_code == 201
    data = response.json()
    assert float(data["subtotal"]) == 100.00
    assert float(data["tax_amount"]) == 10.00
    assert float(data["total_amount"]) == 110.00
    assert data["status"] == "completed"
    assert "sale_id" in data


def test_create_sale_missing_fields(client):
    response = client.post("/sale/", json={
        "subtotal": 100.00
    })
    assert response.status_code == 422


def test_get_sale_success(client):
    sale_data = {
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 200.00,
        "tax_amount": 20.00,
        "total_amount": 220.00,
        "status": "completed"
    }
    create_response = client.post("/sale/", json=sale_data)
    sale_id = create_response.json()["sale_id"]
    
    response = client.get(f"/sale/{sale_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["sale_id"] == sale_id
    assert float(data["subtotal"]) == 200.00


def test_get_sale_not_found(client):
    random_uuid = str(uuid.uuid4())
    response = client.get(f"/sale/{random_uuid}")
    assert response.status_code == 404


def test_update_sale_success(client):
    sale_data = {
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00,
        "tax_amount": 10.00,
        "total_amount": 110.00,
        "status": "completed"
    }
    create_response = client.post("/sale/", json=sale_data)
    sale_id = create_response.json()["sale_id"]
    
    update_data = {
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "tax_amount": 15.00,
        "subtotal": 150.00,
        "total_amount": 165.00,
        "status": "cancelled"
    }
    response = client.put(f"/sale/{sale_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert float(data["subtotal"]) == 150.00
    assert float(data["total_amount"]) == 165.00
    assert data["status"] == "cancelled"


def test_update_sale_not_found(client):
    random_uuid = str(uuid.uuid4())
    update_data = {
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "tax_amount": 10.00,
        "subtotal": 150.00,
        "total_amount": 165.00,
        "status": "cancelled"
    }
    response = client.put(f"/sale/{random_uuid}", json=update_data)
    assert response.status_code == 404


def test_delete_sale_success(client):
    sale_data = {
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00,
        "tax_amount": 10.00,
        "total_amount": 110.00,
        "status": "completed"
    }
    create_response = client.post("/sale/", json=sale_data)
    sale_id = create_response.json()["sale_id"]
    
    response = client.delete(f"/sale/{sale_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/sale/{sale_id}")
    assert get_response.status_code == 404


def test_delete_sale_not_found(client):
    random_uuid = str(uuid.uuid4())
    response = client.delete(f"/sale/{random_uuid}")
    assert response.status_code == 404


def test_list_sales_with_data(client):
    client.post("/sale/", json={
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00,
        "tax_amount": 10.00,
        "total_amount": 110.00,
        "status": "completed"
    })
    client.post("/sale/", json={
        "customer_id": MOCK_CUSTOMER_ID,
        "user_id": MOCK_USER_ID,
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 200.00,
        "tax_amount": 20.00,
        "total_amount": 220.00,
        "status": "completed"
    })
    
    response = client.get("/sale/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
