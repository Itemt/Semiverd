"""
controllers/auth_controller.py - Endpoints de autenticación de Semiverd
Incluye login tradicional y login facial simulado (MVP)
"""

import base64
import io
import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.database import get_db
from models.models import Usuario
from models.schemas import (
    UsuarioCrear, UsuarioRespuesta, TokenRespuesta,
    LoginRequest, LoginFacialRequest, MensajeRespuesta
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "semiverd-secret-key-dev")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ─────────────────────────────────────────────────────────
# Funciones de utilidad
# ─────────────────────────────────────────────────────────

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)


def hashear_password(password: str) -> str:
    return pwd_context.hash(password)


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un JWT con los datos del usuario"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    """Valida el JWT y retorna el usuario activo"""
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None or not usuario.activo:
        raise credenciales_exception

    return usuario


# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────

@router.post("/registrar", response_model=UsuarioRespuesta, status_code=201)
def registrar_usuario(datos: UsuarioCrear, db: Session = Depends(get_db)):
    """
    Registra un nuevo guardián en Semiverd.
    Verifica que el correo no esté ya en uso.
    """
    # Verificar si el correo ya está registrado
    usuario_existente = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya tiene una cuenta en Semiverd"
        )

    # Crear el nuevo usuario
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        apodo=datos.apodo or datos.nombre,
        hashed_password=hashear_password(datos.password),
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.post("/login", response_model=TokenRespuesta)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """
    Login estándar con correo y contraseña.
    Retorna un JWT para autenticar las siguientes peticiones.
    """
    usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()

    if not usuario or not verificar_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta cuenta está desactivada"
        )

    # Actualizar racha de días
    usuario.ultimo_acceso = datetime.utcnow()
    db.commit()

    token = crear_token_acceso(data={"sub": usuario.correo})
    return TokenRespuesta(access_token=token, usuario=usuario)


@router.post("/token")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint OAuth2 estándar compatible con docs de FastAPI"""
    usuario = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    if not usuario or not verificar_password(form_data.password, usuario.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = crear_token_acceso(data={"sub": usuario.correo})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login-facial", response_model=TokenRespuesta)
def login_facial(datos: LoginFacialRequest, db: Session = Depends(get_db)):
    """
    Login facial simulado para el MVP.
    """
    try:
        imagen_data = datos.imagen_base64
        if "," in imagen_data:
            imagen_data = imagen_data.split(",")[1]

        imagen_bytes = base64.b64decode(imagen_data)
        if len(imagen_bytes) < 100:
            raise HTTPException(
                status_code=400,
                detail="La imagen capturada no es válida"
            )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Error al procesar la imagen. Intenta de nuevo."
        )

    if datos.correo:
        usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="No se encontró un guardián con ese correo"
            )

        if not usuario.foto_perfil:
            usuario.foto_perfil = datos.imagen_base64[:500]  # Guardar miniatura
            db.commit()

        token = crear_token_acceso(data={"sub": usuario.correo})
        return TokenRespuesta(
            access_token=token,
            usuario=usuario
        )
    else:
        raise HTTPException(
            status_code=422,
            detail="Para el MVP, proporciona tu correo junto con la foto facial"
        )


@router.get("/yo", response_model=UsuarioRespuesta)
def obtener_mi_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Retorna el perfil del usuario autenticado"""
    return usuario_actual


@router.post("/logout", response_model=MensajeRespuesta)
def logout(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """
    Logout simbólico.
    """
    return MensajeRespuesta(mensaje=f"¡Hasta pronto, {usuario_actual.nombre}! Sigue cuidando el planeta 🌱")
