import numpy as np
from pandas import DataFrame

from src.common.types import Period


class Download:

    def __init__(self, financelib) -> None:
        self.financelib = financelib

    def get_stock_historical_data(self, symbol: str) -> DataFrame:
        """
        Returns historical data in descending order.
        :param symbol: Symbol of the stock we want to get historical data.
        :return: A pandas dataframe with the historical data in descending order.
        """
        ticker = self.financelib.Ticker(symbol)
        prices = ticker.history(period=Period.YEAR)

        prices.sort_index(ascending=False, inplace=True)  # Today's index should be 0
        prices = prices.reset_index()  # Required to add row number as index

        prices['change'] = (prices.Close - prices.Close.shift(-1)) / prices.Close.shift(-1)
        prices['log_return'] = (np.log(prices.Close / prices.Close.shift(-1)))
        return prices
