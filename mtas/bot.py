import os
from getpass import getpass

import telebot

from mtas.config import get_config, save_config

config = get_config()

token = os.environ.get("BOT_TOKEN")
if not token:
    token = config["main"]["token"]
if not token:
    config["main"]["token"] = getpass("Bot API key: ")
    save_config()
    token = config["main"]["token"]

bot = telebot.TeleBot(token, skip_pending=True,
                      parse_mode="Markdown", threaded=True)
