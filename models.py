from typing import Optional
from sqlmodel import SQLModel, Field, Column, LargeBinary

class ArtistaDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool = Field(default=True)
    imagen_bytes: bytes = Field(sa_column=Column(LargeBinary), default=None)
    eliminado: bool = Field(default=False)

class CancionDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool = Field(default=False)
    imagen_bytes: bytes = Field(sa_column=Column(LargeBinary), default=None)
    eliminado: bool = Field(default=False)