from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models import Cancion
from utils.connection_db import get_session

ruta_canciones = APIRouter(prefix="/canciones", tags=["canciones"])

@ruta_canciones.post("/")
async def agregar_cancion(cancion: Cancion, session: AsyncSession = Depends(get_session)):
    session.add(cancion)
    await session.commit()
    await session.refresh(cancion)
    return cancion

@ruta_canciones.get("/")
async def obtener_canciones(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Cancion).where(Cancion.eliminado == False))
    return result.scalars().all()

@ruta_canciones.delete("/{cancion_id}")
async def eliminar_cancion(cancion_id: int, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    cancion.eliminado = True
    session.add(cancion)
    await session.commit()
    return {"mensaje": "Canción eliminada (marcada como eliminada)"}
@ruta_canciones.patch("/{cancion_id}")
async def modificar_parcial_cancion(cancion_id: int, datos: dict, session: AsyncSession = Depends(get_session)):
    cancion = await session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    for key, value in datos.items():
        if hasattr(cancion, key):
            setattr(cancion, key, value)
    session.add(cancion)
    await session.commit()
    return {"mensaje": "Canción modificada parcialmente"}

@ruta_canciones.get("/buscar/titulo/{titulo}")
async def buscar_cancion_por_titulo(titulo: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Cancion).where(Cancion.titulo.ilike(f"%{titulo}%")))
    return result.scalars().all()

@ruta_canciones.get("/historial")
async def obtener_todas_canciones(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Cancion))
    return result.scalars().all()