from sqlmodel import SQLModel, Field, Column, LargeBinary
from typing import Optional

class ArtistaDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool = Field(default=True)
    imagen_bytes: Optional[bytes] = Field(sa_column=Column(LargeBinary), default=None, repr=False)
    eliminado: bool = Field(default=False)

class CancionDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool = Field(default=False)
    imagen_bytes: Optional[bytes] = Field(sa_column=Column(LargeBinary), default=None, repr=False)
    eliminado: bool = Field(default=False)

class ArtistaResponse(SQLModel):
    id: int
    nombre: str
    pais: str
    genero_principal: str
    activo: bool
    eliminado: bool

class CancionResponse(SQLModel):
    id: int
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool
    eliminado: bool