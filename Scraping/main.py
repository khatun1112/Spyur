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
connection = pymysql.connect(user=database_config['user'],
                             password=database_config['password'],
                             host=database_config['host'],
                             port=database_config['port'],
                             database=database_config['database'])

def save_to_csv(df, csv_path, append=False):
    mode = 'a' if append else 'w'
    header = not append
    df.to_csv(csv_path, index=False, mode=mode, header=header)

if __name__ == "__main__":
    with open("Scraping/company_link.txt", "r") as file:
        urls = file.readlines()
    urls = ['https://www.spyur.am' + url.strip() for url in urls]

    # Define paths for the CSV files
    company_csv = "company_table.csv"
    executive_csv = "executive_table.csv"
    product_csv = "product_table.csv"
    activity_csv = "activity_table.csv"

    append = False  # Initially, write mode with headers

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

            # Save DataFrames to CSV files
            save_to_csv(company_table, company_csv, append)
            logging.info(f"Company table appended to {company_csv}")

            save_to_csv(executive_table, executive_csv, append)
            logging.info(f"Executive table appended to {executive_csv}")

            save_to_csv(product_table, product_csv, append)
            logging.info(f"Product table appended to {product_csv}")

            save_to_csv(activity_table, activity_csv, append)
            logging.info(f"Activity table appended to {activity_csv}")

            append = True  # Switch to append mode after the first write

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            filename, line_number, func_name, text = tb[-1]
            logging.error(f"An error occurred during the scraping process: {e}, line: {line_number}, function: {func_name}, filename: {filename}")

    logging.info("Data scraping process completed. Check log file for details.")
    connection.close()
