import os
import shutil

# Ruta base del proyecto
base = r"C:\xampp\htdocs\Libros\proyect_1891"

# Carpetas origen y destino
origen = os.path.join(base, "data", "images")
destino = os.path.join(base, "src", "static", "images")

# Crear carpeta destino si no existe
os.makedirs(destino, exist_ok=True)

# Verificar que la carpeta origen exista
if not os.path.exists(origen):
    print(f"❌ No se encontró la carpeta de origen: {origen}")
else:
    # Copiar imágenes
    for archivo in os.listdir(origen):
        if archivo.lower().endswith((".jpg", ".png", ".jpeg")):
            shutil.copy(
                os.path.join(origen, archivo),
                os.path.join(destino, archivo)
            )
    print(f"✅ Todas las imágenes fueron copiadas a: {destino}")
