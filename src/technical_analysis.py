import pandas as pd
from pandas import DataFrame
import requests


# TECHNICAL ANALYSIS METHODS. THEY WILL BE ADDED TO A CLASS
# TO MAKE IT EASIER TO IMPORT

# [+] COMPLETE #1
def SMA(df:DataFrame, TI:str="SMA", period:int=[30,41,60,82,90], column:str="close") -> DataFrame:
	"""
	Simple moving average - rolling mean in pandas lingo. Also known as 'MA'.
	The simple moving average (SMA) is the most basic of the moving averages used for trading.
	"""
	TI = TI.upper()
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}_{}".format(TI, str(p), column)
			df[col_name] = df[column].rolling(window=p).mean()
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}_{}".format(TI, str(period), column)
		df[col_name] = df[column].rolling(window=period).mean()
		return df

# [+] COMPLETE #2
def SMM(df:DataFrame, TI:str="SMM", period:int=[9,18,27,45,81], column:str="close") -> Series:
	"""
	'Simple Moving Median', an alternative to 'Simple Moving Average'.
	SMA is susceptible to rare events such as rapid shocks or other anomalies.
	A more robust estimate of time series trends is the simple moving median
	over n time periods.
	"""
	TI = TI.upper()
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}_{}".format(TI, str(p), column)
			df[col_name] = df[column].rolling(window=p).median()
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}_{}".format(TI, str(period), column)
		df[col_name] = df[column].rolling(window=period).median()
		return df

# [+] COMPLETE #3
def SSMA(df:DataFrame, TI:str="SSMA", period:int=[9,18,27,45,81], column:str="close", adjust:bool=True) -> Series:
	"""
	Smoothed simple moving average.
	:param df: df
	:param TI: Technical Indicator Symbol
	:param period: range of time
	:param column: open/close/high/low column of the DataFrame
	:return: Adds columns to the dataframe that is passed to the function
	to be saved to a database and eventually used for Machine Learning and Price Prediction
	"""
	TI = TI.upper()
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}_{}".format(TI, str(p), column)
			df[col_name] = df[column].ewm(ignore_na=False, alpha=1.0 / p, min_periods=0, adjust=adjust).mean()
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}_{}".format(TI, str(period), column)
		df[col_name] = df[column].ewm(ignore_na=False, alpha=1.0 / period, min_periods=0, adjust=adjust).mean()
		return df


# [+] COMPLETE #4
def EMA(df:DataFrame, TI:str="EMA", period:int=[9,18,27,45,81], column:str="close", adjust:bool=True) -> Series:
	"""
	"Exponential Weighted Moving Average" - Like all moving average indicators, they are
	much better suited for trending markets.

	When the market is in a strong and sustained uptrend, the EMA indicator line
	will also show an uptrend and vice-versa for a down trend.

	EMAs are commonly used in conjunction with other indicators to confirm
	significant market moves and to gauge their validity.
	"""
	TI = TI.upper()
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}_{}".format(TI, str(p), column)
			df[col_name] = df[column].ewm(span=p, adjust=adjust).mean()
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}_{}".format(TI, str(period), column)
		df[col_name] = df[column].ewm(span=period, adjust=adjust).mean()
		return df


# [+] COMPLETE #5
def DEMA(df:DataFrame, TI:str="DEMA", period:int=[9,18,27,45,81], column:str="close", adjust:bool=True) -> Series:
	"""
	'Double Exponential Moving Average' - attempts to remove the inherent lag with
	Moving Averages by placing more weight on recent values.

	- The name suggests this is achieved by applying a double exponential smoothing
	which is not the case. The name double comes from the fact that the value of an
	EMA (Exponential Moving Average) is doubled.

	- To keep it in line with the actual data and to remove the lag the value
	'EMA of EMA' is subtracted from the previously doubled EMA. Because EMA(EMA) is
	used in the calculation, DEMA needs 2 * period -1 samples to start producing
	values in contrast to the period samples needed by a regular EMA
	"""
	TI = TI.upper()
	# I have to calculate DEMA using the EMA() function.
	DEMA = 2 * EMA(df, period) - EMA(df, period).ewm(span=period, adjust=adjust).mean()
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}_{}".format(TI, str(p), column)
			DEMA = 2 * EMA(df, p) - EMA(df, p).ewm(span=p, adjust=adjust).mean()
			df[col_name] = DEMA
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}_{}".format(TI, str(period), column)
		# I have to calculate DEMA using the EMA() function.
		DEMA = 2 * EMA(df, period) - EMA(df, period).ewm(span=period, adjust=adjust).mean()
		df[col_name] = DEMA
		return df


