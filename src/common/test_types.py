import datetime
import unittest

import pandas as pd

from common.types import ClosePrice


class TypesTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_ClosePrice_given_date_as_iso_string_return_a_ClosePrice(self):
        # arrange
        date_str = '2022-08-22'
        close_value = 100
        expected_date = datetime.date.fromisoformat(date_str)
        # act
        close_price = ClosePrice(date_str, close_value)
        # assert
        self.assertEqual(close_price.date, expected_date)
        self.assertEqual(close_price.value, close_value)

    def test_create_ClosePrice_given_date_as_timestamp_return_a_ClosePrice(self):
        # arrange
        a_datetime = datetime.datetime(2022, 8, 22)
        timestamp_date = pd.Timestamp(a_datetime)
        close_value = 100
        # act
        close_price = ClosePrice(timestamp_date, close_value)
        # assert
        self.assertEqual(close_price.date, a_datetime.date())
        self.assertEqual(close_price.value, close_value)

    def test_create_ClosePrice_given_date_as_datetime_return_a_ClosePrice(self):
        # arrange
        a_datetime = datetime.datetime(2022, 8, 22)
        close_value = 100
        # act
        close_price = ClosePrice(a_datetime, close_value)
        # assert
        self.assertEqual(close_price.date, a_datetime.date())
        self.assertEqual(close_price.value, close_value)

    def test_create_ClosePrice_given_date_as_date_return_a_ClosePrice(self):
        # arrange
        a_date = datetime.date(2022, 8, 22)
        close_value = 100
        # act
        close_price = ClosePrice(a_date, close_value)
        # assert
        self.assertEqual(close_price.date, a_date)
        self.assertEqual(close_price.value, close_value)

    def test_create_ClosePrice_given_date_as_int_raise_an_exception(self):
        # arrange
        date_millis = datetime.datetime(2022, 8, 22).timestamp() * 1_000
        close_value = 100
        # act and assert
        self.assertRaises(ValueError, ClosePrice, date_millis, close_value)

    def test_create_ClosePrice_given_an_invalid_date_raise_an_exception(self):
        # arrange
        invalid_date = '2022-30-30'
        close_value = 100
        # act and assert
        self.assertRaises(ValueError, ClosePrice, invalid_date, close_value)
