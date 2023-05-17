#!/usr/bin/env python
import os

from mtas.log import get_logger
from mtas.config import get_config
from mtas.server import bot


logger = get_logger()   
config = get_config()


def main():
    logger.info("Starting the bot...")
    bot.infinity_polling(
        restart_on_change=config["main"]["debug"], path_to_watch=os.path.join(".", "mtas"))
    logger.info("The bot has stopped.")


if __name__ == "__main__":
    main()
