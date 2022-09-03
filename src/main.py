import yfinance as yf
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext
)

from bot.bot import Bot
from common import env_validator
from download.download import Download

downloader = Download(yf)
bot = Bot(downloader)


def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(bot.reply_start())


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(bot.reply_help())


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


def unknown_command(update: Update, context: CallbackContext) -> None:
    message = "I don't understand that, but " + bot.reply_help()
    update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    telegram_token = env_validator.get_telegram_token_or_throw()
    updater = Updater(telegram_token)

    # get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # supported commands
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("price", price_command))
    dispatcher.add_handler(CommandHandler("return", return_command))
    dispatcher.add_handler(CommandHandler("vol", volatility_command))
    dispatcher.add_handler(CommandHandler("all", all_command))

    # handle unknown commands or text
    dispatcher.add_handler(MessageHandler(Filters.command | Filters.text, unknown_command))

    # start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
