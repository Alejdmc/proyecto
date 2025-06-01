from fastapi import FastAPI
from routes.artistas import ruta_artistas
from routes.canciones import ruta_canciones
from utils.connection_db import init_db
from routes.info import ruta_info
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(ruta_artistas)
app.include_router(ruta_canciones)
app.include_router(ruta_info)