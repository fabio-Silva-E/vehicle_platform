import os

from dotenv import load_dotenv

from .base import *

load_dotenv()
ASAAS_WEBHOOK_TOKEN = os.getenv("ASAAS_WEBHOOK_TOKEN")
ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".ngrok-free.app",
]


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
