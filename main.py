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
    if sys.platform == 'darwin' and ".app/Contents/MacOS" in executable_dir:
        # En macOS dentro del .app bundle, subir niveles para encontrar el .env al lado del .app
        app_path = executable_dir.split(".app/Contents/MacOS")[0] + ".app"
        executable_dir = os.path.dirname(app_path)
    # En Windows: executable_dir ya apunta a la carpeta del .exe, no hace falta ajuste
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

    from models.database import engine, SessionLocal
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
    
    # Auto-semillar la base de datos si está vacía
    db = SessionLocal()
    try:
        from seed import cargar_misiones, cargar_tips, cargar_recompensas
        # Solo cargar si no hay misiones registradas
        if db.query(models.Mision).count() == 0:
            print("🌱 Base de datos vacía detectada. Iniciando auto-semillado...")
            cargar_misiones(db)
            cargar_tips(db)
            cargar_recompensas(db)
            print("🌿 Auto-semillado completado con éxito.")
    except Exception as seed_err:
        print(f"⚠️ Advertencia al auto-semillar la base de datos: {seed_err}")
        db.rollback()
    finally:
        db.close()
except Exception as e:
    print("\n❌ ERROR AL INICIALIZAR LA BASE DE DATOS:")
    traceback.print_exc()
    print("\nPor favor, verifica la conexión y los permisos de la base de datos.")
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
    import threading
    import time

    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8000
    SERVER_URL  = f"http://{SERVER_HOST}:{SERVER_PORT}"

    def iniciar_servidor():
        """Arranca uvicorn en un hilo demonio (background)."""
        uvicorn.run(
            app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            log_level="info",
        )

    # Lanzar el servidor en segundo plano
    hilo_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
    hilo_servidor.start()

    # Intentar usar pywebview para una ventana de escritorio nativa
    try:
        import webview

        def esperar_servidor_y_abrir(window):
            """Espera a que el servidor esté listo y luego carga la URL."""
            intentos = 0
            import urllib.request
            while intentos < 30:
                try:
                    urllib.request.urlopen(f"{SERVER_URL}/salud", timeout=1)
                    window.load_url(SERVER_URL)
                    return
                except Exception:
                    intentos += 1
                    time.sleep(0.5)
            # Fallback: cargar de todos modos si no respondió
            window.load_url(SERVER_URL)

        # Crear ventana nativa (sin chrome de browser, sin barra de dirección)
        ventana = webview.create_window(
            title="Semiverd - Las Cuatro Semillas Verdes",
            url="about:blank",          # Cargamos la URL real al confirmar que el servidor arrancó
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True,
            text_select=False,          # Evita selección de texto como en browser
        )

        # Cargar la URL real una vez que el servidor esté listo
        threading.Thread(
            target=esperar_servidor_y_abrir,
            args=(ventana,),
            daemon=True
        ).start()

        # Arrancar pywebview (bloquea hasta que el usuario cierra la ventana)
        webview.start(debug=False)

    except ImportError:
        # Fallback si pywebview no está disponible: abrir en el browser del sistema
        import webbrowser
        print("⚠️  pywebview no está instalado. Abriendo en el navegador del sistema...")
        time.sleep(1.5)
        webbrowser.open(SERVER_URL)
        # Mantener el proceso vivo mientras el servidor corre
        hilo_servidor.join()

