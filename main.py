from fastapi import FastAPI
from routes.artistas import ruta_artistas
from routes.canciones import ruta_canciones
from utils.connection_db import init_db
from routes.info import ruta_info
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(ruta_artistas)
app.include_router(ruta_canciones)
app.include_router(ruta_info)