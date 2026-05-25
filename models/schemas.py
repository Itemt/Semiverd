"""
schemas.py - Esquemas Pydantic para validación de datos y serialización
Proyecto: Semiverd MVP
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ─────────────────────────────────────────────────────────
# Schemas: Usuario
# ─────────────────────────────────────────────────────────

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del guardián")
    apellido: Optional[str] = Field(None, max_length=100)
    correo: EmailStr
    apodo: Optional[str] = Field(None, max_length=50, description="Nombre de guardián en el juego")


class UsuarioCrear(UsuarioBase):
    """Schema para crear un nuevo usuario"""
    password: str = Field(..., min_length=6, description="Contraseña mínimo 6 caracteres")


class UsuarioRespuesta(UsuarioBase):
    """Schema de respuesta con datos públicos del usuario"""
    id: int
    puntos_totales: int
    nivel: str
    nivel_arbol: int
    racha_dias: int
    monedas_verdes: int
    foto_perfil: Optional[str] = None
    fecha_registro: datetime

    class Config:
        from_attributes = True


class UsuarioActualizar(BaseModel):
    """Schema para actualizar datos del usuario"""
    nombre: Optional[str] = None
    apodo: Optional[str] = None
    foto_perfil: Optional[str] = None


# ─────────────────────────────────────────────────────────
# Schemas: Autenticación
# ─────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


class LoginFacialRequest(BaseModel):
    """Login con foto capturada. La imagen llega como base64"""
    imagen_base64: str = Field(..., description="Foto capturada en base64")
    correo: Optional[str] = None      # Correo del usuario para vincular/registrar
    nombre: Optional[str] = None      # Nombre para auto-registrar si no existe


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioRespuesta


# ─────────────────────────────────────────────────────────
# Schemas: Misión
# ─────────────────────────────────────────────────────────

class MisionBase(BaseModel):
    titulo: str
    descripcion: str
    descripcion_corta: Optional[str] = None
    nombre_zona: str
    guardianes: str
    categoria: str
    puntos_recompensa: int = 100
    dificultad: int = Field(1, ge=1, le=5)
    icono_emoji: str = "🌱"
    color_hex: str = "#4CAF50"


class MisionRespuesta(MisionBase):
    id: int
    orden: int
    activa: bool
    imagenes_personajes: List[str] = []

    class Config:
        from_attributes = True


class MisionConProgreso(MisionRespuesta):
    """Misión con el progreso del usuario actual"""
    estado: str = "bloqueada"
    porcentaje_completado: float = 0.0
    puntos_ganados: int = 0


# ─────────────────────────────────────────────────────────
# Schemas: Progreso
# ─────────────────────────────────────────────────────────

class ActualizarProgreso(BaseModel):
    """Schema para actualizar el progreso de una misión"""
    porcentaje_completado: float = Field(..., ge=0.0, le=100.0)
    estado: str


class ProgresoRespuesta(BaseModel):
    id: int
    usuario_id: int
    mision_id: int
    estado: str
    porcentaje_completado: float
    puntos_ganados: int
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────
# Schemas: Tips
# ─────────────────────────────────────────────────────────

class TipRespuesta(BaseModel):
    id: int
    titulo: str
    contenido: str
    categoria: Optional[str]
    icono_emoji: str
    guardian_autor: Optional[str]

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────
# Schemas: Recompensas
# ─────────────────────────────────────────────────────────

class RecompensaRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    icono_emoji: str
    tipo: str
    fecha_obtenida: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────
# Schemas: Respuestas generales
# ─────────────────────────────────────────────────────────

class MensajeRespuesta(BaseModel):
    mensaje: str
    exito: bool = True


class EstadisticasUsuario(BaseModel):
    """Panel de estadísticas completo del usuario"""
    usuario: UsuarioRespuesta
    misiones_completadas: int
    misiones_en_progreso: int
    recompensas: List[RecompensaRespuesta]
    nivel_arbol: int
    puntos_para_siguiente_nivel: int
