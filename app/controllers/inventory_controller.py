from uuid import UUID
from sanic import response
from app.controllers.inventory_validators import validate_product_id
from app.services.inventory_service import InventoryService
from app.exceptions import InvalidInputError, InvalidUUIDFormatError, ProductNotFoundError, InvalidContentTypeError, InvalidJSONError

class InventoryController:
    def __init__(self):
        self.inventory_service = InventoryService()

    def get_product(self, request, product_id: str):
        try:
            validate_product_id(product_id)
            product = self.inventory_service.get_product_or_raise_error(product_id)
            return response.json(product.to_dict(), status=200)
        except InvalidUUIDFormatError as e:
            return response.json({"error": e.message}, status=400)
        except ProductNotFoundError:
            return response.json({"error": ProductNotFoundError().message}, status=404)
        
    def get_all_products(self, request):
        products = self.inventory_service.get_all_products()
        return response.json([product.to_dict() for product in products], status=200)
    
    def create_product(self, request):
        try:
            data = request.json
        except:
            return response.json({"error": InvalidJSONError().message}, status=400)

        # Validate inputs
        if not data.get("name") or not data.get("description") or not data.get("quantity"):
            return response.json({"error": InvalidInputError().message}, status=400)

        product_name = data.get("name")
        description = data.get("description")
        quantity = data.get("quantity")

        # Validate content type is json
        if request.headers.get("Content-Type") != "application/json":
            return response.json({"error": InvalidContentTypeError().message}, status=415)
        
        product = self.inventory_service.create_product(product_name, description, quantity)
        return response.json(product.to_dict(), status=201)
    
    def update_product(self, request, product_id: str):
        try:
            data = request.json
        except:
            return response.json({"error": InvalidJSONError().message}, status=400)
        
        # Validate content type is json
        if request.headers.get("Content-Type") != "application/json":
            return response.json({"error": InvalidContentTypeError().message}, status=415)
        
        # Validate inputs
        if not data.get("name") or not data.get("description") or not data.get("quantity"):
            return response.json({"error": InvalidInputError().message}, status=400)
        
        product_name = data.get("name")
        description = data.get("description")
        quantity = data.get("quantity")

        product = self.inventory_service.update_product(product_id, product_name, description, quantity)
        return response.json(product.to_dict(), status=200)
    
    def delete_product(self, request, product_id: str):
        self.inventory_service.delete_product(product_id)
        return response.json({"message": "Product deleted successfully"}, status=200)




