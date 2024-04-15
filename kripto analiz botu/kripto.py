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

#Eren Terzi  
  