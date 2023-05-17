from getpass import getpass
import os
import re

import telebot
import telebot.types as tt
import telebot.formatting as tf

from mtas.config import get_config, save_config
from mtas.log import get_logger
from mtas import __version__

from mtas.actions.reg import get_reg_event_code, begin_reg
from mtas.bot import bot as orig_bot

bot = orig_bot


MSG_REG = "🎫 Book"
MSG_CHECK = "✅ Check"
MSG_ADMIN = "🤓 Admin"


HELP = f"""
*MSLU Ticket Arrangement System {__version__}*
(https://github.com/alex-rusakevich/mtas)
""".strip()

logger = get_logger()
config = get_config()

# region Loading password and token
admin_pass = os.environ.get("ADMIN_PASS")
if not admin_pass:
    admin_pass = config["main"]["admin-pass"]
if not admin_pass:
    config["main"]["admin-pass"] = getpass("Bot API key: ")
    save_config()
    admin_pass = config["main"]["admin-pass"]
# endregion


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, f"Hello there, {message.from_user.first_name}!")

    def choose_action(msg):
        markup = tt.ReplyKeyboardMarkup(resize_keyboard=True)
        reg_btn = tt.KeyboardButton(MSG_REG)
        check_btn = tt.KeyboardButton(MSG_CHECK)
        admin_btn = tt.KeyboardButton(MSG_ADMIN)
        markup.add(reg_btn, check_btn, admin_btn)

        bot.send_message(
            message.chat.id, "What do you want to do?", reply_markup=markup)

        bot.register_next_step_handler(msg, user_choosed_action)


    txt_with_command = message.text.split()
    if len(txt_with_command) != 2:
        choose_action(message)
        return
    command = txt_with_command[1]
    find_cmd = re.findall(r"(reg|chk|adm)_([\w-]+)", command)
    if len(find_cmd) != 1:
        choose_action(message)
        return
    find_cmd = find_cmd[0]
    if len(find_cmd) != 2:
        choose_action(message)
        return
    purpose, event_id = find_cmd

    if purpose == 'reg':
        begin_reg(message, event_id)

def user_choosed_action(message):
    if message.text in (MSG_REG, "/book"):
        bot.send_message(
            message.chat.id, "Please, enter event's id:")
        bot.register_next_step_handler(message, get_reg_event_code)

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
