from getpass import getpass
import datetime
import hashlib
import os
import sys
from pathlib import Path

import telebot
import telebot.types as tt
import telebot.formatting as tf

from mtas.config import get_config, save_config
from mtas.log import get_logger
from mtas import __version__


HELP = f"""
*MSLU Ticket Arrangement System {__version__}*
(https://github.com/alex-rusakevich/mtas)
""".strip()

logger = get_logger()
config = get_config()

# region Loading password and token
token = os.environ.get("BOT_TOKEN")
if not token:
    token = config["main"]["token"]
if not token:
    config["main"]["token"] = getpass("Bot API key: ")
    save_config()
    token = config["main"]["token"]

admin_pass = os.environ.get("ADMIN_PASS")
if not admin_pass:
    admin_pass = config["main"]["admin-pass"]
if not admin_pass:
    config["main"]["admin-pass"] = getpass("Bot API key: ")
    save_config()
    admin_pass = config["main"]["admin-pass"]
# endregion

bot = telebot.TeleBot(token, skip_pending=True,
                      parse_mode="Markdown", threaded=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):


    bot.send_message(
        message.chat.id, f"Hello there, {message.from_user.first_name}!")


@bot.message_handler(content_types=['text'])
def main_text_handler(message):
    if (message.text in ("/help", )):
        bot.send_message(
            message.chat.id, HELP)
    elif message.text.lower() in ("я тебя люблю", "i love you",
                                  "我爱你", "я тебя люблю!", "i love you!", "我爱你！", "521", "520"):
        try:
            bot.send_sticker(
                message.chat.id, "CAACAgIAAxkBAAEJAkdkZJ2OU5DV1melgSjQGkkg7O9jkQACoBwAAipooUjogwEq_q_PRy8E")
        except:
            bot.send_message(message.chat.id, "❤️")
