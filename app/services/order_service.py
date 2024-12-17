from repositories.order_repository import OrderRepository
from models import Order
from exceptions import InvalidInputError, InvalidUUIDFormatError, InsufficientInventoryError, OrderNotFoundError, UserNotFoundError, ProductNotFoundError
from services.inventory_service import InventoryService
from typing import List
from uuid import UUID

class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.inventory_service = InventoryService()

    def get_order_or_raise_error(self, order_id: str) -> Order:

        
        order = self.order_repository.find_order_by_id(order_id)
        if not order:
            raise OrderNotFoundError
        
        return order

    def get_all_orders_for_user(self, user_id: str) -> List[Order]:
        return self.order_repository.find_all_orders_for_user(user_id)

    def create_order(
            self,
            product_id: str,
            user_id: str,
            quantity: int
    ) -> Order:
        try:
            # Validate inputs
            UUID(product_id)
            if not isinstance(quantity, int) or quantity <= 0:
                raise InvalidInputError

            # Check product availability
            product = self.inventory_service.get_product_or_raise_error(product_id)
            if product.quantity < quantity:
                raise InsufficientInventoryError

            # Start transaction-like operation
            order = None
            try:
                # First create the order
                order = self.order_repository.create_order(product_id, user_id, quantity)
                
                # Then update inventory
                updated_product = self.inventory_service.update_product(
                    product_id=product_id,
                    product_name=product.product_name,
                    description=product.description,
                    quantity=product.quantity - quantity
                )
                
                if not updated_product:
                    # If inventory update failed, roll back the order
                    self.order_repository.delete_order(order.order_id)
                    raise Exception("Failed to update inventory")

                return order

            except Exception as e:
                # If anything fails during the transaction, clean up and re-raise
                if order is not None:
                    self.order_repository.delete_order(order.order_id)
                raise e

        except ValueError:
            raise InvalidUUIDFormatError
        
    def delete_order(self, order_id: str) -> None:
        self.order_repository.delete_order(order_id)