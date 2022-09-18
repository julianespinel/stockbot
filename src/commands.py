import yfinance as yf
from telegram import Update
from telegram.ext import (
    CallbackContext, CommandHandler, MessageHandler, Filters
)

from bot.bot import Bot
from download.download import Download

downloader = Download(yf)
bot = Bot(downloader)


def add_supported_commands(dispatcher) -> None:
    # supported commands
    dispatcher.add_handler(CommandHandler("start", _start_command))
    dispatcher.add_handler(CommandHandler("help", _help_command))
    dispatcher.add_handler(CommandHandler("price", _price_command))
    dispatcher.add_handler(CommandHandler("return", _return_command))
    dispatcher.add_handler(CommandHandler("vol", _volatility_command))
    dispatcher.add_handler(CommandHandler("all", _all_command))

    # handle unknown commands or text
    dispatcher.add_handler(
        MessageHandler(Filters.command | Filters.text, _unknown_command)
    )


# private functions: commands supported by the bot.


def _start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(bot.reply_start())


def _help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(bot.reply_help())


def _price_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/price symbol`
    For example: `/price amzn`
    """
    text = update.message.text
    message = bot.reply_price_stats(text)
    update.message.reply_text(message)


def _return_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/return symbol`
    For example: `/return amzn`
    """
    text = update.message.text
    message = bot.reply_return_stats(text)
    update.message.reply_text(message)


def _volatility_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/vol symbol`
    For example: `/vol amzn`
    """
    text = update.message.text
    message = bot.reply_volatility_stats(text)
    update.message.reply_text(message)


def _all_command(update: Update, context: CallbackContext) -> None:
    """
    This command expects the following: `/all symbol`
    For example: `/all amzn`
    """
    text = update.message.text
    message = bot.reply_all_stats(text)
    update.message.reply_text(message)


def _unknown_command(update: Update, context: CallbackContext) -> None:
    message = "I don't understand that, but " + bot.reply_help()
    update.message.reply_text(message)
