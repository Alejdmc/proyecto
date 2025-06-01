from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models import Artista
from utils.connection_db import get_session
from fastapi import Path

ruta_artistas = APIRouter(prefix="/artistas", tags=["artistas"])

@ruta_artistas.post("/")
async def agregar_artista(artista: Artista, session: AsyncSession = Depends(get_session)):
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista

@ruta_artistas.get("/")
async def obtener_artistas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Artista).where(Artista.eliminado == False))
    return result.scalars().all()

@ruta_artistas.delete("/{artista_id}")
async def eliminar_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    artista.eliminado = True
    session.add(artista)
    await session.commit()
    return {"mensaje": "Artista eliminado (marcado como eliminado)"}
@ruta_artistas.patch("/{artista_id}")
async def modificar_parcial_artista(artista_id: int, datos: dict, session: AsyncSession = Depends(get_session)):
    artista = await session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    for key, value in datos.items():
        if hasattr(artista, key):
            setattr(artista, key, value)
    session.add(artista)
    await session.commit()
    return {"mensaje": "Artista modificado parcialmente"}

@ruta_artistas.get("/buscar/nombre/{nombre}")
async def buscar_artista_por_nombre(nombre: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Artista).where(Artista.nombre.ilike(f"%{nombre}%")))
    return result.scalars().all()

@ruta_artistas.get("/historial")
async def obtener_todos_artistas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Artista))
    return result.scalars().all()