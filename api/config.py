from passlib.context import CryptContext


SECRET_KEY = "drvz&eaqvs5!jvstndusl8g545j*l+9m7k3ubat$2w1az=ybdb"
ALGORITHM = "HS256"
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "floppshop.confirmation@gmail.com"
EMAIL_PASSWORD = "FloppShop123"

SITE = "dicegame.net"
FRONTEND_HOST = 'http://localhost:3000'

DATABASE_URL = "postgresql://dicegameuser:dicegamepassword@localhost/dicegame"
