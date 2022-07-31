import math
from datetime import datetime
from typing import NamedTuple

from pandas.core.frame import DataFrame

from common_types import Period


class PriceStats(NamedTuple):
    min_close: float
    max_close: float
    difference: float
    max_negative_change: float
    max_positive_change: float

    # def __str__(self):
    #     attributes = [self.min_close, self.max_close, self.difference,
    #                   self.max_negative_change, self.max_positive_change]
    #     strings = [str(attribute) for attribute in attributes]
    #     return ','.join(strings)


def get_low_and_high_prices(prices: DataFrame) -> None:
    print(f'1 m: {_get_price_stats_in_period(prices, Period.MONTH)}')
    print(f'3 m: {_get_price_stats_in_period(prices, Period.QUARTER)}')
    print(f'6 m: {_get_price_stats_in_period(prices, Period.HALF)}')
    print(f'12m: {_get_price_stats_in_period(prices, Period.YEAR)}')


def get_volatility(prices: DataFrame) -> None:
    print(f'1 m: {_get_volatility_in_period(prices, Period.MONTH)}')
    print(f'3 m: {_get_volatility_in_period(prices, Period.QUARTER)}')
    print(f'6 m: {_get_volatility_in_period(prices, Period.HALF)}')
    print(f'12m: {_get_volatility_in_period(prices, Period.YEAR)}')


# -----------------------------------------------------------------------------
# private methods
# -----------------------------------------------------------------------------

def _get_price_stats_in_period(prices: DataFrame, period: Period) -> PriceStats:
    """
    Return price statistics in a given time period.
    :param prices: Dataframe containing historical price information.
    :param period: Period to get the statistics from the prices dataframe.
    :return: A PriceStats object containing the required information.
    """
    trading_days = _get_trading_days(period)
    min_close_date = prices.Close[:trading_days].idxmin()
    min_close = prices.loc[min_close_date].Close
    max_close_date = prices.Close[:trading_days].idxmax()
    max_close = prices.loc[max_close_date].Close

    difference = _get_price_difference(min_close_date, max_close_date, min_close, max_close)

    max_negative_change = prices.change[:trading_days].min()
    max_positive_change = prices.change[:trading_days].max()

    return PriceStats(min_close, max_close, difference, max_negative_change, max_positive_change)


def _get_price_difference(min_close_date: datetime, max_close_date: datetime, min_close: float,
                          max_close: float) -> float:
    initial, final = (min_close, max_close) if min_close_date <= max_close_date else (max_close, min_close)
    difference = final / initial - 1
    return difference


def _get_volatility_in_period(prices: DataFrame, period: Period) -> float:
    """
    Return volatility defined as sigma(p) = daily sigma * sqrt(p),
    where p = trading days in the given period.
    """
    # calculate daily logarithmic return
    trading_days = _get_trading_days(period)
    daily_std = prices.log_return[:trading_days].std()
    return daily_std * math.sqrt(trading_days)


def _get_trading_days(period: Period) -> int:
    match period:
        case Period.MONTH:
            return 22
        case Period.QUARTER:
            return 63
        case Period.HALF:
            return 126
        case _:
            # Return year by default
            return 252


import download

prices = download.get_stock_historical_data('AMZN', Period.YEAR)
get_low_and_high_prices(prices)
get_volatility(prices)
