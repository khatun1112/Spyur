import requests
from bs4 import BeautifulSoup
import logging

def get_company_links(base_url):
    page = 1

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler('company_link.log', mode='w')
                        ])
    proxy = {
        "http": "http://brd-customer-hl_92e289be-zone-datacenter_proxy1-ip-45.143.104.217:dnrfxzvtp140@brd.superproxy.io:22225",
        "https": "http://brd-customer-hl_92e289be-zone-datacenter_proxy1-ip-45.143.104.217:dnrfxzvtp140@brd.superproxy.io:22225",
    }

    while True:
        url = f"{base_url}-{page}/?type=bd&yp_cat1=3&yp_cat2=l2.3.7%2Cl2.3.24%2Cl2.3.10%2Cl2.3.36%2Cl2.3.38%2Cl2.3.37%2Cl2.3.32%2Cl2.3.47%2Cl2.3.48%2Cl2.3.33%2Cl2.3.41%2Cl2.3.44%2Cl2.3.45%2Cl2.3.40%2Cl2.3.31%2Cl2.3.28%2Cl2.3.39%2Cl2.3.30%2Cl2.3.26%2Cl2.3.25%2Cl2.3.23%2Cl2.3.35%2Cl2.3.5%2Cl2.3.27%2Cl2.3.34%2Cl2.3.8%2Cl2.3.9%2Cl2.3.42%2Cl2.3.29%2Cl2.3.17%2Cl2.3.18%2Cl2.3.20%2Cl2.3.12%2Cl2.3.13%2Cl2.3.14%2Cl2.3.16%2Cl2.3.19%2Cl2.3.15%2Cl2.3.21%2Cl2.3.11%2Cl2.3.22%2Cl2.3.6%2Cl2.3.46%2Cl2.3.43&yp_cat3=&search=Search"
        logging.info(f"Requesting URL: {url}")
        try:
            response = requests.get(url, proxies=proxy)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve page {page}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        company_items = soup.find('div', id='results_list_wrapper')

        if not company_items:
            logging.info(f"No company items found on page {page}")
            break

        links_found = False
        with open('company_link.txt', 'a') as file:
            for item in company_items.find_all('a', href=True):
                links_found = True
                link = item['href']
                file.write(link + '\n')
                logging.info(f"Found link: {link}")

        if not links_found:
            logging.info(f"No links found in div with id='results_list_wrapper' on page {page}")
            break

        page += 1
        logging.info(f"Moving to page {page}")

    logging.info("Finished processing all pages.")
    print("Finished processing all pages.")

if __name__ == "__main__":
    base_url = "https://www.spyur.am/en/yellow_pages"
    get_company_links(base_url)
