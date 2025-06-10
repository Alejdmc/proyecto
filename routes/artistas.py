from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import ArtistaDB, ArtistaResponse
from utils.connection_db import get_session

router = APIRouter(prefix="/api/artistas_db", tags=["artistas"])

@router.post("/", response_model=ArtistaResponse)
async def crear_artista(
    nombre: str = Form(...),
    pais: str = Form(...),
    genero_principal: str = Form(...),
    activo: str = Form("false"),
    imagen: UploadFile = File(None),
    session: AsyncSession = Depends(get_session)
):
    activo_bool = activo.lower() == "true"
    imagen_bytes = None
    if imagen and imagen.filename:
        imagen_bytes = await imagen.read()
        print("Tamaño de la imagen subida (artista):", len(imagen_bytes))
    else:
        print("No se recibió imagen para artista")
    artista = ArtistaDB(
        nombre=nombre,
        pais=pais,
        genero_principal=genero_principal,
        activo=activo_bool,
        imagen_bytes=imagen_bytes
    )
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return {
        **artista.dict(),
        "tiene_imagen": bool(artista.imagen_bytes)
    }

@router.get("/", response_model=List[ArtistaResponse])
async def get_artistas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ArtistaDB).where(ArtistaDB.eliminado == False))
    artistas = result.scalars().all()
    return [
        {**a.dict(), "tiene_imagen": bool(a.imagen_bytes)} for a in artistas
    ]

@router.get("/{artista_id}", response_model=ArtistaResponse)
async def get_artista_por_id(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return {
        **artista.dict(),
        "tiene_imagen": bool(artista.imagen_bytes)
    }

@router.get("/{artista_id}/imagen")
async def obtener_imagen_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrada")
    if artista.imagen_bytes:
        return Response(content=artista.imagen_bytes, media_type="image/jpeg")
    return Response(status_code=204)

@router.put("/{artista_id}", response_model=ArtistaResponse)
async def put_artista(
    artista_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    genero_principal: str = Form(...),
    activo: str = Form("false"),
    imagen: UploadFile = File(None),
    session: AsyncSession = Depends(get_session)
):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    artista.nombre = nombre
    artista.pais = pais
    artista.genero_principal = genero_principal
    artista.activo = activo.lower() == "true"
    if imagen and imagen.filename:
        artista.imagen_bytes = await imagen.read()
    await session.commit()
    await session.refresh(artista)
    return {
        **artista.dict(),
        "tiene_imagen": bool(artista.imagen_bytes)
    }

@router.patch("/{artista_id}", response_model=ArtistaResponse)
async def patch_artista(
    artista_id: int,
    data: dict = None,
    session: AsyncSession = Depends(get_session)
):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    if data:
        for key, value in data.items():
            if hasattr(artista, key) and key not in ("id", "imagen_bytes"):
                setattr(artista, key, value)
    await session.commit()
    await session.refresh(artista)
    return {
        **artista.dict(),
        "tiene_imagen": bool(artista.imagen_bytes)
    }

@router.delete("/{artista_id}")
async def delete_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    artista.eliminado = True
    await session.commit()
    return {"ok": True}