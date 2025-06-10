from sqlmodel import SQLModel, Field
from typing import Optional

class ArtistaDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool = False
    eliminado: bool = False
    imagen_url: Optional[str] = None
    imagen_bytes: Optional[bytes] = None

class ArtistaResponse(SQLModel):
    id: int
    nombre: str
    pais: str
    genero_principal: str
    activo: bool
    eliminado: bool
    tiene_imagen: bool = False

class CancionDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool = False
    eliminado: bool = False
    imagen_url: Optional[str] = None
    imagen_bytes: Optional[bytes] = None

class CancionResponse(SQLModel):
    id: int
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool
    eliminado: bool
    tiene_imagen: bool = False