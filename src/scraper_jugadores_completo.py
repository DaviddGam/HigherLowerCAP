import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

# ---------- CONFIG ----------
START_ID = 1
END_ID = 17130
BASE_URL = "https://1891.uy/jugadores/{id}/rodolfo-abalde"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CSV_PATH = os.path.join(OUTPUT_DIR, "jugadores_goles_fotos_con_default.csv")
SAVE_INTERVAL = 50
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}
# ----------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
session = requests.Session()
session.headers.update(HEADERS)

# Cargar CSV existente
df = pd.read_csv(CSV_PATH)
jugadores_existentes = {int(row["ID"]): row for _, row in df.iterrows()}

def obtener_numero(soup, titulo):
    for li in soup.select("li.tournament-row"):
        title_tag = li.select_one("p.title")
        if title_tag and titulo.lower() in title_tag.get_text(strip=True).lower():
            value_tag = li.select_one("p.value")
            if value_tag:
                try:
                    return int(value_tag.get_text(strip=True))
                except:
                    return 0
    return 0

def obtener_estadisticas_por_categoria(soup, categoria):
    section = soup.find("h3", string=lambda s: s and categoria.lower() in s.lower())
    if not section:
        return {}
    container = section.find_parent("div", class_="row-content")
    values = container.select("ul.data-list li")
    datos = {}
    for li in values:
        title = li.select_one("p.title")
        val = li.select_one("p.value, p.value.number")
        if title and val:
            key = title.get_text(strip=True).replace("\n", " ").replace(" ", "_").lower()
            try:
                datos[key] = int(val.get_text(strip=True))
            except:
                datos[key] = val.get_text(strip=True)
    return datos

def scrapear_nuevas_columnas(player_id):
    url = BASE_URL.format(id=player_id)
    try:
        resp = session.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")

        fecha_nacimiento = soup.select_one("li.birth-date p.value")
        fecha_nacimiento = fecha_nacimiento.get_text(strip=True) if fecha_nacimiento else None

        posicion = soup.select_one("li.position p.value")
        if posicion:
            posicion = posicion.get_text(strip=True)
        lugar_nacimiento = soup.select_one("li.birth-place p.value")
        lugar_nacimiento = lugar_nacimiento.get_text(strip=True) if lugar_nacimiento else None
        apodo = soup.select_one("li.nickname p.value")
        apodo = apodo.get_text(strip=True) if apodo else None

        campeonatos_uruguayos = obtener_numero(soup, "Campeonatos Uruguayos")
        titulos_internacionales = obtener_numero(soup, "Títulos Internacionales")

        oficiales = obtener_estadisticas_por_categoria(soup, "Partidos Oficiales")
        amistosos = obtener_estadisticas_por_categoria(soup, "Partidos Amistosos")
        clasicos_oficiales = obtener_estadisticas_por_categoria(soup, "Clásicos Oficiales")
        clasicos_amistosos = obtener_estadisticas_por_categoria(soup, "Clásicos Amistosos")

        nuevas_columnas = {
            "FechaNacimiento": fecha_nacimiento,
            "Posicion": posicion,
            "LugarNacimiento": lugar_nacimiento,
            "Apodo": apodo,
            "CampeonatosUruguayos": campeonatos_uruguayos,
            "TitulosInternacionales": titulos_internacionales,
            **{f"Oficiales_{k}": v for k, v in oficiales.items()},
            **{f"Amistosos_{k}": v for k, v in amistosos.items()},
            **{f"ClasicosOficiales_{k}": v for k, v in clasicos_oficiales.items()},
            **{f"ClasicosAmistosos_{k}": v for k, v in clasicos_amistosos.items()},
        }

        return nuevas_columnas

    except Exception as e:
        print(f"[ERROR] ID {player_id}: {e}")
        return None

# ---------- MAIN ----------
for idx, row in df.iterrows():
    player_id = int(row["ID"])
    nuevas = scrapear_nuevas_columnas(player_id)
    if nuevas:
        for k, v in nuevas.items():
            df.at[idx, k] = v
        print(f"✅ ID {player_id} actualizado")
    else:
        print(f"[INFO] ID {player_id} sin datos nuevos")
    time.sleep(random.uniform(0.8, 1.5))

# Guardar CSV actualizado
df.to_csv(CSV_PATH.replace(".csv", "_actualizado.csv"), index=False, encoding="utf-8-sig")
print("🏁 CSV actualizado con nuevas columnas.")
