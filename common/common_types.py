import datetime
from datetime import date
from enum import Enum
from typing import NamedTuple

import pandas as pd

DECIMAL_PLACES = 4


class Period(str, Enum):
    MONTH = '1mo'
    QUARTER = '3mo'
    HALF = '6mo'
    YEAR = '12mo'


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
