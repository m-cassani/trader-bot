import os
import pandas as pd

def load_tickers(file_path='data/input/tickers.txt'):
    """Load tickers from the input file."""
    if not os.path.exists(file_path):
        print(f"Tickers file not found at {file_path}")
        return []

    with open(file_path, 'r') as file:
        tickers = [line.strip() for line in file if line.strip()]
    return tickers

def save_data(data, ticker):
    """Save raw stock data to a CSV file."""
    output_dir = 'data/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f'{ticker}.csv')
    data.to_csv(file_path)
    print(f"Saved raw data for {ticker} to {file_path}")

def save_trade_log(ticker, trade_log):
    """Save trade log (buy/sell operations) to a CSV file."""
    output_dir = 'data/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f'{ticker}_trades.csv')
    trade_log_df = pd.DataFrame(trade_log)
    trade_log_df.to_csv(file_path, index=False)
    print(f"Saved trade log for {ticker} to {file_path}")

def save_summary(summary_data):
    """Save summary of portfolio results to a CSV file."""
    output_dir = 'data/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, 'summary.csv')
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(file_path, index=False)
    print(f"Saved portfolio summary to {file_path}")
