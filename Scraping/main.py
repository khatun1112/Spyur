from tqdm import tqdm
from utils import get_company_info, get_company_products, get_company_activities
from utils_db import save_to_mysql
from config import database_config, proxy_config
import logging
import pymysql
import traceback
import requests
from bs4 import BeautifulSoup


# Establish a connection to the MySQL database
connection = pymysql.connect(user= database_config['user'],
                             password= database_config['password'],
                             host = database_config['host'],
                             port = database_config['port'],
                             database = database_config['database'])


if __name__ == "__main__":
    with open("try.txt", "r") as file:
        urls = file.readlines()
    urls = ['https://www.spyur.am' + url.strip() for url in urls]

    for url in tqdm(urls):
        try:
            logging.info(f"Fetching data from: {url}")
            response = requests.get(url, proxies=proxy_config)
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
            company_table, executive_table = get_company_info(content, url)
            product_table = get_company_products(content, url)
            activity_table = get_company_activities(content, url)

            logging.info("Company data scraping completed successfully.")
            save_to_mysql(company_table, 'company_table', connection)
            save_to_mysql(executive_table, 'executive_table', connection)

            logging.info("Product data scraping completed successfully.")
            save_to_mysql(product_table, 'product_table', connection)

            logging.info("Activity data scraping completed successfully.")
            save_to_mysql(activity_table, 'activity_table', connection)


        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            filename, line_number, func_name, text = tb[-1]
            logging.error(f"An error occurred during the scraping process: {e}, line: {line_number}, function: {func_name}, filename: {filename}")

    logging.info("Data scraping process completed. Check log file for details.")
    connection.close()