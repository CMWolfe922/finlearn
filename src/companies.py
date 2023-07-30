"""
This script will be to create an object that scrapes
the web for the data required to create a new 
compaines dataframe object.
""" 

import pandas as pd
import requests 
from bs4 import BeautifulSoup as bs
import string

class Companies():
    
    def __init__(self, exchange):
        self.exchange = exchange
        
    def get(self):
        
        alpha = list(string.ascii_uppercase)
        
        symbols = []
        # names = []
        
        # loop through the letters in the alphabet to get the stocks on each page
        # from the table and store them in a list
        for each in alpha:
            url = "http://eoddata.com/stocklist/{}/{}.htm".format(
                self.exchange, each)
            # resp = requests.get(url)
            # site = resp.content
            # soup = bs(requests.get(url).content, 'html.parser')
            # table = soup.find('table', {'class': 'quotes'})
            # symbols.append(row.findAll('td')[0].text.rstrip() for row in bs(requests.get(url).content, 'html.parser').find('table', {'class': 'quotes'}).findAll('td')[0].text.rstrip())
            table = bs(requests.get(url).content, 'html.parser').find('table', {'class': 'quotes'})
            symbols.append(row.findAll('td')[0].text.rstrip() for row in table.findAll('tr')[1:])
            # for row in table.findAll('tr')[1:]:
            #     symbols.append(row.findAll('td')[0].text.rstrip())

            # for row in table.findAll('tr')[1:]:
            #     names.append(row.findAll('td')[1].text.rstrip())

        # remove the extra letters on the end of the symbols
        # symbols_clean_short = [each.replace('.','-')[0] for each.split('-')[0] in symbols]
        # names_clean_short = [each.replace('.','-')[0] for each.split('-')[0] in names]
        
        # symbols_clean = []
        # names_clean = []
        
        # for each in symbols:
        #     each = each.replace('.', '-')
        #     symbols_clean.append((each.split('-')[0]))

        # for each in names:
        #     each = each.replace('.', '-')
        #     names_clean.append((each.split('-')[0]))
            
        # companies = list(zip(symbols_clean, names_clean))
        # companies = [(self.exchange.upper(), ) + elem for elem in companies]
        # columns = ['exchange', 'symbol', 'name']
        # df = pd.DataFrame([x for x in companies], columns=columns)
        # return df
        yield symbols

    
if __name__ == "__main__":
    c = Companies('nasdaq')
    df = c.get()
    for each in df:
        for s in each:
            for i in s:
                print(i)