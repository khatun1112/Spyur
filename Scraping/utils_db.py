from sqlalchemy import create_engine
import logging

def save_to_mysql(df, table_name):
    """
    Save a pandas DataFrame to a MySQL table.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        table_name (str): The name of the table to save the DataFrame to.
    """
    # Database connection details
    user = 'Khatun'
    password = 'Khatun2004++'
    host = 'localhost'
    port = '3306'
    database = 'company_data'

    # Create a connection to the database
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    
    try:
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        logging.info(f"Data saved to {table_name} table successfully.")
    except Exception as e:
        logging.error(f"An error occurred while saving data to {table_name} table: {e}")
