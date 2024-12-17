from sanic import response

class HealthController:
    def health_check(self, request):
        return response.json({"message": "OK"}, status=200)
