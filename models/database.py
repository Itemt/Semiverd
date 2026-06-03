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

load_dotenv()

# Determinar el directorio base correcto (donde corre el .exe o el script)
if getattr(sys, 'frozen', False):
    executable_dir = os.path.dirname(sys.executable)
    if ".app/Contents/MacOS" in executable_dir:
        # En macOS dentro del .app bundle, subir niveles para colocar la base de datos al lado de la app
        app_path = executable_dir.split(".app/Contents/MacOS")[0] + ".app"
        BASE_DIR = os.path.dirname(app_path)
    else:
        BASE_DIR = executable_dir
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URL de conexión a la base de datos (SQLite local en la misma carpeta)
DB_PATH = os.path.join(BASE_DIR, "semiverd.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Motor de base de datos
engine_kwargs = {
    "echo": os.getenv("DEBUG", "False").lower() == "true"
}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}  # Importante para SQLite en FastAPI

engine = create_engine(DATABASE_URL, **engine_kwargs)

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
