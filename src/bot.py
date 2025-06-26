import pandas as pd
import os
from utils.data_collector import download_stock_data
from strategies.moving_average_crossover import calculate_moving_averages

def load_tickers(file_path='data/input/tickers.txt'):
    with open(file_path, 'r') as file:
        tickers = [line.strip() for line in file if line.strip()]
    return tickers

def save_data(data, ticker):
    if not os.path.exists('data/output'):
        os.makedirs('data/output')
    data.to_csv(f'data/output/{ticker}.csv')

if __name__ == "__main__":
    tickers = load_tickers()

    for ticker in tickers:
        print(f"Processing {ticker}...")

        # Download fresh data
        stock_data = download_stock_data(ticker)

        # Save raw data
        save_data(stock_data, ticker)

        # Generate signals
        stock_data = calculate_moving_averages(stock_data)

        # Save signals
        stock_data.to_csv(f'data/output/{ticker}_signals.csv')

        print(f"Signals for {ticker} saved successfully.\n")
