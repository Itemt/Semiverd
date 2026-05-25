"""
models.py - Modelos de base de datos con SQLAlchemy
Proyecto: Semiverd MVP

Tablas:
  - usuarios: Jugadores registrados con sus puntos y nivel
  - misiones: Los 4 retos de las Semillas Verdes
  - progreso_usuario: Registro de qué misiones ha completado cada usuario
  - tips: Consejos ecológicos de la Academia de Guardianes
  - recompensas: Medallas y logros del sistema
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, Text, Float, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from models.database import Base


# ─────────────────────────────────────────────────────────
# Enumeraciones
# ─────────────────────────────────────────────────────────

class NivelUsuario(str, enum.Enum):
    """Niveles de progreso del guardián"""
    SEMILLA = "Semilla"
    BROTE = "Brote"
    ARBOL = "Árbol"
    GUARDAAN = "Guardián"
    MAESTRO = "Maestro del Bosque"


class EstadoMision(str, enum.Enum):
    """Estado de una misión para el usuario"""
    BLOQUEADA = "bloqueada"
    DISPONIBLE = "disponible"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"


class CategoriaMision(str, enum.Enum):
    """Categorías de las misiones"""
    AGUA = "agua"
    BOSQUE = "bosque"
    CIUDAD = "ciudad"
    ENERGIA = "energia"


# ─────────────────────────────────────────────────────────
# Modelo: Usuario
# ─────────────────────────────────────────────────────────

class Usuario(Base):
    """
    Representa a un guardián/jugador de Semiverd.
    Guarda su progreso, puntos y nivel de árbol.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=True)
    correo = Column(String(200), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    apodo = Column(String(50), nullable=True)  # Nombre de guardián

    # Gamificación
    puntos_totales = Column(Integer, default=0)
    nivel = Column(String(50), default=NivelUsuario.SEMILLA)
    nivel_arbol = Column(Integer, default=1)      # 1-10: crecimiento del árbol
    racha_dias = Column(Integer, default=0)        # Días consecutivos activo
    monedas_verdes = Column(Integer, default=0)    # Moneda interna

    # Foto de perfil (base64 o ruta)
    foto_perfil = Column(Text, nullable=True)
    face_encoding = Column(Text, nullable=True)    # Vector 128D serializado en JSON

    # Estado
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    ultimo_acceso = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    progresos = relationship("ProgresoUsuario", back_populates="usuario", cascade="all, delete-orphan")
    recompensas_ganadas = relationship("RecompensaUsuario", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.nombre} - Nivel: {self.nivel} - Puntos: {self.puntos_totales}>"


# ─────────────────────────────────────────────────────────
# Modelo: Misión
# ─────────────────────────────────────────────────────────

class Mision(Base):
    """
    Representa un reto ecológico de las Cuatro Semillas Verdes.
    Cada misión tiene un guardián líder, descripción y puntos de recompensa.
    """
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    descripcion_corta = Column(String(300), nullable=True)

    # Identidad narrativa
    nombre_zona = Column(String(100), nullable=False)    # Río Caudal, Bosque de Humo, etc.
    guardianes = Column(String(200), nullable=False)     # Juliana, Camila, etc.
    categoria = Column(String(50), nullable=False)       # agua, bosque, ciudad, energia

    # Gamificación
    puntos_recompensa = Column(Integer, default=100)
    monedas_recompensa = Column(Integer, default=10)
    dificultad = Column(Integer, default=1)              # 1-5 estrellas
    orden = Column(Integer, default=1)                   # Orden en el mapa

    # Media
    icono_emoji = Column(String(10), default="🌱")
    color_hex = Column(String(7), default="#4CAF50")     # Color temático

    # Estado
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    progresos = relationship("ProgresoUsuario", back_populates="mision")

    def __repr__(self):
        return f"<Mision '{self.titulo}' - Zona: {self.nombre_zona}>"


# ─────────────────────────────────────────────────────────
# Modelo: Progreso de Usuario en Misiones
# ─────────────────────────────────────────────────────────

class ProgresoUsuario(Base):
    """
    Tabla de unión entre Usuario y Misión.
    Registra el progreso, estado y puntuación de cada misión por usuario.
    """
    __tablename__ = "progreso_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    mision_id = Column(Integer, ForeignKey("misiones.id"), nullable=False, index=True)

    # Estado de la misión
    estado = Column(String(20), default=EstadoMision.BLOQUEADA)
    porcentaje_completado = Column(Float, default=0.0)  # 0.0 - 100.0
    intentos = Column(Integer, default=0)

    # Recompensas obtenidas
    puntos_ganados = Column(Integer, default=0)
    monedas_ganadas = Column(Integer, default=0)

    # Fechas
    fecha_inicio = Column(DateTime(timezone=True), nullable=True)
    fecha_completada = Column(DateTime(timezone=True), nullable=True)
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="progresos")
    mision = relationship("Mision", back_populates="progresos")

    def __repr__(self):
        return f"<Progreso Usuario:{self.usuario_id} Mision:{self.mision_id} - {self.estado}>"


# ─────────────────────────────────────────────────────────
# Modelo: Tips (Academia de Guardianes)
# ─────────────────────────────────────────────────────────

class Tip(Base):
    """
    Consejo ecológico diario de la Academia de Guardianes.
    Se muestran en rotación en la sección 'Consejos para tu plantita'.
    """
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    categoria = Column(String(80), nullable=True)  # jardinería, reciclaje, agua, etc.
    icono_emoji = Column(String(10), default="💡")
    guardian_autor = Column(String(100), nullable=True)  # Qué semilla lo recomienda
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Tip '{self.titulo}' - Categoría: {self.categoria}>"


# ─────────────────────────────────────────────────────────
# Modelo: Recompensas / Medallas
# ─────────────────────────────────────────────────────────

class Recompensa(Base):
    """
    Catálogo de medallas y logros disponibles en Semiverd.
    """
    __tablename__ = "recompensas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    icono_emoji = Column(String(10), default="🏅")
    tipo = Column(String(50), default="medalla")     # medalla, titulo, objeto
    condicion = Column(String(200), nullable=True)   # Descripción de cómo ganarse
    puntos_necesarios = Column(Integer, default=0)

    usuarios_con_recompensa = relationship("RecompensaUsuario", back_populates="recompensa")

    def __repr__(self):
        return f"<Recompensa '{self.nombre}'>"


class RecompensaUsuario(Base):
    """
    Recompensas otorgadas a usuarios específicos.
    """
    __tablename__ = "recompensas_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    recompensa_id = Column(Integer, ForeignKey("recompensas.id"), nullable=False)
    fecha_obtenida = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="recompensas_ganadas")
    recompensa = relationship("Recompensa", back_populates="usuarios_con_recompensa")
