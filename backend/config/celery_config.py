import os
from pathlib import Path

import environ
from celery import Celery

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery(
    "config",
)
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")
CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = 'Asia/Krasnoyarsk'

# CELERY_RESULT_BACKEND = "rpc://"
# CELERY_BROKER_URL = 'pyamqp://guest:guest@rabbitmq:5672//'


celery_app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    ignore_result=CELERY_IGNORE_RESULT,
    accept_content=CELERY_ACCEPT_CONTENT,
    result_serializer=CELERY_RESULT_SERIALIZER,
    task_serializer=CELERY_TASK_SERIALIZER,
)

celery_app.conf.beat_schedule = {}
