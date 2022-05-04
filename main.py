from src.getter import Get, stock_chunks
from src.pricehistory import price_history
from src.fundamentals import fundamental
from src.quotes import quote
from sqlalchemy import create_engine
from models.sqliteModels import generate_symbols
from models.mysql_db import insert_quote_and_fundamental_data_mysql, connection_uri, marketdata_db
import pandas as pd
import os
import time

# create a Get object
get = Get()


if __name__ == '__main__':
    # time main file
    s = time.time()

    # =========================================================================== #
    # STEP 1: GET THE QUOTE AND FUNDAMENTAL DATA AND INSERT TO DATABASE
    # =========================================================================== #
    # Get the quote and fundamental data using stock_chunks
    quote_data = pd.concat([quote.data(each) for each in stock_chunks])
    fundamental_data = pd.concat([fundamental.data(each)
                                 for each in stock_chunks])

    # create the marketdata database engine:
    engine = connection_uri + '/' + marketdata_db

    # insert the quote and fundamental data into mysql db
    insert_quote_and_fundamental_data_mysql(
        quote_data, fundamental_data, engine)

    # =========================================================================== #
    # STEP 2: GET THE PRICEHISTORY DATA AND INSERT INTO DATABASE
    # =========================================================================== #
    # Generator function that will generate one symbol at a time for price
    # history data. This way the function will run once for each symbol
    # stock = generate_symbols()
    # =========================================================================== #

    e = time.time()
    print("[+] Program finished in {} minutes".format((e - s) / 60))
