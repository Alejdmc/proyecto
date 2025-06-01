from sqlmodel import SQLModel, Field

class ArtistaDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    genero_principal: str
    activo: bool

class CancionDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool