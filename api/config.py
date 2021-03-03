from passlib.context import CryptContext
import os


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

SITE = os.environ.get("SITE")
FRONTEND_HOST = os.environ.get("FRONTEND_HOST")

DATABASE_URL = os.environ.get("DATABASE_URL")
