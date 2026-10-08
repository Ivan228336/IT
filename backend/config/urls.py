import os
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
import environ
from ninja import NinjaAPI

from modules.auth_service.api.v1 import auth_service_router
from modules.core.utils.email_send import email_check_router
from modules.core.utils.healthcheck import health_router


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read `.env`
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

api = NinjaAPI(title="sinx_API", version="1.0.1")
api.add_router("/health", health_router)
api.add_router("/auth", auth_service_router)
api.add_router("/", email_check_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("api/", api.urls, name="api")
    # API documentation
    # ...
]

admin.site.site_header = env.str("DJANGO_ADMIN_TITLE", default="Админ. панель")
admin.site.site_title = env.str("DJANGO_ADMIN_TITLE", default="Админ. панель")

if settings.DEBUG:
    # debug-toolbar
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    # WhiteNoise
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
