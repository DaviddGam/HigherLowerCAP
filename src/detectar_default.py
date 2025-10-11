from PIL import Image
import imagehash
import os
import pandas as pd

# Ruta a tus imágenes 
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

# Ruta al CSV que ya generaste
CSV_PATH = os.path.join(os.path.dirname(__file__), "jugadores_goles_fotos.csv")

# Leer CSV
df = pd.read_csv(CSV_PATH)

# Diccionario para hashes
hashes = {}
hash_counts = {}

print("Analizando imágenes...\n")

for filename in os.listdir(IMAGES_DIR):
    if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
        continue
    path = os.path.join(IMAGES_DIR, filename)
    try:
        img = Image.open(path).convert("L").resize((64, 64))
        img_hash = imagehash.average_hash(img)
        str_hash = str(img_hash)

        if str_hash in hash_counts:
            hash_counts[str_hash] += 1
        else:
            hash_counts[str_hash] = 1

        hashes[filename.split(".")[0]] = str_hash

    except Exception as e:
        print(f"Error con {filename}: {e}")

# Encontrar el hash más repetido (probablemente la foto default)
default_hash = max(hash_counts, key=hash_counts.get)
default_count = hash_counts[default_hash]

print(f"\n🔍 Hash más repetido (default probable): {default_hash}")
print(f"📸 Cantidad de imágenes iguales: {default_count}\n")

# Agregar columna para marcar si es default o no
df["DefaultFoto"] = df["ID"].astype(str).apply(lambda x: hashes.get(x) == default_hash if x in hashes else False)

# Guardar CSV actualizado
OUTPUT_PATH = CSV_PATH.replace(".csv", "_con_default.csv")
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"✅ Archivo actualizado guardado en:\n{OUTPUT_PATH}")
print(f"Jugadores con foto default: {df['DefaultFoto'].sum()} de {len(df)} totales")
