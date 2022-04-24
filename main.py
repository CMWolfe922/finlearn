from src.getter import Get
from models.sqliteModels import _query_symbols
import os

# create a Get object
get = Get()

# Table for the list of companies
companies_table_name = "companies"

# Database that companies is saved in
mkt_db = "marketdata"

# run if name == main script
if __name__ == '__main__':
    df = get.companies_df()
    _query_symbols(df)
