#!/usr/bin/env python3
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go

def simulate_realtime_data(csv_path):
    # Load the CSV file
    df = pd.read_csv(csv_path, parse_dates=True, index_col='Datetime')

    # Extract necessary columns
    df['Timestamp'] = df.index.astype(int) // 10**9  # Convert Datetime to Unix timestamp
    data = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]

    # Set up the initial candlestick chart
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=('Candlestick Chart', 'Volume'))

    # Add initial candlestick trace
    candlestick_trace = go.Candlestick(x=data.index,
                                       open=data['Open'],
                                       high=data['High'],
                                       low=data['Low'],
                                       close=data['Close'],
                                       name='Candlestick')
    fig.add_trace(candlestick_trace, row=1, col=1)

    # Add initial volume trace
    volume_trace = go.Bar(x=data.index, y=data['Volume'], name='Volume')
    fig.add_trace(volume_trace, row=2, col=1)

    # Update layout
    fig.update_layout(
            title='Updated Candlestick Plot',
            xaxis=dict(
                rangeslider=dict(visible=False),  # Disable rangeslider
                type='date',  # Use 'date' type for the x-axis
            ),
            yaxis=dict(constrain='domain'),  # Automatically adjust y-axis based on the visible range
            xaxis2=dict(rangeslider=dict(visible=False), type='date', anchor='y2'),  # Link x-axis2 to y2-axis
            yaxis2=dict(anchor='x2', range=[0, data['Volume'].max() * 1.2]),  # Set the initial y-axis range for volume
        )

    # Display the initial figure
    fig.show()

    latest_data = pd.read_csv(csv_path, parse_dates=True, index_col='Datetime').iloc[-1:]

    # Extract necessary columns for the latest data
    latest_data['Timestamp'] = latest_data.index.astype(int) // 10**9
    latest_data = latest_data[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]

    # Update candlestick trace with the latest data
    candlestick_trace.x = latest_data.index
    candlestick_trace.open = latest_data['Open']
    candlestick_trace.high = latest_data['High']
    candlestick_trace.low = latest_data['Low']
    candlestick_trace.close = latest_data['Close']

    # Update volume trace with the latest data
    volume_trace.x = latest_data.index
    volume_trace.y = latest_data['Volume']

if __name__ == "__main__":
    symbol = "AAPL"
    csv_path = f'{symbol}_historical_data.csv'
    simulate_realtime_data(csv_path)
