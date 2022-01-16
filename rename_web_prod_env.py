DEBUG = 0
SECRET_KEY = "_______GENERATE_ME_WITH_THE_FUNCTION_BELOW________"
ALLOWED_HOSTS = "example.com www.example.com"
CSRF_TRUSTED_ORIGINS = "http://example.com"

CELERY_BROKER_URL = "<brokerName>://<brokerHost>:<brokerPort>"
CELERY_RESULT_BACKEND = "<brokerName>://<brokerHost>:<brokerPort>"

DATABASE = "postgres"
SQL_ENGINE = "django.db.backends.postgresql_psycopg2"
SQL_USER = ""
SQL_PASSWORD = ""
SQL_DB = ""
SQL_HOST = ""
SQL_PORT = ""

MONGO_DATABASE_NAME = ""
MONGO_HOST = ""
MONGO_PORT = ""
MONGO_USERNAME = ""
MONGO_PASSWORD = ""

EMAIL_HOST_USER = "administrative back-end email to send messages from"
EMAIL_HOST_PASSWORD = "password to this email account"
EMAIL_INTERVAL_SECONDS = "set it here or, which is more handy, - in the powerful admin cabinet"

ADMIN_NAME = ""
ADMIN_EMAIL = "valid@email.here"
ADMIN_PASSWORD = ""


def generate_key():
    """Run this file with python to generate and get from console the key you can use in production.
    Delete this function upon key creation."""
    import string
    import random
    chars = string.ascii_lowercase + string.digits + "!@#$%^&*(-_=+)"
    print(''.join(random.SystemRandom().choice(chars) for _ in range(50)))


generate_key()
