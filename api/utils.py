import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from .models import UserModel
from . import config
import os
import asyncio


def get_template(filename: str):
    with open(os.path.join(config.BASE_DIR, filename), "r") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_confirmation_mail(user: UserModel):
    if config.EMAIL_HOST is None:
        return
    site = config.SITE
    confirmation_url = f"{config.FRONTEND_HOST}/confirm-email/{user.id}/{user.email.activation_token}"
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


def send_new_password(user: UserModel, password: str):
    params = {
        "site": config.SITE,
        "username": user.username,
        "password": password
    }
    smtp = smtplib.SMTP(host=config.EMAIL_HOST, port=config.EMAIL_PORT)
    smtp.starttls()
    smtp.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    mail = MIMEMultipart()
    message_template = get_template("password_reset.txt")
    message = message_template.substitute(**params)
    mail['From'] = config.EMAIL_ADDRESS
    mail['To'] = user.email.address
    mail['Subject'] = "Dice game password reset"
    mail.attach(MIMEText(message, "plain"))
    smtp.send_message(mail)


def times_in_array(n, array):  # Returns value that appears n-times in given array, works for cases below
    for val in array:
        if array.count(val) == n:
            return val


def look_for_patterns(dices: list[int]) -> int:
    unique_dices = set(dices)
    if len(unique_dices) == 1:  # Poker
        return 8
    elif len(unique_dices) == 2:
        for dice in dices:
            if dices.count(dice) == 4:  # Kareta
                return 7
            elif dices.count(dice) == 2 or dices.count(dice) == 3:  # Full
                return 6
    elif len(unique_dices) == 3:
        for dice in dices:
            if dices.count(dice) == 3:  # Trojka
                return 3
        for dice in dices:
            if dices.count(dice) == 1:  # Dwie pary
                return 2
    elif len(unique_dices) == 4:
        for dice in dices:
            if dices.count(dice) == 2:  # Para
                return 1
    else:
        if 6 not in dices:  # Maly St
            return 4
        elif 1 not in dices:  # Duzy St
            return 5
        else:
            return 0


def compare_dices(dices1: list[int], dices2: list[int], pattern: int) -> int:
    if dices1 == dices2:
        return -1
    if pattern == 8:  # Poker
        if dices1[0] > dices2[0]:
            return 0
        elif dices1[0] < dices2[0]:
            return 1
    elif pattern == 7:  # Kareta
        dice1 = times_in_array(4, dices1)
        dice2 = times_in_array(4, dices2)
        if dice1 > dice2:
            return 0
        elif dice2 > dice1:
            return 1
        elif dice1 == dice2:
            if sum(dices1) > sum(dices2):
                return 0
            elif sum(dices1) < sum(dices2):
                return 1
            else:
                return -1
    elif pattern == 6:
        if sum(dices1) > sum(dices2):
            return 0
        elif sum(dices1) < sum(dices2):
            return 1
    elif pattern == 3:
        dice1 = times_in_array(3, dices1)
        dice2 = times_in_array(3, dices2)
        if dice1 > dice2:
            return 0
        elif dice2 > dice1:
            return 1
        elif dice1 == dice2:
            if sum(dices1) > sum(dices2):
                return 0
            elif sum(dices1) < sum(dices2):
                return 1
            else:
                return -1
    elif pattern == 2:
        single_dice1 = times_in_array(1, dices1)
        single_dice2 = times_in_array(1, dices2)
        dices1_twopairs = dices1[:]
        dices1_twopairs.remove(single_dice1)
        dices2_twopairs = dices2[:]
        dices2_twopairs.remove(single_dice2)
        if sum(dices1_twopairs) > sum(dices2_twopairs):
            return 0
        elif sum(dices1_twopairs) < sum(dices2_twopairs):
            return 1
        else:
            if single_dice1 > single_dice2:
                return 0
            elif single_dice2 > single_dice1:
                return 1
            else:
                return -1
    elif pattern == 1:
        dice1 = times_in_array(2, dices1)
        dice2 = times_in_array(2, dices2)
        if dice1 > dice2:
            return 0
        elif dice2 > dice1:
            return 1
        else:
            if sum(dices1) > sum(dices2):
                return 0
            elif sum(dices1) < sum(dices2):
                return 1
            else:
                return -1


def get_scoring_cards():
    cards = {"h" + str(i): 1 for i in range(2, 15)}
    cards.update({
        "s12": 13,
        "s13": 10,
        "s14": 7
    })
    return cards
