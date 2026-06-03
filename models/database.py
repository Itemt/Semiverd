"""
database.py - Configuración de la conexión a SQLite con SQLAlchemy
Proyecto: Semiverd MVP
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Determinar el directorio base correcto (donde corre el .exe o el script)
if getattr(sys, 'frozen', False):
    executable_dir = os.path.dirname(sys.executable)
    if ".app/Contents/MacOS" in executable_dir:
        # En macOS dentro del .app bundle, subir niveles para colocar la base de datos al lado de la app
        app_path = executable_dir.split(".app/Contents/MacOS")[0] + ".app"
        BASE_DIR = os.path.dirname(app_path)
    else:
        BASE_DIR = executable_dir
    
    # Cargar variables de entorno del archivo .env al lado del ejecutable
    env_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(env_path)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv()

# URL de conexión a la base de datos (SQLite local en la misma carpeta)
DB_PATH = os.path.join(BASE_DIR, "semiverd.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Motor de base de datos
engine_kwargs = {
    "echo": os.getenv("DEBUG", "False").lower() == "true"
}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}  # Importante para SQLite en FastAPI

# Intentar conectar y crear motor, con fallback a SQLite si falla
try:
    engine = create_engine(DATABASE_URL, **engine_kwargs)
    # Probar conexión para validar que funcione el host/puerto de base de datos externa
    with engine.connect() as conn:
        pass
except Exception as e:
    # Si la URL configurada no es SQLite y falla la conexión, retrocedemos a SQLite local
    if not DATABASE_URL.startswith("sqlite"):
        print(f"\n⚠️ Advertencia: No se pudo conectar a la base de datos configurada ({DATABASE_URL.split('@')[-1]}).")
        print(f"Error original: {e}")
        print("🔄 Cambiando automáticamente a la base de datos SQLite de respaldo (semiverd.db)...\n")
        DATABASE_URL = f"sqlite:///{DB_PATH}"
        engine_kwargs["connect_args"] = {"check_same_thread": False}
        engine = create_engine(DATABASE_URL, **engine_kwargs)
    else:
        # Si es SQLite y falló, lanzar excepción
        raise e

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
