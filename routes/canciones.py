from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import CancionDB, CancionResponse
from utils.connection_db import get_session

router = APIRouter(prefix="/api/canciones_db", tags=["canciones"])

# 1. ENDPOINT FIJO "all" ANTES DEL DINÁMICO
@router.get("/all")
async def get_all_canciones(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CancionDB))
    return result.scalars().all()

@router.post("/", response_model=CancionResponse)
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

@router.get("/", response_model=List[CancionResponse])
async def get_canciones(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CancionDB).where(CancionDB.eliminado == False))
    return result.scalars().all()

@router.get("/{cancion_id}", response_model=CancionResponse)
async def get_cancion_por_id(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion or cancion.eliminado:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

@router.get("/{cancion_id}/imagen")
async def obtener_imagen_cancion(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(CancionDB, cancion_id)
    if not cancion or not cancion.imagen_bytes:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return Response(content=cancion.imagen_bytes, media_type="image/jpeg")

@router.put("/{cancion_id}", response_model=CancionResponse)
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
        cancion.imagen_bytes = await imagen.read()
    await session.commit()
    await session.refresh(cancion)
    return cancion

@router.patch("/{cancion_id}", response_model=CancionResponse)
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
            if hasattr(cancion, key) and key not in ("id", "imagen_bytes"):
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
