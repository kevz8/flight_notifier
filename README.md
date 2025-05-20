# Google Flights Price Scraper

This project scrapes flight listings from Google Flights based on user-inputted origin, destination, and departure date, and stores the data in a local SQLite database. The frontend form accepts IATA airport codes and displays clean input using JavaScript and HTML input validation.

## Features

- Scrapes flight data using `requests` and `BeautifulSoup`
- Stores data in an SQLite database with duplicate prevention
- Parses and stores:
  - Airline company
  - Flight duration
  - Price
  - Departure and arrival times
  - Number of stops
- Enforces uppercase 3-letter airport codes in form fields
- Error handling
- Supports automated scraping
- Can track rolling averages of flight prices

## Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/google-flights-scraper.git
   cd google-flights-scraper

2. run ```pip install -r requirements.txt```

3. run the server
```python app```
