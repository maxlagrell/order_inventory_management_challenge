from sanic import Sanic
from app.product_routes import PRODUCT_ROUTES
from controllers.health_controller import HealthController
from controllers.inventory_controller import InventoryController
from controllers.order_controller import OrderController

# Create Sanic app instance
app = Sanic("my_sanic_app")

health_controller = HealthController()
inventory_controller = InventoryController()
order_controller = OrderController()

app.blueprint(PRODUCT_ROUTES)

# health check
@app.get("/ping")
async def health_check(request):
    return health_controller.health_check(request)


# Create a new order
@app.post("/orders")
async def create_order(request):
    return order_controller.create_order(request)

# Get all orders for a user
@app.get("/users/<user_id>/orders")
async def get_all_orders_for_user(request, user_id):
    return order_controller.get_all_orders_for_user(request, user_id)

# Get a specific order
@app.get("/orders/<order_id>")
async def get_order(request, order_id):
    return order_controller.get_order(request, order_id)

# Delete an order
@app.delete("/orders/<order_id>")
async def delete_order(request, order_id):
    return order_controller.delete_order(request, order_id)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True
    )