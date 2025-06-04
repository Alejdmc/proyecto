from typing import Optional
from sqlmodel import SQLModel, Field

class ArtistaDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool = True
    eliminado: bool = False
    imagen_url: Optional[str] = None

class CancionDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool = False
    eliminado: bool = False
    imagen_url: Optional[str] = None