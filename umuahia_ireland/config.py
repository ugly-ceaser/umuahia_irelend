import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

APP_NAME = os.getenv("APP_NAME")
APP_URL = os.getenv("APP_URL")

