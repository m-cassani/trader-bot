import pandas as pd
import os
import argparse

from utils.data_collector import download_stock_data
from utils.plot_signals import plot_signals
from utils.file_manager import load_tickers, save_data

from strategies import moving_average_crossover

# ================= ARGUMENT PARSER =================

parser = argparse.ArgumentParser(description="Trading Bot Configuration")

parser.add_argument('--mode', choices=['test-historical', 'test-realtime'], required=True, help="Select execution mode.")
parser.add_argument('--strategy', choices=['moving_average_crossover'], required=True, help="Select trading strategy.")
parser.add_argument('--window_size', type=int, default=365, help="Rolling window size in days for realtime backtest.")
parser.add_argument('--initial_cash', type=float, default=5000.0, help="Initial portfolio cash.")
parser.add_argument('--duration', type=int, default=7, help="Execution duration in days (for realtime mode).")

args = parser.parse_args()

# ================= STRATEGY MAPPING =================

strategies = {
    'moving_average_crossover': moving_average_crossover.calculate_moving_averages
}

strategy_function = strategies[args.strategy]

# ================= MAIN FUNCTION =================

def run_historical_backtest():
    from backtest.historical_backtest import historical_backtest

    tickers = load_tickers()
    all_data = []

    for ticker in tickers:
        print(f"\nProcessing {ticker}...")

        # Download fresh data
        stock_data = download_stock_data(ticker)
        save_data(stock_data, ticker)

        # Apply strategy to generate signals
        stock_data = strategy_function(stock_data)

        # Save signals CSV
        stock_data.to_csv(f'data/output/{ticker}_signals.csv')

        # Plot signals
        save_path = f'data/output/{ticker}_signals.png'
        plot_signals(stock_data, ticker, save_path=save_path)
        print(f"Signals for {ticker} saved successfully.\n")

        # Filter recent data (last 30 days)
        one_month_ago = stock_data.index[-1] - pd.Timedelta(days=30)
        recent_data = stock_data.loc[stock_data.index >= one_month_ago]

        # Add a 'Ticker' column to identify each dataframe inside the combined list
        recent_data = recent_data.copy()
        recent_data['Ticker'] = ticker

        all_data.append(recent_data)

    # Run historical backtest passing the list of dataframes (portfolio)
    portfolio_values = historical_backtest(all_data, initial_cash=args.initial_cash, allocation_pct=0.1)


def run_realtime_backtest():
    from backtest.realtime_backtest import realtime_backtest

    tickers = load_tickers()

    # Start realtime backtest for all tickers
    realtime_backtest(tickers, strategy_function, args.initial_cash, args.duration, args.window_size)


# ================= ENTRY POINT =================

if __name__ == "__main__":
    if args.mode == 'test-historical':
        run_historical_backtest()

    elif args.mode == 'test-realtime':
        run_realtime_backtest()

    else:
        print("Invalid mode selected. Please choose 'test-historical' or 'test-realtime'.")
