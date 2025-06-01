from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Proyecto Integrador API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Archivos locales para guardar datos persistentes
ARTISTAS_FILE = "data_artistas.json"
CANCIONES_FILE = "data_canciones.json"

# === CARGAR DATOS AL INICIO ===
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

artistas_db = load_data(ARTISTAS_FILE)
canciones_db = load_data(CANCIONES_FILE)

# === GUARDAR DATOS ===
def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# === MODELOS ===
class Artista(BaseModel):
    nombre: str
    pais: str
    genero_principal: str
    activo: bool

class Cancion(BaseModel):
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool

# === RUTAS HTML ===
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/artistas", response_class=HTMLResponse)
async def artistas_page(request: Request):
    return templates.TemplateResponse("artistas.html", {"request": request})

@app.get("/canciones", response_class=HTMLResponse)
async def canciones_page(request: Request):
    return templates.TemplateResponse("canciones.html", {"request": request})

@app.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})

# === API ENDPOINTS ===
@app.get("/api/artistas", response_model=list[Artista])
async def get_artistas():
    return artistas_db

@app.post("/api/artistas")
async def add_artista(artista: Artista):
    if any(a['nombre'].lower() == artista.nombre.lower() for a in artistas_db):
        raise HTTPException(status_code=400, detail="Artista ya existe")
    artistas_db.append(artista.dict())
    save_data(ARTISTAS_FILE, artistas_db)
    return {"mensaje": "Artista agregado"}

@app.put("/api/artistas/{nombre}")
async def update_artista(nombre: str, artista: Artista):
    for idx, a in enumerate(artistas_db):
        if a['nombre'].lower() == nombre.lower():
            artistas_db[idx] = artista.dict()
            save_data(ARTISTAS_FILE, artistas_db)
            return {"mensaje": "Artista actualizado"}
    raise HTTPException(status_code=404, detail="Artista no encontrado")

@app.delete("/api/artistas/{nombre}")
async def delete_artista(nombre: str):
    global artistas_db
    artistas_db = [a for a in artistas_db if a['nombre'].lower() != nombre.lower()]
    save_data(ARTISTAS_FILE, artistas_db)
    return {"mensaje": f"Artista '{nombre}' eliminado (si existía)"}

@app.get("/api/canciones", response_model=list[Cancion])
async def get_canciones():
    return canciones_db

@app.post("/api/canciones")
async def add_cancion(cancion: Cancion):
    if any(c['titulo'].lower() == cancion.titulo.lower() for c in canciones_db):
        raise HTTPException(status_code=400, detail="Canción ya existe")
    canciones_db.append(cancion.dict())
    save_data(CANCIONES_FILE, canciones_db)
    return {"mensaje": "Canción agregada"}

@app.put("/api/canciones/{titulo}")
async def update_cancion(titulo: str, cancion: Cancion):
    for idx, c in enumerate(canciones_db):
        if c['titulo'].lower() == titulo.lower():
            canciones_db[idx] = cancion.dict()
            save_data(CANCIONES_FILE, canciones_db)
            return {"mensaje": "Canción actualizada"}
    raise HTTPException(status_code=404, detail="Canción no encontrada")

@app.delete("/api/canciones/{titulo}")
async def delete_cancion(titulo: str):
    global canciones_db
    canciones_db = [c for c in canciones_db if c['titulo'].lower() != titulo.lower()]
    save_data(CANCIONES_FILE, canciones_db)
    return {"mensaje": f"Canción '{titulo}' eliminada (si existía)"}
