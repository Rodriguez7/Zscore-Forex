import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta

# Download historical data for EUR/USD forex pair
data = yf.download('EURUSD=X', period='1d', interval='15m')

# Calculate the mean and standard deviation of the closing prices
mean = data['Close'].rolling(window=20).mean()
std_dev = data['Close'].rolling(window=20).std()

# Calculate the Z-score
data['Z-Score'] = (data['Close'] - mean) / std_dev

# Calculate the Bollinger Bands
data['Upper Band'] = mean + (2 * std_dev)
data['Lower Band'] = mean - (2 * std_dev)

# Calculate the ATR
data['ATR'] = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'])

# Initialize columns for signals and positions
data['Buy_Signal'] = False
data['Sell_Signal'] = False
data['Buy_Position'] = np.nan
data['Sell_Position'] = np.nan

# Generate signals and positions
for i in range(1, len(data)):
    # Buy signal: Z-score crosses above 0 and price crosses below lower Bollinger Band
    if data['Z-Score'].iloc[i] > 0 and data['Close'].iloc[i] < data['Lower Band'].iloc[i]:
        data['Buy_Signal'].iloc[i] = True
        data['Buy_Position'].iloc[i] = data['Close'].iloc[i] + data['ATR'].iloc[i]
        
    # Sell signal: Price reaches buy position + 3*ATR
    elif data['Buy_Signal'].iloc[i-1] and data['Close'].iloc[i] >= data['Buy_Position'].iloc[i-1] + 3*data['ATR'].iloc[i]:
        data['Sell_Signal'].iloc[i] = True
        data['Sell_Position'].iloc[i] = data['Close'].iloc[i]

# Plot the closing prices, Bollinger Bands, and signals
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='Close')
plt.plot(data.index, data['Upper Band'], label='Upper Band', linestyle='--')
plt.plot(data.index, data['Lower Band'], label='Lower Band', linestyle='--')
plt.scatter(data[data['Buy_Signal']].index, data[data['Buy_Signal']]['Close'], color='green', marker='^', alpha=1)
plt.scatter(data[data['Sell_Signal']].index, data[data['Sell_Signal']]['Close'], color='red', marker='v', alpha=1)

plt.title('EUR/USD Close Prices, Bollinger Bands, and Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
