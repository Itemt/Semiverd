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
    load_dotenv(os.path.join(executable_dir, ".env"))
else:
    load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Crear la app FastAPI de inmediato (import rápido, sin dlib/numpy aún)
# ─────────────────────────────────────────────────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="🌱 Semiverd API",
    description="API REST del MVP de Semiverd - Las Cuatro Semillas Verdes de Barrancabermeja.",
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

# Endpoint de salud disponible desde el primer momento (uvicorn lo sirve
# en cuanto arranca, antes de que los controladores pesados terminen de cargar)
@app.get("/salud", tags=["Raíz"])
def verificar_salud():
    return {"estado": "saludable", "servicio": "semiverd-api"}

@app.get("/api-info", tags=["Raíz"])
def raiz():
    return {"mensaje": "🌿 Bienvenido a la API de Semiverd", "version": "1.0.0"}

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

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_URL  = f"http://{SERVER_HOST}:{SERVER_PORT}"

# ─────────────────────────────────────────────────────────────────────────────
# 4. HTML de pantalla de carga
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
# 5. Inicialización pesada en segundo plano
#    (face_recognition, dlib, numpy, DB, seed) — no bloquea la apertura de
#    la ventana. Una vez listo, uvicorn arranca y la ventana carga la UI real.
# ─────────────────────────────────────────────────────────────────────────────
def _inicializar_y_servir():
    """
    Importa las dependencias pesadas y arranca uvicorn en background.
    Se lanza en un hilo demonio antes de abrir la ventana, así el proceso
    de carga corre en paralelo con la inicialización de pywebview.
    """
    try:
        import uvicorn

        # Imports pesados (dlib, face_recognition, numpy, PIL…)
        from models.database import engine, SessionLocal
        from models import models
        from controllers import (
            auth_controller, missions_controller,
            users_controller, tips_controller
        )

        # Registrar rutas y favicon
        app.include_router(auth_controller.router)
        app.include_router(missions_controller.router)
        app.include_router(users_controller.router)
        app.include_router(tips_controller.router)

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

        # Inicializar base de datos
        models.Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            from seed import cargar_misiones, cargar_tips, cargar_recompensas
            if db.query(models.Mision).count() == 0:
                print("🌱 Base de datos vacía. Iniciando auto-semillado...")
                cargar_misiones(db)
                cargar_tips(db)
                cargar_recompensas(db)
                print("🌿 Auto-semillado completado.")
        except Exception as seed_err:
            print(f"⚠️ Error al auto-semillar: {seed_err}")
            db.rollback()
        finally:
            db.close()

        # Arrancar uvicorn (bloquea este hilo para siempre)
        uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="warning")

    except Exception:
        print("\n❌ ERROR CRÍTICO durante la inicialización:")
        traceback.print_exc()
        if getattr(sys, 'frozen', False):
            input("\nPresione Enter para salir...")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# 6. Función principal de arranque
# ─────────────────────────────────────────────────────────────────────────────
def arrancar():
    import urllib.request

    # Lanzar la inicialización pesada de inmediato en background
    threading.Thread(target=_inicializar_y_servir, daemon=True).start()

    try:
        import webview
        import tempfile

        # Escribir HTML de carga en fichero temporal
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
            """
            Espera a que el servidor responda /salud y carga la UI real.
            60 intentos × 0.5 s = hasta 30 s de espera máxima.
            En Windows, dlib puede tardar 15-25 s en cargarse desde el .exe.
            """
            for _ in range(60):
                try:
                    urllib.request.urlopen(f"{SERVER_URL}/salud", timeout=1)
                    ventana.load_url(SERVER_URL)
                    try:
                        os.unlink(tmp.name)
                    except Exception:
                        pass
                    return
                except Exception:
                    time.sleep(0.5)

            # Fallback: cargar de todos modos
            ventana.load_url(SERVER_URL)

        threading.Thread(target=esperar_y_cargar, daemon=True).start()

        # Bloquea hasta que el usuario cierra la ventana
        webview.start(debug=False)

    except ImportError:
        # pywebview no disponible → abrir en navegador del sistema
        import webbrowser
        print("⚠️  pywebview no disponible. Abriendo en el navegador del sistema...")
        for _ in range(60):
            try:
                urllib.request.urlopen(f"{SERVER_URL}/salud", timeout=1)
                break
            except Exception:
                time.sleep(0.5)
        webbrowser.open(SERVER_URL)
        # Mantener el proceso vivo
        while True:
            time.sleep(60)


# ─────────────────────────────────────────────────────────────────────────────
# 7. Entry point (desarrollo y ejecutable congelado)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__" or getattr(sys, 'frozen', False):
    arrancar()
