import os
import mongoengine

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

    'street_food_app.apps.StreetFoodAppConfig',
]

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

SQLITE_PATH = 'db.sqlite3' if DEBUG else '../database/db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.getenv('SQL_DB', 'street_food_dev'),
        'USER': os.getenv('SQL_USER', 'street_food_dev'),
        'PASSWORD': os.getenv('SQL_PASSWORD', 'street_food_dev'),
        'HOST': os.getenv('SQL_HOST', 'db'),
        'PORT': int(os.getenv('SQL_PORT', '5432')),
    }
}

mongoengine.connect(
    db=os.environ.get('MONGO_DATABASE_NAME', 'street_food_dev'),
    username=os.environ.get('MONGO_USERNAME', 'street_food_dev'),
    password=os.environ.get('MONGO_PASSWORD', 'street_food_dev'),
    host=os.environ.get('MONGO_HOST', 'db_nosql'),
    port=int(os.environ.get('MONGO_PORT', '27017')),
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
