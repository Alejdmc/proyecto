from sqlmodel import SQLModel, Field
from typing import Optional

class Artista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool = True
    eliminado: bool = False
    imagen: Optional[str] = None

class Cancion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista_id: int
    explicita: bool = False
    eliminado: bool = False