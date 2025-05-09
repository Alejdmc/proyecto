from pydantic import BaseModel

class Cancion(BaseModel):
    titulo: str
    genero: str
    duracion: float
    artista: str
    explicita: bool
    eliminado: bool = False

class Artista(BaseModel):
    nombre: str
    pais: str
    activo: bool
    genero_principal: str
    eliminado: bool = False
#