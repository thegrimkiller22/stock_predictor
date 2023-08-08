import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from ta.momentum import RSIIndicator
from ta.trend import MACD


def fetch_stock_data(stock_symbol, interval):
    stock_data = yf.download(stock_symbol, period="1mo", interval=interval)
    return stock_data


def calculate_technical_indicators(data):
    data['RSI'] = RSIIndicator(data['Close']).rsi()
    macd_indicator = MACD(data['Close'])
    data['MACD'] = macd_indicator.macd()
    data['MACD_Signal'] = macd_indicator.macd_signal()
    data['MA'] = data['Close'].rolling(window=44).mean()
    return data


def generate_chart(data, stock_symbol):
    fig = go.Figure(data=[
        go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                       name='Candlestick'),
        go.Scatter(x=data.index, y=data['MA'], mode='lines', name='Moving Average'),
        go.Scatter(x=data[data['Indicator'] == 'Buy'].index, y=data[data['Indicator'] == 'Buy']['Close'],
                   mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=10)),
        go.Scatter(x=data[data['Indicator'] == 'Sell'].index, y=data[data['Indicator'] == 'Sell']['Close'],
                   mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=10))
    ])
    fig.update_layout(title=f"{stock_symbol} Stock Price with Buy/Sell Indicators", xaxis_rangeslider_visible=False)
    return fig


def main():
    st.title("Real-Time Stock Chart with Buy/Sell Indicators")

    stock_symbol = st.text_input("Enter stock symbol", "UBER")
    update_interval = st.slider("Update Interval (seconds)", 10, 300, 60)

    stock_data = fetch_stock_data(stock_symbol, "1d")
    stock_data = calculate_technical_indicators(stock_data)

    stock_data['Indicator'] = 'Hold'
    stock_data.loc[(stock_data['RSI'] < 30) & (stock_data['MACD'] > stock_data['MACD_Signal']), 'Indicator'] = 'Buy'
    stock_data.loc[(stock_data['RSI'] > 70) & (stock_data['MACD'] < stock_data['MACD_Signal']), 'Indicator'] = 'Sell'

    chart = generate_chart(stock_data, stock_symbol)
    st.plotly_chart(chart)


if __name__ == "__main__":
    main()
