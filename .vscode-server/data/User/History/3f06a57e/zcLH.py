# utils.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import logging

# Define the proxy settings
proxy = {
    "http": "http://your-proxy-address",
    "https": "http://your-proxy-address",
}

# Function to generate Id values
def generate_id(value):
    return hashlib.md5(value.encode()).hexdigest()

def get_company_info(urls):
    company_data = []
    executive_data = []
    contacts_data = []

    for url in urls:
        try:
            logging.info(f"Fetching data from: {url}")
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')
                # Scraping logic
            else:
                logging.error(f"Failed to retrieve data from {url}, status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while processing {url}: {e}")

    if company_data and executive_data and contacts_data:
        company_table = pd.DataFrame(company_data)
        executive_table = pd.DataFrame(executive_data)
        contacts_table = pd.DataFrame(contacts_data)

        company_table['company_name_id'] = company_table['company_name'].apply(generate_id)
        executive_table['company_name_id'] = executive_table['company_name'].apply(generate_id)
        contacts_table['company_name_id'] = contacts_table['company_name'].apply(generate_id)

        return company_table, executive_table, contacts_table
    else:
        logging.error("No data could be scraped from the provided URLs.")
        return None, None, None

# Similarly update get_company_products and get_company_activities
