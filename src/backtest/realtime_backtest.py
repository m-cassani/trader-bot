import time
import pandas as pd
from datetime import datetime, timedelta
from utils.data_collector import download_stock_data
from utils.plot_signals import plot_signals
from utils.file_manager import save_trade_log, save_summary

def realtime_backtest(tickers, strategy_function, initial_cash, duration_days=7, refresh_interval=60, window_size=365):
    print("\n--- Starting Realtime Backtest ---\n")

    portfolio = {ticker: {'shares': 0, 'cash': initial_cash / len(tickers), 'trade_log': []} for ticker in tickers}
    start_time = datetime.now()
    end_time = start_time + timedelta(days=duration_days)

    # Inicializa o histórico com o tamanho da janela
    historical_data = {}

    for ticker in tickers:
        print(f"Loading initial historical data for {ticker}...")
        data = download_stock_data(ticker, period=f'{window_size}d', interval='1d')
        if data.empty:
            print(f"No initial data for {ticker}. Skipping...")
            continue
        data['Ticker'] = ticker
        historical_data[ticker] = data

    while datetime.now() < end_time:
        print(f"\nRunning realtime check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for ticker in tickers:
            if ticker not in historical_data:
                continue

            print(f"\nChecking {ticker}...")

            # Coleta o dado mais recente
            recent_data = download_stock_data(ticker, period='7d', interval='1d')

            if recent_data.empty:
                print(f"No new data for {ticker}.")
                continue

            # Concatena com o histórico e mantém somente os últimos 'window_size' dias
            combined_data = pd.concat([historical_data[ticker], recent_data])
            combined_data = combined_data[~combined_data.index.duplicated(keep='last')]  # Remove duplicados
            combined_data = combined_data.sort_index()
            combined_data = combined_data.last(f'{window_size}D')  # Mantém somente a janela

            historical_data[ticker] = combined_data

            # Aplica a estratégia
            combined_data = strategy_function(combined_data)

            # Pega o sinal mais recente
            latest_row = combined_data.iloc[-1]
            signal = int(latest_row['Signal'])
            price = latest_row['Close']

            ticker_cash = portfolio[ticker]['cash']
            ticker_shares = portfolio[ticker]['shares']

            if signal == 1 and ticker_cash > 0:
                shares_to_buy = (0.1 * ticker_cash) / price
                portfolio[ticker]['shares'] += shares_to_buy
                portfolio[ticker]['cash'] -= shares_to_buy * price
                portfolio[ticker]['trade_log'].append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'action': 'BUY',
                    'price': price,
                    'shares': shares_to_buy
                })
                print(f"BUY {shares_to_buy:.4f} shares of {ticker} at {price:.2f}")

            elif signal == -1 and ticker_shares > 0:
                proceeds = ticker_shares * price
                portfolio[ticker]['cash'] += proceeds
                portfolio[ticker]['trade_log'].append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'action': 'SELL',
                    'price': price,
                    'shares': ticker_shares
                })
                portfolio[ticker]['shares'] = 0
                print(f"SELL all shares of {ticker} at {price:.2f}, proceeds: {proceeds:.2f}")

            else:
                print(f"No action for {ticker} at this moment.")

            # Salva log contínuo
            save_trade_log(ticker, portfolio[ticker]['trade_log'])

            # Gera gráfico atualizado
            save_path = f'data/output/{ticker}_signals_realtime.png'
            plot_signals(combined_data, ticker, save_path=save_path)

        print(f"\nWaiting {refresh_interval} seconds for the next check...\n")
        time.sleep(refresh_interval)

    # Resumo final
    summary = []
    for ticker in tickers:
        if ticker not in portfolio:
            continue

        cash = portfolio[ticker]['cash']
        shares = portfolio[ticker]['shares']

        if shares > 0:
            stock_data = historical_data[ticker]
            last_price = stock_data.iloc[-1]['Close']
            total_value = cash + (shares * last_price)
        else:
            total_value = cash

        profit = total_value - (initial_cash / len(tickers))

        summary.append({
            'ticker': ticker,
            'final_cash': cash,
            'remaining_shares': shares,
            'total_value': total_value,
            'profit': profit
        })

    save_summary(summary)
    print("\n--- Realtime Backtest Completed ---\n")
