# SECURITY WARNING: don't run with debug turned on in production!
import dj_database_url
from dotenv import load_dotenv

from .base import *

load_dotenv()
ASAAS_WEBHOOK_TOKEN = os.getenv("ASAAS_WEBHOOK_TOKEN")
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "terrier-equipped-supposedly.ngrok-free.app",
    "vehicle-platform.onrender.com",
]
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": int(os.getenv("POSTGRES_DB_PORT", 5432)),
        }
    }
