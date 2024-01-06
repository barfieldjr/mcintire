import json

def lookup_cik(ticker):
    with open ("./data/ticker-map.json") as f:
        ticker_map = json.load(f)
        # print cik based on ticker
        return(ticker_map[ticker.lower()])