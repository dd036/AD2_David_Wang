import json
archivo = "PROYECTO_FINAL/saves.json"
def guardar_partida(partida):
    with open(archivo, "w") as f:
        json.dump(partida, f, indent=2)
