from src.getter import Get
from src.pricehistory import pricehistory
from src.fundamentals import fundamental
from src.quotes import quote
from models.sqliteModels import generate_symbols
from models.sqliteModels import stock_chunks
import pandas as pd
import os
import time

# create a Get object
get = Get()


if __name__ == '__main__':
    # time main file
    s = time.time()

    # =========================================================================== #
    # Generator function that will generate one symbol at a time for price
    # history data. This way the function will run once for each symbol
    stock = generate_symbols()

    # Get the quote and fundamental data using stock_chunks
    quote_data = pd.concat([quote.data(each) for each in stock_chunks])
    fundamental_data = pd.concat([fundamental.data(each)
                                 for each in stock_chunks])
    # =========================================================================== #

    e = time.time()
    print(e - s)
