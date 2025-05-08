import time
from send_lowest_fare import extract_json, find_cheapest_flight, send_email
from google_flight_scraper import main as scraper_main
from google_flight_scraper import drop_table
from time_series_analysis import get_price_trend
from flask import Flask, request, jsonify, send_file
from apscheduler.schedulers.background import BackgroundScheduler
import os
import matplotlib.pyplot as plt

app = Flask(__name__, static_folder='public', static_url_path='')
global currOrigin
global currDestination
global currDate
global currEmail

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/search', methods=['POST'])

def search():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')
    departDate = data.get('departDate')
    # returnDate = data.get('returnDate')
    email = data.get('email')

    currOrigin = origin
    currDestination = destination
    currDate = departDate
    currEmail = email

    scraper_main(origin, destination, departDate)
    flights = extract_json()
    subject = 'Flight tracker'
    cheapest = find_cheapest_flight(flights)
    body = f'{cheapest}'
    to_email = email

    try:
        send_email(subject, body, to_email)
    except:
        # no email input
        pass

    return jsonify({ 'status': 'ok', 'cheapest': cheapest['price']})

@app.route('/clear', methods=['POST'])
def clear_db():
    try:
        drop_table()
    except:
        # Table doesn't exist
        pass
    return jsonify('Database clared')

@app.route('/graph')
def graph():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    departDate = request.args.get('departDate')

    fig = get_price_trend(origin, destination, departDate)

    plot_dir = os.path.join('data')
    fig.savefig(os.path.join(plot_dir, 'time_series.png'))
    plt.close(fig)
    return send_file(os.path.join(plot_dir, 'time_series.png'), mimetype = 'image/png')

def schedule():

    if not currOrigin or not currDestination or not currDate:
        return
    
    scraper_main(currOrigin, currDestination, currDate)

    flights = extract_json()
    subject = 'Flight tracker'
    cheapest = find_cheapest_flight(flights)
    body = f'{cheapest}'
    to_email = currEmail

    try:
        send_email(subject, body, to_email)
    except:
        # no email input
        pass

    return jsonify({ 'status': 'ok', 'cheapest': cheapest['price']})

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule, 'interval', hours = 24)
    scheduler.start()

    try:
        app.run(debug = True)
    finally:
        scheduler.shutdown()