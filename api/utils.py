import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from .models import User
from . import config
import os

base_dir = os.path.join(os.getcwd(), 'api')


def get_template(filename: str):
    with open(os.path.join(base_dir, filename), "r") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_confirmation_mail(user: User):
    site = "dicegame.net"
    confirmation_url = f"http://localhost:8000/{user.email.activation_token}"
    smtp = smtplib.SMTP(host=config.EMAIL_HOST, port=config.EMAIL_PORT)
    smtp.starttls()
    smtp.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    mail = MIMEMultipart()
    params = {
        "site": site,
        "confirmation_url": confirmation_url,
        "username": user.username
    }
    message_template = get_template("registration.txt")
    message = message_template.substitute(**params)
    mail['From'] = config.EMAIL_ADDRESS
    mail['To'] = user.email.address
    mail['Subject'] = "Dice game confirmation"
    mail.attach(MIMEText(message, "plain"))
    smtp.send_message(mail)
