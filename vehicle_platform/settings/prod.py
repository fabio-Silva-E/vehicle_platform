from .base import  *
from dotenv import load_dotenv
# SECURITY WARNING: don't run with debug turned on in production!

load_dotenv()
ASAAS_WEBHOOK_TOKEN = os.getenv("ASAAS_WEBHOOK_TOKEN")
DEBUG = True
ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")
ALLOWED_HOSTS =  ["127.0.0.1", "localhost","terrier-equipped-supposedly.ngrok-free.app", "https://vehicle-platform.onrender.com/",]


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': int(os.environ['POSTGRES_DB_PORT']),
    }
}
