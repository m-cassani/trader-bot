import time
from datetime import datetime, timedelta
import pandas as pd

from utils.data_collector import download_stock_data
from utils.file_manager import save_trade_log, save_summary


def realtime_backtest(tickers, strategy_function, initial_cash=5000, allocation_pct=0.1, duration_days=7, window_size=365):
    
    cash = initial_cash
    positions = {ticker: 0 for ticker in tickers}
    buy_signals = 0
    sell_signals = 0
    trade_log = []
    
    start_time = datetime.now()
    end_time = start_time + timedelta(days=duration_days)
    
    historical_data = {}
    for ticker in tickers:
        print(f"[{datetime.now()}] Downloading historical data for {ticker}...")
        historical_data[ticker] = download_stock_data(ticker, period=f'{window_size}d', interval='1d')

    
    while datetime.now() < end_time:
        for ticker in tickers:
            # Download most recent data for ticker
            print(f"[{datetime.now()}] Downloading most recent data for {ticker}")
            new_data = download_stock_data(ticker, period='1d', interval='1m')
            if new_data.empty:
                continue

            # Atualizar a janela deslizante
            historical_data[ticker] = pd.concat([historical_data[ticker], new_data]).drop_duplicates().iloc[-window_size:]
            
            # Aplicar a estratégia
            updated_data = strategy_function(historical_data[ticker])
            latest_signal = updated_data['Signal'].iloc[-1]
            latest_price = updated_data['Close'].iloc[-1]
            if hasattr(latest_price, 'item'):
                latest_price = latest_price.item()

            if latest_signal == 1 and cash > 0:
                amount_to_invest = cash * allocation_pct
                shares_to_buy = int(amount_to_invest // latest_price)
                if shares_to_buy > 0:
                    cash -= shares_to_buy * latest_price
                    positions[ticker] += shares_to_buy
                    buy_signals += 1
                    trade_log.append({'timestamp': datetime.now(), 'ticker': ticker, 'action': 'BUY', 'price': latest_price, 'shares': shares_to_buy})
                    print(f"[{datetime.now()}] BUY {shares_to_buy} shares of {ticker} at {latest_price:.2f}, cash left {cash:.2f}")

            elif latest_signal == -1 and positions[ticker] > 0:
                shares_to_sell = positions[ticker]
                cash += shares_to_sell * latest_price
                positions[ticker] = 0
                sell_signals += 1
                trade_log.append({'timestamp': datetime.now(), 'ticker': ticker, 'action': 'SELL', 'price': latest_price, 'shares': shares_to_sell})
                print(f"[{datetime.now()}] SELL {shares_to_sell} shares of {ticker} at {latest_price:.2f}, cash {cash:.2f}")
            
            time.sleep(5)  # Pequeno delay entre iterações para evitar bloqueio de API

        time.sleep(60)  # Delay entre ciclos completos de tickers

    # Calculando valor final da carteira
    final_value = cash
    for ticker in tickers:
        if positions[ticker] > 0:
            latest_price = historical_data[ticker]['Close'].iloc[-1]
            final_value += positions[ticker] * latest_price

    profit = final_value - initial_cash
    profit_pct = (profit / initial_cash) * 100

    print("\n--- REALTIME BACKTEST SUMMARY ---")
    print(f"Initial cash: R${initial_cash:.2f}")
    print(f"Final portfolio value: R${final_value:.2f}")
    print(f"Total profit: R${profit:.2f} ({profit_pct:.2f}%)")
    print(f"Remaining cash: R${cash:.2f}")
    print(f"Positions: {positions}")
    print(f"Buy signals: {buy_signals}")
    print(f"Sell signals: {sell_signals}")

    # Salvar arquivos
    save_trade_log(trade_log)
    summary = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'initial_cash': round(initial_cash, 2),
        'final_cash': round(cash, 2),
        'total_value': round(final_value, 2),
        'profit': round(profit, 2),
        'profit_pct': round(profit_pct, 2),
        'positions': {t: positions[t] for t in positions if positions[t] > 0},
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }
    save_summary("realtime_backtest", summary)