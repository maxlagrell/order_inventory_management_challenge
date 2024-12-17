from sanic import Blueprint
from controllers.health_controller import HealthController

health_controller = HealthController()

HEALTH_ROUTES = Blueprint("health_api", url_prefix="/health")

@HEALTH_ROUTES.route(methods=["GET"])
async def health_check(request):
    return health_controller.health_check(request)