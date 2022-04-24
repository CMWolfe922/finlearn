# QUOTE DATA FROM TD AMERITRADE
# This script is responsible for creating a class for 
# retrieving quote data

from .urls import TDA_BASE
from config.secrets import TDA_APIKEY
import requests
import pandas as pd
from time import sleep

class Fundamental:

	def __init__(self, *stocks):
		self.stocks = stocks

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


# create a fundamental obj to import to tests
fundamental = Fundamental()

"""
The Quote data and Fundamental data both need to have there
stock param lists chuncked into chuncks of 200. It allows 
for the methods to get a response more quickly.
"""