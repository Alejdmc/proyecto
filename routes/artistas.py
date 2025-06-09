from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from models import ArtistaDB
from utils.connection_db import get_session

router = APIRouter(prefix="/api/artistas_db", tags=["artistas"])

@router.post("/")
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
    return artista

@router.get("/")
async def get_artistas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ArtistaDB).where(ArtistaDB.eliminado == False))
    return result.scalars().all()

@router.get("/{artista_id}")
async def get_artista_por_id(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@router.get("/{artista_id}/imagen")
async def obtener_imagen_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or not artista.imagen_bytes:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return Response(content=artista.imagen_bytes, media_type="image/jpeg")  # Cambia a image/png si corresponde

@router.put("/{artista_id}")
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
    return artista

@router.patch("/{artista_id}")
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
            if hasattr(artista, key) and key != "id":
                setattr(artista, key, value)
    await session.commit()
    await session.refresh(artista)
    return artista

@router.delete("/{artista_id}")
async def delete_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    artista.eliminado = True
    await session.commit()
    return {"ok": True}