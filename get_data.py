#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_save_intraday_data(symbol, start_date, end_date, interval='1m', save_path='intraday_data.csv'):
    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize an empty DataFrame to store the intraday data
    intraday_data = pd.DataFrame()

    # Define the chunk size (7 days in this example)
    chunk_size = 7

    # Fetch data in chunks
    while start_date <= end_date:
        # Calculate the end date for the current chunk
        chunk_end_date = min(start_date + timedelta(days=chunk_size - 1), end_date)

        # Download historical data for the current chunk
        data = yf.download(symbol, start=start_date, end=chunk_end_date, interval=interval)

        # Concatenate the data to the main DataFrame
        intraday_data = pd.concat([intraday_data, data])

        # Update the start_date for the next chunk
        start_date = chunk_end_date + timedelta(days=1)

    # Save the combined data to a CSV file
    intraday_data.to_csv(save_path)

    print(f"Intraday data for {symbol} from {start_date} to {end_date} saved to {save_path}")

if __name__ == "__main__":
    # Replace these values with your desired symbol and date range
    symbol = 'AAPL'
    start_date = '2024-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')  # Current date

    # Specify the interval (1m for 1 minute, 5m for 5 minutes, etc.)
    interval = '1m'

    # Specify the file path where you want to save the data
    save_path = 'intraday_data.csv'

    # Get and save intraday data
    get_save_intraday_data(symbol, start_date, end_date, interval, save_path)
