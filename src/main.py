import requests
from bs4 import BeautifulSoup as parse
from datetime import datetime as hoy
#from utils import extraer_marca, sleep_random, guardar_csv



def get_product_links(page_url, headers):
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = parse(response.text, "lxml")

    links = []

    # table = soup.find("table", class_="wikitable sortable jquery-tablesorter")
    table = soup.find_all("table", class_="wikitable")

    table_body = table[0].find("tbody")

    rows = table_body.find_all("tr")[1:]
    
    for row in rows:
        cells = row.find_all("td")[0]
        if not cells:
            continue

        link_tag = cells.find("a", href=True, class_=False)
        if link_tag:
            links.append("https://es.wikipedia.org/"+link_tag["href"])

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


import requests

url = "https://es.wikipedia.org/wiki/Provincia_(Espa%C3%B1a)"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

print(get_product_links(url, headers))
