from bs4 import BeautifulSoup
import requests
import json

def get_url(origin, destination, outbound, inbound = None):
    if inbound == None:
        return f'https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{origin}%20on%{outbound}%20oneway%202%20seats%20on%20cheapest&curr=CAD'
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
    stops_element = listing.find('div', class_='EfT7Ae AdWm1c tPgKwe').find('span', class_='ogfYpf')
    return stops_element.text.strip()

def main():
    # Make a request to Google Flights URL and parse HTML
    url = get_url("origin", "destination", "outbound date", "inbound date")
    result = requests.get(url)
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

    # Save results to a JSON file
    json.dump(flight_data, open('google_flights_data.json', 'w'), indent = 4)

if __name__ == "__main__":
    main()