import json
import os

def lookup_cik(ticker):

    current_dir = os.path.dirname(__file__)
    ticker_map_path = os.path.join(current_dir, "data", "ticker-map.json")

    with open (ticker_map_path) as f:
        ticker_map = json.load(f)
        return(ticker_map[ticker.lower()])