import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import time
from ta.momentum import rsi
from ta.trend import macd, macd_signal

# Create the Streamlit application
st.title("Real-Time Stock Chart with Buy/Sell Indicators")

# Set the interval for data updates (in seconds)
update_interval = 60

# Create an empty DataFrame to store the data
data = pd.DataFrame()

# Continuously fetch and update the data
while True:
    # Get the stock symbol from the user
    stock = st.text_input("Enter stock symbol", "UBER", key='stock_input')

    # Retrieve the market data for the specified stock
    stock_data = yf.download(stock, period="1mo", interval="1d")

    # Calculate the RSI and MACD
    stock_data['RSI'] = rsi(stock_data['Close'], window=14)
    stock_data['MACD'] = macd(stock_data['Close'], window_slow=26, window_fast=12)
    stock_data['MACD_Signal'] = macd_signal(stock_data['Close'], window_slow=26, window_fast=12, window_sign=9)

    # Append the new data to the existing DataFrame
    data = pd.concat([data, stock_data])

    # Calculate the 44-day moving average
    data['MA'] = data['Close'].rolling(window=44).mean()

    # Add a new column for buy/sell indicators
    data['Indicator'] = 'Hold'

    # Determine buy and sell signals based on conditions
    # (data['Close'] > data['MA']) & add to get moving average 44

    data.loc[(data['RSI'] < 30) & (data['MACD'] > data['MACD_Signal']), 'Indicator'] = 'Buy'

    # (data['Close'] < data['MA']) & add this line to get moving average 44

    data.loc[(data['RSI'] > 70) & (data['MACD'] < data['MACD_Signal']), 'Indicator'] = 'Sell'

    # Create a candlestick chart with the indicators using Plotly
    fig = go.Figure(data=[
        go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Candlestick'),
        go.Scatter(x=data.index, y=data['MA'], mode='lines', name='Moving Average'),
        go.Scatter(x=data[data['Indicator'] == 'Buy'].index, y=data[data['Indicator'] == 'Buy']['Close'], mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=10)),
        go.Scatter(x=data[data['Indicator'] == 'Sell'].index, y=data[data['Indicator'] == 'Sell']['Close'], mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=10))
    ])

    # Customize the chart layout
    fig.update_layout(
        title=f"{stock} Stock Price with Buy/Sell Indicators",
        xaxis_rangeslider_visible=False
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    # Wait for the specified interval before refreshing the page
    time.sleep(update_interval)
    st.experimental_rerun()
