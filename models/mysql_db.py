from sqlalchemy import create_engine
from mysql.connector import connect, Error
from getpass import getpass
from config.secrets import MYSQL_HOST, MYSQL_PORT, MYSQL_PASSWORD, MYSQL_USER, MYSQL_MARKET_DB, MYSQL_PRICEHISTORY_DB
import pandas as pd

h, u, pw = MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD

# DATABASES FOR INSERTING AND QUERYING DATA FROM:
marketdata_db = MYSQL_MARKET_DB
pricehistory_db = MYSQL_PRICEHISTORY_DB


# CREATE A FUNCTION FOR CONNECTING TO EACH DATABASE:
def create_marketdata_engine():
    DB = marketdata_db
    connection_uri = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB}"
    _engine = create_engine(connection_uri, echo=True)
    return _engine


def create_pricehistory_engine():
    DB = pricehistory_db
    connection_uri = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB}"
    _engine = create_engine(connection_uri, echo=True)
    return _engine


# CONNECTION URI FOR SQLALCHEMY TO CREATE ENGINE. MUST ADD /{DB} TO END WHEN USED
connection_uri = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"


# CREATE A FUNCTION TO SELECT SYMBOLS FROM MYSQL DATABASE
def _select_symbols():
    """Selects rows from table. Give DB name, table name, and
    num of rows to select and display"""
    db = marketdata_db
    table = 'companies'
    query_symbols = f"SELECT symbol FROM {table}"
    try:
        symbols = []
        with connect(host=h, user=u, password=pw, database=db) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_symbols)
                result = cursor.fetchall()
                for row in result:
                    symbols.append(row[0])
        return symbols
    except Error as e:
        print(f"[-] Error Ocurred: ---> {e}; ")


# CREATE A GENERATOR FUNCTION TO SELECT SYMBOLS FROM MYSQL ONE AT A TIME
def generate_symbols():
    data = _select_symbols()
    symbols = [stock for stock in data]
    for symbol in symbols:
        yield symbol


# ========================================================================================== #
# FUNCTIONS TO INSERT QUOTE AND FUNDAMENTAL DATA INTO THE MARKETDATA DATABASE
# ========================================================================================== #

# FUNCTION TO INSERT QUOTE DATA INTO DATABASE


def insert_quote_data_mysql(quote_df, engine):
    """
    :param quote_df: Quote Data Dataframe
    :param engine: database connection variable for mysql
    """
    try:
        quote_df.to_sql(name="quote_data", con=engine,
                        if_exists="append", index=False)
        print("[+] Quote Data Inserted")
    except:
        raise ValueError(
            "[-] Data not inserted correctly. Make sure datatype is correct"
        )


# FUNCTION TO INSERT FUNDAMENTAL DATA INTO DATABASE
def insert_fundamental_data_mysql(fun_df, engine):
    """
    :param fun_df: Quote Data Dataframe
    :param db: database connection variable
    """
    try:
        fun_df.to_sql(name="fundamental_data", con=engine,
                      if_exists="append", index=False)
        print("[+] Fundamental Data Inserted")
    except:
        raise ValueError(
            "[-] Data not inserted correctly. Make sure it was a string object."
        )


# FUNCTION TO INSERT THE IMPORTED QUOTE AND FUNDAMENTAL DATA INTO THE DATABASE
def insert_quote_and_fundamental_data_mysql(quote_data, fundamental_data, engine):
    """
    :param quote_data: the quote data from the tdameritrade api
    :param fundamental_data: the fundamental data from the tdameritrade api
    """
    # [1] use the insert_quote_data function imported from models.py
    # to insert quote data into the database.
    insert_quote_data_mysql(quote_data, engine)

    # [2] use the insert_fundamental_data function imported from models.py
    # to insert fundamental data into the database.
    insert_fundamental_data_mysql(fundamental_data, engine)
