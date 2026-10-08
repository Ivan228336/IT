from django.http import HttpResponse
from ninja import Router


health_router = Router()

@health_router.get("/")
def healthcheck(request) -> HttpResponse:
    return HttpResponse("OK", content_type="text/plain")
