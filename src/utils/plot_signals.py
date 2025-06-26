import matplotlib.pyplot as plt
import os

def plot_signals(data, ticker, save_path=None):
    """
    Plot closing price with buy/sell signals.
    Save to file if save_path is given, else show plot.
    """
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.plot(data.index, data['SMA_Short'], label='SMA Short', color='orange')
    plt.plot(data.index, data['SMA_Long'], label='SMA Long', color='magenta')

    # Buy signals (Signal == 1)
    buys = data[data['Signal'] == 1]
    plt.scatter(buys.index, buys['Close'], marker='^', color='green', label='Buy Signal', s=100)

    # Sell signals (Signal == -1)
    sells = data[data['Signal'] == -1]
    plt.scatter(sells.index, sells['Close'], marker='v', color='red', label='Sell Signal', s=100)

    plt.title(f'{ticker} Price and Trading Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        plt.close()
        print(f"Saved plot to {save_path}")
    else:
        plt.show()
