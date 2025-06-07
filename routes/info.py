from fastapi import APIRouter

ruta_info = APIRouter(prefix="/info", tags=["informacion"])

@ruta_info.get("/desarrollador")
def info_desarrollador():
    return {
        "nombre": "Daniel Alejandro Monroy Castellanos",
        "codigo": "67001386",
        "correo": "damonroy86@ucatolica.edu.co"
    }

@ruta_info.get("/planeacion")
def info_planeacion():
    return {
        "casos_uso": [
            "Registrar artistas locales y desde Spotify",
            "Registrar canciones locales y consultar desde Spotify",
            "Consultar artistas y canciones por distintos filtros",
            "Filtrar artistas por país y canciones por género",
            "Actualizar información de artistas y canciones (PUT y PATCH)",
            "Eliminación lógica de artistas y canciones",
            "Visualización de eliminados y activos",
            "Carga de imágenes para canciones"
        ],
        "objetivos": "Desarrollar una aplicación web con FastAPI que gestione artistas y canciones, usando datos locales y de Spotify, permitiendo CRUD completo y análisis simple.",
        "fuente_datos": "Datos generados por usuario y almacenados en PostgreSQL remoto; API pública de Spotify para consultas externas."
    }

@ruta_info.get("/diseno")
def info_diseno():
    return {
        "diagrama_clases": (
            "Modelos principales:\n"
            " - ArtistaDB: id, nombre, pais, genero_principal, activo, eliminado, imagen_url\n"
            " - CancionDB: id, titulo, genero, duracion, artista, explicita, eliminado, imagen_url"
        ),
        "mapa_endpoints": [
            # ARTISTAS
            "GET    /api/artistas_db/                  # Listar todos los artistas (incluye eliminados si se desea)",
            "POST   /api/artistas_db/                  # Crear artista",
            "GET    /api/artistas_db/{id}              # Obtener artista por ID (solo no eliminado)",
            "GET    /api/artistas_db?pais={pais}       # Filtrar artistas por país",
            "PUT    /api/artistas_db/{id}              # Actualizar artista (total)",
            "PATCH  /api/artistas_db/{id}              # Actualizar artista (parcial)",
            "DELETE /api/artistas_db/{id}              # Eliminación lógica de artista",

            # CANCIONES
            "GET    /api/canciones_db/                 # Listar todas las canciones (activos y eliminados)",
            "POST   /api/canciones_db/                 # Crear canción",
            "GET    /api/canciones_db/{id}             # Obtener canción por ID (solo no eliminada)",
            "GET    /api/canciones_db/genero/{genero}  # Filtrar canciones por género",
            "PUT    /api/canciones_db/{id}             # Actualizar canción (total)",
            "PATCH  /api/canciones_db/{id}             # Actualizar canción (parcial)",
            "DELETE /api/canciones_db/{id}             # Eliminación lógica de canción",
            "POST   /api/canciones_db/con-imagen       # Crear canción con imagen",

            # SPOTIFY
            "GET    /api/spotify/artistas?nombre={nombre}   # Buscar artistas en Spotify",
            "GET    /api/spotify/canciones?titulo={titulo}  # Buscar canciones en Spotify",

            # INFO
            "GET    /info/desarrollador                # Información del desarrollador",
            "GET    /info/planeacion                   # Planeación del proyecto",
            "GET    /info/diseno                       # Diseño y mapa de endpoints",
            "GET    /info/objetivo                     # Objetivo general del proyecto"
        ],
        "mockups": (
            "Wireframes y formularios HTML para agregar, editar y consultar artistas/canciones, "
            "tablas para visualizar registros locales y consultas externas (Spotify)."
        )
    }

@ruta_info.get("/objetivo")
def objetivo_proyecto():
    return {
        "objetivo_general": (
            "Desarrollar un servicio web con FastAPI que permita registrar, consultar y analizar información "
            "sobre artistas y canciones contemporáneas, evidenciando patrones de duración, estilo y contenido explícito, "
            "para estudiar cómo han cambiado las preferencias musicales con las nuevas generaciones."
        )
    }