from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from models import CancionDB
from utils.connection_db import get_session
from fastapi import File, UploadFile, Form
import shutil
import os


UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ruta_canciones = APIRouter(prefix="/api/canciones_db", tags=["Canciones"])

@ruta_canciones.get("/")
async def obtener_todos(session=Depends(get_session)):
    result = await session.exec(select(CancionDB).where(CancionDB.eliminado == False))
    return result.all()

@ruta_canciones.get("/{id}")
async def obtener_por_id(id: int, session=Depends(get_session)):
    cancion = await session.get(CancionDB, id)
    if not cancion or cancion.eliminado:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

@ruta_canciones.get("/genero/{genero}")
async def obtener_por_genero(genero: str, session=Depends(get_session)):
    result = await session.exec(select(CancionDB).where(CancionDB.genero == genero, CancionDB.eliminado == False))
    return result.all()

@ruta_canciones.post("/")
async def crear_cancion(cancion: CancionDB, session=Depends(get_session)):
    session.add(cancion)
    await session.commit()
    await session.refresh(cancion)
    return cancion

@ruta_canciones.put("/{id}")
async def actualizar_total(id: int, cancion: CancionDB, session=Depends(get_session)):
    db_item = await session.get(CancionDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    for key, value in cancion.dict().items():
        setattr(db_item, key, value)
    await session.commit()
    return db_item

@ruta_canciones.patch("/{id}")
async def actualizar_parcial(id: int, updates: dict, session=Depends(get_session)):
    db_item = await session.get(CancionDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    for key, value in updates.items():
        setattr(db_item, key, value)
    await session.commit()
    return db_item

@ruta_canciones.delete("/{id}")
async def eliminar_logico(id: int, session=Depends(get_session)):
    db_item = await session.get(CancionDB, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    db_item.eliminado = True
    await session.commit()
    return {"mensaje": "Canción marcada como eliminada"}

@ruta_canciones.post("/con-imagen")
async def crear_cancion_con_imagen(
    titulo: str = Form(...),
    genero: str = Form(...),
    duracion: float = Form(...),
    artista: str = Form(...),
    explicita: bool = Form(...),
    imagen: UploadFile = File(...),
    session=Depends(get_session)
):
    file_location = f"{UPLOAD_DIR}/{imagen.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(imagen.file, f)

    cancion = CancionDB(
        titulo=titulo,
        genero=genero,
        duracion=duracion,
        artista=artista,
        explicita=explicita,
        eliminado=False,
        imagen_url=file_location
    )
    session.add(cancion)
    await session.commit()
    await session.refresh(cancion)
    return cancion

