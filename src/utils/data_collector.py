import yfinance as yf
import os

def load_tickers(file_path):
    """
    Load ticker symbols from a text file.
    """
    with open(file_path, 'r') as file:
        tickers = [line.strip() for line in file if line.strip()]
    return tickers

def download_stock_data(ticker, period='1y', interval='1d'):
    """
    Download historical stock data from Yahoo Finance.
    """
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)

    # Add ticker column to the dataset
    data['Ticker'] = ticker

    return data

def save_data(data, ticker):
    """
    Save stock data to a CSV file inside data/output.
    """
    if not os.path.exists('data/output'):
        os.makedirs('data/output')

    file_path = f'data/output/{ticker}.csv'
    data.to_csv(file_path)
    print(f"Data for {ticker} saved successfully to {file_path}.")

if __name__ == "__main__":
    tickers = load_tickers('data/input/tickers.txt')

    for ticker in tickers:
        print(f"Downloading {ticker}...")
        stock_data = download_stock_data(ticker)
        save_data(stock_data, ticker)
        print(f"Data for {ticker} saved successfully.\n")
