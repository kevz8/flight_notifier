from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import datetime
import logging

DB_PATH = 'data/flight_data.db'

def get_url(origin, destination, outbound, inbound = None):
    if not inbound:
        return f'https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{origin}%20on{outbound}%20oneway%202%20seats%20on%20cheapest&curr=CAD'
    else:
        return f'https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{origin}%20on%{outbound}%20%20through%20{inbound}%202%20seats%20on%20cheapest&curr=CAD'

def scrape_listings(soup):
    return soup.find_all('li', class_='pIav2d')

def scrape_company_name(listing):
    airline = listing.find('div', class_='Ir0Voe').find('div', class_='sSHqwe tPgKwe ogfYpf').find('span')
    return airline.text.strip()

def scrape_flight_duration(listing):
    duration_element = listing.find('div', class_='Ak5kof').find('div', class_='gvkrdb AdWm1c tPgKwe ogfYpf')
    return duration_element.text.strip()

def scrape_price(listing):
    price_element = listing.find('div', class_='U3gSDe').find('div', class_='FpEdX').find('span')
    return price_element.text.strip()

def scrape_departure_arrival_dates(listing):
    departure_date_element = listing.select_one('span.mv1WYe span:first-child [jscontroller="cNtv4b"] span')
    departure_date = departure_date_element.text.strip().replace('\u202f', ' ') if departure_date_element else None
    arrival_date_element = listing.select_one('span.mv1WYe span:last-child [jscontroller="cNtv4b"] span')
    arrival_date = arrival_date_element.text.strip().replace('\u202f', ' ')
    return departure_date, arrival_date

def scrape_flight_stops(listing):
    stops_element = listing.find('div', class_='EfT7Ae AdWm1c tPgKwe').find('span', class_='ogfYpf').text.strip()
    if "Nonstop" in stops_element:
        return 0
    
    return int(stops_element.split()[0])

def init_db():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        origin TEXT,
        destination TEXT,
        departure_date TEXT,
        company_name TEXT,
        departure_time TEXT,
        arrival_time TEXT,
        stops INTEGER,
        price INTEGER,
        scraped_at TEXT,
        PRIMARY KEY (origin, destination, departure_date, company_name, departure_time, arrival_time, stops, scraped_at))
    ''')

def drop_table():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute('''
        DROP TABLE flights
    ''')

def main(origin, destination, departDate):
    # Make a request to Google Flights URL and parse HTML
    url = get_url(origin, destination, departDate)
    
    try:
        result = requests.get(url)
    except requests.RequestException as e:
        logging.error(f"Failed to scrape url: {e}")
        return -1
    
    try:
        content = result.text
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup.prettify())

        # Scrape flight listings
        listings = scrape_listings(soup)

        # Iterate through each listing and extract flight information
        flight_data = []
        for listing in listings:
            company_name = scrape_company_name(listing)
            flight_duration = scrape_flight_duration(listing)
            price = scrape_price(listing)
            departure_date, arrival_date = scrape_departure_arrival_dates(listing)
            stops = scrape_flight_stops(listing)

            # Store flight information in a dictionary
            flight_info = {
                'company_name': company_name,
                'flight_duration': flight_duration,
                'price': price,
                'departure_time': departure_date,
                'arrival_time': arrival_date,
                'stops': stops
            }

            flight_data.append(flight_info)
    except (AttributeError, IndexError) as e:
        logging.error(f"Parsing error: {e}")
        return -1

    try:
        # initiate and store values in database
        init_db()
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        scraped_at = datetime.datetime.utcnow().isoformat()

        for f in flight_data:
            price_int = int(f['price'].replace('CA$', '').replace(',', '').strip())
            cursor.execute('''
                INSERT OR IGNORE INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (origin, destination, departDate, f['company_name'], f['departure_time'], f['arrival_time'], f['stops'], price_int, scraped_at))
        
        con.commit()
        con.close()
    except sqlite3.DatabaseError as e:
        logging.error(f"Database insertion failed: {e}")
        return -1
    
    try:
        # Save results to a JSON file
        json.dump(flight_data, open('./data/google_flights_data.json', 'w'), indent = 4)
    except IOError as e:
        logging.error(f"Error saving JSON: {e}")
        return -1

# if __name__ == "__main__":
#     main('YVR', 'NRT', '2025-12-23')