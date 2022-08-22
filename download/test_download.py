import unittest
from unittest.mock import MagicMock

import pandas as pd
import yfinance as yf

from download.download import Download


class DownloadTests(unittest.TestCase):

    def test_get_stock_historical_data_returns_valid_data(self):
        # arrange
        mocked_yf = self._get_mocked_yfinance()

        symbol = 'AMZN'
        downloader = Download(mocked_yf)
        # act
        prices = downloader.get_stock_historical_data(symbol)
        # assert
        self.assertEqual(len(prices), 252)
        self.assertEqual(len(prices.change), 252)
        self.assertEqual(len(prices.log_return), 252)

    @staticmethod
    def _get_mocked_yfinance():
        expected_df = pd.read_csv('download/test_files/AMZN_from_yfinance.csv')
        mocked_ticker = MagicMock()
        mocked_ticker.history = MagicMock(return_value=expected_df)
        yf.Ticker = MagicMock(return_value=mocked_ticker)
        return yf


if __name__ == '__main__':
    unittest.main()
