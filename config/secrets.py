import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

# TDAmeritrade Secrets
TDA_APIKEY = config['TDA']['apikey']
TDA_CONSUMERID = config['TDA']['consumer_id']
TDA_USERNAME = config['TDA']['username']
TDA_PASSWORD = config['TDA']['password']

# MySQL Windows Database
MYSQL_USER = config['MySQL Windows']['user']
MYSQL_PASSWORD = config['MySQL Windows']['password']
MYSQL_HOST = config['MySQL Windows']['host']
MYSQL_PORT = config['MySQL Windows']['port']
MYSQL_CONNECTION_STRING = config['MySQL Windows']['cxn_uri']
MYSQL_MARKET_DB = config['MySQL Windows']['market_db']
MYSQL_PRICEHISTORY_DB = config['MySQL Windows']['pricehistory_db']

# Reddit secrets
REDDIT_APIKEY = config['Reddit']['apikey']
REDDIT_USER_AGENT = config['Reddit']['user_agent']
REDDIT_USERNAME = config['Reddit']['username']
REDDIT_CLIENT_ID = config['Reddit']['client_id']
REDDIT_REDIRECT_URI = config['Reddit']['redirect_uri']

# Twitter secrets
TWITTER_APIKEY = config['Twitter']['apikey']
TWITTER_API_SECRET = config['Twitter']['api_secret']
TWITTER_ACCESS_TOKEN = config['Twitter']['access_token']
TWITTER_ACCESS_TOKEN_SECRET = config['Twitter']['access_token_secret']

# Price History Parameters
PERIOD = config['Params']['period']
PERIODTYPE = config['Params']['periodType']
FREQUENCY = config['Params']['frequency']
FREQUENCYTYPE = config['Params']['frequencyType']
