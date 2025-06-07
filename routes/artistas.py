from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import ArtistaDB
from utils.connection_db import get_session

ruta_artistas = APIRouter(prefix="/api/artistas_db", tags=["artistas"])

@ruta_artistas.post("/")
async def crear_artista(artista: ArtistaDB, session: AsyncSession = Depends(get_session)):
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista

@ruta_artistas.get("/")
async def obtener_artistas(
    pais: str = Query(None, description="Filtrar por país"),
    solo_activos: bool = Query(False, description="Mostrar solo los no eliminados"),
    session: AsyncSession = Depends(get_session)
):

    if solo_activos:
        query = select(ArtistaDB).where(ArtistaDB.eliminado == False)
    else:
        query = select(ArtistaDB)
    result = await session.execute(query)
    artistas = result.scalars().all()
    if pais:
        pais = pais.strip().lower()
        artistas = [
            artista for artista in artistas
            if artista.pais and artista.pais.strip().lower() == pais
        ]
    return artistas

@ruta_artistas.get("/{id}")
async def obtener_artista(id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@ruta_artistas.put("/{id}")
async def actualizar_total(id: int, artista: ArtistaDB, session: AsyncSession = Depends(get_session)):
    db_item = await session.get(ArtistaDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    artista_data = artista.dict(exclude_unset=True)
    for key, value in artista_data.items():
        if key != "id":
            setattr(db_item, key, value)
    await session.commit()
    await session.refresh(db_item)
    return db_item

@ruta_artistas.patch("/{id}")
async def actualizar_parcial(id: int, updates: dict, session: AsyncSession = Depends(get_session)):
    db_item = await session.get(ArtistaDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    for key, value in updates.items():
        if key != "id":
            setattr(db_item, key, value)
    await session.commit()
    await session.refresh(db_item)
    return db_item

@ruta_artistas.delete("/{id}")
async def eliminar_logico(id: int, session: AsyncSession = Depends(get_session)):
    db_item = await session.get(ArtistaDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    db_item.eliminado = True
    await session.commit()
    await session.refresh(db_item)
    return {"mensaje": "Artista marcado como eliminado"}