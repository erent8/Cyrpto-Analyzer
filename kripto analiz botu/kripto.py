# import requests
# import time
# import csv
# from datetime import datetime
# import pandas as pd
# import matplotlib.pyplot as plt

# def fetch_price(coin_id):
#     url = f"YOUR_API_KEY"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data[coin_id]['usd']
#     else:
#         print(f"Failed to fetch data for {coin_id}. Status code: {response.status_code}")
#         return None

# def track_prices(coin_ids, interval_minutes=5, duration_minutes=30):
#     total_intervals = duration_minutes // interval_minutes
#     price_data = {coin: [] for coin in coin_ids.keys()}  # Dictionary to store price data for each coin

#     for _ in range(total_intervals):
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         for name, id in coin_ids.items():
#             price = fetch_price(id)
#             price_data[name].append((current_time, price))
#             print(f"Fetched {name} (${id}): {price} USD at {current_time}")
#             time.sleep(1)  # To avoid hitting API rate limits quickly
#         time.sleep(interval_minutes * 60 - len(coin_ids))  # Wait for the next interval, adjusting for the fetch time

#     return price_data

# def analyze_and_plot(price_data):
#     for coin, data in price_data.items():
#         times = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S") for record in data if record[1] is not None]
#         prices = [record[1] for record in data if record[1] is not None]
#         if not prices:
#             continue

#         plt.figure(figsize=(10, 5))
#         plt.plot(times, prices, marker='o', linestyle='-', color='gray')
#         plt.title(f"{coin} Price Change Over Time")
#         plt.xlabel("Time")
#         plt.ylabel("Price in USD")
#         plt.grid(True)

#         # Calculate and annotate percentage change
#         start_price = prices[0]
#         end_price = prices[-1]
#         percentage_change = ((end_price - start_price) / start_price) * 100
#         change_color = 'red' if percentage_change < 0 else 'green'
#         plt.annotate(f"{percentage_change:.2f}%", (times[-1], prices[-1]), color=change_color)

#         plt.show()

# if __name__ == "__main__":
#     coin_ids = {
#         'Bitcoin': 'bitcoin',
#         'Ethereum': 'ethereum',
#         'Tether': 'tether',
#         'BNB': 'binancecoin',
#         'Solana': 'solana',
#         'USDC': 'usd-coin',
#         'XRP': 'ripple'
#     }

#     price_data = track_prices(coin_ids)
#     analyze_and_plot(price_data)



import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def fetch_price(coin_id):
    url = f"YOUR_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[coin_id]['usd']
    else:
        print(f"Failed to fetch data for {coin_id}. Status code: {response.status_code}")
        return None

def send_email(subject, body, to_email):
    gmail_user = 'your-email@gmail.com'  # Gmail adresiniz
    gmail_password = 'your-app-password'  # Gmail uygulama şifreniz

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, to_email, msg.as_string())
    server.quit()

    print('E-posta gönderildi!')

def track_and_notify(coin_ids, to_email):
    previous_prices = {coin: fetch_price(coin) for coin in coin_ids.keys()}
    while True:
        time.sleep(300)  # 5 minutes
        for coin, id in coin_ids.items():
            current_price = fetch_price(id)
            if current_price is None:
                continue
            previous_price = previous_prices[coin]
            percentage_change = ((current_price - previous_price) / previous_price) * 100

            if abs(percentage_change) >= 2:
                direction = 'increased' if percentage_change > 0 else 'decreased'
                subject = f"{coin} Price Alert"
                body = f"The price of {coin} has {direction} by {abs(percentage_change):.2f}% to ${current_price}."
                send_email(subject, body, to_email)
                previous_prices[coin] = current_price  # Update the last known price

if __name__ == "__main__":
    coin_ids = {
        'Bitcoin': 'bitcoin',
        'Ethereum': 'ethereum',
        'BNB': 'binancecoin',
        'Solana': 'solana',
        'USDC': 'usd-coin',
        'XRP': 'ripple'
    }
    to_email = 'recipient-email@example.com'  # Alıcı e-posta adresi
    track_and_notify(coin_ids, to_email)
