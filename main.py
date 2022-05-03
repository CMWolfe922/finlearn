from src.getter import Get, stock_chunks
from src.pricehistory import pricehistory
from src.fundamentals import fundamental
from src.quotes import quote
from models.sqliteModels import generate_symbols
import pandas as pd
import os
import time

# create a Get object
get = Get()


if __name__ == '__main__':
    # time main file
    s = time.time()

    # =========================================================================== #
    # Get the quote and fundamental data using stock_chunks
    quote_data = pd.concat([quote.data(each) for each in stock_chunks])
    fundamental_data = pd.concat([fundamental.data(each)
                                 for each in stock_chunks])

    # Generator function that will generate one symbol at a time for price
    # history data. This way the function will run once for each symbol
    # stock = generate_symbols()
    # =========================================================================== #

    e = time.time()
    print("[+] Program finished in {} minutes".format((e - s) / 60))
