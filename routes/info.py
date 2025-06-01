
from fastapi import APIRouter
ruta_info = APIRouter(prefix="/info", tags=["informacion"])

@ruta_info.get("/desarrollador")
def info_desarrollador():
    return {
        "nombre": "Daniel Pérez",
        "codigo": "123456789",
        "correo": "daniel.perez@correo.com"
    }

@ruta_info.get("/planeacion")
def info_planeacion():
    return {
        "casos_uso": [
            "Registrar artistas",
            "Registrar canciones",
            "Consultar artistas/canciones",
            "Filtrar por género o país",
            "Eliminar lógico (marcar eliminados)"
        ],
        "objetivos": "Desarrollar una plataforma estilo Spotify para gestionar artistas y canciones.",
        "fuente_datos": "Datos generados por usuario, almacenados en PostgreSQL remoto."
    }

@ruta_info.get("/diseno")
def info_diseno():
    return {
        "diagrama_clases": "Modelos: Artista (id, nombre, país, género, activo, eliminado, imagen), Cancion (id, titulo, genero, duracion, artista_id, explicita, eliminado)",
        "mapa_endpoints": [
            "/artistas",
            "/canciones",
            "/info/desarrollador",
            "/info/planeacion",
            "/info/diseno",
            "/info/objetivo"
        ],
        "mockups": "Wireframes de formularios HTML para agregar y consultar artistas/canciones"
    }

@ruta_info.get("/objetivo")
def objetivo_proyecto():
    return {
        "objetivo_general": "Crear una API funcional y una interfaz web para gestionar artistas y canciones, demostrando habilidades de desarrollo, base de datos y despliegue online."
    }