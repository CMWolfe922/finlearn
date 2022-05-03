# Create a Get class that gets particular data
# from the web or from other methods
import string
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from models.sqliteModels import _query_symbols


class Get:

    # This function chunks the list of symbols into groups of 200
    def chunks(self, l, n):
        """
        :param l: takes in a list
        :param n: Lets you know how long you want each chunk to be
        """
        n = max(1, n)
        print(f"[+] Chunk symbols into groups of 200..")
        return (l[i: i + n] for i in range(0, len(l), n))

    # This method will return a DataFrame with all the companies
    # listed in the exchanges list
    def companies_df(self):

        exchanges = ["NYSE", "NASDAQ", "AMEX", "OTCBB"]

        def get_companies(exchange="NYSE"):
            """
            :param exchange: The Stock exchange for which you want
            to get a current list of all the symbols for.
            Default -> NYSE

            :returns: a list of tuples containing every company name and symbol in
            the market exchange passed to the function
            """
            alpha = list(string.ascii_uppercase)

            symbols = []
            name = []

            # loop through the letters in the alphabet to get the stocks on each page
            # from the table and store them in a list
            for each in alpha:
                url = "http://eoddata.com/stocklist/{}/{}.htm".format(
                    exchange, each)
                resp = requests.get(url)
                site = resp.content
                soup = bs(site, 'html.parser')
                table = soup.find('table', {'class': 'quotes'})
                for row in table.findAll('tr')[1:]:
                    symbols.append(row.findAll('td')[0].text.rstrip())
                for row in table.findAll('tr')[1:]:
                    name.append(row.findAll('td')[1].text.rstrip())

            # remove the extra letters on the end of the symbols
            symbols_clean = []
            name_clean = []

            for each in symbols:
                each = each.replace('.', '-')
                symbols_clean.append((each.split('-')[0]))

            for each in name:
                each = each.replace('.', '-')
                name_clean.append((each.split('-')[0]))

            return name_clean, symbols_clean

        NYSE_company, NYSE_symbol = get_companies(exchanges[0])
        NASDAQ_company, NASDAQ_symbol = get_companies(exchanges[1])
        AMEX_company, AMEX_symbol = get_companies(exchanges[2])
        OTCBB_company, OTCBB_symbol = get_companies(exchanges[3])

        columns = ["exchange", "symbol", "name"]

        # New York Stock Exchange companies
        NYSE = list(zip(NYSE_symbol, NYSE_company))
        NYSE = [("NYSE",) + elem for elem in NYSE]
        NYSE_df = pd.DataFrame([x for x in NYSE], columns=columns)

        # NASDAQ Companies
        NASDAQ = list(zip(NASDAQ_symbol, NASDAQ_company))
        NASDAQ = [("NASDAQ",) + elem for elem in NASDAQ]
        NASDAQ_df = pd.DataFrame([x for x in NASDAQ], columns=columns)

        # American Stock Exchange Companies
        AMEX = list(zip(AMEX_symbol, AMEX_company))
        AMEX = [("AMEX",) + elem for elem in AMEX]
        AMEX_df = pd.DataFrame([x for x in AMEX], columns=columns)

        # Over the Counter Bulletin Board Exchange "Pink Sheets"
        # These are the penny stocks and I think their is a lot of
        # possibilities with finding a niche in here
        OTCBB = list(zip(OTCBB_symbol, OTCBB_company))
        OTCBB = [("OTCBB",) + elem for elem in OTCBB]
        OTCBB_df = pd.DataFrame([x for x in OTCBB], columns=columns)

        # Now we append all the dataframes together so that we have
        # one massive master list. Also, the good think is we can still
        # use the smaller datasets if need be.

        _companies_df = NYSE_df.append(NASDAQ_df)
        _companies_df = _companies_df.append(AMEX_df)
        _companies_df = _companies_df.append(OTCBB_df)

        # Now check for duplicates and drop them from the main dataset
        _companies_df = _companies_df.drop_duplicates(
            subset="symbol", keep="first")
        _companies_df = _companies_df.drop_duplicates(
            subset="name", keep="first")

        companies_df = _companies_df.copy()
        companies_df.reset_index(inplace=True)
        companies_df.drop(columns='index', inplace=True)

        return companies_df


# Create a Get Obj for Tests
get = Get()

# Create a stock_chunks variable to be used with fundamentals and quotes
_stocks = _query_symbols()

# ready to be imported into whichever script needs it:
stock_chunks = list(get.chunks(list(set(_stocks)), 200))
