import os
import requests

# Configuration for API key
def read_api_key(config_file='config.txt'):
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith("API_KEY"):
                return line.strip().split('=')[1]
    raise ValueError("API key not found in config file.")

API_KEY = read_api_key()

# Function to download bulk CSVs
def download_bulk_csvs(api_endpoints, api_key, csv_folder='Bulk_CSV'):
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    
    for endpoint, url in api_endpoints.items():
        full_url = f"{url}&apikey={api_key}"
        response = requests.get(full_url)
        if response.status_code == 200:
            filename = os.path.join(csv_folder, f"{endpoint}.csv")
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {endpoint}: {response.status_code}")

bulk_api_endpoints = {
    "ratios_ttm_bulk": "https://financialmodelingprep.com/api/v4/ratios-ttm-bulk?",
    "rating_bulk": "https://financialmodelingprep.com/api/v4/rating-bulk?",
    "stock_peers_bulk": "https://financialmodelingprep.com/api/v4/stock_peers_bulk?",
    "scores_bulk": "https://financialmodelingprep.com/api/v4/scores-bulk?",
    "earnings_surprises_bulk": "https://financialmodelingprep.com/api/v4/earnings-surprises-bulk?year=2020",
    "dcf_bulk": "https://financialmodelingprep.com/api/v4/dcf-bulk?",
    "profile_all": "https://financialmodelingprep.com/api/v4/profile/all?",
    "price_target_summary_bulk": "https://financialmodelingprep.com/api/v4/price-target-summary-bulk?",
    "upgrades_downgrades_consensus_bulk": "https://financialmodelingprep.com/api/v4/upgrades-downgrades-consensus-bulk?",
    "etf_holder_bulk": "https://financialmodelingprep.com/api/v4/etf-holder-bulk?",
    "financial_growth_bulk": "https://financialmodelingprep.com/api/v4/financial-growth-bulk?year=2020&period=quarter",
    "income_statement_bulk": "https://financialmodelingprep.com/api/v4/income-statement-bulk?year=2020&period=quarter",
    "balance_sheet_statement_bulk": "https://financialmodelingprep.com/api/v4/balance-sheet-statement-bulk?year=2020&period=quarter",
    "cash_flow_statement_bulk": "https://financialmodelingprep.com/api/v4/cash-flow-statement-bulk?year=2020&period=quarter",
    "ratios_bulk": "https://financialmodelingprep.com/api/v4/ratios-bulk?year=2020&period=quarter",
    "key_metrics_bulk": "https://financialmodelingprep.com/api/v4/key-metrics-bulk?year=2020&period=quarter",
    "income_statement_growth_bulk": "https://financialmodelingprep.com/api/v4/income-statement-growth-bulk?year=2020&period=quarter",
    "balance_sheet_statement_growth_bulk": "https://financialmodelingprep.com/api/v4/balance-sheet-statement-growth-bulk?year=2020&period=quarter",
    "cash_flow_statement_growth_bulk": "https://financialmodelingprep.com/api/v4/cash-flow-statement-growth-bulk?year=2020&period=quarter"
}

download_bulk_csvs(bulk_api_endpoints, API_KEY)
