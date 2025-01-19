import requests
import csv
from bs4 import BeautifulSoup

def fetch_certificates(domain):
    url = f"https://crt.sh/?q={domain}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_certificates(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    
    if not tables:
        print("No tables found on the page.")
        # Print the HTML content for debugging
        print(html)
        return set()
    
    # Assuming the table we need is the first one
    table = tables[1]
    
    rows = table.find_all('tr')[1:]  # Skip the header row

    certificates = set()
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 4:
            cert_id = cols[0].text.strip()
            cert_name = cols[4].text.strip()
            certificates.add((cert_id, cert_name))
    
    return certificates

def save_to_csv(certificates, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Certificate ID', 'Common Name'])
        for cert in certificates:
            writer.writerow(cert)

def main():
    domain = input("Enter the domain name: ")
    html = fetch_certificates(domain)
    certificates = parse_certificates(html)
    if certificates:
        save_to_csv(certificates, f"{domain}_certificates.csv")
    else:
        print("No certificates found.")

if __name__ == "__main__":
    main()