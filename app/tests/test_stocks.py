"""The user endpoints tests"""
import os
import unittest
import json
import psycopg2
# from instance.config import app_config
from datetime import datetime
from ..app import create_app
from ..app.api.models.stock import Stock
from dotenv import load_dotenv
from loguru import logger

load_dotenv(verbose=True)


class StocksTest(unittest.TestCase):

    def setUp(self):
        """ set the variables before each test """
        self.current_date = datetime.now()
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.auth_header = {'token': os.getenv("TOKEN")}
        os.system("stellar snapshot test_snapshot_{}".format(self.current_date.strftime("%m/%d/%Y_%H:%M:%S")))

    def tearDown(self):
        os.system("stellar restore test_snapshot_{}".format(self.current_date.strftime("%m/%d/%Y_%H:%M:%S")))

    # ACÁ EMPIEZAS A DEFINIR TUS TESTS
    def test_details(self):
        response = self.client.get('/stocks/details', headers=self.auth_header)
        # revisamos que nos de una respuesta ok
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], False)
        self.assertGreater(len(data['result']), 0)

    def test_days_returns(self):
        response = self.client.get('stocks/days_returns/40', headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], False)
        self.assertGreater(len(data['result']), 0)

    def test_add_stock(self):
        stock = {
            "exchange": "TES",
            "ticker": "TEST",
            "stock_name": "Testing"
        }
        response = self.client.post('stocks/',
                                    data=json.dumps(stock),
                                    content_type='application/json',
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], False)

    def test_get_stocks(self):
        response = self.client.get('stocks/', headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], False)
        self.assertGreater(len(data['result']), 0)

    def test_update_stock(self):
        stock = {
            "exchange": "TES",
            "ticker": "TEST",
            "stock_name": "Testing"
        }
        response = self.client.patch('stocks/1112/update',
                                     data=json.dumps(stock),
                                     content_type='application/json',
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], False)
        new_stock = Stock().get_stock(id=1112)
        self.assertEqual(stock['exchange'], new_stock["exchange"])
        self.assertEqual(stock['ticker'], new_stock["ticker"])
        self.assertEqual(stock['stock_name'], new_stock["stock_name"])
        self.assertGreater(len(data['result']), 0)

    def test_delete_stock(self):
        response = self.client.delete('stocks/delete/1112', headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], False)
        new_stock = Stock().get_stock(id=1112)
        self.assertEqual(True, new_stock is None)


if __name__ == "__main__":
    unittest.main()
