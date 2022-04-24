# QUOTE DATA FROM TD AMERITRADE
# This script is responsible for creating a class for 
# retrieving quote data

from .urls import TDA_BASE
from config.secrets import TDA_APIKEY
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone
import time


today = datetime.today().astimezone(timezone("US/Central"))
today_fmt = today.strftime("%m-%d-%Y")

class Quote:

	def __init__(self, *stocks):
		self.stocks = stocks

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


# create a quote obj to import to tests
quote = Quote()

"""
The Quote data and Fundamental data both need to have there
stock param lists chuncked into chuncks of 200. It allows 
for the methods to get a response more quickly.
"""