import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://1891.uy/jugadores?orderBy=A&order=A&page={}"
START_PAGE = 1
END_PAGE = 109
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "jugadores_1891.csv")

# Crear directorio de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def obtener_nombres_de_pagina(page_num):
    url = BASE_URL.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    jugadores = soup.find_all("a", class_="name")
    return [jugador.get_text(strip=True) for jugador in jugadores]

def main():
    nombres_totales = []

    for page in range(START_PAGE, END_PAGE + 1):
        try:
            nombres = obtener_nombres_de_pagina(page)
            if nombres:
                print(f"Página {page} procesada ({len(nombres)} jugadores).")
                nombres_totales.extend(nombres)
            else:
                print(f"[AVISO] Página {page} vacía o inaccesible.")
        except Exception as e:
            print(f"[ERROR] Página {page}: {e}")
        time.sleep(1)  # Pausa para no sobrecargar el servidor

    # Eliminar duplicados y guardar en CSV
    nombres_unicos = list(dict.fromkeys(nombres_totales))
    df = pd.DataFrame(nombres_unicos, columns=["Nombre"])
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"¡Guardados {len(nombres_unicos)} jugadores en {OUTPUT_CSV}!")

if __name__ == "__main__":
    main()
