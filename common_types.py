from enum import Enum


class Period(str, Enum):
    MONTH = '1mo'
    QUARTER = '3mo'
    HALF = '6mo'
    YEAR = '12mo'
