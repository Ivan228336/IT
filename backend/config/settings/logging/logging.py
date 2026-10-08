"""Module for configuration logging in Django project with logging package.

Configuration for the Django saved in root handler.
For integration use another handler with writing to the file.
"""


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "integration": {
            "format": "[%(asctime)s - %(name)s - %(levelname)s] at %(funcName)s() => %(message)s",
        },
        "root": {
            "format": "[%(asctime)s - %(name)s - %(levelname)s] at %(funcName)s() => %(message)s",
        },
        "celery": {
            "format": "%(asctime)s [%(levelname)s] <PID %(process)d:%(processName)s> at %(funcName)s() => %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "integration",
            "stream": "ext://sys.stdout",
        },
        "default_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "maxBytes": 52428800,
            "backupCount": 50,
            "formatter": "integration",
            "filename": "logs/base_logger/logger.log",
            "encoding": "utf-8",
        },
        "telegram_handler": {
            "class": "config.settings.logging.handlers.TelegramLogger",
            "level": "CRITICAL",
            "formatter": "integration",
        },
        "code_debug": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "console_debug": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "default_logger": {
            "level": "INFO",
            "handlers": ["default_handler", "telegram_handler"],
            "propagate": False,
        },
    },
}
