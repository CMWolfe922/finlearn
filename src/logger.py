# Use Loguru to create a decorator function that allows me
# to log data into the data directory after each
# method or function is executed

from loguru import logger


class FinancialLog(logger):

    def __init__(self):
        self.base_format = "{time} - {level} - {name} - {message} "
