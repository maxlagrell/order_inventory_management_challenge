from app.repositories.inventory_repository import InventoryRepository
from uuid import UUID
from app.exceptions import ProductNotFoundError, InsufficientInventoryError, InvalidInputError, InvalidUUIDFormatError
from app.models import Inventory
from typing import List

class InventoryService:
    def __init__(self):
        self.inventory_repository = InventoryRepository()

    def get_product_or_raise_error(self, product_id: str) -> Inventory:
        product = self.inventory_repository.find_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError
        
        return product

    def get_all_products(self) -> List[Inventory]:
        return self.inventory_repository.find_all_products()
    
    def create_product(
            self,
            product_name: str,
            description: str,
            quantity: int
    ) -> Inventory:
        if not product_name or not description or not quantity:
            raise InvalidInputError
        
        product = self.inventory_repository.create_product(product_name, description, quantity)
        return product
    
    def update_product (
            self,
            product_id: str,
            product_name: str,
            description: str,
            quantity: int
    ) -> Inventory:
        if not product_id or not product_name or not description or not quantity:
            raise InvalidInputError
        
        product = self.inventory_repository.update_product(product_id, product_name, description, quantity)
        return product

    def delete_product(self, product_id: str) -> None:
        self.inventory_repository.delete_product(product_id)
