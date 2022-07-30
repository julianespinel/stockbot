import math

from pandas.core.frame import DataFrame

from common_types import Period


def get_volatility(prices: DataFrame) -> None:
    print(_get_volatility_in_period(prices, Period.MONTH))
    print(_get_volatility_in_period(prices, Period.QUARTER))
    print(_get_volatility_in_period(prices, Period.HALF))
    print(_get_volatility_in_period(prices, Period.YEAR))


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
get_volatility(prices)
