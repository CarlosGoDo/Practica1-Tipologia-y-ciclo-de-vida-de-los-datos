import requests
from bs4 import BeautifulSoup as parse
from io import StringIO
import pandas as pd


URL_BASE = "https://es.wikipedia.org"
URL_PROVINCIAS = "https://es.wikipedia.org/wiki/Provincia_(Espa%C3%B1a)"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}


def get_annex(page_url, headers):
    response = requests.get(page_url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = parse(response.text, "lxml")
    links = set()

    annex = soup.find_all("a", href=True, string=lambda s: s and "Anexo" in s)
    for a in annex:
        href = a["href"]
        if href.startswith("/wiki/"):
            links.add(URL_BASE + href)

    return sorted(list(links))


def normalizar_provincia(x):
    if pd.isna(x):
        return x

    x = str(x).strip()

    equivalencias = {
        "Coruña, La": "La Coruña",
        "Palmas, Las": "Las Palmas",
        "Rioja, La": "La Rioja",
        "Baleares": "Islas Baleares",
        "Gerona": "Girona",
        "Lérida": "Lleida",
        "Orense": "Ourense",
        "Álava": "Araba/Álava",
        "Guipúzcoa": "Gipuzkoa",
        "Vizcaya": "Bizkaia"
    }

    return equivalencias.get(x, x)


def limpiar_tabla_base(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    if "Nombre" in df.columns:
        df = df.rename(columns={"Nombre": "Provincia"})

    if "Provincia" not in df.columns:
        return None

    # si por alguna razón hay varias columnas llamadas Provincia
    if isinstance(df["Provincia"], pd.DataFrame):
        df["Provincia"] = df["Provincia"].iloc[:, 0]

    df["Provincia"] = df["Provincia"].astype(str).str.strip().apply(normalizar_provincia)

    filas_basura = ["España", "Total", "Otras (Chafarinas y Vélez de la Gomera)", "-", "nan"]
    df = df[~df["Provincia"].isin(filas_basura)].copy()

    return df


def parse_province_generic(prov_link, headers):
    response = requests.get(prov_link, headers=headers, timeout=20)
    response.raise_for_status()

    soup = parse(response.text, "lxml")
    table = soup.find("table", class_="wikitable")

    if table is None:
        raise ValueError("No se encontró ninguna tabla con clase 'wikitable'")

    df = pd.read_html(StringIO(str(table)), header=None)[0]

    if not any(isinstance(c, str) for c in df.columns):
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)

    return limpiar_tabla_base(df)



def parse_tabla_extranjeros_manual(prov_link, headers):
    response = requests.get(prov_link, headers=headers, timeout=20)
    response.raise_for_status()

    soup = parse(response.text, "lxml")
    table = soup.find("table", class_="wikitable")

    if table is None:
        raise ValueError("No se encontró la tabla de extranjeros")

    rows = table.find_all("tr")

    izquierda = []
    derecha = []

    def extraer_numero_total(texto):
        # Ejemplos válidos: 1.072.173 / 32.439 / 5.085
        m = re.search(r"\d{1,3}(?:\.\d{3})+", texto)
        return m.group(0) if m else None

    def extraer_porcentaje(texto):
        # Ejemplos válidos: 23,0 / 21,8 / 7,4 / 5,9
        m = re.search(r"\d{1,2},\d", texto)
        return m.group(0) if m else None

    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        prov_izq = cells[0].get_text(" ", strip=True)
        total_txt = cells[1].get_text(" ", strip=True)
        prov_der = cells[2].get_text(" ", strip=True)
        pct_txt = cells[3].get_text(" ", strip=True)

        total = extraer_numero_total(total_txt)
        pct = extraer_porcentaje(pct_txt)

        if prov_izq and total:
            izquierda.append({
                "Provincia": prov_izq,
                "Extranjeros totales": total
            })

        if prov_der and pct:
            derecha.append({
                "Provincia": prov_der,
                "% de extranjeros": pct
            })

    df_izq = pd.DataFrame(izquierda)
    df_der = pd.DataFrame(derecha)

    df_izq = limpiar_tabla_base(df_izq)
    df_der = limpiar_tabla_base(df_der)

    return df_izq.merge(df_der, on="Provincia", how="outer")

def es_link_relevante(link):
    # ignoramos anexos que no son tablas provinciales útiles
    irrelevantes = [
        "Anexo:Provincias_de_Espa%C3%B1a_por_IDH",
        "Anexo:Banderas_espa%C3%B1olas",
        "Anexo:Gastronom%C3%ADa_de_las_provincias_espa%C3%B1olas",
        "Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n",
        "Anexo:Comunidades_y_ciudades_aut%C3%B3nomas_de_Espa%C3%B1a"
    ]

    return not any(x in link for x in irrelevantes)


def main():
    links = get_annex(URL_PROVINCIAS, HEADERS)
    print("Num links:", len(links))

    df_global = None

    for i, link in enumerate(links):
        try:
            if not es_link_relevante(link):
                print("Me salto:", link)
                continue

            if "Extranjeros_en_Espa%C3%B1a_por_provincias" in link:
                df = parse_tabla_extranjeros_manual(link, HEADERS)
            else:
                df = parse_province_generic(link, HEADERS)

            if df is None or "Provincia" not in df.columns:
                print("Me salto:", link)
                continue

            rename_map = {
                col: f"{col}_{i}"
                for col in df.columns
                if col != "Provincia"
            }
            df = df.rename(columns=rename_map)

            if df_global is None:
                df_global = df.copy()
            else:
                df_global = df_global.merge(df, on="Provincia", how="outer")

        except Exception as e:
            print("Me salto:", link, "| Error:", e)

    df_global.to_csv("datos_raw.csv", index=False)
    print("CSV guardado como datos_raw.csv")





if __name__ == "__main__":
    main()
