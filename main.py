"""
main.py - Punto de entrada de la API Semiverd con FastAPI y Frontend unificado
Proyecto: Semiverd MVP - Las Cuatro Semillas Verdes de Barrancabermeja
"""

import os
import sys
import traceback
import threading
import time
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# 1. Cargar .env lo antes posible
# ─────────────────────────────────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    executable_dir = os.path.dirname(sys.executable)
    if sys.platform == 'darwin' and ".app/Contents/MacOS" in executable_dir:
        app_path = executable_dir.split(".app/Contents/MacOS")[0] + ".app"
        executable_dir = os.path.dirname(app_path)
    env_path = os.path.join(executable_dir, ".env")
    load_dotenv(env_path)
else:
    load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Importar dependencias críticas
# ─────────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────────
# 3. Directorios base
# ─────────────────────────────────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PICTURES_DIR = os.path.join(BASE_DIR, "views", "pictures")
WEB_DIR      = os.path.join(BASE_DIR, "views", "web")
FAVICON_PATH = os.path.join(WEB_DIR, "favicon.png")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Inicializar base de datos y auto-semillar si está vacía
# ─────────────────────────────────────────────────────────────────────────────
try:
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        from seed import cargar_misiones, cargar_tips, cargar_recompensas
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

# ─────────────────────────────────────────────────────────────────────────────
# 5. Crear aplicación FastAPI
# ─────────────────────────────────────────────────────────────────────────────
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if os.path.exists(PICTURES_DIR):
    app.mount("/pictures", StaticFiles(directory=PICTURES_DIR), name="pictures")

if os.path.exists(WEB_DIR):
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Página HTML de pantalla de carga (se muestra mientras el servidor arranca)
# ─────────────────────────────────────────────────────────────────────────────
LOADING_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <title>Cargando Semiverd…</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0d1f0e;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      height: 100vh;
      font-family: 'Segoe UI', sans-serif;
      color: #c8f0c8;
    }
    .logo { font-size: 3.5rem; margin-bottom: 1rem; animation: pulse 2s infinite; }
    h1 { font-size: 1.8rem; font-weight: 700; color: #5cd65c; margin-bottom: 0.5rem; }
    p  { font-size: 1rem; color: #88bb88; margin-bottom: 2rem; }
    .spinner {
      width: 48px; height: 48px;
      border: 5px solid #1e3d1e;
      border-top-color: #5cd65c;
      border-radius: 50%;
      animation: spin 0.9s linear infinite;
    }
    @keyframes spin   { to { transform: rotate(360deg); } }
    @keyframes pulse  { 0%,100% { transform: scale(1); } 50% { transform: scale(1.1); } }
  </style>
</head>
<body>
  <div class="logo">🌱</div>
  <h1>Semiverd</h1>
  <p>Iniciando aplicación, un momento…</p>
  <div class="spinner"></div>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# 7. Función de arranque: servidor + ventana nativa (usado por PyInstaller y dev)
# ─────────────────────────────────────────────────────────────────────────────
def arrancar():
    import uvicorn
    import urllib.request

    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8000
    SERVER_URL  = f"http://{SERVER_HOST}:{SERVER_PORT}"

    # ── 7a. Arrancar uvicorn en un hilo demonio ──────────────────────────────
    def iniciar_servidor():
        uvicorn.run(
            app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            log_level="warning",   # menos ruido en producción
        )

    hilo_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
    hilo_servidor.start()

    # ── 7b. Intentar pywebview (ventana desktop nativa) ──────────────────────
    try:
        import webview

        # Escribir HTML de carga en un fichero temporal para que pywebview lo muestre
        import tempfile
        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.html', delete=False, encoding='utf-8'
        )
        tmp.write(LOADING_HTML)
        tmp.flush()
        tmp.close()
        loading_url = f"file:///{tmp.name.replace(os.sep, '/')}"

        ventana = webview.create_window(
            title="Semiverd - Las Cuatro Semillas Verdes",
            url=loading_url,
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True,
            text_select=False,
        )

        def esperar_y_cargar():
            """Espera hasta que FastAPI responda y entonces carga la URL real."""
            max_intentos = 20          # hasta 10 segundos de espera
            for _ in range(max_intentos):
                try:
                    urllib.request.urlopen(f"{SERVER_URL}/salud", timeout=1)
                    ventana.load_url(SERVER_URL)
                    # Limpiar fichero temporal
                    try:
                        os.unlink(tmp.name)
                    except Exception:
                        pass
                    return
                except Exception:
                    time.sleep(0.5)

            # Fallback: cargar de todos modos aunque no haya respondido
            ventana.load_url(SERVER_URL)

        threading.Thread(target=esperar_y_cargar, daemon=True).start()

        # webview.start() bloquea hasta que el usuario cierra la ventana
        webview.start(debug=False)

    except ImportError:
        # pywebview no instalado → abrir en browser del sistema (dev/fallback)
        import webbrowser
        print("⚠️  pywebview no disponible. Abriendo en el navegador del sistema...")

        # Esperar a que el servidor arranque antes de abrir el browser
        for _ in range(20):
            try:
                urllib.request.urlopen(f"{SERVER_URL}/salud", timeout=1)
                break
            except Exception:
                time.sleep(0.5)

        webbrowser.open(SERVER_URL)
        # Mantener el proceso vivo
        hilo_servidor.join()


# ─────────────────────────────────────────────────────────────────────────────
# 8. Entry point: tanto en desarrollo (python main.py) como congelado (.exe)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__" or getattr(sys, 'frozen', False):
    arrancar()
