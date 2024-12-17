import pytest
from app.models import Inventory
from app.repositories.inventory_repository import InventoryRepository
from app.database import inventory

@pytest.fixture
def inventory_repository():
    """
    Fixture to provide a clean InventoryRepository instance for each test
    """
    inventory.clear()
    return InventoryRepository()

@pytest.fixture
def sample_product(inventory_repository):
    """
    Fixture to provide a sample product in the inventory
    """
    product = Inventory("Test Product", "Test Description", 10)
    inventory[product.product_id] = product
    return product

def test_find_product_by_id(inventory_repository, sample_product):
    # Test fnding product by product_id
    found_product = inventory_repository.find_product_by_id(sample_product.product_id)
    assert found_product is not None
    assert found_product.product_name == "Test Product"
    assert found_product.quantity == 10

    # Test finding non-existent product
    non_existent_product = inventory_repository.find_product_by_id("non-existent-product")
    assert non_existent_product is None

def test_find_all_products(inventory_repository, sample_product):
    # Test with empty inventory
    inventory.clear()
    all_products = inventory_repository.find_all_products()
    assert len(all_products) == 0

    # Add the sample product back to inventory
    inventory[sample_product.product_id] = sample_product

    # Test with one product
    all_products = inventory_repository.find_all_products()
    assert len(all_products) == 1
    assert all_products[0].product_name == "Test Product"
    assert all_products[0].quantity == 10

def test_create_product(inventory_repository):
    # Test creating a new product
    new_product = inventory_repository.create_product(
        "New Product",
        "New Description",
        5
    )
    assert new_product is not None
    assert new_product.product_name == "New Product"
    assert new_product.quantity == 5
    assert new_product.description == "New Description"

    # Verify that the product was added to the inventory
    assert new_product.product_id in inventory

def test_update_product(inventory_repository, sample_product):
    # Test updating existing product
    updated_product = inventory_repository.update_product(
        sample_product.product_id,
        "Updated Product",
        "Updated Description",
        15
    )
    
    assert updated_product is not None
    assert updated_product.product_name == "Updated Product"
    assert updated_product.quantity == 15
    assert updated_product.description == "Updated Description"

    # Test updating non-existent product
    result = inventory_repository.update_product(
        "non-existent-product_id",
        "Updated Product",
        "Updated Description",
        15
    )
    assert result is None

def test_delete_product(inventory_repository, sample_product):
    # Test deleting existing product
    deleted_product = inventory_repository.delete_product(sample_product.product_id)
    assert deleted_product is not None
    assert deleted_product.product_name == "Test Product"

    # Verify product was removed from inventory
    assert sample_product.product_id not in inventory

    # Test deleting non-existent product
    result = inventory_repository.delete_product("non-existent-product_id")
    assert result is None