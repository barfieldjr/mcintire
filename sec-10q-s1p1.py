import requests
import re
from bs4 import BeautifulSoup
from cik_lookup import lookup_cik
import sys

# Set up the headers with a proper User-Agent
headers = {
    'User-Agent': 'Your Name or Application (your.email@example.com)'  # Replace with your actual info
}

# Function to fetch the latest 10-Q filing
def fetch_latest_10q(cik, headers, ticker):
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    submissions_response = requests.get(submissions_url, headers=headers)
    if submissions_response.status_code == 200:
        data = submissions_response.json()
        filings = data.get('filings', {}).get('recent', {})
        accession_numbers = filings.get('accessionNumber', [])
        index = next((i for i, form in enumerate(filings.get('form', [])) if form == '10-Q'), None)
        if index is not None:
            latest_10q_accession_number = accession_numbers[index]
            index_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{latest_10q_accession_number.replace('-', '')}/{latest_10q_accession_number}-index.html"
            return fetch_document(index_url, headers, ticker)
    return None, None

# Function to fetch the document from the index URL
def fetch_document(index_url, headers, ticker):
    ticker = ticker+'-'
    index_response = requests.get(index_url, headers=headers)
    if index_response.status_code == 200:
        soup = BeautifulSoup(index_response.content, 'html.parser')
        doc_link = soup.find(lambda tag: tag.name == 'a' and ticker in tag.get('href', ''))
        if doc_link:
            doc_href = doc_link.get('href').replace('/ix?doc=', '')
            doc_url = f'https://www.sec.gov{doc_href}'
            return doc_url, requests.get(doc_url, headers=headers)
    return None, None

def extract_divs_between_markers(html_content, start_marker, end_marker):
    # Convert markers to regex patterns
    def marker_to_regex(marker):
        # Escape alphanumeric characters, replace non-alphanumeric with regex for optional space and any non-alphanumeric
        return re.compile("".join([r"\s*" + re.escape(char) + r"\s*" if char.isalnum() else r"\s*[^a-zA-Z0-9]*\s*" for char in marker]), re.IGNORECASE)

    start_pattern = marker_to_regex(start_marker)
    end_pattern = marker_to_regex(end_marker)

    soup = BeautifulSoup(html_content, 'html.parser')
    divs_between_markers = []
    found_start_marker = False
    first_occurrence_passed = False  # Flag to indicate that the first occurrence has been found

    for div in soup.find_all('div'):
        div_text = div.get_text()
        if start_pattern.search(div_text):
            if first_occurrence_passed:
                found_start_marker = True
                continue
            else:
                first_occurrence_passed = True
                continue
        if end_pattern.search(div_text) and found_start_marker:
            break
        if found_start_marker:
            divs_between_markers.append(div)
    return divs_between_markers

# Main execution
def extract_results(ticker="aapl"):
    cik = "000" +lookup_cik(ticker)

    _, doc_response = fetch_latest_10q(cik, headers, ticker)

    if doc_response and doc_response.status_code == 200:
        filename = "./temp/tester1.html"
        with open(filename, 'wb') as file:
            file.write(doc_response.content)

        # The start and end markers with HTML entities unescaped
        start_marker = 'Item 2.Management’s Discussion and Analysis of Financial Condition and Results of Operations'
        end_marker = 'ITEM 3.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK'

        # Read the HTML content from the file
        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract divs between markers
        divs_between_markers = extract_divs_between_markers(html_content, start_marker, end_marker)
        
        # Print extracted divs
        if divs_between_markers:
            print("Item 2. Management’s Discussion and Analysis of Financial Condition and Results of Operations")
            for div in divs_between_markers:
                print(div.text)
                continue
        else:
            print("Unable to scrape section-1 part-1 No divs found between the markers.")

    else:
        print(f"Failed to fetch or save the document. HTTP status code: {doc_response.status_code if doc_response else 'N/A'}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        extract_results(ticker)
    else:
        print("Please provide a ticker symbol as a command line argument.")