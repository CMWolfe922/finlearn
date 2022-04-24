from operator import length_hint
from src.pricehistory import pricehistory
from src.quotes import quote
from src.fundamentals import fundamental
from src.getter import get
import pandas as pd
import random
import unittest
import time
from models.sqliteModels import generate_symbols

# use symbol generator to create 100 random stock symbols
symbol = generate_symbols

# create a list of stocks to try the multiprocessing map func on
# by generating 100 symbols

stocks = ['MSFT', 'FB', 'AMZN', 'AAPL', 'CHWY',
          'BAC', 'JNJ', 'BA', 'LMT', 'KO', 'SHOP']


class TestPriceHistory(unittest.TestCase):
    """
    Create tests for PriceHistory class
    """

    def test_get_DataFrame(self):
        """
        Test that PriceHistory.data() returns a DataFrame
        """
        # Pick a random stock symbol for the param
        stock = random.choice(stocks)
        result = pricehistory.data(stock)
        self.assertIsInstance(result, pd.DataFrame)

    def test_received_data_for_all_stock_symbols(self):
        """
        Use the map function to get price history data or whatever
        data is needed.
        """
        length_of_stocks = len(stocks)
        results = map(pricehistory.data, stocks)
        rlist = []
        for i in results:
            rlist.append(i)
        length_of_results = len(rlist)
        self.assertIsInstance(length_of_stocks, length_of_results)


class TestQuoteData(unittest.TestCase):
    """
    Create Tests for the Quote Data Class:
    """

    def test_get_DataFrame(self):
        """
        Test that Quote.data() returns a DataFrame
        """
        stock = random.choice(stocks)
        result = quote.data(stock)
        self.assertIsInstance(result, pd.DataFrame)

    def test_received_data_for_all_stock_symbols(self):
        """
        Use the map function to get quote data or whatever
        data is needed.
        """
        length_of_stocks = len(stocks)
        results = map(quote.data, stocks)
        rlist = []
        for i in results:
            rlist.append(i)
        length_of_results = len(rlist)
        self.assertIsInstance(length_of_stocks, length_of_results)


class TestFundamentalData(unittest.TestCase):
    """
    Create Tests for the Fundamental Data Class:
    """

    def test_get_DataFrame(self):
        """
        Test that Fundamental.data() returns a DataFrame
        """
        stock = random.choice(stocks)
        result = fundamental.data(stock)
        self.assertIsInstance(result, pd.DataFrame)

    def test_received_data_for_all_stock_symbols(self):
        """
        Use the map function to get quote data or whatever
        data is needed.
        """
        length_of_stocks = len(stocks)
        results = map(fundamental.data, stocks)
        rlist = []
        for i in results:
            rlist.append(i)
        length_of_results = len(rlist)
        self.assertIsInstance(length_of_stocks, length_of_results)


if __name__ == '__main__':
    s = time.time()
    unittest.main()

    e = time.time()

    print(e - s)
