import json
import smtplib
from email.mime.text import MIMEText

def extract_json():
    with open('./data/google_flights_data.json') as file:
        flights = json.load(file)
    return flights

def find_cheapest_flight(flights):
    clean_prices = clean_price_data(flights['price'])
    cheapest_flight = 0

    for price in clean_prices:
        if price < cheapest_flight:
            cheapest_flight = price

    return cheapest_flight

def clean_price_data(price):
    return float(price.replace('CA$', '').replace(',', ''))

def send_email(subject, body, to_email):
    
    smtp_server = 'smtp.email.com'
    smtp_port = 587
    smtp_user = 'smtp email'
    smtp_password = 'smtp password'
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())