import pandas as pd
import pymysql
import logging
from sqlalchemy import create_engine

def save_to_mysql(df, table_name):
    """
    Save a pandas DataFrame to a MySQL table, allowing duplicates and appending new data.
    """

    # Database connection details
    user = 'root'
    password = 'Khat2004++'
    host = 'localhost'
    port = '3306'
    database = 'company_data'

    # Create a connection to the database
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    
    # Get column names and data from the DataFrame
    columns = list(df.columns)
    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join(columns)
    update_str = ', '.join([f"{col}=VALUES({col})" for col in columns])

    # SQL query with ON DUPLICATE KEY UPDATE clause
    sql = f"""
    INSERT INTO {table_name} ({columns_str}) 
    VALUES ({placeholders}) 
    ON DUPLICATE KEY UPDATE {update_str}
    """
    
    # Create a connection using pymysql for executing raw SQL
    connection = pymysql.connect(user=user, password=password, host=host, port=int(port), database=database)
    
    try:
        with connection.cursor() as cursor:
            # Convert DataFrame to list of tuples
            data = [tuple(row) for row in df.values]
            
            # Execute the SQL query
            cursor.executemany(sql, data)
            connection.commit()
            logging.info(f"Data appended to {table_name} table successfully.")
    except pymysql.MySQLError as e:
        logging.error(f"An error occurred while saving data to {table_name} table: {e}")
    finally:
        connection.close()