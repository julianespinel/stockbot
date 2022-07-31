import unittest
from unittest.mock import MagicMock

import pandas as pd
import yfinance as yf

from common_types import Period
from download import Download


class DownloadTests(unittest.TestCase):

    def test_get_stock_historical_data_returns_valid_data(self):
        # arrange
        expected_df = pd.read_csv('csv_files/AMZN.csv')
        mocked_ticker = MagicMock()
        mocked_ticker.history = MagicMock(return_value=expected_df)
        yf.Ticker = MagicMock(return_value=mocked_ticker)

        symbol = 'AMZN'
        period = Period.YEAR
        downloader = Download(yf)
        # act
        prices = downloader.get_stock_historical_data(symbol, period)
        # assert
        self.assertEqual(len(prices), 252)
        self.assertEqual(len(prices.change), 252)
        self.assertEqual(len(prices.log_return), 252)


if __name__ == '__main__':
    unittest.main()
