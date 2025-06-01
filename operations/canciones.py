import csv
import os
from typing import List
from models import Cancion

ARCHIVO_CANCIONES = "canciones.csv"

def leer_canciones() -> List[Cancion]:
    canciones = []
    if not os.path.exists(ARCHIVO_CANCIONES):
        return canciones
    with open(ARCHIVO_CANCIONES, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fila["duracion"] = float(fila["duracion"])
            fila["explicita"] = fila["explicita"].lower() == "true"
            fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
            canciones.append(Cancion(**fila))
    return [c for c in canciones if not c.eliminado]

def escribir_canciones(canciones: List[Cancion]):
    with open(ARCHIVO_CANCIONES, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=Cancion.model_fields.keys())
        escritor.writeheader()
        for cancion in canciones:
            escritor.writerow(cancion.model_dump())