# [+] COMPLETE #6
def TEMA(df:DataFrame, TI:str="TEMA", period:int=[9,18,27,45,81], adjust:bool=True) -> Series:
	"""
	Triple exponential moving average - attempts to remove the inherent lag associated
	to Moving Averages by placing more weight on recent values.

	The name suggests this is achieved by applying a triple exponential smoothing
	which is not the case. The name triple comes from the fact that the value of an
	EMA (Exponential Moving Average) is triple.

	To keep it in line with the actual data and to remove the lag the value
	'EMA of EMA' is subtracted 3 times from the previously tripled EMA.

	Finally 'EMA of EMA of EMA' is added.
	Because EMA(EMA(EMA)) is used in the calculation, TEMA needs 3 * period - 2
	samples to start producing values in contrast to the period samples
	needed by a regular EMA.
	"""
	TI = TI.upper()
	#============================================================================#

	#============================================================================#
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}".format(TI, str(p))
			#========================================================================#
			triple_ema = 3 * EMA(df, p)
			ema_ema_ema = (
					EMA(df, p).ewm(ignore_na=False, span=p, adjust=adjust).mean()
					.ewm(ignore_na=False, span=p, adjust=adjust).mean()
					)
			TEMA = (
				triple_ema - 3 * EMA(df, p).ewm(span=p, adjust=adjust).mean() + ema_ema_ema
				)
			#========================================================================#
			df[col_name] = TEMA
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}".format(TI, str(period))
		# I have to calculate TEMA using the EMA() function.
		triple_ema = 3 * EMA(df, period)
		ema_ema_ema = (
				EMA(df, period).ewm(ignore_na=False, span=period, adjust=adjust).mean()
				.ewm(ignore_na=False, span=period, adjust=adjust).mean()
				)
		TEMA = (
				triple_ema - 3 * EMA(df, period).ewm(span=period, adjust=adjust).mean() + ema_ema_ema
				)
		df[col_name] = TEMA
		return df

# [+] COMPLETE #7
def TRIMA(df: DataFrame, TI: str="TRIMA", period: int = [18,36,54,81,108]) -> DataFrame:
	"""
	The Triangular Moving Average (TRIMA) [also known as TMA] represents an average of prices,
	but places weight on the middle prices of the time period.
	The calculations double-smooth the data using a window width that is one-half the length of the series.
	source: https://www.thebalance.com/triangular-moving-average-tma-description-and-uses-1031203
	"""
	TI = TI.upper()
	valid = False
	# Checks for list of period values
	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}".format(TI, str(p))
			TRIMA = SMA(df, p).rolling(window=p).sum()
			df[col_name] = TRIMA / p
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}".format(TI, str(period))
		TRIMA = SMA(df, period).rolling(window=period).sum()
		df[col_name] = TRIMA / period
		return df

# [+] COMPLETE #8
def TRIX(df: DataFrame, TI:str="TRIX", period:int=[20,38,56,76,90], column:str="close", adjust:bool=True) -> DataFrame:
	"""
	The TRIX indicator calculates the rate of change of a triple exponential moving average.
	The values oscillate around zero. Buy/sell signals are generated when the TRIX crosses above/below zero.
	A (typically) 9 period exponential moving average of the TRIX can be used as a signal line.
	A buy/sell signals are generated when the TRIX crosses above/below the signal line and is also above/below zero.
	The TRIX was developed by Jack K. Hutson, publisher of Technical Analysis of Stocks & Commodities magazine,
	and was introduced in Volume 1, Number 5 of that magazine.
	"""
	TI = TI.upper()
	valid = False

	data = df[column]

	def _ema(data, period, adjust):
		return pd.Series(data.ewm(span=period, adjust=adjust).mean())

	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}".format(TI, str(p))
			m = _ema(_ema(_ema(data, p, adjust), p, adjust), p, adjust)
			df[col_name] = 100 * (m.diff() / m)
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}".format(TI, str(period))
		m = _ema(_ema(_ema(data, period, adjust), period, adjust), period, adjust)
		df[col_name] = 100 * (m.diff() / m)
		return df

