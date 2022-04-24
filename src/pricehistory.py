# PRICE HISTORY SCRIPT 
# This script is responsible for getting the price 
# history of any symbol passed to the constructor
from .urls import TDA_BASE
from config.secrets import TDA_APIKEY
import requests
import pandas as pd

class PriceHistory:

	def __init__(self,**params):
		self.params = params

	def data(self, stock):
		"""
		:param symbol: company symbol/ticker
		:Example: MSFT 10 day minute 10

		:returns: 
		raw json data (Open, High, Low, close, Volume, and Time (epoch time))
		"""
		url = TDA_BASE + f"marketdata/{stock}/pricehistory"

		params = {
			'period': self.params['params']['period'],
			'periodType': self.params['params']['periodType'],
			'frequency': self.params['params']['frequency'],
			'frequencyType': self.params['params']['frequencyType'],
		}

		# Other users will need their own TD Ameritrade API Key
		params.update({"apikey": TDA_APIKEY})

		# request price history data
		req = requests.get(url, params=params).json()

		candles = dict(req)  # turn candles into a dict() type
		extracted_candles_list = candles["candles"]
		symbol = candles["symbol"]  # symbol of the compan's price data

		# Create data frame from extracted data
		df = pd.DataFrame.from_dict(extracted_candles_list, orient="columns")
		df.rename(columns={"datetime": "unix"}, inplace=True)
		df["unix"] = [x for x in df["unix"] // 10 ** 3]

		# This is to insert the companies symbol into the data frame
		# in every row next to the unix_time so that I can identify
		# who the data belongs to.
		df["symbol"] = symbol

		return df

params = {
	'symbol': 'stock',
	'period': '10',
	'periodType': 'day',
	'frequency': '1',
	'frequencyType': 'minute',
}

pricehistory = PriceHistory(params=params)
