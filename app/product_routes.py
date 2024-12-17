from sanic import Sanic, Blueprint
from controllers.health_controller import HealthController
from controllers.inventory_controller import InventoryController
from controllers.order_controller import OrderController


# Create Sanic app instance
app = Sanic("my_sanic_app")

health_controller = HealthController()
inventory_controller = InventoryController()
order_controller = OrderController()

PRODUCT_ROUTES = Blueprint("product_api", url_prefix="/products")


# health check
@app.get("/ping")
async def health_check(request):
    return health_controller.health_check(request)

# Create a new product
@PRODUCT_ROUTES.route(methods=["POST"])
async def create_product(request):
    return inventory_controller.create_product(request)

# Get a list of all products
@PRODUCT_ROUTES.route(methods=["GET"])
async def get_all_products(request):
    return inventory_controller.get_all_products(request)

# Get a specific product
@PRODUCT_ROUTES("/<product_id>", methods=["GET"])
async def get_product(request, product_id):
    return inventory_controller.get_product(request, product_id)

# Update a product
@PRODUCT_ROUTES("/<product_id>", methods=["PUT"])
async def update_product(request, product_id):
    return inventory_controller.update_product(request, product_id)

# Delete a product
@PRODUCT_ROUTES("/<product_id>", methods=["DELETE"])
async def delete_product(request, product_id):
    return inventory_controller.delete_product(request, product_id)