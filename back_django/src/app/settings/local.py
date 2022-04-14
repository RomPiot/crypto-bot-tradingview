# flake8: noqa
from .base import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH"),
    }
}

ENV_BANNER_SHOW = os.environ.get("ENV_BANNER_SHOW")
ENV_BANNER_NAME = "LOCAL ENVIRONMENT"
ENV_BANNER_BG_COLOR = "#FF2222"
ENV_BANNER_TEXT_COLOR = "white"

INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
