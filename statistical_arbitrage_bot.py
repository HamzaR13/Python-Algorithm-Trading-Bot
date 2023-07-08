import numpy as np
import pandas as pd
import yfinance as yf

class StatisticalArbitrageBot:
    def __init__(self, symbol_1, symbol_2, window, threshold):
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.window = window
        self.threshold = threshold
        self.prices_1 = []
        self.prices_2 = []
        self.positions = []

    def calculate_zscore(self):
        if len(self.prices_1) < self.window or len(self.prices_2) < self.window:
            return 0  # Insufficient data for calculation
        else:
            window_prices_1 = np.array(self.prices_1[-self.window:])
            window_prices_2 = np.array(self.prices_2[-self.window:])
            spread = window_prices_1 - window_prices_2
            mean_spread = np.mean(spread)
            std_spread = np.std(spread)
            current_spread = self.prices_1[-1] - self.prices_2[-1]
            zscore = (current_spread - mean_spread) / std_spread
            return zscore

    def execute_trade(self, price_1, price_2, zscore):
        if zscore > self.threshold and self.positions[-1] != -1:
            self.positions.append(-1)  # Short sell symbol_1 and buy symbol_2
            print(f"SELL {self.symbol_1}: {price_1}")
            print(f"BUY {self.symbol_2}: {price_2}")
        elif zscore < -self.threshold and self.positions[-1] != 1:
            self.positions.append(1)  # Buy symbol_1 and short sell symbol_2
            print(f"BUY {self.symbol_1}: {price_1}")
            print(f"SELL {self.symbol_2}: {price_2}")
        else:
            self.positions.append(0)  # No trade signal
            print("No trade")

    def run(self, price_data_1, price_data_2):
        for price_1, price_2 in zip(price_data_1, price_data_2):
            self.prices_1.append(price_1)
            self.prices_2.append(price_2)
            zscore = self.calculate_zscore()
            self.execute_trade(price_1, price_2, zscore)


if __name__ == '__main__':
    symbol_1 = 'AAPL'
    symbol_2 = 'MSFT'
    window = 20
    threshold = 1.0
    start_date = '2022-01-01'
    end_date = '2022-12-31'

    data_1 = yf.download(symbol_1, start=start_date, end=end_date)
    price_data_1 = data_1['Close'].values

    data_2 = yf.download(symbol_2, start=start_date, end=end_date)
    price_data_2 = data_2['Close'].values

    trading_bot = StatisticalArbitrageBot(symbol_1, symbol_2, window, threshold)
    trading_bot.run(price_data_1, price_data_2)
