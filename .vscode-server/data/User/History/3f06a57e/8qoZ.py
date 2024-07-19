import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('company_info.log', mode='w')
                    ])

# Define the proxy settings
proxy = {
    "http": "http://brd-customer-hl_92e289be-zone-datacenter_proxy1-ip-45.143.104.217:dnrfxzvtp140@brd.superproxy.io:22225",
    "https": "http://brd-customer-hl_92e289be-zone-datacenter_proxy1-ip-45.143.104.217:dnrfxzvtp140@brd.superproxy.io:22225",
}

# Function to generate Id values
def generate_id(value):
    """
    Generate a unique ID for a given value using MD5 hashing.

    Args:
        value (str): The input value to hash.

    Returns:
        str: The MD5 hash of the input value as a hexadecimal string.
    """
    return hashlib.md5(value.encode()).hexdigest()

def get_company_info(urls):
    """
    Scrape company information, executive information, and contact details from a list of URLs.

    Args:
        urls (list): A list of URLs to scrape.

    Returns:
        tuple: A tuple containing three pandas DataFrames:
            - company_table: Contains company information.
            - executive_table: Contains executive information.
            - contacts_table: Contains contact details.
    """ 
    company_data = []
    executive_data = []
    contacts_data = []

    for url in urls:
        try:
            logging.info(f"Fetching data from: {url}")
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')

                company_info = {}
                company_name_tag = content.find('h1', class_="page_title")
                company_name = company_name_tag.get_text(strip=True).replace("\"", "") if company_name_tag else "Unknown" 

                lead_block = content.find('div', class_='lead_block')
                if lead_block:
                    inner_title = lead_block.find('div', class_='inner_title')
                    if inner_title:
                        inner_title = inner_title.text.strip()
                    lead_info_blocks = lead_block.find_all('div', class_='lead_info')
                    lead_infos = [info.text.strip() for info in lead_info_blocks]
                else:
                    inner_title = None
                    lead_infos = []

                company_info['Company Name'] = company_name

                address_block = content.find('div', class_='address_block')
                address = address_block.get_text(strip=True) if address_block else "N/A"

                phone_numbers = []
                phone_info_div = content.find('div', class_='phone_info')
                if phone_info_div:
                    phone_numbers = [a.get_text(strip=True) for a in phone_info_div.find_all('a', href=True)]
                phone_number = ', '.join(phone_numbers)

                site_urls = []
                site_links = content.find_all('a', class_='web_link', href=True)
                if site_links:
                    site_urls = [link['href'] for link in site_links if link['href'].endswith('.am')]

                web_links = []
                if site_links:
                    web_links = [link['href'] for link in site_links if not link['href'].endswith('.am')]

                other_info = content.find('div', class_='other_info')

                data = {}
                if other_info:
                    info_list = other_info.find('ul', class_='info_list').find_all('li')
                    for item in info_list:
                        if 'key_words' in item.get('class', []):
                            continue
                        
                        subtitle_div = item.find('div', class_='inner_subtitle')
                        text_block_div = item.find('div', class_='text_block')
                        
                        if subtitle_div and text_block_div:
                            subtitle = subtitle_div.get_text(strip=True)
                            text_block = text_block_div.get_text(strip=True)
                            
                            data[subtitle] = text_block

                combined_info = {
                    'company_name': company_name,
                    'address': address,
                    'number_of_employees': data.get('Number of employees', 'N/A'),
                    'form_of_ownership': data.get('Form of ownership', 'N/A'),
                    'year_established': data.get('Year established', 'N/A'),
                    'date_of_information_update': data.get('Date of information update', 'N/A')
                }

                company_data.append(combined_info)

                for executive in lead_infos:
                    executive_data.append({
                        'company_name': company_name,
                        'executive': executive if executive else "N/A"
                    })

                contacts_data.append({
                    'company_name': company_name,
                    'phone_numbers': phone_number,
                    'site_url': ', '.join(site_urls),
                    'web_link': ', '.join(web_links)
                })
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

def get_company_products(urls):
    """
    Scrape company product information from a list of URLs.

    Args:
        urls (list): A list of URLs to scrape.

    Returns:
        tuple: A tuple containing two pandas DataFrames:
            - company_product_table: Contains company and product information.
            - product_table: Contains detailed product information.
    """
    company_prod_data = []
    prod_data = []

    for url in urls:
        try:
            logging.info(f"Fetching product data from: {url}")
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')

                company_name_tag = content.find('h1', class_="page_title")
                company_name = company_name_tag.get_text(strip=True).replace("\"", "") if company_name_tag else "Unknown"

                product_info_blocks = content.find_all('div', class_='product_info')
                for block in product_info_blocks:
                    product_name_tag = block.find('div', class_='product_name')
                    product_name = product_name_tag.get_text(strip=True) if product_name_tag else "N/A"

                    product_desc_tag = block.find('div', class_='product_description')
                    product_desc = product_desc_tag.get_text(strip=True) if product_desc_tag else "N/A"

                    company_prod_data.append({
                        'company_name': company_name,
                        'product_name': product_name,
                        'product_description': product_desc
                    })

                # Create a DataFrame for the product data
                company_product_table = pd.DataFrame(company_prod_data)
                
                # Extract unique products
                unique_products = pd.DataFrame({
                    'product_name': [data['product_name'] for data in company_prod_data],
                    'product_description': [data['product_description'] for data in company_prod_data]
                }).drop_duplicates()

                return company_product_table, unique_products
            else:
                logging.error(f"Failed to retrieve product data from {url}, status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while processing {url}: {e}")

    return None, None

def get_company_activities(urls, product_table):
    """
    Scrape company activities information from a list of URLs.

    Args:
        urls (list): A list of URLs to scrape.
        product_table (DataFrame): A DataFrame containing product information.

    Returns:
        tuple: A tuple containing two pandas DataFrames:
            - company_activity_table: Contains company and activity information.
            - activity_table: Contains detailed activity information.
    """
    company_activity_data = []
    activity_data = []

    for url in urls:
        try:
            logging.info(f"Fetching activity data from: {url}")
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')

                company_name_tag = content.find('h1', class_="page_title")
                company_name = company_name_tag.get_text(strip=True).replace("\"", "") if company_name_tag else "Unknown"

                activity_info_blocks = content.find_all('div', class_='activity_info')
                for block in activity_info_blocks:
                    activity_name_tag = block.find('div', class_='activity_name')
                    activity_name = activity_name_tag.get_text(strip=True) if activity_name_tag else "N/A"

                    activity_desc_tag = block.find('div', class_='activity_description')
                    activity_desc = activity_desc_tag.get_text(strip=True) if activity_desc_tag else "N/A"

                    company_activity_data.append({
                        'company_name': company_name,
                        'activity_name': activity_name,
                        'activity_description': activity_desc
                    })

                # Create a DataFrame for the activity data
                company_activity_table = pd.DataFrame(company_activity_data)
                
                # Extract unique activities
                unique_activities = pd.DataFrame({
                    'activity_name': [data['activity_name'] for data in company_activity_data],
                    'activity_description': [data['activity_description'] for data in company_activity_data]
                }).drop_duplicates()

                return company_activity_table, unique_activities
            else:
                logging.error(f"Failed to retrieve activity data from {url}, status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while processing {url}: {e}")

    return None, None
