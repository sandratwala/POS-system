import uuid

MOCK_SALE_ID = "c27ee8c296f04db59948ba358c965ac9"

def test_list_receipts_empty(client):
    response = client.get("/receipt/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_receipt_success(client):
    receipt_data = {
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-001",
        "receipt_type": "sales_receipt",
        "receipt_data": "Test receipt data"
    }
    response = client.post("/receipt/", json=receipt_data)
    assert response.status_code == 201
    data = response.json()
    assert data["receipt_number"] == "RCP-001"
    assert data["receipt_type"] == "sales_receipt"
    assert "receipt_id" in data


def test_create_receipt_missing_fields(client):
    response = client.post("/receipt/", json={
        "receipt_number": "RCP-001"
    })
    assert response.status_code == 422


def test_get_receipt_success(client):
    receipt_data = {
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-002",
        "receipt_type": "sales_receipt",
        "receipt_data": "Test receipt data"
    }
    create_response = client.post("/receipt/", json=receipt_data)
    receipt_id = create_response.json()["receipt_id"]
    
    response = client.get(f"/receipt/{receipt_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["receipt_id"] == receipt_id
    assert data["receipt_number"] == "RCP-002"


def test_get_receipt_not_found(client):
    random_uuid = str(uuid.uuid4())
    response = client.get(f"/receipt/{random_uuid}")
    assert response.status_code == 404


def test_update_receipt_success(client):
    receipt_data = {
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-003",
        "receipt_type": "sales_receipt",
        "receipt_data": "Original data"
    }
    create_response = client.post("/receipt/", json=receipt_data)
    receipt_id = create_response.json()["receipt_id"]
    
    update_data = {
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-004",
        "receipt_type": "sales_receipt",
        "receipt_data": "Updated data"
    }
    response = client.put(f"/receipt/{receipt_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["receipt_number"] == "RCP-004"
    assert data["receipt_data"] == "Updated data"


def test_update_receipt_not_found(client):
    random_uuid = str(uuid.uuid4())
    update_data = {
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-999",
        "receipt_type": "sales_receipt",
        "receipt_data": "Updated data"
    }
    response = client.put(f"/receipt/{random_uuid}", json=update_data)
    assert response.status_code == 404


def test_delete_receipt_success(client):
    receipt_data = {
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-005",
        "receipt_type": "sales_receipt",
        "receipt_data": "To be deleted"
    }
    create_response = client.post("/receipt/", json=receipt_data)
    receipt_id = create_response.json()["receipt_id"]
    
    response = client.delete(f"/receipt/{receipt_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/receipt/{receipt_id}")
    assert get_response.status_code == 404


def test_delete_receipt_not_found(client):
    random_uuid = str(uuid.uuid4())
    response = client.delete(f"/receipt/{random_uuid}")
    assert response.status_code == 404


def test_list_receipts_with_data(client):
    client.post("/receipt/", json={
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-006",
        "receipt_type": "sales_receipt",
        "receipt_data": "Receipt 1"
    })
    client.post("/receipt/", json={
        "sale_id": MOCK_SALE_ID,
        "receipt_number": "RCP-007",
        "receipt_type": "sales_receipt",
        "receipt_data": "Receipt 2"
    })
    
    response = client.get("/receipt/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
