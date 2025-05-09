from fastapi import FastAPI
from routes.canciones import ruta_canciones
from routes.artistas import ruta_artistas

app = FastAPI()

app.include_router(ruta_canciones)
app.include_router(ruta_artistas)
