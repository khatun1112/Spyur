import pandas as pd
import hashlib
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('links.log', mode='w')
                    ])


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


def get_company_info(content, url):
    try:
        logging.info(f"Fetching company information from {url}")

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
        phone_number = ', '.join(phone_numbers) if phone_numbers else 'N/A'

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

        company_data = [{
            'company_name': company_name,
            'address': address,
            'number_of_employees': data.get('Number of employees', 'N/A'),
            'form_of_ownership': data.get('Form of ownership', 'N/A'),
            'year_established': data.get('Year established', 'N/A'),
            'date_of_information_update': data.get('Date of information update', 'N/A'),
            'phone_numbers': phone_number,
            'site_url': ', '.join(site_urls) if site_urls else 'N/A',
            'web_link': ', '.join(web_links) if web_links else 'N/A',
            'url': url
        }]

        executive_data = [{'executive': executive, 'url': url} for executive in lead_infos] if lead_infos else [{'executive': 'N/A', 'url': url}]
        

    except Exception as e:
        logging.error(f"An error occurred while processing: {e}")
        return pd.DataFrame(), pd.DataFrame()


    company_table = pd.DataFrame(company_data)
    executive_table = pd.DataFrame(executive_data)

    company_table['url_id'] = company_table['url'].apply(generate_id)
    executive_table['url_id'] = executive_table['url'].apply(generate_id)
    executive_table['executive_id'] = executive_table['executive'].apply(generate_id)

    return company_table, executive_table




def get_company_products(content, url):
    """
    Scrape company product information from a list of URLs.

    Args:
        content (BeautifulSoup): Parsed HTML content of the page.
        url (str): URL of the page.

    Returns:
        pd.DataFrame: A DataFrame containing company and product information.
    """
    prod_data = []


    logging.info(f"Fetching product information from {url}")

    info_sections = content.find_all('div', class_='info_section')

    # Initialize the flag to check if products data is found
    products_data_found = False

    # Loop through each info section and extract the desired data
    for section in info_sections:
        title = section.find('div', class_='info_title').text.strip()
        section_content = section.find('div', class_='info_content')

        if "Products, services by" in title:
            products_data_found = True
            prod_content = section_content.find('ul', class_='multilevel_list')
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
                            'url': url,
                            'product_name': product_name,
                            'prod_first_level_cluster': first_level_text,
                            'prod_second_level_cluster': second_level_text
                        })

    if not products_data_found:
        logging.warning(f"An error occurred while processing product data")
        prod_data.append({
            'url': url,
            'product_name': 'N/A',
            'prod_first_level_cluster': 'N/A',
            'prod_second_level_cluster': 'N/A'
        })



    product_table = pd.DataFrame(prod_data)

    product_table['url_id'] = product_table['url'].apply(generate_id)
    product_table['product_name_id'] = product_table['product_name'].apply(generate_id)

    return product_table



def get_company_activities(content, url):
    """
    Scrape company activity information from a list of URLs.

    Args:
        content (BeautifulSoup): Parsed HTML content of the page.
        url (str): URL of the page.

    Returns:
        pd.DataFrame: A DataFrame containing company activity information.
    """
    act_data = []


    logging.info(f"Fetching activity information from {url}")

    info_sections = content.find_all('div', class_='info_section')

    # Initialize the flag to check if activities data is found
    activities_data_found = False

    # Loop through each info section and extract the desired data
    for section in info_sections:
        title = section.find('div', class_='info_title').text.strip()
        section_content = section.find('div', class_='info_content')

        if "Activity types by" in title:
            activities_data_found = True
            act_content = section_content.find('ul', class_='multilevel_list')
            if not act_content:
                continue

            for first_level in act_content.find_all('div', class_='first_level_info'):
                first_level_text = first_level.get_text(strip=True)
                second_level_ul = first_level.find_next_sibling('ul')

                if not second_level_ul:
                    continue

                for second_level in second_level_ul.find_all('div', class_='second_level_info'):
                    second_level_text = second_level.get_text(strip=True)
                    activity_ul = second_level.find_next_sibling('ul')

                    if not activity_ul:
                        continue

                    for activity in activity_ul.find_all('a'):
                        activity_name = activity.get_text(strip=True)
                        act_data.append({
                            'url': url,
                            'activity_name': activity_name,
                            'act_first_level_cluster': first_level_text,
                            'act_second_level_cluster': second_level_text
                        })

    if not activities_data_found:
        logging.warning(f"An error occurred while processing activity data")
        act_data.append({
            'url': url,
            'activity_name': 'N/A',
            'act_first_level_cluster': 'N/A',
            'act_second_level_cluster': 'N/A'
        })



    activity_table = pd.DataFrame(act_data)

    activity_table['url_id'] = activity_table['url'].apply(generate_id)
    activity_table['activity_name_id'] = activity_table['activity_name'].apply(generate_id)

    return activity_table


