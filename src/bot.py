import pandas as pd
import os
from utils.data_collector import download_stock_data
from strategies.moving_average_crossover import calculate_moving_averages
from utils.plot_signals import plot_signals
from backtest.historical_backtest import historical_backtest

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

        # Plot signals
        save_path = f'data/output/{ticker}_signals.png'
        plot_signals(stock_data, ticker, save_path=save_path)
        print(f"Signals for {ticker} saved successfully.\n")

        # Backtest with historical data
        one_month_ago = stock_data.index[-1] - pd.Timedelta(days=30)
        recent_data = stock_data.loc[stock_data.index >= one_month_ago]
        portfolio_values = historical_backtest(recent_data, initial_cash=1000, allocation_pct=0.1)
