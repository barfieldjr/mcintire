import html
import requests
from bs4 import BeautifulSoup

# Set up the headers with a proper User-Agent
headers = {
    'User-Agent': 'Your Name or Application (your.email@example.com)'  # Replace with your actual info
}

# Function to fetch the latest 10-Q filing
def fetch_latest_10q(cik, headers):
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
            return fetch_document(index_url, headers)
    return None, None

# Function to fetch the document from the index URL
def fetch_document(index_url, headers):
    index_response = requests.get(index_url, headers=headers)
    if index_response.status_code == 200:
        soup = BeautifulSoup(index_response.content, 'html.parser')
        doc_link = soup.find(lambda tag: tag.name == 'a' and 'aapl-' in tag.get('href', ''))
        if doc_link:
            doc_href = doc_link.get('href').replace('/ix?doc=', '')
            doc_url = f'https://www.sec.gov{doc_href}'
            return doc_url, requests.get(doc_url, headers=headers)
    return None, None

# Function to extract divs between markers from the HTML content
def extract_divs_between_markers(html_content, start_marker, end_marker):
    soup = BeautifulSoup(html_content, 'html.parser')
    divs_between_markers = []
    found_start_marker = False
    for div in soup.find_all('div'):
        if start_marker in div.get_text():
            found_start_marker = True
            continue
        if end_marker in div.get_text():
            break
        if found_start_marker:
            divs_between_markers.append(div)
    return divs_between_markers

# Main execution
def main():
    cik = '0000320193'
    doc_url, doc_response = fetch_latest_10q(cik, headers)
    if doc_response and doc_response.status_code == 200:
        filename = "tester1.html"
        with open(filename, 'wb') as file:
            file.write(doc_response.content)
        print(f"Latest 10-Q filing saved as {filename}")

        # The start and end markers with HTML entities unescaped
        start_marker = html.unescape('Item 2.&#160;&#160;&#160;&#160;Management&#8217;s Discussion and Analysis of Financial Condition and Results of Operations')
        end_marker = html.unescape('Item 3.&#160;&#160;&#160;&#160;Quantitative and Qualitative Disclosures About Market Risk')

        # Read the HTML content from the file
        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract divs between markers
        divs_between_markers = extract_divs_between_markers(html_content, start_marker, end_marker)
        
        # Print extracted divs
        for div in divs_between_markers:
            print(div.text)
    else:
        print(f"Failed to fetch or save the document. HTTP status code: {doc_response.status_code if doc_response else 'N/A'}")

if __name__ == "__main__":
    main()
