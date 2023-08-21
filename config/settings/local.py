from .base import *
from .base import env


env.read_env(str(BASE_DIR / ".envs" / ".local"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DOMAIN = "localhost:8000"
ALLOWED_HOSTS = ['*','localhost:8000','django']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000'
]

DOMAIN = 'localhost:8000'


# Email Settings
# EMAIL_BACKEND=os.getenv('EMAIL_BACKEND')
# EMAIL_HOST=os.getenv('EMAIL_HOST')
# EMAIL_PORT=os.getenv('EMAIL_PORT')
# EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL=os.getenv('DEFAULT_FROM_EMAIL')
# EMAIL_USE_SSL=os.getenv('EMAIL_USE_SSL')
# EMAIL_USE_TSL=os.getenv('EMAIL_USE_TSL')


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT')
    }
}
