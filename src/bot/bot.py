import logging

from pandas import DataFrame

import bot.text_formatter as formatter
from analyst import analyst
from download.download import Download

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

    def reply_start(self):
        return (
            "I compute statistics about prices, returns and volatility from "
            "stocks, ETFs and REITs. I get the data from Yahoo Finance.\n\n"
            "/help will show the list of supported commands."
        )

    def reply_help(self):
        return (
            'I support the following commands:\n\n'
            '/start - show the description of what I can do\n'
            '/help - show the list of commands I support\n'
            '/price {symbol} - get price stats\n'
            '/return {symbol} - get return stats\n'
            '/vol {symbol} - get volatility stats\n'
            '/all {symbol} - get price, return, and volatility stats'
        )

    def reply_price_stats(self, text: str) -> str:
        try:
            symbol = self._get_symbol(text)
            prices = self._get_prices(symbol)

            current_price = analyst.get_current_price(prices)
            price_stats = analyst.get_price_stats(prices)
            readable_price_stats = formatter.human_readable_prices(price_stats)
            message = (f'The price of {symbol.upper()} is:\n\n'
                       f'Current price:\n'
                       f'{formatter.as_decimal(current_price.value)} ({current_price.date})\n\n'
                       f'Stats:\n\n{readable_price_stats}')
            return message
        except Exception as e:
            error_message = str(e)
            logger.error(error_message)
            return error_message

    def reply_return_stats(self, text: str) -> str:
        try:
            symbol = self._get_symbol(text)
            prices = self._get_prices(symbol)

            current_price = analyst.get_current_price(prices)
            return_stats = analyst.get_return_stats(prices)
            readable_return_stats = formatter.human_readable_annual_stats(return_stats)
            message = (f'The return of {symbol.upper()} is:\n\n'
                       f'Current price:\n'
                       f'{formatter.as_decimal(current_price.value)} ({current_price.date})\n\n'
                       f'Stats:\n\n{readable_return_stats}')
            return message
        except Exception as e:
            error_message = str(e)
            logger.error(error_message)
            return error_message

    def reply_volatility_stats(self, text: str) -> str:
        try:
            symbol = self._get_symbol(text)
            prices = self._get_prices(symbol)

            current_price = analyst.get_current_price(prices)
            volatility_stats = analyst.get_volatility_stats(prices)
            readable_volatility_stats = formatter.human_readable_annual_stats(volatility_stats)
            message = (f'The volatility of {symbol.upper()} is:\n\n'
                       f'Current price:\n'
                       f'{formatter.as_decimal(current_price.value)} ({current_price.date})\n\n'
                       f'Stats:\n\n{readable_volatility_stats}')
            return message
        except Exception as e:
            error_message = str(e)
            logger.error(error_message)
            return error_message

    def reply_all_stats(self, text: str) -> str:
        try:
            symbol = self._get_symbol(text)
            prices = self._get_prices(symbol)

            current_price = analyst.get_current_price(prices)
            price_stats = analyst.get_price_stats(prices)
            return_stats = analyst.get_return_stats(prices)
            volatility_stats = analyst.get_volatility_stats(prices)
            readable_all_stats = formatter.human_readable_all_annual_stats(price_stats, return_stats, volatility_stats)
            message = (f'The stats of {symbol.upper()} are:\n\n'
                       f'Current price:\n'
                       f'{formatter.as_decimal(current_price.value)} ({current_price.date})\n\n'
                       f'Stats:\n\n{readable_all_stats}')
            return message
        except Exception as e:
            error_message = str(e)
            logger.error(error_message)
            return error_message

    def monitor_portfolio(self, portfolio: list[str]) -> list[str]:
        messages = []
        for symbol in portfolio:
            prices = self.downloader.get_stock_historical_data(symbol)
            price_anomaly = analyst.get_price_anomaly(prices)
            if price_anomaly:
                message = formatter.human_readable_price_anomaly(symbol, price_anomaly)
                messages.append(message)

        if not messages:
            messages.append('No new price alerts for today')

        return messages

    # private methods

    @staticmethod
    def _is_valid_message(text: str) -> bool:
        if not text:
            return False
        parts = text.split(SPACE)
        return len(parts) == 2

    def _get_symbol(self, text: str) -> str:
        if not self._is_valid_message(text):
            logger.error(f'The given command is not valid: {text}')
            raise ValueError(
                f'Error: please provide a symbol after the command, '
                f'for example: /price amzn'
            )

        symbol = text.split(SPACE)[1]
        return symbol

    def _get_prices(self, symbol: str) -> DataFrame:
        prices = self.downloader.get_stock_historical_data(symbol)
        if prices.empty:
            message = f'Error: the symbol {symbol} does not exists'
            raise ValueError(message)

        return prices
