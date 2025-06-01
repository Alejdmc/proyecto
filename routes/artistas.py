from fastapi import APIRouter, HTTPException
from models import Artista
from operations.artistas import leer_artistas, escribir_artistas, ARCHIVO_ARTISTAS
import os
import csv

ruta_artistas = APIRouter(prefix="/artistas", tags=["artistas"])

@ruta_artistas.get("/")
def obtener_artistas():
    return leer_artistas()

@ruta_artistas.post("/")
def agregar_artista(artista: Artista):
    artistas = leer_artistas()
    if any(a.nombre.lower() == artista.nombre.lower() for a in artistas):
        raise HTTPException(status_code=400, detail="Ya existe un artista con ese nombre")
    artistas.append(artista)
    escribir_artistas(artistas)
    return {"mensaje": "Artista agregado correctamente"}

@ruta_artistas.delete("/{nombre}")
def eliminar_artista(nombre: str):
    ARCHIVO_ARTISTAS = "artistas.csv"
    if not os.path.exists(ARCHIVO_ARTISTAS):
        raise HTTPException(status_code=404, detail="No hay artistas registrados")
    actualizado = []
    encontrado = False
    with open(ARCHIVO_ARTISTAS, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila["nombre"].lower() == nombre.lower() and fila.get("eliminado", "false").lower() != "true":
                fila["eliminado"] = "true"
                encontrado = True
            actualizado.append(fila)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    with open(ARCHIVO_ARTISTAS, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=actualizado[0].keys())
        escritor.writeheader()
        for fila in actualizado:
            escritor.writerow(fila)
    return {"mensaje": "Artista eliminado (marcado como eliminado, no borrado)"}

@ruta_artistas.get("/todos")
def obtener_todos_los_artistas():
    artistas = []
    if not os.path.exists(ARCHIVO_ARTISTAS):
        return artistas
    with open(ARCHIVO_ARTISTAS, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fila["activo"] = fila["activo"].lower() == "true"
            fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
            artistas.append(Artista(**fila))
    return artistas

@ruta_artistas.get("/buscar/pais/{pais}")
def buscar_artistas_por_pais(pais: str):
    artistas = []
    if not os.path.exists(ARCHIVO_ARTISTAS):
        return artistas
    with open(ARCHIVO_ARTISTAS, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila["pais"].lower() == pais.lower():
                fila["activo"] = fila["activo"].lower() == "true"
                fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
                artistas.append(Artista(**fila))
    return artistas

@ruta_artistas.get("/eliminados")
def obtener_artistas_eliminados():
    artistas = []
    if not os.path.exists(ARCHIVO_ARTISTAS):
        return artistas
    with open(ARCHIVO_ARTISTAS, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fila["activo"] = fila["activo"].lower() == "true"
            fila["eliminado"] = fila.get("eliminado", "false").lower() == "true"
            if fila["eliminado"]:
                artistas.append(Artista(**fila))
    return artistas