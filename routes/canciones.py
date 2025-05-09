from fastapi import APIRouter, HTTPException
from models import Cancion
from operations.canciones import leer_canciones, escribir_canciones, ARCHIVO_CANCIONES
import os
import csv

ruta_canciones = APIRouter(prefix="/canciones", tags=["canciones"])

@ruta_canciones.get("/todas")
def obtener_todas_las_canciones():
    canciones = []
    if not os.path.exists(ARCHIVO_CANCIONES):
        return canciones
    with open(ARCHIVO_CANCIONES, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fila["duracion"] = float(fila["duracion"])
            fila["explicita"] = fila["explicita"].lower() == "true"
            fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
            canciones.append(Cancion(
                titulo=fila["titulo"],
                genero=fila["genero"],
                duracion=fila["duracion"],
                artista=fila["artista"],
                explicita=fila["explicita"],
                eliminado=fila["eliminado"]
            ))
    return canciones
@ruta_canciones.get("/")
def obtener_canciones():
    return leer_canciones()

@ruta_canciones.post("/")
def agregar_cancion(cancion: Cancion):
    canciones = leer_canciones()
    if any(c.titulo.lower() == cancion.titulo.lower() for c in canciones):
        raise HTTPException(status_code=400, detail="Ya existe una cancion con ese título")
    canciones.append(cancion)
    escribir_canciones(canciones)
    return {"mensaje": "Cancion agregada correctamente"}

@ruta_canciones.delete("/{titulo}")
def eliminar_cancion(titulo: str):
    ARCHIVO_CANCIONES = "canciones.csv"
    if not os.path.exists(ARCHIVO_CANCIONES):
        raise HTTPException(status_code=404, detail="No hay canciones registradas")
    actualizado = []
    encontrado = False
    with open(ARCHIVO_CANCIONES, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila["titulo"].lower() == titulo.lower() and fila.get("eliminado", "false").lower() != "true":
                fila["eliminado"] = "true"
                encontrado = True
            actualizado.append(fila)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    with open(ARCHIVO_CANCIONES, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=actualizado[0].keys())
        escritor.writeheader()
        for fila in actualizado:
            escritor.writerow(fila)
    return {"mensaje": "Canción eliminada (marcada como eliminada, no borrada)"}

@ruta_canciones.get("/buscar/genero/{genero}")
def buscar_canciones_por_genero(genero: str):
    canciones = []
    if not os.path.exists(ARCHIVO_CANCIONES):
        return canciones
    with open(ARCHIVO_CANCIONES, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila["genero"].lower() == genero.lower():
                fila["duracion"] = float(fila["duracion"])
                fila["explicita"] = fila["explicita"].lower() == "true"
                fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
                canciones.append(Cancion(**fila))
    return canciones

@ruta_canciones.get("/eliminadas")
def obtener_canciones_eliminadas():
    canciones = []
    if not os.path.exists(ARCHIVO_CANCIONES):
        return canciones
    with open(ARCHIVO_CANCIONES, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fila["duracion"] = float(fila["duracion"])
            fila["explicita"] = fila["explicita"].lower() == "true"
            fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
            if fila["eliminado"]:
                canciones.append(Cancion(**fila))
    return canciones
