from sanic import Blueprint
from controllers.order_controller import OrderController
from controllers.inventory_controller import InventoryController

order_controller = OrderController()
inventory_controller = InventoryController()


ORDER_ROUTES = Blueprint("order_api", url_prefix="/orders")

# Create a new order
@ORDER_ROUTES.route(methods=["POST"])
async def create_order(request):
    return order_controller.create_order(request)

# Get all orders for a user
@ORDER_ROUTES.route("/users/<user_id>/orders", methods=["GET"])
async def get_all_orders_for_user(request, user_id):
    return order_controller.get_all_orders_for_user(request, user_id)

# Get a specific order
@ORDER_ROUTES.route("/<order_id>", methods=["GET"])
async def get_order(request, order_id):
    return order_controller.get_order(request, order_id)

# Delete an order
@ORDER_ROUTES.route("/<order_id>", methods=["DELETE"])
async def delete_order(request, order_id):
    return order_controller.delete_order(request, order_id)