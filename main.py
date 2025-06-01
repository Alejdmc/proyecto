from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.connection_db import init_db, get_session
from models import ArtistaDB, CancionDB
from spotify_client import spotify_search

app = FastAPI(title="Proyecto Integrador API")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def on_startup():
    await init_db()

# HTML
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

# POSTGRES ENDPOINTS
@app.get("/api/artistas_db")
async def get_artistas_db(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(ArtistaDB))
    return result.all()

@app.post("/api/artistas_db")
async def add_artista_db(artista: ArtistaDB, session: AsyncSession = Depends(get_session)):
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista

@app.get("/api/canciones_db")
async def get_canciones_db(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(CancionDB))
    return result.all()

@app.post("/api/canciones_db")
async def add_cancion_db(cancion: CancionDB, session: AsyncSession = Depends(get_session)):
    session.add(cancion)
    await session.commit()
    await session.refresh(cancion)
    return cancion

# SPOTIFY ENDPOINTS
@app.get("/api/spotify/artistas")
async def spotify_artistas(q: str):
    data = await spotify_search(q, "artist")
    return data

@app.get("/api/spotify/canciones")
async def spotify_canciones(q: str):
    data = await spotify_search(q, "track")
    return data