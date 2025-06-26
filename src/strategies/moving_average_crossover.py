def calculate_moving_averages(data, short_window=9, long_window=21):
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    
    data['Signal'] = 0
    # Calcula a diferença entre as médias
    data['Diff'] = data['SMA_Short'] - data['SMA_Long']
    # Detecta cruzamento: compra quando a diferença cruza de negativa para positiva
    data.loc[(data['Diff'] > 0) & (data['Diff'].shift(1) <= 0), 'Signal'] = 1
    # Venda quando cruza de positiva para negativa
    data.loc[(data['Diff'] < 0) & (data['Diff'].shift(1) >= 0), 'Signal'] = -1
    
    data.drop(columns=['Diff'], inplace=True)
    return data
