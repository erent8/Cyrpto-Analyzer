import requests
import time
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

# Configuration
config = ConfigParser()
config.read('config.ini')
API_KEY = config['API']['Key']
GMAIL_USER = config['GMAIL']['User']
GMAIL_PASSWORD = config['GMAIL']['Password']

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SLEEP_INTERVAL = 300  # 5 minutes
PRICE_CHANGE_THRESHOLD = 2.0  # Percent

def fetch_price(coin_id):
    """Fetches the latest price for a given coin."""
    url = f"https://api.example.com/data/price?fsym={coin_id}&tsyms=USD&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['USD']
    else:
        logging.error(f"Failed to fetch data for {coin_id}. Status code: {response.status_code}")
        return None

def send_email(subject, body, to_email):
    """Sends an email with the given subject and body."""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
        server.quit()
        logging.info('Email sent successfully!')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

def track_and_notify(coin_ids, to_email):
    """Tracks coin prices and sends notification emails when significant changes occur."""
    previous_prices = {coin: fetch_price(coin) for coin in coin_ids.keys()}
    while True:
        time.sleep(SLEEP_INTERVAL)
        for coin, id in coin_ids.items():
            current_price = fetch_price(id)
            if current_price is None:
                continue
            previous_price = previous_prices[coin]
            percentage_change = ((current_price - previous_price) / previous_price) * 100

            if abs(percentage_change) >= PRICE_CHANGE_THRESHOLD:
                direction = 'increased' if percentage_change > 0 else 'decreased'
                subject = f"{coin} Price Alert"
                body = f"The price of {coin} has {direction} by {abs(percentage_change):.2f}% to ${current_price}."
                send_email(subject, body, to_email)
                previous_prices[coin] = current_price

if __name__ == "__main__":
    coin_ids = {
        'Bitcoin': 'BTC',
        'Ethereum': 'ETH',
        'BNB': 'BNB',
        'Solana': 'SOL',
        'USDC': 'USDC',
        'XRP': 'XRP'
    }
    to_email = config['RECIPIENT']['Email']
    track_and_notify(coin_ids, to_email)
