import uuid

MOCK_SALE_ID = "c27ee8c296f04db59948ba358c965ac9"

def test_list_payments_empty(client):
    response = client.get("/payment/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_payment_success(client):
    payment_data = {
        "sale_id": MOCK_SALE_ID,
        "payment_method": "cash",
        "amount": 100.00,
        "payment_date": "2024-01-01T00:00:00Z",
        "status": "completed"
    }
    response = client.post("/payment/", json=payment_data)
    assert response.status_code == 201
    data = response.json()
    assert data["payment_method"] == "cash"
    assert float(data["amount"]) == 100.00
    assert data["status"] == "completed"
    assert "payment_id" in data


def test_create_payment_missing_fields(client):
    response = client.post("/payment/", json={
        "amount": 100.00
    })
    assert response.status_code == 422


def test_get_payment_success(client):
    payment_data = {
        "sale_id": MOCK_SALE_ID,
        "payment_method": "credit_card",
        "amount": 200.00,
        "payment_date": "2024-01-01T00:00:00Z",
        "status": "completed"
    }
    create_response = client.post("/payment/", json=payment_data)
    payment_id = create_response.json()["payment_id"]
    
    response = client.get(f"/payment/{payment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["payment_id"] == payment_id
    assert data["payment_method"] == "credit_card"


def test_get_payment_not_found(client):
    random_uuid = str(uuid.uuid4())
    response = client.get(f"/payment/{random_uuid}")
    assert response.status_code == 404


def test_update_payment_success(client):
    payment_data = {
        "sale_id": MOCK_SALE_ID,
        "payment_method": "cash",
        "amount": 100.00,
        "payment_date": "2024-01-01T00:00:00Z",
        "status": "completed"
    }
    create_response = client.post("/payment/", json=payment_data)
    payment_id = create_response.json()["payment_id"]
    update_data = {
        "sale_id": MOCK_SALE_ID,
        "payment_method": "cash",
        "payment_date": "2024-01-01T00:00:00Z",
        "amount": 150.00,
        "status": "refunded"
    }
    response = client.put(f"/payment/{payment_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert float(data["amount"]) == 150.00
    assert data["status"] == "refunded"


def test_update_payment_not_found(client):
    random_uuid = str(uuid.uuid4())
    update_data = {
        "sale_id": MOCK_SALE_ID,
        "payment_method": "cash",
        "payment_date": "2024-01-01T00:00:00Z",
        "amount": 150.00,
        "status": "refunded"
    }
    response = client.put(f"/payment/{random_uuid}", json=update_data)
    assert response.status_code == 404


def test_delete_payment_success(client):
    payment_data = {
        "sale_id": MOCK_SALE_ID,
        "payment_method": "cash",
        "amount": 100.00,
        "payment_date": "2024-01-01T00:00:00Z",
        "status": "completed"
    }
    create_response = client.post("/payment/", json=payment_data)
    payment_id = create_response.json()["payment_id"]
    
    response = client.delete(f"/payment/{payment_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/payment/{payment_id}")
    assert get_response.status_code == 404


def test_delete_payment_not_found(client):
    random_uuid = str(uuid.uuid4())
    response = client.delete(f"/payment/{random_uuid}")
    assert response.status_code == 404


def test_list_payments_with_data(client):
    client.post("/payment/", json={
        "sale_id": MOCK_SALE_ID,
        "payment_method": "cash",
        "amount": 100.00,
        "payment_date": "2024-01-01T00:00:00Z",
        "status": "completed"
    })
    client.post("/payment/", json={
        "sale_id": MOCK_SALE_ID,
        "payment_method": "credit_card",
        "amount": 200.00,
        "payment_date": "2024-01-01T00:00:00Z",
        "status": "completed"
    })
    
    response = client.get("/payment/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
