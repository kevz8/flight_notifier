import json
import smtplib
from email.mime.text import MIMEText

def extract_json():
    with open('data/google_flights_data.json') as file:
        flights = json.load(file)
    return flights

def find_cheapest_flight(flights):
    def parse_price(price):
        return float(price.replace('CA$', '').replace(',', '').strip())
    
    cheapest_flight = min(flights, key=lambda flight: parse_price(flight['price']))
    return cheapest_flight

def clean_price_data(price):
    return float(price.replace('CA$', '').replace(',', ''))

def send_email(subject, body, to_email):
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'email'
    smtp_password = 'password'
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())