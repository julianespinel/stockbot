import unittest
from unittest.mock import patch

import pandas as pd

from src.analyst import analyst
from src.common.types import PriceStats, ClosePrice, PriceAnomaly, Period


class AnalystTests(unittest.TestCase):

    def test_get_return_stats_return_correct_dictionary(self):
        """
        The expected values from this test were calculated in
        the file: csv_files/stock-monitor-example-AMZN.ods
        """
        # arrange
        expected_df = pd.read_csv(
            'src/analyst/test_files/AMZN_from_stockbot.csv')
        # act
        return_stats = analyst.get_return_stats(expected_df).round()
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
        prices = pd.read_csv('src/analyst/test_files/AMZN_from_stockbot.csv')
        # act
        price_stats = analyst.get_price_stats(prices)
        # assert
        self.assertEqual(len(price_stats), 4)

        month = price_stats.month.round()
        self.assertEqual(month, self._get_expected_month_price_stats())

        quarter = price_stats.quarter.round()
        self.assertEqual(quarter, self._get_expected_quarter_price_stats())

        half = price_stats.half.round()
        self.assertEqual(half, self._get_expected_half_price_stats())

        year = price_stats.year.round()
        self.assertEqual(year, self._get_expected_year_price_stats())

    def test_get_volatility_return_correct_dictionary(self):
        """
        The expected values from this test were calculated in
        the file: csv_files/stock-monitor-example-AMZN.ods
        """
        # arrange
        prices = pd.read_csv('src/analyst/test_files/AMZN_from_stockbot.csv')
        # act
        volatility = analyst.get_volatility_stats(prices)
        # assert
        self.assertEqual(len(volatility), 4)
        self.assertEqual(volatility.month, 0.1536)
        self.assertEqual(volatility.quarter, 0.3148)
        self.assertEqual(volatility.half, 0.3995)
        self.assertEqual(volatility.year, 0.4350)

    @patch('src.analyst.analyst.get_current_price')
    def test_get_price_anomaly_return_year_anomaly(self, get_current_price):
        # arrange
        current_price = ClosePrice('2022-07-29', 1.0)
        # expected_price is less than the min price of the last year
        get_current_price.return_value = current_price
        prices = pd.read_csv('src/analyst/test_files/AMZN_from_stockbot.csv')
        # act
        anomaly = analyst.get_price_anomaly(prices)
        # assert
        self.assertIsNotNone(anomaly)
        self.assertEqual(
            anomaly.round(), self._get_expected_year_price_alert(current_price))

    @patch('src.analyst.analyst.get_current_price')
    def test_get_price_anomaly_return_month_anomaly(self, get_current_price):
        # arrange
        current_price = ClosePrice('2022-07-29', 104.0)
        # expected_price is less than the min price of the last month
        get_current_price.return_value = current_price
        prices = pd.read_csv('src/analyst/test_files/AMZN_from_stockbot.csv')
        # act
        anomaly = analyst.get_price_anomaly(prices)
        # assert
        self.assertIsNotNone(anomaly)
        self.assertEqual(
            anomaly.round(), self._get_expected_month_price_alert(current_price))

    @patch('src.analyst.analyst.get_current_price')
    def test_get_price_anomaly_return_none(self, get_current_price):
        # arrange
        expected_price = ClosePrice('2022-07-29', 120.0)
        # expected_price is within min and max of the last year
        get_current_price.return_value = expected_price
        prices = pd.read_csv('src/analyst/test_files/AMZN_from_stockbot.csv')
        # act
        anomaly = analyst.get_price_anomaly(prices)
        # assert
        self.assertIsNone(anomaly)

    @staticmethod
    def _get_expected_month_price_stats():
        min_close = ClosePrice('2022-06-30', 106.21)
        max_close = ClosePrice('2022-07-29', 134.95)
        expected_month = PriceStats(min_close, max_close, 0.2706, -0.0523, 0.1036)
        return expected_month

    @staticmethod
    def _get_expected_quarter_price_stats():
        min_close = ClosePrice('2022-06-14', 102.31)
        max_close = ClosePrice('2022-07-29', 134.95)
        expected_month = PriceStats(min_close, max_close, 0.3190, -0.1405, 0.1036)
        return expected_month

    @staticmethod
    def _get_expected_half_price_stats():
        min_close = ClosePrice('2022-06-14', 102.31)
        max_close = ClosePrice('2022-03-29', 169.3150)
        expected_month = PriceStats(min_close, max_close, -0.3957, -0.1405, 0.1354)
        return expected_month

    @staticmethod
    def _get_expected_year_price_stats():
        min_close = ClosePrice('2022-06-14', 102.31)
        max_close = ClosePrice('2021-11-18', 184.8030)
        expected_month = PriceStats(min_close, max_close, -0.4464, -0.1405, 0.1354)
        return expected_month

    @staticmethod
    def _get_expected_month_price_alert(current_price: ClosePrice):
        min_price = ClosePrice('2022-06-30', 106.21)
        max_price = ClosePrice('2022-07-29', 134.95)
        return PriceAnomaly(Period.MONTH, min_price, current_price, max_price)

    @staticmethod
    def _get_expected_year_price_alert(current_price: ClosePrice):
        min_price = ClosePrice('2022-06-14', 102.31)
        max_price = ClosePrice('2021-11-18', 184.8030)
        return PriceAnomaly(Period.YEAR, min_price, current_price, max_price)
