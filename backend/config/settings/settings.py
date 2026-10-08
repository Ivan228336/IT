import os
import json
import sys
from datetime import timedelta
from pathlib import Path
from .logging.logging import LOGGING
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Read `.env`
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "debug_toolbar",
    "django_summernote",
    "import_export",
    "constance",
    "constance.backends.database",
    "modules.core",
    "modules.auth_service",
    "django_cleanup.apps.CleanupConfig",  # должен быть последним в списке (https://pypi.org/project/django-cleanup/)
]

AUTH_USER_MODEL = "core.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "ninja.compatibility.files.fix_request_files_middleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
        "TEST": {
            'NAME':'test_db',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "ru"
TIME_ZONE = env.str("DJANGO_TIMEZONE", default="Asia/Krasnoyarsk")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# WhiteNoise
# https://whitenoise.evans.io/en/stable/#quickstart-for-django-apps
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Summernote media files
# https://github.com/summernote/django-summernote#setup
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]

# Constance
# https://django-constance.readthedocs.io/en/latest/
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_ADDITIONAL_FIELDS = {
    "text_field": [
        "django.forms.fields.Field",
        {
            "widget": "django_summernote.widgets.SummernoteWidget",
            "required": False,
        },
    ],
    "email_field": [
        "django.forms.fields.EmailField",
        {
            "required": False,
        },
    ],
    "bool_field": [
        "django.forms.fields.BooleanField",
        {
            "required": False,
        },
    ],
}
CONSTANCE_CONFIG = {
    "NOTIFICATION_EMAIL": ("", "Email для уведомлений", "email_field"),
    "NOTIFICATION_ENABLED": ("", "Включить уведомления", "bool_field"),
    "PRIVACY_POLICY": ("", "Политика конфиденциальности", "text_field"),
}


if DEBUG:
    SPECTACULAR_SETTINGS = {
        "TITLE": env.str("DJANGO_ADMIN_TITLE"),
        "VERSION": "",
        "SWAGGER_UI_DIST": "SIDECAR",
        "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
        "REDOC_DIST": "SIDECAR",
    }

    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

EMAIL_TEST_MODE=env.bool('EMAIL_TEST_MODE', default=False)
EMAIL_DEFAULT_FROM = env.str('EMAIL_DEFAULT_FROM')
EMAIL_TEST_ADDRESS=env.str('EMAIL_TEST_ADDRESS')

if EMAIL_TEST_MODE: #режим True - для тестов, вывод будет идти в консоль
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')  # Gmail email address
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')  # Gmail email password



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "USERNAME" : env.str("REDIS_USER"),
            "PASSWORD": env.str('REDIS_PASSWORD'),
            "DECODE_RESPONSES": True,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True
            }
        },
        "KEY_PREFIX": "address_suggest",
        "VERSION": 1,
    },
    "blacklist": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2", 
    },
}

if 'test' in sys.argv or os.environ.get('DJANGO_TEST_MODE'):
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-cache',
    }

FRONTEND_URL=env.str('FRONTEND_URL')