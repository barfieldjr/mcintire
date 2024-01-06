import json

ticker_map = {}

with open("./data/ticker-map.txt", "r") as f:
    for line in f:
        ticker, cik = line.strip().split("\t")
        ticker_map[ticker] = cik

with open("./data/ticker-map.json", "w") as f:
    json.dump(ticker_map, f)

print(ticker_map)
