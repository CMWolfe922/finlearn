import sqlite3 as sql
from dataclasses import dataclass
from humanize import naturaltime
from time import time
import pandas as pd
import os

market_db_uri = 'data\\marketdata.db'
ph_db_uri = 'data\\pricehistory.db'


# ----------------------------------------------------------- #
# CREATE FUNCTION TO INSERT COMPANY DATA FROM STOCKDATA
# ----------------------------------------------------------- #
def _insert_companies(company_df, db_name=market_db_uri, table_name="companies"):
    """
    :param company_df: pandas DataFrame of list of companies
    :param db_name: name of database to insert data into
    :param table_name: name of table to save data to in database

    :return: Message stating companies were inserted correctly
    or a message saying database and table already exists. If
    table and database already exists, then the query_symbols
    function will be called
    """

    table = table_name
    db = db_name
    df = company_df

    print(f"[1.1.1] Create new database {db}.. ")
    conn = sql.connect(db)  # create database
    df.to_sql(name=table, con=conn, if_exists="replace", index=True)
    conn.close()
    print(f"[1.1.2] Insert data to {table} table in {db}.. ")
    # basically this should only work the very first time
    # the program is run and no database exists yet.


# ================================================================================ #
# FUNCTION BEGINS: second step, give values to
table_name = "companies"

# ----------------------------------------------------------- #
# CREATE FUNCTION TO QUERY SYMBOLS FROM DB IF IT EXISTS
# ----------------------------------------------------------- #


def _query_symbols(db_name, table_name):
    """
    :param db_name: name of database to retrieve symbols from
    :param table_name: name of table symbols are saved in

    :return: all the stock symbols in a list to be chunked
    """
    table = table_name
    db = db_name
    symbols = []
    if os.path.exists(db):
        query_symbols = f"SELECT symbol FROM {table} "
        conn = sql.connect(db)
        cur = conn.cursor()
        for row in cur.execute(query_symbols):
            symbols.append(row)

        if len(symbols) > 19000:
            return symbols
