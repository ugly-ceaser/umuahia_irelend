import os
from pathlib import Path
from .config import (
    SECRET_KEY,
    DEBUG,
    DB_NAME,
    ALLOWED_HOSTS,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    APP_NAME,
    APP_URL,
    EMAIL_BACKEND,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USE_TLS,
    FRONTEND_URL,
)

APP_NAME = APP_NAME
APP_URL = APP_URL

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = SECRET_KEY

DEBUG = DEBUG

ALLOWED_HOSTS = list(ALLOWED_HOSTS)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "app.apps.AppConfig",
    "_admin.apps.AdminConfig",
    "dashboard.apps.DashboardConfig",
    "users.apps.UsersConfig",
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

ROOT_URLCONF = "umuahia_ireland.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "umuahia_ireland.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR / "static"),)

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR / "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR / "media")

LOGIN_URL = "accounts:user_login_page"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_EMAIL = EMAIL_HOST_USER

AUTH_USER_MODEL = "users.CustomUser"

EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

FRONTEND_URL = FRONTEND_URL
