from flask import Flask, render_template, jsonify
import pandas as pd
import random
import os
import sys
import webbrowser

app = Flask(__name__)

# --------------------------
# Detectar base_path según si estamos en exe o script
# --------------------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # dentro del exe
else:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --------------------------
# Rutas de archivos
# --------------------------
CSV_PATH = os.path.join(base_path, "data", "jugadores_goles_fotos_con_default.csv")
print("Leyendo CSV desde:", CSV_PATH)

# Cargar CSV y filtrar jugadores con foto real
df_jugadores = pd.read_csv(CSV_PATH)
df_jugadores = df_jugadores.dropna(subset=['ID', 'Nombre', 'Goles']).reset_index(drop=True)
df_jugadores = df_jugadores[df_jugadores['DefaultFoto'] == False].reset_index(drop=True)

print(f"Total jugadores con foto real: {len(df_jugadores)}")

# --------------------------
# Variables globales para control de 0 goles consecutivos
# --------------------------
ultimo_jugador_id = None
ultimo_0_goles = False

def elegir_jugador():
    global ultimo_jugador_id, ultimo_0_goles
    df_0 = df_jugadores[df_jugadores["Goles"] == 0]
    df_plus = df_jugadores[df_jugadores["Goles"] > 0]

    if ultimo_0_goles and len(df_plus) > 0:
        jugador = df_plus.sample(1).to_dict('records')[0]
    else:
        if random.random() < 0.7 and len(df_plus) > 0:
            jugador = df_plus.sample(1).to_dict('records')[0]
        else:
            jugador = df_0.sample(1).to_dict('records')[0]

    if jugador["ID"] == ultimo_jugador_id and len(df_plus) > 0:
        jugador = df_plus.sample(1).to_dict('records')[0]

    ultimo_jugador_id = jugador["ID"]
    ultimo_0_goles = jugador["Goles"] == 0

    return jugador

# --------------------------
# Rutas de Flask
# --------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_players')
def get_players():
    if len(df_jugadores) < 2:
        return jsonify({'error': 'No hay suficientes jugadores con foto'})

    player1 = elegir_jugador()
    player2 = elegir_jugador()
    while player2["ID"] == player1["ID"]:
        player2 = elegir_jugador()

    return jsonify({
        'player1': {
            'id': int(player1['ID']),
            'name': player1['Nombre'],
            'goals': int(player1['Goles']),
            'foto': player1['Foto']
        },
        'player2': {
            'id': int(player2['ID']),
            'name': player2['Nombre'],
            'goals': int(player2['Goles']),
            'foto': player2['Foto']
        }
    })

# --------------------------
# Ejecutar app y abrir navegador automáticamente
# --------------------------
if __name__ == '__main__':
    import webbrowser
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)
    app.run(debug=False)  # no debug → no doble apertura