# [+] COMPLETE #9
def VAMA(df: DataFrame, TI:str="VAMA", period:int=[8,16,24,40,56], column:str="close") -> DataFrame:
	"""
	Volume Adjusted Moving Average

	vp = df["volume"] * df[column]
	volsum = df["volume"].rolling(window=period).mean()
	volRatio = pd.Series(vp / volsum, name="VAMA")
	cumSum = (volRatio * df[column]).rolling(window=period).sum()
	cumDiv = volRatio.rolling(window=period).sum()
	"""
	TI = TI.upper()
	valid = False

	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}".format(TI, str(p))

			vp = df["volume"] * df[column]
			volsum = df["volume"].rolling(window=p).mean()
			volRatio = pd.Series(vp / volsum, name="VAMA")
			cumSum = (volRatio * df[column]).rolling(window=p).sum()
			cumDiv = volRatio.rolling(window=p).sum()

			df[col_name] = cumSum / cumDiv
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}".format(TI, str(period))

		vp = df["volume"] * df[column]
		volsum = df["volume"].rolling(window=period).mean()
		volRatio = pd.Series(vp / volsum, name="VAMA")
		cumSum = (volRatio * df[column]).rolling(window=period).sum()
		cumDiv = volRatio.rolling(window=period).sum()

		df[col_name] = cumSum / cumDiv
		return df

# [+] COMPLETE #10
def ZLEMA(df:DataFrame, TI:str="ZLEMA", period:int=[26,12,9,36,48], adjust:bool=True, column:str="close") -> DataFrame:
	"""
	ZLEMA is an abbreviation of Zero Lag Exponential Moving Average. It was
	developed by John Ehlers and Rick Way.
	ZLEMA is a kind of Exponential moving average but its main idea is to
	eliminate the lag arising from the very nature of the moving averages
	and other trend following indicators. As it follows price closer, it
	also provides better price averaging and responds better to price swings.
	"""
	TI = TI.upper()
	valid = False

	if len(period) > 1: valid = True
	if valid:
		for p in period:
			col_name = "{}{}_{}".format(TI, str(p), column)
			lag = (p  - 1) / 2
			ema = pd.Series((df[column] + (df[column].diff(lag))))
			df[col_name] = ema.ewm(span=period, adjust=adjust).mean()
		return df

	else:
		# Just create one column since there is only one period value
		col_name = "{}{}_{}".format(TI, str(period))
		lag = (period  - 1) / 2
		ema = pd.Series((df[column] + (df[column].diff(lag))))
		df[col_name] = ema.ewm(span=period, adjust=adjust).mean()
	return df


# ============================================================ #


# Now I need to build an analyzer:
def analyzer(df, **kwargs):
	"""
	:param df: The dataframe object returned from price data
	:param kwargs: Allows for specifying certain params that can
	be passed to different functions.
	:returns: DataFrame object with added columns of all the functions
	the dataframe gets passed to.

	:Technical Analysis Types: SMA, SMM, SSMA, EMA, DEMA, TEMA, TRIMA, TRIX, VAMA, ZLEMA
	:SMA: df:DataFrame, TI:str="SMA", period=41, column:str="close"
	:SMM: df:DataFrame, TI:str="SMM", period:int=9, column:str="close"
	:SSMA: df:DataFrame, TI:str="SSMA", period:int=9, column:str="close", adjust:bool=True
	:EMA: df:DataFrame, TI:str="EMA", period:int=9, column:str="close", adjust:bool=True
	:DEMA: df:DataFrame, TI:str="DEMA", period:int=9, column:str="close", adjust:bool=True
	:TEMA: df:DataFrame, TI:str="TEMA", period:int=9, adjust:bool=True
	:TRIMA: df: DataFrame, TI: str="TRIMA", period: int = 18
	:TRIX: df: DataFrame, TI:str="TRIX", period:int=20, column:str="close", adjust:bool=True
	:VAMA: df: DataFrame, TI:str="VAMA", period:int=8, column:str="close"
	:ZLEMA: df:DataFrame, TI:str="ZLEMA", period:int=26, adjust:bool=True, column:str="close"

	"""
	# Setup basic for now:
	# TODO: Add custom params intaking, or set them eventually by grouping certain
	# TI into 3 or 4 groups so you only have to pass 3 or 4 sets of params to kwargs
	data = df

	# Pass df to each Analysis Function
	SMA(data)
	SMM(data)
	SSMA(data)
	EMA(data)
	DEMA(data)
	TEMA(data)
	TRIMA(data)
	TRIX(data)
	VAMA(data)
	ZLEMA(data)

	return data
