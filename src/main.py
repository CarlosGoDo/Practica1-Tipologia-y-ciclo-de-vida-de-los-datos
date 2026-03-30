import requests
from bs4 import BeautifulSoup as parse
from datetime import datetime as hoy
#from utils import extraer_marca, sleep_random, guardar_csv

BASE_URL = "https://www.pccomponentes.com/portatiles"

def get_product_links(page_url):
    response = requests.get(page_url)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = parse(response.text, "html.parser")

    links = []
    for producto in soup.find_all("..."):
        link = producto.find("a")["href"]
        links.append(link)

    return links


def parse_product(product_url):
    response = requests.get(product_url)
    response.raise_for_status() # Raise an exception for bad status codes
    soup = parse(response.text, "html.parser")

    data = {}

    data["scrape_date"] = hoy()
    data["product_name"] = ...
    data["price_eur"] = ...
    data["brand"] = extraer_marca(product_name)
    data["rating"] = ...
    data["review_count"] = ...
    data["availability"] = ...
    data["main_category"] = "Portátiles"
    data["subcategory"] = ...
    data["product_url"] = product_url

    return data




url = "https://www.pccomponentes.com/portatiles"
r = requests.get(url, timeout=20)

print(r.status_code)
print(r.headers)
print(r.text[:500])

