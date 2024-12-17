from sanic import Blueprint
from controllers.inventory_controller import InventoryController

inventory_controller = InventoryController()

PRODUCT_ROUTES = Blueprint("product_api", url_prefix="/products")

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