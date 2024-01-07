import json
from bs4 import BeautifulSoup
from datetime import datetime

def parse_earnings(file_path):
    earnings = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        current_date = None
        for tr in soup.find_all('tr'):
            date_td = tr.find('td', class_='theDay')
            if date_td:
                date_text = date_td.get_text(strip=True)
                # Convert the date to a datetime object and then to the desired format
                parsed_date = datetime.strptime(date_text, "%A, %B %d, %Y")
                current_date = parsed_date.strftime("%Y-%m-%d")
                earnings[current_date] = []
            else:
                ticker_link = tr.find('a', class_='bold middle')
                if ticker_link and current_date:
                    ticker = ticker_link.get_text(strip=True)
                    earnings[current_date].append(ticker)

    return earnings

file_path = '../data/earnings-calendar.html'  
output_file_path = '../data/earnings_data.json'  

earnings_data = parse_earnings(file_path)

# Dumping the earnings data to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(earnings_data, json_file, ensure_ascii=False, indent=4)

print(f"Earnings data successfully written to {output_file_path}")
