import pandas as pd

# Ruta a tu CSV
CSV_PATH = "../data/jugadores_goles_fotos_con_default.csv"

# Cargar CSV
df = pd.read_csv(CSV_PATH)

# Filtrar jugadores con foto real y 0 goles
jugadores_foto_real_0goles = df[(df['DefaultFoto'] == False) & (df['Goles'] == 0)]

# Mostrar estadísticas
total_jugadores = len(df)
total_foto_real_0goles = len(jugadores_foto_real_0goles)
porcentaje = (total_foto_real_0goles / total_jugadores) * 100

print(f"Cantidad de jugadores con foto real y 0 goles: {total_foto_real_0goles}")
print(f"Total de jugadores: {total_jugadores}")
print(f"Porcentaje de jugadores con foto real y 0 goles: {porcentaje:.2f}%")
