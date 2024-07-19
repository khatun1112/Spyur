import pandas as pd
from utils import get_company_info, get_company_products, get_company_activities
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('company_info.log', mode='w')
                    ])

# Database connection parameters
USERNAME = 'Khatun'
PASSWORD = 'Khatun2004++'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'spyur_companies'

def save_to_mysql(df, table_name, engine):
    try:
        if not df.empty:
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            logging.info(f"DataFrame saved to {table_name} table in MySQL successfully.")
        else:
            logging.info(f"DataFrame for {table_name} is empty and was not saved.")
    except Exception as e:
        logging.error(f"An error occurred while saving DataFrame to MySQL: {e}")

def process_urls(urls, engine):
    batch_size = 5
    total_urls = len(urls)
    
    for i in range(0, total_urls, batch_size):
        batch_urls = urls[i:i + batch_size]
        
        logging.info(f"Processing batch {i // batch_size + 1} with URLs {batch_urls}")

        # Fetch data for the batch of URLs
        company_table, executive_table, contacts_table = get_company_info(batch_urls)
        company_product_table, product_table = get_company_products(batch_urls)
        company_activity_table, activity_table = get_company_activities(batch_urls, product_table)

        # Save DataFrames to MySQL
        save_to_mysql(company_table, 'company_info', engine)
        save_to_mysql(executive_table, 'executive_info', engine)
        save_to_mysql(contacts_table, 'contacts', engine)
        save_to_mysql(company_product_table, 'company_products', engine)
        save_to_mysql(product_table, 'products', engine)
        save_to_mysql(company_activity_table, 'company_activities', engine)
        save_to_mysql(activity_table, 'activities', engine)

if __name__ == "__main__":
    try:
        with open("links.txt", "r") as file:
            urls = file.readlines()
        urls = ['https://www.spyur.am' + url.strip() for url in urls]

        # Database connection string
        engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

        # Process URLs in batches and save to MySQL
        process_urls(urls, engine)

    except Exception as e:
        logging.error(f"An error occurred in the main block: {e}")

    print("Data scraping process completed. Check log file for details.")
