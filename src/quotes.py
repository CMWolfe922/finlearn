# QUOTE DATA FROM TD AMERITRADE
# This script is responsible for creating a class for
# retrieving quote data

import multiprocessing
from urls import TDA_BASE
from config.secrets import TDA_APIKEY 
from models.mysql_db import insert_quote_data_mysql, create_marketdata_engine, _select_symbols
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone
import time
from loguru import logger
import os.path

# DATE BUILDING AND MANAGEMENT
today = datetime.today().astimezone(timezone("US/Central"))
today_fmt = today.strftime("%m-%d-%Y")

# CREATE THE LOGGER FOR THIS SCRIPT:
log_path = str(os.path.pardir) + '/logs/'
base_fmt = "[{time:YYYY-MM-DD at HH:mm:ss}]|[{name}-<lvl>{message}</lvl>]"
logger.add(log_path+"main.log", rotation="5 MB",
           colorize=True, enqueue=True, catch=True)

# QUERY STOCK SYMBOLS FROM MYSQL DATABASE:
stocks = _select_symbols()


class Quote:

    def __init__(self, stocks: list):
        self.stocks = stocks
        self.stock_chunks = self.chunks(stocks) # Chunks the stock list upon instantiation 
        self.engine = create_marketdata_engine() # Creates a database connection engine upon instantiation

        # This function chunks the list of symbols into groups of 200
    def chunks(self, l: list, n: int = 200):
        """
        :param l: takes in a list
        :param n: Lets you know how long you want each chunk to be
        """
        n = max(1, n)
        print(f"[+] Chunk symbols into groups of 200..")
        return (l[i: i + n] for i in range(0, len(l), n))

    def data(self, stock):
        """
        :param stock: a stock symbol
        :return: raw json data to be passed to the
        """
        url = TDA_BASE + "marketdata/quotes"  # market data url
        params = {"apikey": TDA_APIKEY, "symbol": stock}
        request = requests.get(url=url, params=params).json()

        time.sleep(1)  # set sleep so that api works

        # create df
        df = pd.DataFrame.from_dict(
            request, orient="index").reset_index(drop=True)

        # Quote Data: formatting the dates and other columns
        # Now I need to add the dates and format the dates for the database
        df["date"] = pd.to_datetime(today_fmt)
        df["date"] = df["date"].dt.date
        df["divDate"] = pd.to_datetime(df["divDate"])
        df["divDate"] = df["divDate"].dt.date

        # Remove anything without a price
        df = df.loc[df["bidPrice"] > 0]

        # Rename columns, They can't start with a number
        df = df.rename(
            columns={"52WkHigh": "_52WkHigh", "52WkLow": "_52WkLow"})

        return df

    def execute_main(self):
        """
        :Description: Main method to obtain Quote data for every stock in the stocks list
        passed to the Quotes() class when instantiated. This method will execute the 
        Quote.data method using a chunked stocks list.
        """
        logger.info("[-] Executing the main Quote Object Method - {time}")
        try:
            quote_data = pd.concat([self.data(each)
                                   for each in self.stock_chunks])
            logger.info("[+] Quote Data Received - {time}")
            insert_quote_data_mysql(quote_data, self.engine)

        except Exception as e:
            logger.error("Error Caused Due to {}", e)


class ProcessQuote(multiprocessing.Process):

    def __init__(self, task):
        super(ProcessQuote, self).__init__()
        self.task = task

    def run(self):
        # THIS WILL EXECUTE THE MAIN METHOD IN QUOTE USING MAP AND THREADED POOL PROCESSES:
        pass


# create a quote obj to import to tests
quote = Quote(stocks=stocks)

# # execute main method as a test
# quote.execute_main()
"""
The Quote data and Fundamental data both need to have there
stock param lists chuncked into chuncks of 200. It allows
for the methods to get a response more quickly.
"""
