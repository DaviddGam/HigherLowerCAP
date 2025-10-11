import pandas as pd
import os

# Ruta al CSV generado por el scraper
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CSV_PATH = os.path.join(OUTPUT_DIR, "jugadores_goles_fotos.csv")

# Cargar el CSV
df = pd.read_csv(CSV_PATH)

# ---- Estadísticas ----
jugadores_sin_goles = df[df["Goles"] == 0]
cantidad_sin_goles = len(jugadores_sin_goles)

print(f"Jugadores con 0 goles: {cantidad_sin_goles}")
print(f"Total de jugadores: {len(df)}")
print(f"Porcentaje sin goles: {cantidad_sin_goles / len(df) * 100:.2f}%")

# ---- Jugadores sin foto personalizada ----
sin_foto = df[df["Foto"].isna() | (df["Foto"].str.contains("default", na=False))]
print(f"Jugadores sin foto personalizada: {len(sin_foto)}")
