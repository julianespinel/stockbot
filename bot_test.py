import unittest
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from bot import Bot


class BotTests(unittest.TestCase):

    def setUp(self):
        self.downloader_mock = MagicMock()
        self.bot = Bot(self.downloader_mock)

    def test_reply_start_success_get_expected_message(self):
        # arrange
        expected_message = Path('test_messages/start.txt').read_text().rstrip()
        # act
        message = self.bot.reply_start()
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_help_success_get_expected_message(self):
        # arrange
        expected_message = Path('test_messages/help.txt').read_text().rstrip()
        # act
        message = self.bot.reply_help()
        # assert
        self.assertEqual(message, expected_message)

    # region price stats tests

    def test_reply_price_stats_error_get_not_valid_command_error(self):
        # arrange
        text = '/price'
        expected_message = (
            f'Error: please provide a symbol after the command, '
            f'for example: /price amzn'
        )
        # act
        message = self.bot.reply_price_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_price_stats_error_get_symbol_not_found_error(self):
        # arrange
        symbol = 'aaaa'
        text = f'/price {symbol}'
        self._mock_downloader_to_get_empty_historical_data()
        expected_message = f'Error: the symbol {symbol} does not exists'
        # act
        message = self.bot.reply_price_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_price_stats_success_get_expected_stats(self):
        # arrange
        text = '/price amzn'
        self._mock_downloader_to_get_historical_data()
        expected_message = Path('test_messages/price.txt').read_text().rstrip()
        # act
        message = self.bot.reply_price_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    # endregion

    # region return stats tests

    def test_reply_return_stats_error_get_not_valid_command_error(self):
        # arrange
        text = '/return'
        expected_message = (
            f'Error: please provide a symbol after the command, '
            f'for example: /price amzn'
        )
        # act
        message = self.bot.reply_return_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_return_stats_error_get_symbol_not_found_error(self):
        # arrange
        symbol = 'aaaa'
        text = f'/return {symbol}'
        self._mock_downloader_to_get_empty_historical_data()
        expected_message = f'Error: the symbol {symbol} does not exists'
        # act
        message = self.bot.reply_return_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_return_stats_success_get_expected_stats(self):
        # arrange
        text = '/return amzn'
        self._mock_downloader_to_get_historical_data()
        expected_message = Path('test_messages/return.txt').read_text().rstrip()
        # act
        message = self.bot.reply_return_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    # endregion

    # region volatility stats tests

    def test_reply_volatility_stats_error_get_not_valid_command_error(self):
        # arrange
        text = '/vol'
        expected_message = (
            f'Error: please provide a symbol after the command, '
            f'for example: /price amzn'
        )
        # act
        message = self.bot.reply_volatility_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_volatility_stats_error_get_symbol_not_found_error(self):
        # arrange
        symbol = 'aaaa'
        text = f'/vol {symbol}'
        self._mock_downloader_to_get_empty_historical_data()
        expected_message = f'Error: the symbol {symbol} does not exists'
        # act
        message = self.bot.reply_volatility_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_volatility_stats_success_get_expected_stats(self):
        # arrange
        text = '/vol amzn'
        self._mock_downloader_to_get_historical_data()
        expected_message = Path('test_messages/volatility.txt').read_text().rstrip()
        # act
        message = self.bot.reply_volatility_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    # endregion

    # region all stats tests

    def test_reply_all_stats_error_get_not_valid_command_error(self):
        # arrange
        text = '/all'
        expected_message = (
            f'Error: please provide a symbol after the command, '
            f'for example: /price amzn'
        )
        # act
        message = self.bot.reply_all_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_all_stats_error_get_symbol_not_found_error(self):
        # arrange
        symbol = 'aaaa'
        text = f'/all {symbol}'
        self._mock_downloader_to_get_empty_historical_data()
        expected_message = f'Error: the symbol {symbol} does not exists'
        # act
        message = self.bot.reply_all_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_all_stats_success_get_expected_stats(self):
        # arrange
        text = '/all amzn'
        self._mock_downloader_to_get_historical_data()
        expected_message = Path('test_messages/all.txt').read_text().rstrip()
        # act
        message = self.bot.reply_all_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    # endregion

    # region private methods

    def _mock_downloader_to_get_historical_data(self):
        expected_df = pd.read_csv('csv_files/AMZN_from_stockbot.csv')
        self.downloader_mock.get_stock_historical_data = MagicMock(return_value=expected_df)

    def _mock_downloader_to_get_empty_historical_data(self):
        expected_df = pd.DataFrame([])
        self.downloader_mock.get_stock_historical_data = MagicMock(return_value=expected_df)

    # endregion
