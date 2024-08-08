# Workplace Gender Roles in Armenia
By COPA
####
This project explores female representation in executive roles within the Armenian workplace across various industries. 
The analysis uses data scraped and cleaned from Armenian Yellow Pages (Spyur.am), providing insights into gender distribution and roles in different sectors. 
The project includes sections such as Web Scraping and Data Extraction, Data Cleaning and Processing and Streamlit dashboard to visualize the data interactively.
Our Dashboard: http://34.159.101.186:8501/

# Web Scraping and Data Extraction

This repository contains a Python-based web scraping and data extraction pipeline for collecting company information, products, and activities from a specified website. 
The extracted data is stored in a MySQL database.

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

## Functions

 **`main.py`**

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


**`utils.py`**

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


 **`utils_db.py`**
 
**Database Functions:**
  - **save_to_mysql(df, table_name, connection):** Saves a pandas DataFrame to a MySQL table with duplicate handling.

#
# Data Cleaning and Processing

This section describes the data cleaning and processing tasks performed on SQL tables extracted from the Spyur dataset. 
The focus is on preparing data related to female roles in higher executive positions within Armenian companies for further analysis and visualization.

## Overview

The project involves cleaning and processing four SQL tables:
- `company_table`
- `executive_table`
- `activity_table`
- `product_table`

The cleaned data is used for analysis and visualization with Streamlit.

## Files and Processing Steps

### 1. `company_exp.ipynb`

**Purpose:** Process and clean the `company_table`.

**Tasks:**
- Extracted location information from the `address` column using `geopy` to obtain latitude and longitude coordinates.
- Performed additional data cleaning, including removing empty entries and adjusting data types.

**Output:** Cleaned `company_table` saved for later merging.

### 2. `executive_exp.ipynb`

**Purpose:** Process and clean the `executive_table`.

**Tasks:**
- Extracted and cleaned first names of executives by identifying Armenian last names and removing middle names.
- Created `first_name` and `roles` columns.
- Mapped names to genders using a dictionary obtained via the OpenAI API (GPT-4), adding a `gender` column.
- Performed general data cleaning.

**Output:** Cleaned `executive_table` saved for later merging.

### 3. `activity_exp.ipynb`

**Purpose:** Process and clean the `activity_table`.

**Tasks:**
- Clustered company activities using the OpenAI API (GPT-4).
- Added `cluster` columns to the activities table.

**Output:** Cleaned `activity_table` saved as a pickle file and additional clustering information in JSON format.

### 4. `product_exp.ipynb`

**Purpose:** Process and clean the `product_table`.

**Tasks:**
- Clustered company products using the OpenAI API (GPT-4).
- Added `label` columns to the products table.

**Output:** Cleaned `product_table` saved as a pickle file and additional clustering information in JSON format.

## Dependencies

The following libraries are required for running the data cleaning and processing code:
- `geopy`
- `openai`
- `nltk`
- `pandas`
- `numpy`

These dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```
## Usage

To run the data cleaning and processing notebooks locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone <(https://github.com/khatun1112/Spyur.git)>
    cd <Spyur>
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Open and run the Jupyter notebooks:**

    ```bash
    jupyter notebook
    ```

5. **Execute each notebook in the following order to clean and process the data:**

    - `company_exp.ipynb`
    - `executive_exp.ipynb`
    - `activity_exp.ipynb`
    - `product_exp.ipynb`

The cleaned data will be saved in the specified formats (e.g., pickle files, JSON) for further use.


#
# Streamlit Dashboard

This Streamlit dashboard visualizes the gender distribution in companies, featuring several interactive plots and maps. 
The dashboard provides insights into company sizes, executive gender distribution, and geographical locations of companies.
#
- Before starting the Streamlit dashboard we merged all previously cleaned and prepared tables to get the final spyur.pkl table (you can see it in queries.ipynb).

## Features

1. **Data Loading and Filtering**
    - Load and filter data using various criteria such as company size or/and ownership form.

2. **Interactive Plots**
    - Pie plots to visualize gender distribution percentages.
    - Bar plots to compare gender percentages across different categories.
    - Line plots to show changes in male and female executive counts based on founding year.

3. **Geographical Visualization**
    - Maps showing the location of companies with color coding based on the percentage of female executives.

## Installation

To run this Streamlit dashboard locally, follow these steps:

1. **Clone the repository if you haven't yet:**
    ```sh
    git clone <(https://github.com/khatun1112/Spyur.git)>
    cd <Spyur/Streamlit>
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app:**
    ```sh
    streamlit run main.py
    ```

## Usage

### Data Loading and Filtering

1. **Load the Data:**
    - Ensure your data files are in the correct format and located in the specified directory.
    - The `load_data` function caches the data for faster loading.

2. **Filter the Data:**
    - Use the provided Streamlit widgets to filter data by company size/ownership form.

### Interactive Plots

1. **Pie Plots:**
    - Visualize the percentage distribution of male and female executives using Plotly.
    - Hover over the pie sections to see detailed counts.

2. **Bar Plots:**
    - Compare the number of male and female executives across different categories.
    - Interactive bars allow for better comparison and analysis.

3. **Line Plots:**
    - Show historical trends in male and female executive counts.
    - Use the year slider to filter the data by specific time ranges.

### Geographical Visualization

1. **Maps:**
    - Visualize the geographical distribution of companies using Folium.
    - Color-coded markers indicate the percentage of female executives in different regions.
    - Interact with the map to zoom in and out and explore different areas.

## Contributing

Feel free to contribute to this project by submitting issues. Make sure to follow the standard coding guidelines and ensure any changes are well-documented.

## Contact

For any questions or suggestions, please contact COPA at info@copa.team or https://www.copa.team/
