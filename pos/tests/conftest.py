import os
from urllib import response
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["TESTING"] = "1"

from database import Base, get_db
from main import app


engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False},
    poolclass=StaticPool,)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(client):
    test_user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "role": "cashier"
    }
    response = client.post("/auth/register", json=test_user_data)
    return test_user_data


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login", 
        data={
        "username": test_user["username"],
        "password": test_user["password"]
    }
)

    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def admin_headers(client):
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword",
        "first_name": "Admin",
        "last_name": "User",
        "role": "store_manager"
    }
    client.post("/auth/register", json=admin_data)
    response = client.post(
        "/auth/login", 
        data={
        "username": admin_data["username"],
        "password": admin_data["password"]
    })
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def category_data():
    return {
        "name": "Beverages",
        "description": "Drinks and beverages"
    }


@pytest.fixture
def supplier_data():
    return {
        "company_name": "Test Supplier",
        "contact_name": "John Doe",
        "email": "supplier@example.com",
        "supplier_phone": "1234567890",
        "address": "123 Test Street"
    }


@pytest.fixture
def product_data():
    return {
        "name": "Test Product",
        "price": 10.50,
        "quantity": 100
    }


@pytest.fixture
def customer_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "phone_no": "1234567890",
        "address": "123 Test Street"
    }


@pytest.fixture
def sale_data():
    return {
        "customer_id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "sale_date": "2024-01-01T00:00:00",
        "subtotal": 100.00,
        "tax_amount": 10.00,
        "total_amount": 110.00,
        "status": "completed"
    }


@pytest.fixture
def payment_data():
    return {
        "sale_id": "00000000-0000-0000-0000-000000000000",
        "payment_method": "cash",
        "amount": 110.00,
        "payment_date": "2024-01-01T00:00:00",
        "status": "completed"
    }


@pytest.fixture
def receipt_data():
    return {
        "sale_id": "00000000-0000-0000-0000-000000000000",
        "receipt_number": "RCP-001",
        "receipt_type": "sales_receipt",
        "receipt_data": "Test receipt data"
    }


@pytest.fixture
def sale_item_data():
    return {
        "sale_id": "00000000-0000-0000-0000-000000000000",
        "product_id": "00000000-0000-0000-0000-000000000000",
        "quantity": 2,
        "unit_price": 50.00,
        "total_price": 100.00
    }