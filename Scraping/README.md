# Web Scraping and Data Extraction Pipeline

This repository contains a Python-based web scraping and data extraction pipeline for collecting company information, products, and activities from a specified website. The extracted data is stored in a MySQL database.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Functions](#functions)


## Requirements

- Python 3.x
- MySQL server
- Required Python libraries: listed in `requirements.txt`

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/khatun1112/Spyur.git
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the MySQL database:**
    - Create a MySQL database named `spyur_companies`.
    - Update the database configuration in `config.py` with your MySQL credentials.

5. **Prepare the input file:**
    - Ensure you have a file named `company_link.txt` containing the URLs to scrape.

## Usage

Run the main script to start the scraping and data extraction process:

```bash
python main.py
```

## Project Structure

- **`main.py`**: The main script to run the scraping pipeline.
- **`utils.py`**: Contains utility functions for scraping and data processing.
- **`utils_db.py`**: Contains functions for saving data to MySQL.
- **`config.py`**: Contains configuration details for database connection and proxy settings.
- **`requirements.txt`**: Lists the required Python packages.


## Configuration

**Database Configuration (config.py):**
```python
 database_config = {
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'host': 'localhost',
    'port': 3306,
    'database': 'spyur_companies'
}
```

**Proxy Configuration (config.py):**

```python
proxy_config = {
    "http": "http://your_proxy_url",
    "https": "http://your_proxy_url",
}
```

**Functions**

*main.py*

**Establish MySQL Connection:**

```python
connection = pymysql.connect(
    user=database_config['user'],
    password=database_config['password'],
    host=database_config['host'],
    port=database_config['port'],
    database=database_config['database']
)
```

**Scraping and Data Extraction:**

  - **Read URLs from company_link.txt.**
  - **Fetch and parse HTML content.**
  - **Extract company information, products, and activities.**
  - **Save extracted data to MySQL.**


*utils.py*
**Logging Configuration**

```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('company_info.log', mode='w')
                    ])
)
```


**Utility Functions:**

  - **generate_id(value):** Generates a unique ID using MD5 hashing.
  - **get_company_info(content, url):** Extracts company information.
  - **get_company_products(content, url):** Extracts company products.
  - **get_company_activities(content, url):** Extracts company activities.


*utils_db.py*
**Database Functions:**
  - **save_to_mysql(df, table_name, connection):** Saves a pandas DataFrame to a MySQL table with duplicate handling.
