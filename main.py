"""
main.py - Punto de entrada de la API Semiverd con FastAPI y Frontend unificado
Proyecto: Semiverd MVP - Las Cuatro Semillas Verdes de Barrancabermeja
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from models.database import engine
from models import models
from controllers import auth_controller, missions_controller, users_controller, tips_controller

# Cargar variables de entorno
load_dotenv()

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
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

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


# Endpoints de API Info y Salud
@app.get("/api-info", tags=["Raíz"])
def raiz():
    """Endpoint de bienvenida de la API Semiverd"""
    return {
        "mensaje": "🌿 Bienvenido a la API de Semiverd",
        "descripcion": "Las Cuatro Semillas Verdes de Barrancabermeja",
        "version": "1.0.0",
        "docs": "/docs",
        "estado": "activo"
    }


@app.get("/salud", tags=["Raíz"])
def verificar_salud():
    """Health check del servidor"""
    return {"estado": "saludable", "servicio": "semiverd-api"}


# Montar carpeta de fotos de personajes
app.mount("/pictures", StaticFiles(directory="views/pictures"), name="pictures")

# Montar archivos estáticos para el frontend (servido en la raíz)
app.mount("/", StaticFiles(directory="views/web", html=True), name="web")


# Punto de entrada para desarrollo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
