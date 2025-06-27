from utils.file_manager import save_trade_log, save_summary

def historical_backtest(data_list, initial_cash=5000, allocation_pct=0.1):
    cash = initial_cash
    positions = {}
    portfolio_values = []
    trade_log = []

    buy_signals = 0
    sell_signals = 0

    for data in data_list:
        ticker = data['Ticker'].iloc[0] if 'Ticker' in data.columns else 'Unknown'
        positions.setdefault(ticker, 0)

        for idx, row in data.iterrows():
            price = row['Close']
            if hasattr(price, 'item'):
                price = price.item()

            signal = row['Signal']
            if hasattr(signal, 'item'):
                signal = signal.item()

            if signal == 1 and cash > 0:
                amount_to_invest = cash * allocation_pct
                shares_to_buy = int(amount_to_invest / price)
                cash -= amount_to_invest
                positions[ticker] += shares_to_buy
                buy_signals += 1

                print(f"{idx.date()} BUY {shares_to_buy:.4f} shares of {ticker} at {price:.2f}, cash left {cash:.2f}")

                trade_log.append({
                    'timestamp': idx.strftime('%Y-%m-%d %H:%M:%S'),
                    'ticker': ticker,
                    'action': 'BUY',
                    'price': price,
                    'shares': shares_to_buy
                })

            elif signal == -1 and positions[ticker] > 0:
                proceeds = positions[ticker] * price
                cash += proceeds
                print(f"{idx.date()} SELL {positions[ticker]:.4f} shares of {ticker} at {price:.2f}, cash {cash:.2f}")
                sell_signals += 1

                trade_log.append({
                    'timestamp': idx.strftime('%Y-%m-%d %H:%M:%S'),
                    'ticker': ticker,
                    'action': 'SELL',
                    'price': price,
                    'shares': positions[ticker]
                })

                positions[ticker] = 0

            total_value = cash + sum(positions[t] * price for t in positions)
            portfolio_values.append(total_value)

    final_value = portfolio_values[-1] if portfolio_values else initial_cash
    profit = final_value - initial_cash
    profit_pct = (profit / initial_cash) * 100

    print("\n--- BACKTEST SUMMARY ---")
    print(f"Initial cash: R${initial_cash:.2f}")
    print(f"Final portfolio value: R${final_value:.2f}")
    print(f"Total profit: R${profit:.2f} ({profit_pct:.2f}%)")
    print(f"Remaining cash: R${cash:.2f}")
    print(f"Positions: {positions}")
    print(f"Buy signals: {buy_signals}")
    print(f"Sell signals: {sell_signals}")

    save_trade_log("historical_backtest", trade_log)

    summary = {
        'timestamp': idx.strftime('%Y-%m-%d'),
        'initial_cash': round(initial_cash, 2),
        'final_cash': round(cash, 2),
        'total_value': round(final_value, 2),
        'profit': round(profit, 2),
        'profit_pct': round(profit_pct, 2),
        'positions': {t: positions[t] for t in positions if positions[t] > 0},
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

    save_summary("historical_backtest", [summary])

    return portfolio_values