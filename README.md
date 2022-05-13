# FINLEARN:

---

Finlearn is a financial analysis tool that continues to learn. The point of __finlearn__ is to be a price prediction app that utilizes hundreds of different sources and thousands of data points. Everything from the types of articles posted to weather, to general public "mental health". Finlearn gathers data on every single company listed in the U.S. Stock Market roughly 19,400+ companies 

Finlearn will use social media apps to gauge the general mental health of society. The way to do this, we will need to build an algorithm that checks the kinds of posts that are posted each day. Then the algorithm will need to use a scale to gauge positive or negative. Besides just checking social media, we will also check big box retail stores to see how many reviews have been left and what those review sentiments are. The reason for this is to test for correlation between stock purchase volumes and online shopping. The idea is that "buyers fever" floods over into the market and causes key stocks to go up. So if more people are buying consumer goods, maybe that correlates to more people buying into the markets. Then we can figure out which sectors have the highest correlation.

That is just a few of the simple ideas behind finlearn. But besides those there are more that I plan to use but don't want to share publicly. Although finlearn will be able to be used by the public, we can't share every detail about how the algorithm will work, otherwise it will be useless and have no value.

Also, since most of the analysis is focused on minute data, my price predictor is making predictions an hour to 24 hours in advance and predicting price movement just days in advance. We will have daily price data as well and focus have predictors that make longer predictions, but the main focus is minute data and going off the idea that since the market behavior is changing so rapidly, a lot of the past data isn't as relevant as it used to be. 

---

#### Requirements:
---
To use finlearn you will need to have MySQL downloaded (unless you want all your data in SQLite which wouldn't be that ideal considering the amount of data). Once MySQL is downloaded, create two databases pricehistory and marketdata.

- Then in the config directory, create a 'config.ini' file and add the below information to it:
```
[MySQL Ubuntu]
    user=<user>
    password=<password>
    host=localhost
    port=3306
    cxn_uri=mysql://user:password@localhost:3306/
    market_db=marketdata
    pricehistory_db=pricehistory
    sentiment_db=sentiment_data

[MySQL Windows]
    user=<user>
    password=<password>
    host=localhost
    port=3306
    cxn_uri='mysql+mysqldb://username:password@localhost:3306/'
    market_db=marketdata
    pricehistory_db=pricehistory
    sentiment_db=sentiment_data
    server_ip=<server_ip>

[TDA]
    apikey=<apikey>
    consumer_id=<consumer_id>
    username=<username>
    password=<password>

[Reddit]
    apikey=<apikey> # client secret
    user_agent=<user_agent># app name
    username=<username>
    client_id=<client_id>
    redirect_uri=http://localhost:8080

[Twitter]
    apikey=<apikey>
    api_secret=<api_secret>
    access_token=<access_token>
    access_token_secret=<access_token_secret>

[Polygon]
    apikey=<apikey>

[PostgreSQL Windows]
    password=<password>
    port=5432
    host=localhost
    username=postgres
    market_db=marketdata
    pricehistory_db=pricehistory
    sentiment_db=sentiment_data

[Doppler]
    password=<password>
    devenv_token=<token>
    supportenv_token=<token>

[MongoDB]
    password=<password>
    cluster=<cluster>
    username=<username>
    ips=<ips>
    webdev_uri=<webdev_uri>

[GoogleCloudPlatform]
    password=<password>
    project=<project>
    project_number=<project_number>
    project_id=<project_id>
    kubernetes_cluster=<kubernetes_cluster>
    kubernetes_region=<kubernetes_region>
    mysql_id=<mysql_id>
    mysql_passwd=<mysql password>
    mysql_region=<mysql region>
    mysql_connection_name=<mysql connection name>
    mysql_public_ip=<mysql public ip>
    appengine_vm=<appengine vm name>
    vm_external_ip=<vm external ip address>
    vm_internal_ip=<vm internal ip>
    mysql_service_account=<your mysql service account>

[Alpaca]
    alpaca_email=<alpaca_email>
    alpaca_password=<alpaca_password>

[Params] # controls the pricehistory data that is retrieved
    period=10
    periodType=day
    frequency=1
    frequencyType=minute
```
> TODO: Finish building the database connection so I can workon the data accumulation and get the data collection up and running.

> The fundamental and quote data classes are complete and can be utilized as long as you have a TD Ameritrade developer account. 

    > This way I can simply import both `Fundamental` and `Quote` to the main script, along with `_select_symbols()` and be able to instantiate them on the home page. And by doing so, I will have created the `stock_chunk` list. It will also have the ability to insert data into the database.

> Building the `pricehistory.py` script: This script will be responsible for retrieving price history data for every single stock saved in the marketdata.db database. This is about 19,400+ companies. So I have to build a loop that takes the stocklist and retrieves one stock at a time and then calls the `pricehistory.data()` method. Once the data is retrieved, it will then need to be inserted into the `pricehistory` database. Based on the params used when instantiating the `Pricehistory` object a table name will be generated and every stock will be inserted into the `pricehistory` database in that same table name. to get the price history for a specific symbol you will have to use a query method selecting all rows containing that symbol. 
