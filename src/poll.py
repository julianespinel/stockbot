"""
Execute the bot in Poll mode.
Poll mode: the bot polls Telegram from new messages.
"""
from telegram.ext import Updater

import commands
from common import env_validator


def poll() -> None:
    """Start the bot in polling mode"""
    telegram_token = env_validator.get_or_throw('TELEGRAM_BOT_TOKEN')
    updater = Updater(telegram_token)

    # get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    commands.add_supported_commands(dispatcher)

    # start the bot
    updater.start_polling()

    # Run the bot until we press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    poll()
