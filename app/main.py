from sanic import Sanic
from app.routes.product_routes import PRODUCT_ROUTES
from app.routes.order_routes import ORDER_ROUTES
from app.routes.health_routes import HEALTH_ROUTES

# Create Sanic app instance
app = Sanic("my_sanic_app")

app.blueprint(PRODUCT_ROUTES)
app.blueprint(ORDER_ROUTES)
app.blueprint(HEALTH_ROUTES)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True
    )