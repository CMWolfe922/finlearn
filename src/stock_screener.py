# from config.secrets import mysql_config, url, rapidAPI_yahoo_headers
# I NEED A BETTER WAY TO GET THE MYSQL CONFIG DATA. OR I CAN IMPORT IT FROM mysql_db.py
import mysql.connector as mysql
from mysql.connector import Error
import yfinance as yf
import requests, os
import pandas as pd
import numpy as np
from loguru import logger
from pprint import pprint
from time import monotonic
from concurrent.futures import ThreadPoolExecutor


# ========================================================================================================= #
# TODO: Create global variables and add them below
# ========================================================================================================= #
# Create a path to create a CSV file with all the financial data retrieved:
CSV_PATH = str(os.path.curdir) + '/data/'


# ========================================================================================================= #
# TODO: Create a logger that can log results to the logs directory
# ========================================================================================================= #
log_path = str(os.path.curdir) + '/logs/'
base_fmt = "[{time:YYYY-MM-DD at HH:mm:ss}]|[{name}-<lvl>{message}</lvl>]"
logger.add(log_path+"analyzer.log", rotation="1 MB", colorize=True, enqueue=True, catch=True)


# ========================================================================================================= #
# TODO: Select all the symbols from the companies table in the market data database
# ========================================================================================================= #
def _select_symbols(config:dict=mysql_config):
    """Selects rows from table. Give DB name, table name, and
    num of rows to select and display"""
    table = 'companies'
    query_symbols = f"SELECT symbol FROM {table}"
    try:
        symbols = []
        with mysql.connect(**config) as conn:
            with conn.cursor() as cursor:
                logger.info("--> MySQL Cursor object created successfully.")
                cursor.execute(query_symbols)
                result = cursor.fetchall()
                for row in result:
                    symbols.append(row[0])
        logger.success("[+] Stock Symbols successfully retrieved from database.")
        return symbols
    except Error as e:
        logger.error("[-] Error {} occured", e)

# ========================================================================================================= #
# TODO: Create a function that gets the financials for one symbol, then I can use a map func to get the
# financials for all the tickers in a given list. 
# ========================================================================================================= #
def get_financials(tickers:list):
    try:
        dfs = []
        for ticker in tickers:
            # get the financials for the ticker
            symbol = yf.Ticker(ticker)
            pnl = symbol.financials
            bs = symbol.balancesheet
            cf = symbol.cashflow
            # create the financial statement data frame
            fs = pd.concat([pnl, bs, cf])

            # now make the dataframe format cleaner and swap dates and columns
            data = fs.T
            # reset index (date) into column
            data = data.reset_index()
            data.columns = ['Date', *data.columns[1:]]
            # Add ticker to dataframe
            data['Ticker'] = symbol.ticker
            # append data to dfs list
            dfs.append(data)
            logger.info(f"[+] {ticker} Financials retrieved")

        # Now parse the dataframes
        parser = pd.io.parsers.base_parser.ParserBase({'usecols': None})
        for df in dfs:
            df.columns = parser._maybe_dedup_names(df.columns)
        df = pd.concat(dfs, ignore_index=True)
        df = df.set_index('Ticker', 'Date')
        logger.success("[+] Financial df successfully parsed!")
        
    except Exception as e:
        logger.error(f"[{ticker}] financials not retrieved")

    finally:
        return df


# ========================================================================================================= #
# TODO: append the data to a csv file or create a function to insert to a database: 
# ========================================================================================================= #

def write_to_csv(financials:list):
    """
    :param financials: list of dataframes that needs to be cleaned up to remove the redundant headers
    """
    CSV_FILE = CSV_PATH + 'financials.csv'
    df = financials
    df.to_csv(CSV_FILE, sep = '|', mode='a')
    logger.success("[+] Financials successfully written to CSV")


# ========================================================================================================= #
# PROGRAM LOGIC:
# ========================================================================================================= #

if __name__ == "__main__":
    # Start timer:
    start_time = monotonic()
    # Get the symbols from database
    sym = _select_symbols()
    stocks  = sym[:100]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(get_financials, stocks)

    pprint(results)
    print("*" * 150)
    print(monotonic() - start_time)