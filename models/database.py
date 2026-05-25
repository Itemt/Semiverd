"""
database.py - Configuración de la conexión a PostgreSQL con SQLAlchemy
Proyecto: Semiverd MVP
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# URL de conexión a la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/semiverd_db"
)

# Motor de base de datos con configuración de pool
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,       # Verifica conexiones antes de usarlas
    pool_size=10,             # Tamaño del pool de conexiones
    max_overflow=20,          # Conexiones extras en pico
    echo=os.getenv("DEBUG", "False").lower() == "true"  # SQL logging en modo debug
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI que provee una sesión de base de datos.
    Se usa con Depends(get_db) en los endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
