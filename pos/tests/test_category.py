def test_list_categories_empty(client):
    response = client.get("/category/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_category_success(client):
    category_data = {
        "name": "Beverages",
        "description": "Drinks and beverages"
    }
    response = client.post("/category/", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Beverages"
    assert data["description"] == "Drinks and beverages"
    assert "category_id" in data
    assert data["is_active"] == True


def test_create_category_missing_name(client):
    response = client.post("/category/", json={
        "description": "Missing name"
    })
    assert response.status_code == 422


def test_get_category_success(client):
    category_data = {
        "name": "Snacks",
        "description": "Snack items"
    }
    create_response = client.post("/category/", json=category_data)
    category_id = create_response.json()["category_id"]
    
    response = client.get(f"/category/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Snacks"
    assert data["category_id"] == category_id


def test_get_category_not_found(client):
    response = client.get("/category/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_category_success(client):
    category_data = {
        "name": "Original",
        "description": "Original description"
    }
    create_response = client.post("/category/", json=category_data)
    category_id = create_response.json()["category_id"]
    
    update_data = {
        "name": "Updated Category",
        "description": "Updated description"
    }
    response = client.put(f"/category/{category_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Category"
    assert data["description"] == "Updated description"


def test_update_category_not_found(client):
    update_data = {
        "name": "Nonexistent"
    }
    response = client.put("/category/00000000-0000-0000-0000-000000000000", json=update_data)
    assert response.status_code == 404


def test_delete_category_success(client):
    category_data = {
        "name": "To Delete",
        "description": "Will be deleted"
    }
    create_response = client.post("/category/", json=category_data)
    category_id = create_response.json()["category_id"]
    
    response = client.delete(f"/category/{category_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/category/{category_id}")
    assert get_response.status_code == 404


def test_delete_category_not_found(client):
    response = client.delete("/category/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_categories_with_data(client):
    client.post("/category/", json={"name": "Cat1", "description": "Desc1"})
    client.post("/category/", json={"name": "Cat2", "description": "Desc2"})
    
    response = client.get("/category/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Cat1"
    assert data[1]["name"] == "Cat2"