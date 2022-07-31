import numpy as np
from pandas.core.frame import DataFrame

from common_types import Period


class Download:

    def __init__(self, financelib):
        self.financelib = financelib

    def get_stock_historical_data(self, symbol: str, period: Period) -> DataFrame:
        """
        Returns historical data in descending order.
        :param symbol: Symbol of the stock we want to get historical data.
        :param period: Time range of the historical data we want to get.
        :return: A pandas dataframe with the historical data in descending order.
        """
        ticker = self.financelib.Ticker(symbol)
        prices = ticker.history(period=period)
        prices.sort_index(ascending=False, inplace=True)
        prices['change'] = (prices.Close - prices.Close.shift(-1)) / prices.Close.shift(-1)
        prices['log_return'] = (np.log(prices.Close / prices.Close.shift(-1)))
        return prices
