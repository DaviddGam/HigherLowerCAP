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
IMG_BASE_URL = "https://1891.uy/img/jugadores/{}"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "jugadores_goles_fotos.csv")
SAVE_INTERVAL = 50
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}
# ----------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)

# Cargar CSV parcial si existe
if os.path.exists(OUTPUT_CSV):
    df = pd.read_csv(OUTPUT_CSV)
    jugadores = df.to_dict("records")
    last_id = max(j["ID"] for j in jugadores)
    print(f"Se cargaron {len(jugadores)} jugadores del CSV existente. Continuando desde ID {last_id+1}.")
else:
    jugadores = []
    last_id = START_ID - 1

# ----------------------------
def obtener_datos_jugador(player_id):
    url = BASE_URL.format(id=player_id)
    try:
        resp = session.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")

        # Nombre
        nombre_tag = soup.select_one("h1.page-title span")
        nombre = nombre_tag.get_text(strip=True) if nombre_tag else None

        # Goles
        goles_tag = None
        for li in soup.select("li.tournament-row"):
            title_tag = li.select_one("p.title")
            if title_tag and "Goles" in title_tag.get_text():
                value_tag = li.select_one("p.value")
                goles_tag = value_tag.get_text(strip=True) if value_tag else "0"
                break
        goles = int(goles_tag) if goles_tag else 0

        # Descargar imagen
        foto_path = None
        img_url = IMG_BASE_URL.format(player_id)
        img_resp = session.get(img_url, stream=True)
        if img_resp.status_code == 200:
            foto_path = os.path.join(OUTPUT_DIR, "images", f"{player_id}.jpg")
            with open(foto_path, "wb") as f:
                for chunk in img_resp.iter_content(1024):
                    f.write(chunk)

        if nombre:
            return {"ID": player_id, "Nombre": nombre, "Goles": goles, "Foto": foto_path}
    except Exception as e:
        print(f"[ERROR] ID {player_id}: {e}")
    return None

def guardar_csv(jugadores):
    df = pd.DataFrame(jugadores)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

def main():
    global jugadores
    for player_id in range(last_id + 1, END_ID + 1):
        data = obtener_datos_jugador(player_id)
        if data:
            jugadores.append(data)
            print(f"ID {player_id}: {data['Nombre']} - {data['Goles']} goles")
            time.sleep(random.uniform(0.8, 1.5))
        else:
            print(f"[INFO] ID {player_id} no existe o no se pudo obtener")
            time.sleep(0.05)

        if len(jugadores) % SAVE_INTERVAL == 0:
            guardar_csv(jugadores)
            print(f"[INFO] Guardados {len(jugadores)} jugadores intermedios en CSV.")

    guardar_csv(jugadores)
    print(f"\n¡Scraping finalizado! Total de jugadores guardados: {len(jugadores)}")
    print(f"Archivo CSV: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
