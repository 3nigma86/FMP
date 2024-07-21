import requests
import sqlite3
import schedule
import time
import pandas as pd
import logging
from datetime import datetime
from threading import Thread

# Configure logging
logging.basicConfig(
    filename='fetch_tickers.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Function to read API key from config file
def read_api_key(config_file='config.txt'):
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith("API_KEY"):
                return line.strip().split('=')[1]
    raise ValueError("API key not found in config file.")

# Read API key
API_KEY = read_api_key()

# Define the API endpoints
TICKER_API_URL = f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={API_KEY}"
KEY_METRICS_API_URL = f"https://financialmodelingprep.com/api/v4/key-metrics-ttm-bulk?apikey={API_KEY}"

# Function to fetch ticker symbols
def fetch_ticker_symbols():
    try:
        response = requests.get(TICKER_API_URL)
        response.raise_for_status()
        tickers = response.json()
        
        conn = sqlite3.connect('stocks_data.db')
        cursor = conn.cursor()
        
        for ticker in tickers:
            cursor.execute('''
            INSERT OR IGNORE INTO stocks (ticker_id) VALUES (?)
            ''', (ticker,))
        
        conn.commit()
        conn.close()
        logging.info("Ticker symbols fetched and stored.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching ticker symbols: {e}")

# Function to fetch key metrics and update the database
def fetch_key_metrics():
    max_retries = 5
    retry_delay = 5  # start with a 5-second delay
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(KEY_METRICS_API_URL)
            response.raise_for_status()
            
            with open('key_metrics.csv', 'wb') as file:
                file.write(response.content)
            logging.info("Key metrics CSV downloaded.")
            
            # Read the CSV file
            df = pd.read_csv('key_metrics.csv')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            conn = sqlite3.connect('stocks_data.db')
            cursor = conn.cursor()
            
            for index, row in df.iterrows():
                ticker_id = row['symbol']
                for key in df.columns:
                    if key != 'symbol':
                        value = row[key]
                        cursor.execute('''
                        INSERT OR REPLACE INTO key_metrics (ticker_id, date, key, value) VALUES (?, ?, ?, ?)
                        ''', (ticker_id, timestamp, key, value))
            
            conn.commit()
            conn.close()
            logging.info("Key metrics stored in the database.")
            break
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                retries += 1
                logging.warning(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logging.error(f"Error fetching key metrics: {e}")
                break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            break

# Scheduler setup
schedule.every().monday.at("00:00").do(fetch_ticker_symbols)
schedule.every().monday.at("01:00").do(fetch_key_metrics)

# Rate limiting function
def rate_limited_fetch():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait for one second between checks

# Function to ensure we don't exceed 700 API calls per minute
def limit_api_calls():
    calls = 0
    start_time = datetime.now()

    while True:
        if calls >= 700 and (datetime.now() - start_time).seconds < 60:
            time.sleep(60 - (datetime.now() - start_time).seconds)
            calls = 0
            start_time = datetime.now()
        else:
            rate_limited_fetch()
            calls += 1

# Manual trigger function
def manual_trigger():
    while True:
        print("Manual Trigger Options:")
        print("1. Fetch Ticker Symbols")
        print("2. Fetch Key Metrics")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            fetch_ticker_symbols()
        elif choice == '2':
            fetch_key_metrics()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")

# Start the rate limiting and scheduling with manual trigger
if __name__ == "__main__":
    # Start the scheduling in a separate thread
    scheduling_thread = Thread(target=limit_api_calls)
    scheduling_thread.start()

    # Run the manual trigger in the main thread
    manual_trigger()
