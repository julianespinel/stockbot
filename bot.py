import logging

import analyze
import text_formatter as formatter
from download import Download

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

SPACE = ' '


class Bot:
    """
    This class contains the bot logic.
    The logic in this class should work for a bot in any platform.
    This class handles how to react and answer to a given message.
    The responsibility of connecting with a specific platform (Telegram,
    Signal, WhatsApp, etc) and how to format a message for a specific platform,
    should be taken by other class.
    """

    def __init__(self, downloader: Download):
        self.downloader = downloader

    def reply_help(self):
        return (
            'This bot supports the following commands:\n\n'
            '/price {symbol} - get price stats\n'
            '/return {symbol} - get return stats\n'
            '/volatility {symbol} - get volatility stats\n'
            '/all {symbol} - get price, return, and volatility stats\n'
        )

    def reply_price_stats(self, text):
        if not self._is_valid_message(text):
            logger.error(f'The given command is not valid: {text}')
            return f'Error: please provide a symbol. For example: `/price amzn`'

        symbol = text.split(SPACE)[1]
        prices = self.downloader.get_stock_historical_data(symbol)
        if prices.empty:
            message = f'Error: the given symbol does not exists: {symbol}'
            logger.error(message)
            return message

        price_stats = analyze.get_price_stats(prices)
        current_price = analyze.get_current_price(prices)
        readable_price_stats = formatter.human_readable(price_stats)
        message = (f'The price of {symbol.upper()} is:\n\n'
                   f'Current price:\n'
                   f'{formatter.as_decimal(current_price.value)} ({current_price.date})\n\n'
                   f'Stats:\n\n{readable_price_stats}')
        return message

    # private methods

    @staticmethod
    def _is_valid_message(text: str) -> bool:
        if not text:
            return False
        parts = text.split(SPACE)
        return len(parts) == 2