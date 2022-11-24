import unittest
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from src.bot.bot import Bot


class BotTests(unittest.TestCase):

    def setUp(self):
        self.downloader_mock = MagicMock()
        self.bot = Bot(self.downloader_mock)

    def test_reply_start_success_get_expected_message(self):
        # arrange
        expected_message = Path(
            'src/bot/test_files/start.txt').read_text().rstrip()
        # act
        message = self.bot.reply_start()
        # assert
        self.assertEqual(message, expected_message)

    def test_reply_help_success_get_expected_message(self):
        # arrange
        expected_message = Path(
            'src/bot/test_files/help.txt').read_text().rstrip()
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
        expected_message = Path(
            'src/bot/test_files/price.txt').read_text().rstrip()
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
        expected_message = Path(
            'src/bot/test_files/return.txt').read_text().rstrip()
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
        expected_message = Path(
            'src/bot/test_files/volatility.txt').read_text().rstrip()
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
        expected_message = Path(
            'src/bot/test_files/all.txt').read_text().rstrip()
        # act
        message = self.bot.reply_all_stats(text)
        # assert
        self.assertEqual(message, expected_message)

    # endregion

    # region monitor portfolio

    def test_monitor_portfolio_success_no_new_price_alerts(self):
        portfolio = []
        self._mock_downloader_to_get_historical_data()
        messages = self.bot.monitor_portfolio(portfolio)
        # assert
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], 'No new price alerts for today')

    def test_monitor_portfolio_success_three_new_price_alerts(self):
        portfolio = ['AMZN']
        self._mock_downloader_to_get_historical_data()
        messages = self.bot.monitor_portfolio(portfolio)
        # assert
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0],
            ('Price alert for AMZN:\n'
             'New 3mo Max price: 134.95 (2022-07-29)\n'
             'Old 3mo values: Min: 102.31 (2022-06-14), Max: 134.95 (2022-07-29)')
        )

    # endregion

    # region report portfolio

    def test_report_portfolio_success_empty_report(self):
        portfolio = []
        self._mock_downloader_to_get_historical_data()
        report = self.bot.report_portfolio(portfolio)
        # assert
        self.assertEqual(report, 'Portfolio report\n')

    def test_report_portfolio_success_non_empty_report(self):
        portfolio = ['AMZN']
        self._mock_downloader_to_get_historical_data()
        report = self.bot.report_portfolio(portfolio)
        # assert
        self.assertEqual(
            report,
            ('Portfolio report\n\n'
            'AMZN price: 134.95\n'
            '1wk: 10.24%\n'
            '2wk: 18.85%\n'
            '3wk: 16.80%\n'
            '1mo: 23.90%\n'
            '3mo: 8.58%\n'
            '6mo: -6.27%\n'
            '12mo: -18.89%\n')
        )

    # endregion

    # region private methods

    def _mock_downloader_to_get_historical_data(self):
        expected_df = pd.read_csv(
            'src/analyst/test_files/AMZN_from_stockbot.csv')
        self.downloader_mock.get_stock_historical_data = MagicMock(
            return_value=expected_df)

    def _mock_downloader_to_get_empty_historical_data(self):
        expected_df = pd.DataFrame([])
        self.downloader_mock.get_stock_historical_data = MagicMock(
            return_value=expected_df)

    # endregion
