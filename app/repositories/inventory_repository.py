from app.models import Inventory
from app.database import inventory

class InventoryRepository:
    @staticmethod
    # find product by product_id
    def find_product_by_id(product_id):
        return inventory.get(product_id)
    
    @staticmethod
    # find all products
    def find_all_products():
        return list(inventory.values())
    
    @staticmethod
    # create a new product
    def create_product(product_name, description, quantity):
        product = Inventory(product_name, description, quantity)
        inventory[product.product_id] = product
        return product


    @staticmethod
    # update a product's details
    def update_product(product_id, product_name, description, quantity):
        product = inventory.get(product_id)
        if product:
            product.product_name = product_name
            product.description = description
            product.quantity = quantity
            return product
        return None

    @staticmethod
    # delete a product
    def delete_product(product_id):
        return inventory.pop(product_id, None)
        
