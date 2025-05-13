import sqlite3
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DB_PATH = 'data/flight_data.db'

def get_price_trend(origin, destination, departDate):
    con = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query('''
        SELECT price, scraped_at FROM flights
        WHERE origin = ? AND destination = ? AND departure_date = ?
    ''', con, params=(origin, destination, departDate))

    # print(df.head())

    df['scraped_at'] = pd.to_datetime(df['scraped_at'])

    df['date'] = df['scraped_at'].dt.date
    daily_price_avg = df.groupby('date')['price'].mean()

    # Plot
    print(daily_price_avg)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(daily_price_avg.index, daily_price_avg.values, marker='o', label='Average Price')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # ax.set_xlim(daily_price_avg.index.min())
    fig.autofmt_xdate()
    ax.set_title(f'Price Trend for {origin} → {destination} on {departDate}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (CAD)')
    ax.grid(True)
    ax.legend()
    # plt.show()

    return fig


# if __name__ == '__main__':
#     analyze_price_trend('YVR', 'NRT', '2025-12-23')