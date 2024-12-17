import pytest
from sanic import response
from app.controllers.inventory_controller import InventoryController
from app.models import Inventory
from app.database import inventory
from app.exceptions import InvalidInputError, ProductNotFoundError, InvalidContentTypeError
import json

class MockRequest:
    def __init__(self, json_data=None, headers=None):
        self.json = json_data
        self.headers = headers or {}

@pytest.fixture
def inventory_controller():
    """
    Fixture to provide a clean InventoryController instance for each test
    """
    inventory.clear()
    return InventoryController()

@pytest.fixture
def sample_product(inventory_controller):
    """
    Fixture to provide a sample product in the inventory
    """
    request = MockRequest(
        json_data={
            "name": "Test Product",
            "description": "Test Description",
            "quantity": 10
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    response = inventory_controller.create_product(request)
    return json.loads(response.body.decode())

def test_get_product(inventory_controller, sample_product):
    # Test getting existing product
    product_id = sample_product["product_id"]
    request = MockRequest()
    response = inventory_controller.get_product(request, product_id)

    assert response.status == 200
    response_data = json.loads(response.body.decode())
    assert response_data["product_name"] == "Test Product"
    assert response_data["quantity"] == 10

    # Test getting non-existent product
    response = inventory_controller.get_product(request, "non-existent-product_id")
    assert response.status == 404
    # Get new response data for the error case
    error_response_data = json.loads(response.body.decode())
    assert error_response_data["error"] == ProductNotFoundError().message

def test_get_all_products(inventory_controller, sample_product):
    # Test getting all products
    request = MockRequest()
    response = inventory_controller.get_all_products(request)

    assert response.status == 200
    response_data = json.loads(response.body.decode())
    assert len(response_data) == 1
    assert response_data[0]["product_name"] == "Test Product"
    assert response_data[0]["quantity"] == 10

def test_create_product(inventory_controller):
    # Test successful product creation
    request = MockRequest(
        json_data={
            "name": "Test Product",
            "description": "Test Description",
            "quantity": 5
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    response = inventory_controller.create_product(request)
    
    assert response.status == 201
    response_data = json.loads(response.body.decode())
    assert response_data["product_name"] == "Test Product"
    assert response_data["quantity"] == 5

    # Test invalid content type
    request = MockRequest(
        json_data={
            "name": "Test Product",
            "description": "Test Description",
            "quantity": 5
        },
        headers={
            "Content-Type": "text/plain"
        }
    )
    response = inventory_controller.create_product(request)
    assert response.status == 415
    response_data = json.loads(response.body.decode())
    assert response_data["error"] == InvalidContentTypeError().message

def test_update_product(inventory_controller, sample_product):
    # Test successful product update
    product_id = sample_product["product_id"]
    request = MockRequest(
        json_data={
            "name": "Updated Product",
            "description": "Updated Description",
            "quantity": 15
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    response = inventory_controller.update_product(request, product_id)

    assert response.status == 200
    response_data = json.loads(response.body.decode())
    assert response_data["product_name"] == "Updated Product"
    assert response_data["quantity"] == 15

    # Test invalid content type
    request = MockRequest(
        json_data={
            "name": "Updated Product",
            "description": "Updated Description",
            "quantity": 15
        },
        headers={
            "Content-Type": "text/plain"
        }
    )
    response = inventory_controller.update_product(request, product_id)
    assert response.status == 415
    response_data = json.loads(response.body.decode())
    assert response_data["error"] == InvalidContentTypeError().message

    # Test missing required fields
    request = MockRequest(
        json_data={
            "name": "Updated Product",
            "quantity": 15
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    response = inventory_controller.update_product(request, product_id)
    assert response.status == 400
    response_data = json.loads(response.body.decode())
    assert response_data["error"] == InvalidInputError().message

def test_delete_product(inventory_controller, sample_product):
    # Test successful product deletion
    product_id = sample_product["product_id"]
    request = MockRequest()
    response = inventory_controller.delete_product(request, product_id)

    assert response.status == 200
    response_data = json.loads(response.body.decode())
    assert response_data["message"] == "Product deleted successfully"

    # Verify product is deleted
    response = inventory_controller.get_product(request, product_id)
    assert response.status == 404
    response_data = json.loads(response.body.decode())
    assert response_data["error"] == ProductNotFoundError().message