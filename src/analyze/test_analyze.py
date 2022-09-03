import unittest

import pandas as pd

from analyze import analyze
from common.types import PriceStats, ClosePrice


class AnalyzeTests(unittest.TestCase):

    def test_get_return_stats_return_correct_dictionary(self):
        """
        The expected values from this test were calculated in
        the file: csv_files/stock-monitor-example-AMZN.ods
        """
        # arrange
        expected_df = pd.read_csv('analyze/test_files/AMZN_from_stockbot.csv')
        # act
        return_stats = analyze.get_return_stats(expected_df).round()
        # assert
        self.assertEqual(len(return_stats), 4)
        self.assertEqual(return_stats.month, 0.2390)
        self.assertEqual(return_stats.quarter, 0.0858)
        self.assertEqual(return_stats.half, -0.0627)
        self.assertEqual(return_stats.year, -0.1889)

    def test_get_low_and_high_prices_return_correct_dictionary(self):
        """
        The expected values from this test were calculated in
        the file: csv_files/stock-monitor-example-AMZN.ods
        """
        # arrange
        prices = pd.read_csv('analyze/test_files/AMZN_from_stockbot.csv')
        # act
        price_stats = analyze.get_price_stats(prices)
        # assert
        self.assertEqual(len(price_stats), 4)

        month = price_stats.month.round()
        self.assertEqual(month, self._get_expected_month())

        quarter = price_stats.quarter.round()
        self.assertEqual(quarter, self._get_expected_quarter())

        half = price_stats.half.round()
        self.assertEqual(half, self._get_expected_half())

        year = price_stats.year.round()
        self.assertEqual(year, self._get_expected_year())

    def test_get_volatility_return_correct_dictionary(self):
        """
        The expected values from this test were calculated in
        the file: csv_files/stock-monitor-example-AMZN.ods
        """
        # arrange
        prices = pd.read_csv('analyze/test_files/AMZN_from_stockbot.csv')
        # act
        volatility = analyze.get_volatility_stats(prices)
        # assert
        self.assertEqual(len(volatility), 4)
        self.assertEqual(volatility.month, 0.1536)
        self.assertEqual(volatility.quarter, 0.3148)
        self.assertEqual(volatility.half, 0.3995)
        self.assertEqual(volatility.year, 0.4350)

    @staticmethod
    def _get_expected_month():
        min_close = ClosePrice('2022-06-30', 106.21)
        max_close = ClosePrice('2022-07-29', 134.95)
        expected_month = PriceStats(min_close, max_close, 0.2706, -0.0523, 0.1036)
        return expected_month

    @staticmethod
    def _get_expected_quarter():
        min_close = ClosePrice('2022-06-14', 102.31)
        max_close = ClosePrice('2022-07-29', 134.95)
        expected_month = PriceStats(min_close, max_close, 0.3190, -0.1405, 0.1036)
        return expected_month

    @staticmethod
    def _get_expected_half():
        min_close = ClosePrice('2022-06-14', 102.31)
        max_close = ClosePrice('2022-03-29', 169.3150)
        expected_month = PriceStats(min_close, max_close, -0.3957, -0.1405, 0.1354)
        return expected_month

    @staticmethod
    def _get_expected_year():
        min_close = ClosePrice('2022-06-14', 102.31)
        max_close = ClosePrice('2021-11-18', 184.8030)
        expected_month = PriceStats(min_close, max_close, -0.4464, -0.1405, 0.1354)
        return expected_month
