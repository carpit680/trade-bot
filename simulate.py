#!/usr/bin/env python3
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

def simulate_realtime_data(csv_path, interval=60):
    # Load the CSV file
    df = pd.read_csv(csv_path, parse_dates=True, index_col='Datetime')

    # Extract necessary columns
    df['Timestamp'] = df.index.astype(int) // 10**9  # Convert Datetime to Unix timestamp
    data = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]

    # Set up the initial candlestick chart
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=('Candlestick Chart', 'Volume'))

    # Add initial candlestick trace
    candlestick_trace = go.Candlestick(x=data['Timestamp'],
                                       open=data['Open'],
                                       high=data['High'],
                                       low=data['Low'],
                                       close=data['Close'],
                                       name='Candlestick')
    fig.add_trace(candlestick_trace, row=1, col=1)

    # Add initial volume trace
    volume_trace = go.Bar(x=data['Timestamp'], y=data['Volume'], name='Volume')
    fig.add_trace(volume_trace, row=2, col=1)

    # Update layout
    fig.update_layout(title='Real-time Candlestick Simulation',
                      xaxis_title='Datetime',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)

    # Display the initial figure
    fig.show()

    # Simulate real-time updates
    while True:
        # Get the latest data from the CSV file
        latest_data = pd.read_csv(csv_path, parse_dates=True, index_col='Datetime').iloc[-1:]

        # Extract necessary columns for the latest data
        latest_data['Timestamp'] = latest_data.index.astype(int) // 10**9
        latest_data = latest_data[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Update candlestick trace with the latest data
        candlestick_trace.x = [latest_data['Timestamp']]
        candlestick_trace.open = [latest_data['Open']]
        candlestick_trace.high = [latest_data['High']]
        candlestick_trace.low = [latest_data['Low']]
        candlestick_trace.close = [latest_data['Close']]

        # Update volume trace with the latest data
        volume_trace.x = [latest_data['Timestamp']]
        volume_trace.y = [latest_data['Volume']]

        # Update the figure
        fig.update()

        # Pause to simulate real-time updates
        time.sleep(interval)

if __name__ == "__main__":
    # Specify the path to the saved CSV file
    csv_path = 'intraday_data.csv'

    # Specify the update interval in seconds (e.g., 60 seconds for 1-minute updates)
    update_interval = 60

    # Simulate real-time data and plot candlestick charts with volume
    simulate_realtime_data(csv_path, update_interval)
