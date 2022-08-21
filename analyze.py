import datetime
import math
from datetime import date
from typing import NamedTuple

import pandas as pd
from pandas import DataFrame

from common_types import Period

DECIMAL_PLACES = 4


class AnnualStats(NamedTuple):
    month: float
    quarter: float
    half: float
    year: float

    def round(self):
        return AnnualStats(
            round(self.month, DECIMAL_PLACES),
            round(self.quarter, DECIMAL_PLACES),
            round(self.half, DECIMAL_PLACES),
            round(self.year, DECIMAL_PLACES),
        )


class ClosePrice:

    def __init__(self, a_date: str, close_value: float):
        str_date = self._get_date_as_string(a_date)
        self.date = date.fromisoformat(str_date)
        self.value = close_value

    def round(self):
        return ClosePrice(
            str(self.date),
            round(self.value, DECIMAL_PLACES),
        )

    @staticmethod
    def _get_date_as_string(value) -> str:
        date_type = type(value)
        if date_type is str:
            return value
        elif date_type is pd.Timestamp:
            return value.date().isoformat()
        elif date_type is datetime.datetime:
            return value.date().isoformat()
        elif date_type is datetime.date:
            return value.isoformat()
        else:
            raise ValueError(f'unsupported date type {date_type}')

    def __str__(self):
        return f'{self.date}, {self.value}'

    def __eq__(self, other):
        if not isinstance(other, ClosePrice):
            return False
        return self.date == other.date and self.value == other.value


class PriceStats:

    def __init__(self, min_price: ClosePrice, max_price: ClosePrice,
                 close_price_difference: float,
                 max_negative_change: float, max_positive_change: float):
        self.min_price = min_price
        self.max_price = max_price
        self.min_price_max_price_difference = close_price_difference
        self.max_negative_change = max_negative_change
        self.max_positive_change = max_positive_change

    def round(self):
        return PriceStats(
            self.min_price.round(),
            self.max_price.round(),
            round(self.min_price_max_price_difference, DECIMAL_PLACES),
            round(self.max_negative_change, DECIMAL_PLACES),
            round(self.max_positive_change, DECIMAL_PLACES),
        )

    def __str__(self):
        attributes = [self.min_price, self.max_price,
                      self.min_price_max_price_difference,
                      self.max_negative_change, self.max_positive_change]
        strings = [str(attribute) for attribute in attributes]
        return ','.join(strings)

    def __eq__(self, other):
        if not isinstance(other, PriceStats):
            return False

        return (self.min_price == other.min_price
                and self.max_price == other.max_price
                and self.min_price_max_price_difference == other.min_price_max_price_difference
                and self.max_negative_change == other.max_negative_change
                and self.max_positive_change == other.max_positive_change)


class AnnualPriceStats(NamedTuple):
    month: PriceStats
    quarter: PriceStats
    half: PriceStats
    year: PriceStats


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
