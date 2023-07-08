import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

end_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date
start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
# ^ Get the date 60 days ago

dataF = yf.download("CADUSD=X", start=start_date, end=end_date, interval='1d')
dataF.to_csv('data.csv')


# Fetch historical price data from Yahoo Finance
def fetch_price_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data
