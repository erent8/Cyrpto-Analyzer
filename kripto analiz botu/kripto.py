import requests
import time
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def fetch_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[coin_id]['usd']
    else:
        print(f"Failed to fetch data for {coin_id}. Status code: {response.status_code}")
        return None

def track_prices(coin_ids, interval_minutes=5, duration_minutes=30):
    total_intervals = duration_minutes // interval_minutes
    price_data = {coin: [] for coin in coin_ids.keys()}  # Dictionary to store price data for each coin

    for _ in range(total_intervals):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for name, id in coin_ids.items():
            price = fetch_price(id)
            price_data[name].append((current_time, price))
            print(f"Fetched {name} (${id}): {price} USD at {current_time}")
            time.sleep(1)  # To avoid hitting API rate limits quickly
        time.sleep(interval_minutes * 60 - len(coin_ids))  # Wait for the next interval, adjusting for the fetch time

    return price_data

def analyze_and_plot(price_data):
    for coin, data in price_data.items():
        times = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S") for record in data if record[1] is not None]
        prices = [record[1] for record in data if record[1] is not None]
        if not prices:
            continue

        plt.figure(figsize=(10, 5))
        plt.plot(times, prices, marker='o', linestyle='-', color='gray')
        plt.title(f"{coin} Price Change Over Time")
        plt.xlabel("Time")
        plt.ylabel("Price in USD")
        plt.grid(True)

        # Calculate and annotate percentage change
        start_price = prices[0]
        end_price = prices[-1]
        percentage_change = ((end_price - start_price) / start_price) * 100
        change_color = 'red' if percentage_change < 0 else 'green'
        plt.annotate(f"{percentage_change:.2f}%", (times[-1], prices[-1]), color=change_color)

        plt.show()

if __name__ == "__main__":
    coin_ids = {
        'Bitcoin': 'bitcoin',
        'Ethereum': 'ethereum',
        'Tether': 'tether',
        'BNB': 'binancecoin',
        'Solana': 'solana',
        'USDC': 'usd-coin',
        'XRP': 'ripple'
    }

    price_data = track_prices(coin_ids)
    analyze_and_plot(price_data)
