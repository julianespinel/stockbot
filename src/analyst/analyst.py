import math

from pandas import DataFrame

from common.constants import DECIMAL_PLACES
from common.types import (
    Period,
    AnnualStats,
    ClosePrice,
    AnnualPriceStats,
    PriceStats,
    PriceAnomaly,
)


def get_return_stats(prices: DataFrame) -> AnnualStats:
    return AnnualStats(
        month=_get_return_in_period(prices, Period.MONTH),
        quarter=_get_return_in_period(prices, Period.QUARTER),
        half=_get_return_in_period(prices, Period.HALF),
        year=_get_return_in_period(prices, Period.YEAR),
    )


def get_current_price(prices: DataFrame) -> ClosePrice:
    today_row = prices.iloc[0]
    return ClosePrice(today_row.Date, today_row.Close)


def get_price_stats(prices: DataFrame) -> AnnualPriceStats:
    return AnnualPriceStats(
        month=_get_price_stats_in_period(prices, Period.MONTH),
        quarter=_get_price_stats_in_period(prices, Period.QUARTER),
        half=_get_price_stats_in_period(prices, Period.HALF),
        year=_get_price_stats_in_period(prices, Period.YEAR),
    )


def get_volatility_stats(prices: DataFrame) -> AnnualStats:
    return AnnualStats(
        month=_get_volatility_in_period(prices, Period.MONTH),
        quarter=_get_volatility_in_period(prices, Period.QUARTER),
        half=_get_volatility_in_period(prices, Period.HALF),
        year=_get_volatility_in_period(prices, Period.YEAR),
    )


def get_price_anomaly(prices: DataFrame) -> PriceAnomaly:
    current_price = get_current_price(prices)
    for period in reversed(Period):  # from year to month
        min_price = _get_min_price(prices, period)
        max_price = _get_max_price(prices, period)
        if _is_out_of_bounds(min_price, current_price, max_price):
            return PriceAnomaly(period, min_price, current_price, max_price)

    return None


# -----------------------------------------------------------------------------
# private methods
# -----------------------------------------------------------------------------


def _get_return_in_period(prices: DataFrame, period: Period) -> float:
    today_price = get_current_price(prices)
    initial_row = prices.iloc[_get_trading_days(period) - 1]
    initial_price = ClosePrice(initial_row.Date, initial_row.Close)
    return _get_price_difference(today_price, initial_price)


def _get_price_stats_in_period(prices: DataFrame, period: Period) -> PriceStats:
    """
    Return price statistics in a given time period.
    :param prices: Dataframe containing historical price information.
    :param period: Period to get the statistics from the prices dataframe.
    :return: A PriceStats object containing the required information.
    """
    min_price = _get_min_price(prices, period)
    max_price = _get_max_price(prices, period)

    difference = _get_price_difference(min_price, max_price)

    trading_days = _get_trading_days(period)
    max_negative_change = prices.change[:trading_days].min()
    max_positive_change = prices.change[:trading_days].max()

    return PriceStats(min_price, max_price, difference,
                      max_negative_change, max_positive_change)


def _get_price_difference(a_price: ClosePrice, other_price: ClosePrice) -> float:
    if a_price.date <= other_price.date:
        initial, final = a_price, other_price
    else:
        initial, final = other_price, a_price

    return final.value / initial.value - 1


def _get_min_price(prices: DataFrame, period: Period) -> ClosePrice:
    trading_days = _get_trading_days(period)
    row_id = prices.Close[:trading_days].idxmin()
    row = prices.iloc[row_id]
    return ClosePrice(row.Date, row.Close)


def _get_max_price(prices: DataFrame, period: Period) -> ClosePrice:
    trading_days = _get_trading_days(period)
    row_id = prices.Close[:trading_days].idxmax()
    row = prices.iloc[row_id]
    return ClosePrice(row.Date, row.Close)


def _get_volatility_in_period(prices: DataFrame, period: Period) -> float:
    """
    Return volatility defined as sigma(p) = daily sigma * sqrt(p),
    where p = trading days in the given period.
    See: https://en.wikipedia.org/wiki/Volatility_(finance)#Mathematical_definition
    """
    # calculate daily logarithmic return
    trading_days = _get_trading_days(period)
    daily_std = prices.log_return[:trading_days].std()
    volatility = daily_std * math.sqrt(trading_days)
    return round(volatility, DECIMAL_PLACES)


def _get_trading_days(period: Period) -> int:
    if period == Period.MONTH:
        return 22
    elif period == Period.QUARTER:
        return 63
    elif period == Period.HALF:
        return 126
    else:
        # Return year by default
        return 252


def _is_out_of_bounds(min_price: ClosePrice,
                      current_price: ClosePrice,
                      max_price: ClosePrice):
    return current_price.value <= min_price.value \
           or current_price.value >= max_price.value
