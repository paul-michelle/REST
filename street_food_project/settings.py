import os
from . import dev_db_creds as dev_db
from mongoengine import connect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEV_SECRET_KEY = "ta=]/}1]z'#nl]$%%!}wb'y.9{+|q$m`8|iubxi~`..[i>nhdd"
SECRET_KEY = os.environ.get("SECRET_KEY", DEV_SECRET_KEY)

DEBUG = int(os.environ.get("DEBUG", "1"))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost 127.0.0.1").split(" ")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1:8000 http://localhost:8000").split(" ")
CORS_ALLOW_ALL_ORIGINS = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework_swagger',
    'rest_framework',
    'rest_framework_mongoengine',
    'django_celery_beat',

    'street_food_app.apps.StreetFoodAppConfig',
]

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
if CELERY_RESULT_BACKEND == 'django-db':
    INSTALLED_APPS += ['django_celery_results', ]
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Minsk'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'street_food_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

WSGI_APPLICATION = 'street_food_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', dev_db.SQL_ENGINE),
        'NAME': os.getenv('SQL_DB', dev_db.SQL_DB),
        'USER': os.getenv('SQL_USER', dev_db.SQL_USER),
        'PASSWORD': os.getenv('SQL_PASSWORD', dev_db.SQL_PASSWORD),
        'HOST': os.getenv('SQL_HOST', dev_db.SQL_HOST),
        'PORT': int(os.getenv('SQL_PORT', dev_db.SQL_PORT)),
    }
}

if os.environ.get("MONGO_CLUSTER_URL"):
    connect(
        host=os.environ.get("MONGO_CLUSTER_URL"),
    )

if not os.environ.get("MONGO_CLUSTER_URL"):
    connect(
        db=os.environ.get('MONGO_DATABASE_NAME', dev_db.MONGO_DATABASE_NAME),
        username=os.environ.get('MONGO_USERNAME', dev_db.MONGO_USERNAME),
        password=os.environ.get('MONGO_PASSWORD', dev_db.MONGO_PASSWORD),
        host=os.environ.get('MONGO_HOST', dev_db.MONGO_HOST),
        port=int(os.environ.get('MONGO_PORT', dev_db.MONGO_PORT)),
        authentication_source='admin',
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'staticfiles'))

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'mediafiles'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

SITE_ID = 1
