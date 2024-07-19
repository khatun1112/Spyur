import pandas as pd
from utils import get_company_info, get_company_products, get_company_activities
import logging

if __name__ == "__main__":
    try:
        with open("try1.txt", "r") as file:
            urls = file.readlines()
        urls = ['https://www.spyur.am' + url.strip() for url in urls]
        
        logging.info(f"Fetching data from URLs...")
        company_table, executive_table, contacts_table = get_company_info(urls)
        company_product_table, product_table = get_company_products(urls)
        company_activity_table, activity_table = get_company_activities(urls, product_table)

        if company_table is not None and executive_table is not None and contacts_table is not None:
            logging.info(f"Data scraping for company info completed successfully.")
        else:
            logging.error("Data scraping for company info failed for all URLs.")


        if company_product_table is not None and product_table is not None:
            logging.info(f"Data scraping for company products completed successfully.")
        else:
            logging.error("Data scraping company products failed for all URLs.")
            

        if company_activity_table is not None and activity_table is not None:
            logging.info(f"Data scraping for company activities completed successfully.")   
        else:
            logging.error("Data scraping for company activities failed for all URLs.")    

    except Exception as e:
        logging.error(f"An error occurred in the main block: {e}")

    print("Data scraping process completed. Check log file for details.")
