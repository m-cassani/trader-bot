def historical_backtest(data, initial_cash=1000, allocation_pct=0.1):
    cash = initial_cash
    position = 0
    portfolio_values = []

    for idx, row in data.iterrows():
        price = row['Close']
        if hasattr(price, 'item'):
            price = price.item()

        signal = row['Signal']
        if hasattr(signal, 'item'):
            signal = signal.item()

        if signal == 1 and cash > 0:
            amount_to_invest = cash * allocation_pct
            shares_to_buy = amount_to_invest / price
            cash -= amount_to_invest
            position += shares_to_buy
            print(f"{idx.date()} BUY {shares_to_buy:.4f} shares at {price:.2f}, cash left {cash:.2f}")

        elif signal == -1 and position > 0:
            cash += position * price
            print(f"{idx.date()} SELL {position:.4f} shares at {price:.2f}, cash {cash:.2f}")
            position = 0

        total_value = cash + position * price
        portfolio_values.append(total_value)

    final_value = portfolio_values[-1] if portfolio_values else initial_cash
    profit = final_value - initial_cash
    profit_pct = (profit / initial_cash) * 100

    print("\n--- BACKTEST SUMMARY ---")
    print(f"Initial cash: R${initial_cash:.2f}")
    print(f"Final portfolio value: R${final_value:.2f}")
    print(f"Total profit: R${profit:.2f} ({profit_pct:.2f}%)")
    print(f"Remaining cash: R${cash:.2f}")
    print(f"Remaining position: {position:.4f} shares")

    if position > 0:
        print(f"Unrealized position value: R${position * price:.2f} (at final price R${price:.2f})")
    else:
        print("No open positions remaining.")

    return portfolio_values
