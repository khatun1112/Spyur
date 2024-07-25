from tqdm import tqdm
from utils import get_company_info, get_company_products, get_company_activities
from utils_db import save_to_mysql
import logging
import pymysql
import traceback
import requests
from bs4 import BeautifulSoup

# Database connection details
user = 'Copa'
password = 'COPA888'
host = 'localhost'
port = 3306
database = 'spyur_companies'

# Establish a connection to the MySQL database
connection = pymysql.connect(user=user, password=password, host=host, port=port, database=database)

proxy = {
    "http": "http://brd-customer-hl_92e289be-zone-datacenter_proxy1-ip-45.143.104.217:dnrfxzvtp140@brd.superproxy.io:22225",
    "https": "http://brd-customer-hl_92e289be-zone-datacenter_proxy1-ip-45.143.104.217:dnrfxzvtp140@brd.superproxy.io:22225",
}


if __name__ == "__main__":
    with open("company_link.txt", "r") as file:
        urls = file.readlines()
    urls = ['https://www.spyur.am' + url.strip() for url in urls]

    for url in tqdm(urls):
        try:
            logging.info(f"Fetching data from: {url}")
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')
            else:
                logging.error(f"Failed to fetch data from {url}, status code: {response.status_code}")
                continue
        except Exception as e:
            logging.error(f"An error occurred while fetching {url}: {e}")
            continue

        try:
            logging.info(f"Processing data from: {url}")
            company_table, executive_table, contacts_table = get_company_info(content, url)
            product_table = get_company_products(content, url)
            activity_table = get_company_activities(content, url)

            # Ensure all DataFrames are defined
            if company_table is not None and executive_table is not None and contacts_table is not None:
                logging.info("Company data scraping completed successfully.")
                save_to_mysql(company_table, 'company_table', connection)
                save_to_mysql(executive_table, 'executive_table', connection)
                save_to_mysql(contacts_table, 'contacts_table', connection)
            else:
                logging.error("Company data scraping failed for some tables.")

            if product_table is not None:
                logging.info("Product data scraping completed successfully.")
                save_to_mysql(product_table, 'product_table', connection)
            else:
                logging.error("Product data scraping failed.")

            if activity_table is not None:
                logging.info("Activity data scraping completed successfully.")
                save_to_mysql(activity_table, 'activity_table', connection)
            else:
                logging.error("Activity data scraping failed.")

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            filename, line_number, func_name, text = tb[-1]
            logging.error(f"An error occurred during the scraping process: {e}, line: {line_number}, function: {func_name}, filename: {filename}")

    logging.info("Data scraping process completed. Check log file for details.")
    connection.close()
