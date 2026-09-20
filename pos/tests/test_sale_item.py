import uuid

def test_list_sale_items_empty(client):
    response = client.get("/sale-item/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_sale_item_success(client, auth_headers):
    customer_data = {"first_name": "John", "last_name": "Mwamba", "phone_no": "1234567890"}
    cust_resp = client.post("/customer/", json=customer_data)
    customer_id = cust_resp.json()["customer_id"]

    sale_data = {
        "customer_id": customer_id,
        "user_id": str(uuid.uuid4()),
        "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00,
        "tax_amount": 10.00,
        "total_amount": 110.00,
        "status": "completed"
    }
    sale_resp = client.post("/sale/", json=sale_data)
    sale_id = sale_resp.json()["sale_id"]

    product_data = {"name": "Milkit milk drink", "price": 50.00, "quantity": 10}
    prod_resp = client.post("/product/", json=product_data, headers=auth_headers)
    product_id = prod_resp.json()["product_id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": 50.00,
        "total_price": 100.00
    }
    response = client.post("/sale-item/", json=sale_item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["sale_id"] == sale_id
    assert data["product_id"] == product_id


def test_get_sale_item_success(client, auth_headers):
    cust_resp = client.post("/customer/", json={"first_name": "John", "last_name": "Mwamba"})
    customer_id = cust_resp.json()["customer_id"]
    
    sale_resp = client.post("/sale/", json={
        "customer_id": customer_id, "user_id": str(uuid.uuid4()), "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00, "tax_amount": 10.00, "total_amount": 110.00, "status": "completed"
    })
    sale_id = sale_resp.json()["sale_id"]
    
    prod_resp = client.post("/product/", json={"name": "Milkit", "price": 40.00, "quantity": 10}, headers=auth_headers)
    product_id = prod_resp.json()["product_id"]

    sale_item_data = {
        "sale_id": sale_id, "product_id": product_id, "quantity": 3, "unit_price": 40.00, "total_price": 120.00
    }
    create_response = client.post("/sale-item/", json=sale_item_data)
    data = create_response.json()
    sale_item_id = data.get("sale_item_id") or data.get("id")
    
    response = client.get(f"/sale-item/{sale_item_id}")
    assert response.status_code == 200
    assert int(response.json()["quantity"]) == 3


def test_update_sale_item_success(client, auth_headers):
    cust_resp = client.post("/customer/", json={"first_name": "John", "last_name": "Mwamba"})
    customer_id = cust_resp.json()["customer_id"]
    
    sale_resp = client.post("/sale/", json={
        "customer_id": customer_id, "user_id": str(uuid.uuid4()), "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00, "tax_amount": 10.00, "total_amount": 110.00, "status": "completed"
    })
    sale_id = sale_resp.json()["sale_id"]
    
    prod_resp = client.post("/product/", json={"name": "Milkit", "price": 50.00, "quantity": 10}, headers=auth_headers)
    product_id = prod_resp.json()["product_id"]

    sale_item_data = {
        "sale_id": sale_id, "product_id": product_id, "quantity": 2, "unit_price": 50.00, "total_price": 100.00
    }
    create_response = client.post("/sale-item/", json=sale_item_data)
    sale_item_id = create_response.json().get("sale_item_id") or create_response.json().get("id")
    
    update_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 5,
        "unit_price": 50.00,
        "total_price": 250.00
    }
    response = client.put(f"/sale-item/{sale_item_id}", json=update_data)
    assert response.status_code == 200
    assert int(response.json()["quantity"]) == 5


def test_delete_sale_item_success(client, auth_headers):
    cust_resp = client.post("/customer/", json={"first_name": "John", "last_name": "Mwamba"})
    customer_id = cust_resp.json()["customer_id"]
    
    sale_resp = client.post("/sale/", json={
        "customer_id": customer_id, "user_id": str(uuid.uuid4()), "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00, "tax_amount": 10.00, "total_amount": 110.00, "status": "completed"
    })
    sale_id = sale_resp.json()["sale_id"]
    
    prod_resp = client.post("/product/", json={"name": "Milkit", "price": 10.00, "quantity": 10}, headers=auth_headers)
    product_id = prod_resp.json()["product_id"]

    sale_item_data = {
        "sale_id": sale_id, "product_id": product_id, "quantity": 1, "unit_price": 10.00, "total_price": 10.00
    }
    create_response = client.post("/sale-item/", json=sale_item_data)
    sale_item_id = create_response.json().get("sale_item_id") or create_response.json().get("id")
    
    response = client.delete(f"/sale-item/{sale_item_id}")
    assert response.status_code == 204


def test_list_sale_items_with_data(client, auth_headers):
    cust_resp = client.post("/customer/", json={"first_name": "John", "last_name": "Mwamba"})
    customer_id = cust_resp.json()["customer_id"]
    
    sale_resp = client.post("/sale/", json={
        "customer_id": customer_id, "user_id": str(uuid.uuid4()), "sale_date": "2024-01-01T00:00:00Z",
        "subtotal": 100.00, "tax_amount": 10.00, "total_amount": 110.00, "status": "completed"
    })
    sale_id = sale_resp.json()["sale_id"]
    
    prod_resp = client.post("/product/", json={"name": "Milkit", "price": 10.00, "quantity": 10}, headers=auth_headers)
    product_id = prod_resp.json()["product_id"]

    client.post("/sale-item/", json={
        "sale_id": sale_id, "product_id": product_id, "quantity": 1, "unit_price": 10.00, "total_price": 10.00
    })
    
    response = client.get("/sale-item/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
