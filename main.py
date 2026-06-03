"""
main.py - Punto de entrada de la API Semiverd con FastAPI y Frontend unificado
Proyecto: Semiverd MVP - Las Cuatro Semillas Verdes de Barrancabermeja
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Cargar variables de entorno lo antes posible para configurar la app
if getattr(sys, 'frozen', False):
    # En producción (congelado), buscar el .env en la misma carpeta que el archivo ejecutable real
    executable_dir = os.path.dirname(sys.executable)
    if ".app/Contents/MacOS" in executable_dir:
        # En macOS dentro del .app bundle, subir niveles para encontrar el .env al lado del .app
        app_path = executable_dir.split(".app/Contents/MacOS")[0] + ".app"
        executable_dir = os.path.dirname(app_path)
    env_path = os.path.join(executable_dir, ".env")
    load_dotenv(env_path)
else:
    load_dotenv()

# Intentar importar dependencias crítcas y controladores
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    from models.database import engine
    from models import models
    from controllers import auth_controller, missions_controller, users_controller, tips_controller
except Exception as e:
    print("\n❌ ERROR CRÍTICO AL IMPORTAR DEPENDENCIAS O INICIALIZAR MÓDULOS:")
    traceback.print_exc()
    print("\nEste error suele ocurrir si faltan librerías o dependencias del sistema.")
    if getattr(sys, 'frozen', False):
        input("\nPresione Enter para salir...")
    sys.exit(1)

# Determinar el directorio base para activos estáticos (Soporte para PyInstaller)
if getattr(sys, 'frozen', False):
    # sys._MEIPASS contiene la carpeta temporal donde PyInstaller extrae los activos empaquetados
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorios estáticos
PICTURES_DIR = os.path.join(BASE_DIR, "views", "pictures")
WEB_DIR = os.path.join(BASE_DIR, "views", "web")
FAVICON_PATH = os.path.join(WEB_DIR, "favicon.png")

# Crear todas las tablas al iniciar (si no existen)
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print("\n❌ ERROR AL INICIALIZAR LA BASE DE DATOS:")
    traceback.print_exc()
    print("\nPor favor, verifica la configuración de tu archivo .env y la conexión a la base de datos.")
    if getattr(sys, 'frozen', False):
        input("\nPresione Enter para salir...")
    sys.exit(1)

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
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
