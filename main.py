from src.getter import Get
from models.sqliteModels import _query_symbols
import os
import time

# create a Get object
get = Get()


if __name__ == '__main__':
    # time main file
    s = time.time()
    _query_symbols()
