import os

from celery.schedules import crontab

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "*-fuslvu#e=#8+5)o9e+y_#vo$wu8=gx@b9v*yp!e_p%0afvr9"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "tiny.tjhsst.edu",
    "tiny.csl.tjhsst.edu",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_celery_results',
    "shortener.apps.auth.apps.AuthConfig",
    "shortener.apps.urls.apps.UrlsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shortener.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "shortener.apps.context_processors.base_context",
            ],
        },
    },
]

WSGI_APPLICATION = "shortener.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "authentication.User"

AUTHENTICATION_BACKENDS = ("shortener.apps.auth.oauth.IonOauth2",)

SOCIAL_AUTH_USER_FIELDS = ["username", "first_name", "last_name", "email", "id"]
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "shortener.apps.auth.oauth.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
)
SOCIAL_AUTH_ALWAYS_ASSOCIATE = True
SOCIAL_AUTH_LOGIN_ERROR_URL = "auth:error"
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "urls:create"
LOGOUT_REDIRECT_URL = "auth:login"

SESSION_SAVE_EVERY_REQUEST = True

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "serve")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Celery
CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_TIMEZONE = "America/New_York"
CELERY_BEAT_SCHEDULE = {
    "delete-old-games": {
        "task": "shortener.apps.urls.tasks.delete_old_urls",
        "schedule": crontab(month_of_year=6),
        "args": (),
    }
}

# Shortener
DEFAULT_SLUG_LENGTH = 10  # characters


# Mail
MAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.tjhsst.edu"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_SUBJECT_PREFIX = "[Shortener]"
EMAIL_FROM = "shortener-noreply@tjhsst.edu"
FORCE_EMAIL_SEND = True
DEVELOPER_EMAIL = "sysadmins@tjhsst.edu"


try:
    from .secret import *  # noqa
except ImportError:
    pass
