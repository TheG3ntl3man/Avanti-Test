import unittest
import sys
import decimal
sys.path.append("..") # Adds higher directory to python modules path
from api.models.ohlc_data import OHLCData

class OhlcTest(unittest.TestCase):

    def test_days_returns_invalid(self):
        response = OHLCData().days_return(-1)
        # Checking if the response is empty when the day is invalid
        self.assertEqual(response, [])

    def test_days_returns_valid(self):
        response = OHLCData().days_return(1)
        # Checking if the data types are correct
        self.assertEqual(type(response[0]['stock_name']), str)
        self.assertEqual(type(response[0]['days_return']), decimal.Decimal)


if __name__ == "__main__":
    unittest.main()