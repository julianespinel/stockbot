"""
Monitor
"""
import yfinance as yf
from telegram import Bot as TelegramBot
import telegram as tl

from src.bot.bot import Bot
from src.common import env_validator, logs
from src.download.download import Download

logger = logs.get_logger(__name__)

channel_id = env_validator.get_or_throw('CHANNEL_ID')
telegram_token = env_validator.get_or_throw('TELEGRAM_BOT_TOKEN')

symbols = env_validator.get_or_throw('SYMBOLS')
portfolio = symbols.split(',')

telegram = TelegramBot(token=telegram_token)
downloader = Download(yf)
bot = Bot(downloader)


def lambda_handler(event, context):
    try:
        _monitor(portfolio)
        return {"statusCode": 200}
    except Exception as e:
        logger.error(e)
        return {"statusCode": 500}


# private functions


def _monitor(portfolio: list[str]) -> None:
    messages = bot.monitor_portfolio(portfolio)
    for message in messages:
        logger.info(message)
        telegram.send_message(channel_id, message)


if __name__ == '__main__':
    _monitor(portfolio)
