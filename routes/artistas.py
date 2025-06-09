from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from models import ArtistaDB
from utils.connection_db import get_session
import os

router = APIRouter(prefix="/api/artistas_db", tags=["artistas"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def crear_artista(
    nombre: str = Form(...),
    pais: str = Form(...),
    genero_principal: str = Form(...),
    activo: str = Form("true"),
    imagen: UploadFile = File(None),
    session: AsyncSession = Depends(get_session)
):
    # Convierte string a boolean real
    activo_bool = activo.lower() == "true"
    imagen_url = None
    if imagen and imagen.filename:
        filepath = os.path.join(UPLOAD_DIR, imagen.filename)
        # Si quieres evitar sobrescribir archivos, puedes agregar un sufijo único aquí
        with open(filepath, "wb") as buffer:
            buffer.write(await imagen.read())
        imagen_url = f"/static/uploads/{imagen.filename}"

    artista = ArtistaDB(
        nombre=nombre,
        pais=pais,
        genero_principal=genero_principal,
        activo=activo_bool,
        imagen_url=imagen_url
    )
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista

@router.get("/")
async def get_artistas(pais: str = None, session: AsyncSession = Depends(get_session)):
    query = select(ArtistaDB).where(ArtistaDB.eliminado == False)
    if pais:
        query = query.where(ArtistaDB.pais == pais)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{artista_id}")
async def get_artista(artista_id: int, session: AsyncSession = Depends(get_session)):
    artista = await session.get(ArtistaDB, artista_id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@router.put("/{artista_id}")
async def put_artista(
    artista_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    genero_principal: str = Form(...),
    activo: str = Form("true"),
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
        filepath = os.path.join(UPLOAD_DIR, imagen.filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await imagen.read())
        artista.imagen_url = f"/static/uploads/{imagen.filename}"
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