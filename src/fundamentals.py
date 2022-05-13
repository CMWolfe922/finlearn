# QUOTE DATA FROM TD AMERITRADE
# This script is responsible for creating a class for
# retrieving quote data

from .urls import TDA_BASE
from config.secrets import TDA_APIKEY
from models.mysql_db import create_marketdata_engine, insert_fundamental_data_mysql
import requests
import pandas as pd
from time import sleep
from loguru import logger
import os.path

# CREATE THE LOGGER FOR THIS SCRIPT:
log_path = str(os.path.pardir) + '/logs/'
base_fmt = "[{time:YYYY-MM-DD at HH:mm:ss}]|[{name}-<lvl>{message}</lvl>]"
logger.add(log_path+"fundamentals.log", rotation="2 MB",
           colorize=True, enqueue=True, catch=True)


class Fundamental:

    def __init__(self, stocks: list):
        self.stocks = stocks
        self.stock_chunks = self.chunks(stocks)
        self.engine = create_marketdata_engine()

    # This function chunks the list of symbols into groups of 200
    def chunks(self, l: list, n: int = 200):
        """
        :param l: takes in a list
        :param n: Lets you know how long you want each chunk to be
        """
        n = max(1, n)
        logger.info("[+] Stocks chunked into groups of 200..")
        return (l[i: i + n] for i in range(0, len(l), n))

    def data(self, stock):
        """
        :param stocks: List of stocks chunked into 200 symbol chunks

        :return: This will return tons of information that will then
        be changed into dataframes and inserted into the database.
        """
        url = TDA_BASE + "instruments"

        # pass params
        params = {"apikey": TDA_APIKEY, "symbol": stock,
                  "projection": "fundamental"}

        request = requests.get(url=url, params=params).json()

        sleep(1)

        # create df
        _df = pd.DataFrame.from_dict(
            request, orient="index").reset_index(drop="True")

        def _reshape_fundamentals(df):

            _fund_list = list(df["fundamental"])
            _df = pd.DataFrame([x for x in _fund_list])
            return _df

        df = _reshape_fundamentals(_df)

        return df

    def execute_main(self):
        """
        :Description: Main method to obtain Fundamental data for every stock in the stocks list
        passed to the Fundamental() class when instantiated. This method will execute the 
        Fundamental.data method using a chunked stocks list.
        """
        logger.info("[-] Executing the main Fundamental Object Method")
        try:
            fundamental_data = pd.concat([self.data(each)
                                   for each in self.stock_chunks])
            logger.info("[+] Fundamental Data Received")
            insert_fundamental_data_mysql(fundamental_data, self.engine)

        except Exception as e:
            logger.error("Error Caused Due to {}", e)


"""
The Quote data and Fundamental data both need to have there
stock param lists chuncked into chuncks of 200. It allows
for the methods to get a response more quickly.
"""
