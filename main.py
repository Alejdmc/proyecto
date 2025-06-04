import os

from spotify_client import spotify_search

if os.getenv("RENDER") is None:
    from dotenv import load_dotenv
    load_dotenv()

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.connection_db import init_db, get_session
from models import ArtistaDB, CancionDB
from routes.artistas import ruta_artistas
from routes.canciones import ruta_canciones
import httpx
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(ruta_artistas)
app.include_router(ruta_canciones)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

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

# Spotify integration
async def obtener_token_spotify():
    manual_token = os.getenv("SPOTIFY_MANUAL_TOKEN")
    if manual_token:
        print("➡ Usando token manual")
        return manual_token

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Faltan SPOTIFY_CLIENT_ID o SPOTIFY_CLIENT_SECRET en configuración")

    print("➡ Usando token automático")
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {credentials}"}
    data = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient() as client:
        response = await client.post("https://accounts.spotify.com/api/token", data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error obteniendo token Spotify: {response.text}")

    json_response = response.json()
    if "access_token" not in json_response:
        raise HTTPException(status_code=500, detail="Respuesta de Spotify no contiene access_token")

    return json_response["access_token"]

@app.get("/api/spotify/artistas")
async def buscar_artistas_spotify(nombre: str):
    token = await obtener_token_spotify()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.spotify.com/v1/search", params={"q": nombre, "type": "artist"}, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error consultando Spotify: {response.text}")
    items = response.json().get("artists", {}).get("items", [])
    return [{"nombre": a["name"], "generos": a.get("genres", []), "popularidad": a.get("popularity")} for a in items]

@app.get("/api/spotify/canciones")
async def buscar_canciones_spotify(titulo: str):
    token = await obtener_token_spotify()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.spotify.com/v1/search", params={"q": titulo, "type": "track"}, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error consultando Spotify: {response.text}")
    items = response.json().get("tracks", {}).get("items", [])
    return [{"nombre": c["name"], "artista": ", ".join(a["name"] for a in c.get("artists", [])), "album": c.get("album", {}).get("name")} for c in items]
@app.get("/api/spotify/canciones")
async def spotify_canciones(q: str):
    data = await spotify_search(q, "track")
    return data

# CRUD endpoints locales
@app.post("/api/artistas_db")
async def crear_artista(artista: ArtistaDB, session: AsyncSession = Depends(get_session)):
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista

@app.get("/api/artistas_db")
async def obtener_artistas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ArtistaDB))
    return result.scalars().all()

@app.get("/api/artistas_db/{artista_id}")
async def obtener_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@app.delete("/api/artistas_db/{artista_id}")
async def eliminar_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    await session.delete(artista)
    await session.commit()
    return {"mensaje": "Artista eliminado"}

@app.post("/api/canciones_db")
async def crear_cancion(cancion: CancionDB, session: AsyncSession = Depends(get_session)):
    session.add(cancion)
    await session.commit()
    await session.refresh(cancion)
    return cancion

@app.get("/api/canciones_db")
async def obtener_canciones(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CancionDB))
    return result.scalars().all()

@app.get("/api/canciones_db/{cancion_id}")
async def obtener_cancion(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

@app.delete("/api/canciones_db/{cancion_id}")
async def eliminar_cancion(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    await session.delete(cancion)
    await session.commit()
    return {"mensaje": "Canción eliminada"}
@app.put("/api/canciones_db/{cancion_id}")
async def actualizar_cancion(cancion_id: int, nueva: CancionDB, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")

    cancion.titulo = nueva.titulo
    cancion.genero = nueva.genero
    cancion.duracion = nueva.duracion
    cancion.artista = nueva.artista
    cancion.explicita = nueva.explicita
    cancion.eliminado = nueva.eliminado
    cancion.imagen_url = nueva.imagen_url  # si usas este campo también

    await session.commit()
    await session.refresh(cancion)
    return cancion
