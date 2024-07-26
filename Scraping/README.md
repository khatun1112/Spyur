# Web Scraping and Data Extraction Pipeline

This repository contains a Python-based web scraping and data extraction pipeline for collecting company information, products, and activities from a specified website. The extracted data is stored in a MySQL database.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
  
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

## Project Structure

- **`main.py`**: The main script to run the scraping pipeline.
- **`utils.py`**: Contains utility functions for scraping and data processing.
- **`utils_db.py`**: Contains functions for saving data to MySQL.
- **`config.py`**: Contains configuration details for database connection and proxy settings.
- **`requirements.txt`**: Lists the required Python packages.

