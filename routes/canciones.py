from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models import CancionDB
from utils.connection_db import get_session
import  os

router = APIRouter(prefix="/api/canciones_db", tags=["canciones"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def crear_cancion(
    titulo: str = Form(...),
    genero: str = Form(...),
    duracion: float = Form(...),
    artista: str = Form(...),
    explicita: str = Form("false"),
    imagen: UploadFile = File(None),
    session: AsyncSession = Depends(get_session)
):
    explicita_bool = explicita.lower() == "true"
    imagen_bytes = None
    if imagen and imagen.filename:
        imagen_bytes = await imagen.read()
    cancion = CancionDB(
        titulo=titulo,
        genero=genero,
        duracion=duracion,
        artista=artista,
        explicita=explicita_bool,
        imagen_bytes=imagen_bytes
    )
    session.add(cancion)
    await session.commit()
    await session.refresh(cancion)
    return cancion

@router.get("/{cancion_id}/imagen")
async def obtener_imagen_cancion(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion or not cancion.imagen_bytes:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return Response(content=cancion.imagen_bytes, media_type="image/jpeg")  # Cambia a image/png si corresponde

@router.put("/{cancion_id}")
async def put_cancion(
    cancion_id: int,
    titulo: str = Form(...),
    genero: str = Form(...),
    duracion: float = Form(...),
    artista: str = Form(...),
    explicita: str = Form("false"),
    imagen: UploadFile = File(None),
    session: AsyncSession = Depends(get_session)
):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion or cancion.eliminado:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    cancion.titulo = titulo
    cancion.genero = genero
    cancion.duracion = duracion
    cancion.artista = artista
    cancion.explicita = explicita.lower() == "true"
    if imagen and imagen.filename:
        filepath = os.path.join(UPLOAD_DIR, imagen.filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await imagen.read())
        cancion.imagen_url = f"/static/uploads/{imagen.filename}"
    await session.commit()
    await session.refresh(cancion)
    return cancion

@router.patch("/{cancion_id}")
async def patch_cancion(
    cancion_id: int,
    data: dict = None,
    session: AsyncSession = Depends(get_session)
):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion or cancion.eliminado:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    if data:
        for key, value in data.items():
            if hasattr(cancion, key) and key != "id":
                setattr(cancion, key, value)
    await session.commit()
    await session.refresh(cancion)
    return cancion

@router.delete("/{cancion_id}")
async def delete_cancion(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion or cancion.eliminado:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    cancion.eliminado = True
    await session.commit()
    return {"ok": True}