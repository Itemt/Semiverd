"""
main.py - Punto de entrada de la API Semiverd con FastAPI y Frontend unificado
Proyecto: Semiverd MVP - Las Cuatro Semillas Verdes de Barrancabermeja
Versión: 1.7.0
"""

import os
import sys
import webbrowser
from dotenv import load_dotenv

# 1. Cargar variables de entorno
load_dotenv()

# 2. Crear la app FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="🌱 Semiverd API",
    description="API REST del MVP de Semiverd - Las Cuatro Semillas Verdes de Barrancabermeja.",
    version="1.7.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Directorios y rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_DIR = os.path.join(BASE_DIR, "views", "pictures")
WEB_DIR      = os.path.join(BASE_DIR, "views", "web")
FAVICON_PATH = os.path.join(WEB_DIR, "favicon.png")

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_URL  = f"http://{SERVER_HOST}:{SERVER_PORT}"

# 4. Importar base de datos y controladores
from models.database import engine, SessionLocal
from models import models
from controllers import (
    auth_controller, missions_controller,
    users_controller, tips_controller
)

# Registrar rutas de los controladores
app.include_router(auth_controller.router)
app.include_router(missions_controller.router)
app.include_router(users_controller.router)
app.include_router(tips_controller.router)

# 5. Endpoints base
@app.get("/salud", tags=["Raíz"])
def verificar_salud():
    return {"estado": "saludable", "servicio": "semiverd-api"}

@app.get("/api-info", tags=["Raíz"])
def raiz():
    return {"mensaje": "🌿 Bienvenido a la API de Semiverd", "version": "1.7.0"}

@app.get("/favicon.ico", include_in_schema=False)
def obtener_favicon():
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH)
    return {}

# Montar archivos estáticos
if os.path.exists(PICTURES_DIR):
    app.mount("/pictures", StaticFiles(directory=PICTURES_DIR), name="pictures")
if os.path.exists(WEB_DIR):
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")

# 6. Inicialización de la base de datos y auto-semillado en el startup
@app.on_event("startup")
def inicializar_base_datos():
    print("[Semiverd] Inicializando base de datos...")
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from seed import cargar_misiones, cargar_tips, cargar_recompensas
        if db.query(models.Mision).count() == 0:
            print("[Semiverd] Base vacía — auto-semillando...")
            cargar_misiones(db)
            cargar_tips(db)
            cargar_recompensas(db)
            print("[Semiverd] Auto-semillado completado.")
    except Exception as seed_err:
        print(f"[Semiverd] ⚠️ Error al auto-semillar: {seed_err}")
        db.rollback()
    finally:
        db.close()

# 7. Ejecutar servidor
if __name__ == "__main__":
    import uvicorn
    
    print(f"[Semiverd] Abriendo navegador en {SERVER_URL}…")
    webbrowser.open(SERVER_URL)
    
    print(f"[Semiverd] Arrancando servidor en {SERVER_URL}…")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="warning")
