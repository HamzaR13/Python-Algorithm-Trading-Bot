import numpy as np
import pandas as pd
import yfinance as yf


class MeanReversionBot:
    def __init__(self, symbol, window, threshold): # initiallizing the bot with following parameters
        self.symbol = symbol
        self.window = window # Lookback window for calculating mean and standard deviation
        self.threshold = threshold # Threshold for triggering trades
        self.prices = [] # to store price data 
        self.positions = [] # 1 for long, -1 for short, 0 for neutral (to store trade positions)

    # this method will calculate the z-score based on the current price and historical price data
    # the z-score is the measure of how many standard deviations 
    # method checking if there is enough data available ('window' # of prices) and calculates the mean, the standard deviation, and z-score
    def calculate_zscore(self):
        if len(self.prices) < self.window:
            return 0 # Insufficient data for calculation
        else:
            window_prices = np.array(self.prices[-self.window:])
            mean = np.mean(window_prices)
            std = np.std(window_prices)
            current_price = self.prices[-1]
            zscore = (current_price - mean) / std
            return zscore

    # this method takes current price and z-score as input and is determining whether to execute a trade based on the given thresholds and current position
    # if z-score exceeds the positive threshold and the current positions is not already short (-1), it triggers a short sell
    # if z-score goes below negative threshold and current position not already long (1) it triggers buy
    def execute_trade(self, price, zscore):
        if zscore > self.threshold and self.positions[-1] != -1:
            self.positions.append(-1)  # Short sell signal
            print(f"SELL: {self.symbol} at {price}")
        elif zscore < -self.threshold and self.positions[-1] != 1:
            self.positions.append(1)  # Buy signal
            print(f"BUY: {self.symbol} at {price}")
        else:
            self.positions.append(0)  # No trade signal
            print("No trade")

    # this method is where mean reversion algorithm is executed
    # takes 'price_data' and input which is sequence of prices
    # iterates over 'price_data', adds each price to the 'prices' list
    # then lastly calculates z-score and finally executes a trade
    def run(self, price_data):
        for price in price_data:
            self.prices.append(price)
            zscore = self.calculate_zscore()
            self.execute_trade(price, zscore)


if __name__ == '__main__':
    symbol = 'AAPL'
    window = 20
    threshold = 1.0
    start_date = '2022-01-01'
    end_date = '2022-12-31'

    # Fetch historical price data from Yahoo Finance using yfinance
    # assumes that the file contains a column labeled 'Close' that represents the closing prices of the asset
    # The pd.read_csv() function from the Pandas library is used to read the data from the CSV file, and df['Close'].values retrieves the values of the 'Close' column as a NumPy array, which is assigned to the price_data variable.
    data = yf.download(symbol, start=start_date, end=end_date)
    price_data = data['Close'].values

    # create an instance of the MeanReversionBot class, passing in the symbol, window, and threshold values
    # trading_bot.run(price_data) line then executes the mean reversion algorithm by calling the run() method of the MeanReversionBot instance with the price_data as the argument
    # This will run the mean reversion trading bot on the provided historical price data, triggering trades based on the defined symbol, window, and threshold values
    trading_bot = MeanReversionBot(symbol, window, threshold)
    trading_bot.run(price_data)
    # replace 'price_data.csv' with the actual path or filename of your historical price data file, and adjust the symbol, window, and threshold values according to your trading preferences and strategy

