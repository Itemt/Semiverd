"""
main.py - Punto de entrada de la API Semiverd con FastAPI y Frontend unificado
Proyecto: Semiverd MVP - Las Cuatro Semillas Verdes de Barrancabermeja
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from models.database import engine
from models import models
from controllers import auth_controller, missions_controller, users_controller, tips_controller

# Cargar variables de entorno
load_dotenv()

# Determinar el directorio base (Soporte para PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorios estáticos
PICTURES_DIR = os.path.join(BASE_DIR, "views", "pictures")
WEB_DIR = os.path.join(BASE_DIR, "views", "web")
FAVICON_PATH = os.path.join(WEB_DIR, "favicon.png")

# Crear todas las tablas al iniciar (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🌱 Semiverd API",
    description=(
        "API REST del MVP de Semiverd - La app gamificada de las Cuatro Semillas Verdes. "
        "Aprende sobre el cuidado del medio ambiente completando misiones ecológicas "
        "en Barrancabermeja. ¡Menos cemento, más oxígeno!"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware CORS (permite llamadas desde el frontend)
origins = ["*"] # Permitir todo para el ejecutable local

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todos los routers de la API
app.include_router(auth_controller.router)
app.include_router(missions_controller.router)
app.include_router(users_controller.router)
app.include_router(tips_controller.router)


@app.get("/api-info", tags=["Raíz"])
def raiz():
    return {
        "mensaje": "🌿 Bienvenido a la API de Semiverd",
        "descripcion": "Las Cuatro Semillas Verdes de Barrancabermeja",
        "version": "1.0.0",
        "docs": "/docs",
        "estado": "activo"
    }

@app.get("/salud", tags=["Raíz"])
def verificar_salud():
    return {"estado": "saludable", "servicio": "semiverd-api"}

@app.get("/favicon.ico", include_in_schema=False)
def obtener_favicon():
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH)
    return {"mensaje": "No favicon"}

# Montar carpetas (si existen)
if os.path.exists(PICTURES_DIR):
    app.mount("/pictures", StaticFiles(directory=PICTURES_DIR), name="pictures")

if os.path.exists(WEB_DIR):
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time
    
    # Abre el navegador automáticamente cuando inicia el ejecutable
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000")
        
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
