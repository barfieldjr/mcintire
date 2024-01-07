import json
import sys
import os

def get_earnings(date):
    script_dir = os.path.dirname(__file__)  
    file_path = os.path.join(script_dir, 'data/earnings_data.json')  

    with open(file_path) as f:
        data = json.load(f)

    return data.get(date, [])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        date = sys.argv[1]
        print(get_earnings(date))
    else:
        print("Please provide an earnings date a command line argument.")