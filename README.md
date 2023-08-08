# Real-Time Stock Chart with Buy/Sell Indicators
This Python script creates an interactive web application using the Streamlit library to display a real-time stock chart with buy and sell indicators. The script fetches stock data from Yahoo Finance, calculates technical indicators such as RSI and MACD, and visualizes the data using Plotly.

## Features

- Real-time stock chart with candlestick visualization.
- Buy and sell indicators based on RSI and MACD.
- Interactive input for selecting a stock symbol.
- Continuously updates the chart with new data.
- Displays moving average for a 44-day period.
- Customized layout with title and no x-axis range slider.

## Requirements

Make sure you have the following libraries installed:

- `yfinance`
- `pandas`
- `plotly`
- `streamlit`
- `ta`

You can install these dependencies using the following command:

```bash
pip install yfinance pandas plotly streamlit ta
```

## Usage

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the repository's directory.
3. Run the script using the following command:

```bash
streamlit run real_time_stock_chart.py
```

4. The Streamlit web application will open in your default web browser.
5. Enter the stock symbol you want to visualize in the input field.
6. The application will display a real-time stock chart with buy/sell indicators based on RSI and MACD.
7. The chart will automatically update at the specified interval (60 seconds in the provided code).

## Notes

- The script uses the Yahoo Finance API to fetch stock data. Make sure the provided stock symbols are valid.
- The technical indicator conditions for buy and sell signals can be adjusted in the script.
- You can customize the appearance of the chart by modifying the Plotly chart configuration in the script.
---
