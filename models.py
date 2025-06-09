from typing import Optional
from sqlmodel import SQLModel, Field

class ArtistaDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool
    imagen_url: str = None
    eliminado: bool = Field(default=False)

class CancionDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool = Field(default=False)
    imagen_url: str = None
    eliminado: bool = Field(default=False)