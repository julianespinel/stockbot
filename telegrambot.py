import os

import yfinance as yf
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot import Bot
from download import Download

downloader = Download(yf)
bot = Bot(downloader)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_message = bot.reply_help()
    update.message.reply_text(help_message)


def price_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/price symbol`
    For example: `/price amzn`
    """
    text = update.message.text
    message = bot.reply_price_stats(text)
    update.message.reply_text(message)


def return_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/return symbol`
    For example: `/return amzn`
    """
    text = update.message.text
    message = bot.reply_return_stats(text)
    update.message.reply_text(message)


def volatility_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/vol symbol`
    For example: `/vol amzn`
    """
    text = update.message.text
    message = bot.reply_volatility_stats(text)
    update.message.reply_text(message)


def all_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/all symbol`
    For example: `/all amzn`
    """
    text = update.message.text
    message = bot.reply_all_stats(text)
    update.message.reply_text(message)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", help_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("price", price_command))
    dispatcher.add_handler(CommandHandler("return", return_command))
    dispatcher.add_handler(CommandHandler("vol", volatility_command))
    dispatcher.add_handler(CommandHandler("all", all_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
