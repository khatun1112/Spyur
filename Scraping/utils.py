import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('info.log', mode='w')
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
                    'date_of_information_update': data.get('Date of information update', 'N/A'),
                    'url': url
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
                
                prod_content = content.find('ul', 'multilevel_list')
                if not prod_content:
                    continue

                for first_level in prod_content.find_all('div', class_='first_level_info'):
                    first_level_text = first_level.get_text(strip=True)
                    second_level_ul = first_level.find_next_sibling('ul')

                    if not second_level_ul:
                        continue

                    for second_level in second_level_ul.find_all('div', class_='second_level_info'):
                        second_level_text = second_level.get_text(strip=True)
                        product_ul = second_level.find_next_sibling('ul')

                        if not product_ul:
                            continue

                        for product in product_ul.find_all('a'):
                            product_name = product.get_text(strip=True)
                            prod_data.append({
                                'product_name': product_name,
                                'first_level_cluster': first_level_text,
                                'second_level_cluster': second_level_text
                            })
                            company_prod_data.append({
                                'company_name': company_name,
                                'product_name': product_name
                            })
            else:
                logging.error(f"Failed to retrieve product data from {url}, status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while processing product data from {url}: {e}")

    if company_prod_data and prod_data:
        company_product_table = pd.DataFrame(company_prod_data)
        product_table = pd.DataFrame(prod_data)

        company_product_table['company_name_id'] = company_product_table['company_name'].apply(generate_id)
        company_product_table['product_name_id'] = company_product_table['product_name'].apply(generate_id)
        product_table['product_name_id'] = product_table['product_name'].apply(generate_id)

        return company_product_table, product_table
    else:
        logging.error("No product data could be scraped from the provided URLs.")
        return None, None
    
def get_company_activities(urls, product_table):
    """
    Scrape company activity information from a list of URLs.

    Args:
        urls (list): A list of URLs to scrape.

    Returns:
        tuple: A tuple containing two pandas DataFrames:
            - company_activity_table: Contains company and activity information.
            - activity_table: Contains detailed activity information.
    """
    act_data = []
    comp_act_data = []

    for url in urls:
        try:
            logging.info(f"Fetching activity data from: {url}")
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')

                company_name_tag = content.find('h1', class_="page_title")
                company_name = company_name_tag.get_text(strip=True).replace("\"", "") if company_name_tag else "N/A"
                
                first_levels = content.find_all('div', class_='first_level_info')
                for first_level in first_levels:
                    first_level_text = first_level.get_text(strip=True)
                    second_levels = first_level.find_next_sibling('ul').find_all('div', class_='second_level_info')
                    
                    for second_level in second_levels:
                        second_level_text = second_level.get_text(strip=True)
                        activity = second_level.find_next_sibling('ul').find_all('a', href=True)
                        
                        for link in activity:
                            activity_text = link.get_text(strip=True)
                            act_data.append({
                                'first_level': first_level_text,
                                'second_level': second_level_text,
                                'activity_name': activity_text,
                            })
            else:
                logging.error(f"Failed to retrieve activity data from {url}, status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while processing activity data from {url}: {e}")

    if act_data:
        activity_table = pd.DataFrame(act_data)    
        activity_table['product_name_id'] = activity_table['activity_name'].apply(generate_id)    
        merged_df = activity_table.merge(product_table, on="product_name_id", how="left", indicator=True)
        activity_table = merged_df[merged_df["_merge"] == "left_only"][['product_name_id', "activity_name", "first_level", "second_level"]]
        activity_table.rename(columns={'product_name_id': 'activity_name_id'}, inplace=True)
        activity_table.reset_index(drop=True, inplace=True)

        for act in activity_table['activity_name']:
            comp_act_data.append({
                'activity_name': act,
                'company_name': company_name
            })
        
        company_activity_table = pd.DataFrame(comp_act_data)    
        company_activity_table['company_name_id'] = company_activity_table['company_name'].apply(generate_id)
        company_activity_table['activity_name_id'] = company_activity_table['activity_name'].apply(generate_id)

        return company_activity_table, activity_table
    else:
        logging.error("No activity data could be scraped from the provided URLs.")
        return None, None    

def chunk_list(lst, chunk_size):
    """
    Split a list into chunks of specified size.

    Args:
        lst (list): The list to be split.
        chunk_size (int): The size of each chunk.

    Returns:
        list: A list of chunks, where each chunk is a list of items.
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
