from passlib.context import CryptContext
import smtplib


SECRET_KEY = "drvz&eaqvs5!jvstndusl8g545j*l+9m7k3ubat$2w1az=ybdb"
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
