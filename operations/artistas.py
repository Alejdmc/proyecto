import csv
import os
from typing import List
from models import ArtistaDB

ARCHIVO_ARTISTAS = "artistas.csv"

def leer_artistas() -> List[ArtistaDB]:
    artistas = []
    if not os.path.exists(ARCHIVO_ARTISTAS):
        return artistas
    with open(ARCHIVO_ARTISTAS, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fila["activo"] = fila["activo"].lower() == "true"
            fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
            artistas.append(ArtistaDB(**fila))
    return [a for a in artistas if not a.eliminado]

def escribir_artistas(artistas: List[ArtistaDB]):
    with open(ARCHIVO_ARTISTAS, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=ArtistaDB.model_fields.keys())
        escritor.writeheader()
        for artista in artistas:
            escritor.writerow(artista.model_dump())
