from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from models import ArtistaDB
from utils.connection_db import get_session
from fastapi import File, UploadFile, Form
import shutil
import os

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ruta_artistas = APIRouter(prefix="/api/artistas_db", tags=["Artistas"])

@ruta_artistas.get("/")
async def obtener_todos(session=Depends(get_session)):
    result = await session.exec(select(ArtistaDB).where(ArtistaDB.eliminado == False))
    return result.all()

@ruta_artistas.get("/{id}")
async def obtener_por_id(id: int, session=Depends(get_session)):
    artista = await session.get(ArtistaDB, id)
    if not artista or artista.eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@ruta_artistas.get("/pais/{pais}")
async def obtener_por_pais(pais: str, session=Depends(get_session)):
    result = await session.exec(select(ArtistaDB).where(ArtistaDB.pais == pais, ArtistaDB.eliminado == False))
    return result.all()

@ruta_artistas.post("/")
async def crear_artista(artista: ArtistaDB, session=Depends(get_session)):
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista

@ruta_artistas.put("/{id}")
async def actualizar_total(id: int, artista: ArtistaDB, session=Depends(get_session)):
    db_item = await session.get(ArtistaDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    for key, value in artista.dict().items():
        setattr(db_item, key, value)
    await session.commit()
    return db_item

@ruta_artistas.patch("/{id}")
async def actualizar_parcial(id: int, updates: dict, session=Depends(get_session)):
    db_item = await session.get(ArtistaDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    for key, value in updates.items():
        setattr(db_item, key, value)
    await session.commit()
    return db_item

@ruta_artistas.delete("/{id}")
async def eliminar_logico(id: int, session=Depends(get_session)):
    db_item = await session.get(ArtistaDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    db_item.eliminado = True
    await session.commit()
    return {"mensaje": "Artista marcado como eliminado"}

@ruta_artistas.post("/con-imagen")
async def crear_artista_con_imagen(
    nombre: str = Form(...),
    pais: str = Form(...),
    genero_principal: str = Form(...),
    activo: bool = Form(...),
    imagen: UploadFile = File(...),
    session=Depends(get_session)
):
    file_location = f"{UPLOAD_DIR}/{imagen.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(imagen.file, f)

    artista = ArtistaDB(
        nombre=nombre,
        pais=pais,
        genero_principal=genero_principal,
        activo=activo,
        eliminado=False,
        imagen_url=file_location
    )
    session.add(artista)
    await session.commit()
    await session.refresh(artista)
    return artista