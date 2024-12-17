from uuid import UUID
from sanic import response
from exceptions import InvalidUUIDFormatError, OrderNotFoundError, InvalidInputError, InvalidContentTypeError, InvalidJSONError
from services.order_service import OrderService

class OrderController:
    def __init__(self):
        self.order_service = OrderService()

    def get_order(self, request, order_id: str):
        try:
             
            UUID(order_id)
        
            order = self.order_service.get_order_or_raise_error(order_id)
            return response.json(order.to_dict(), status=200)
        except ValueError as e:
            return response.json({"error": str(e)}, status=400)
        except OrderNotFoundError as e:
            return response.json({"error": e.message}, status=404)
    
    def get_all_orders_for_user(self, request, user_id: str):
        orders = self.order_service.get_all_orders_for_user(user_id)
        return response.json([order.to_dict() for order in orders], status=200)
    
    def create_order(self, request):
        try:
            data = request.json
        except:
            return response.json({"error": InvalidJSONError().message}, status=400)

        # Validate content type is json
        if request.headers.get("Content-Type") != "application/json":
            return response.json({"error": InvalidContentTypeError().message}, status=415)
        
        # Validate inputs
        if not data.get("product_id") or not data.get("user_id") or not data.get("quantity"):
            return response.json({"error": InvalidInputError().message}, status=400)
        
        product_id = data.get("product_id")
        user_id = data.get("user_id")
        quantity = data.get("quantity")

        order = self.order_service.create_order(product_id, user_id, quantity)
        return response.json(order.to_dict(), status=201)
    
    
    def delete_order(self, request, order_id: str):
        self.order_service.delete_order(order_id)
        return response.json({"message": "Order deleted successfully"}, status=200)
