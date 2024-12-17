import pytest
from app.services.inventory_service import InventoryService
from app.models import Inventory
from app.repositories.inventory_repository import InventoryRepository
from app.database import inventory
from app.exceptions import ProductNotFoundError, InvalidInputError

@pytest.fixture
def inventory_service():
    """
    Fixture to provide a clean InventoryService instance for each test
    """
    inventory.clear()
    return InventoryService()

@pytest.fixture
def sample_product(inventory_service):
    """
    Fixture to provide a sample product in the inventory
    """
    product = inventory_service.create_product(
        "Test Product",
        "Test Description",
        10
    )
    return product

def test_get_product_or_raise_error(inventory_service, sample_product):
    # Test getting an existing product
    found_product = inventory_service.get_product_or_raise_error(sample_product.product_id)
    assert found_product is not None
    assert found_product.product_name == "Test Product"
    assert found_product.quantity == 10

    # Test getting a non-existent product
    with pytest.raises(ProductNotFoundError):
        inventory_service.get_product_or_raise_error("non-existent-product_id")

def test_get_all_products(inventory_service, sample_product):
    # Test getting all products
    all_products = inventory_service.get_all_products()
    assert len(all_products) == 1
    assert all_products[0].product_name == "Test Product"
    assert all_products[0].quantity == 10

    # Test with empty inventory
    inventory.clear()
    all_products = inventory_service.get_all_products()
    assert len(all_products) == 0

def test_create_product(inventory_service):
    # Test creating a valid product
    product = inventory_service.create_product(
        "New Product",
        "New Description",
        5
    )
    assert product is not None
    assert product.product_name == "New Product"
    assert product.quantity == 5
    assert product.description == "New Description"

    # Test creating product with invalid input
    with pytest.raises(InvalidInputError):
        inventory_service.create_product("", "Description", 5)

    with pytest.raises(InvalidInputError):
        inventory_service.create_product("Product", "", 5)

    with pytest.raises(InvalidInputError):
        inventory_service.create_product("Product", "Description", 0)

def test_update_product(inventory_service, sample_product):
    # Test updating an existing product
    updated_product = inventory_service.update_product(
        sample_product.product_id,
        "Updated Product",
        "Updated Description",
        15
    )
    assert updated_product is not None
    assert updated_product.product_name == "Updated Product"
    assert updated_product.quantity == 15
    assert updated_product.description == "Updated Description"

    # Test updating with inval
    with pytest.raises(InvalidInputError):
        inventory_service.update_product(
            sample_product.product_id,
            "",
            "Updated Description",
            15
        )

def test_delete_product(inventory_service, sample_product):
    # Test deleting an existing product
    inventory_service.delete_product(sample_product.product_id)
    assert sample_product.product_id not in inventory

    # Test deleting a non-existent product
    inventory_service.delete_product("non-existent-product_id")