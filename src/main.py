import requests
from bs4 import BeautifulSoup as parse
from datetime import datetime as hoy
from io import StringIO

import pandas as pd
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

def get_annex(page_url, headers):

    response = requests.get(page_url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = parse(response.text, "lxml")

    links = set()
    annex = soup.find_all("a", href=True, string=lambda s: s and "Anexo" in s)

    for a in annex:
        links.add("https://es.wikipedia.org/" + a["href"])

    return list(links)


def parse_province(prov_link):
    response = requests.get(prov_link, headers=headers, timeout=20)
    response.raise_for_status()

    soup = parse(response.text, "lxml")

    table = soup.find("table", class_="wikitable")
  
    if table is None:
        raise ValueError("No se encontró ninguna tabla con clase 'wikitable'")


    df_data = pd.read_html(StringIO(str(table)), header=None)[0]

    if not any(isinstance(c, str) for c in df_data.columns):
        df_data.columns = df_data.iloc[0]
        df_data = df_data[1:].reset_index(drop=True)

    return df_data


import requests

url = "https://es.wikipedia.org/wiki/Provincia_(Espa%C3%B1a)"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

links = get_annex(url, headers)

print("Num link: ", len(links))
df_global = None

for i, link in enumerate(links):
    try:
        if "comunidad" in link.lower():
            print("Me salto:", link)
            continue

        df = parse_province(link)

        df.columns = [str(c).strip() for c in df.columns]

        if "Nombre" in df.columns:
            df = df.rename(columns={"Nombre": "Provincia"})

        if "Provincia" not in df.columns:
            print("Me salto:", link)
            continue

        df["Provincia"] = df["Provincia"].astype(str).str.strip()

        rename_map = {
            col: f"{col}_{i}"
            for col in df.columns
            if col != "Provincia"
        }
        df = df.rename(columns=rename_map)


        if df_global is None:
            df_global = df
        else:
            df_global["Provincia"] = df_global["Provincia"].astype(str).str.strip()
            df_global = df_global.merge(df, on="Provincia", how="outer")

    except Exception as e:
        print("Me salto:", link, "| Error:", e)

df_global.to_csv("datos.csv")
