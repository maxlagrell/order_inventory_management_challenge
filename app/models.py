from uuid import uuid4
from datetime import datetime, timezone


class Order:
    def __init__(self, product_id, user_id, quantity):
        self.order_id = str(uuid4())
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "quantity": self.quantity,
            "created_at": self.created_at
        }

class Inventory:
    def __init__(self, product_name, description, quantity):
        self.product_id = str(uuid4())
        self.product_name = product_name
        self.description = description
        self.quantity = quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "description": self.description,
            "quantity": self.quantity
        }
