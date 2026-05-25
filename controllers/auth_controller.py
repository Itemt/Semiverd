"""
controllers/auth_controller.py - Endpoints de autenticación de Semiverd
Incluye login tradicional y login facial real (Face ID)
"""

import base64
import io
import os
import json
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import face_recognition
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, status
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


def obtener_encoding_facial(imagen_base64: str) -> np.ndarray:
    """Decodifica una imagen en base64 y extrae el vector 128D del rostro"""
    try:
        if "," in imagen_base64:
            imagen_base64 = imagen_base64.split(",")[1]

        imagen_bytes = base64.b64decode(imagen_base64)
        if len(imagen_bytes) < 100:
            raise ValueError("Imagen demasiado pequeña o inválida")
            
        # Convertir bytes a imagen RGB de PIL
        img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        img_np = np.array(img)
        
        # Extraer codificaciones faciales
        encodings = face_recognition.face_encodings(img_np)
        if not encodings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se detectó ningún rostro en la foto. Centra tu cara frente a la cámara e intenta de nuevo. 📷"
            )
        return encodings[0]
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar la imagen facial: {str(e)}"
        )


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
    Login / Registro facial real (Face ID).
    - Si se envía 'correo' y el usuario EXISTE: vincula el rostro a su cuenta.
    - Si se envía 'correo' y el usuario NO EXISTE: lo registra automáticamente
      con el rostro capturado (no necesita contraseña).
    - Si no se envía 'correo': realiza búsqueda biométrica directa en la BD.
    """
    # 1. Extraer el encoding del rostro enviado
    encoding_login = obtener_encoding_facial(datos.imagen_base64)

    # Caso 1: Se provee correo → Vincular, verificar o auto-registrar
    if datos.correo:
        usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()

        # Si el usuario ya existe y ya tiene rostro vinculado, se debe VERIFICAR, no sobreescribir libremente
        if usuario and usuario.face_encoding:
            try:
                enc_lista = json.loads(usuario.face_encoding)
                encoding_registrado = np.array(enc_lista)
                # Comparar rostros
                distancias = face_recognition.face_distance([encoding_registrado], encoding_login)
                if len(distancias) == 0 or distancias[0] > 0.58:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="El rostro capturado no coincide con el guardián registrado para este correo. 📷"
                    )
            except HTTPException as he:
                raise he
            except Exception:
                # Si el JSON estaba corrupto, permitimos re-vincular
                pass

        # Si no existe, auto-registrar con los datos proporcionados
        if not usuario:
            nombre_usuario = datos.nombre or datos.correo.split("@")[0].capitalize()
            # Generar una contraseña aleatoria segura (el usuario usará Face ID)
            import secrets
            password_temporal = secrets.token_urlsafe(24)
            usuario = Usuario(
                nombre=nombre_usuario,
                correo=datos.correo,
                apodo=nombre_usuario,
                hashed_password=hashear_password(password_temporal),
                activo=True
            )
            db.add(usuario)
            db.flush()  # Para obtener el ID antes del commit

        # Si el usuario no tenía rostro o era nuevo, almacenamos el encoding
        if not usuario.face_encoding:
            usuario.face_encoding = json.dumps(encoding_login.tolist())
            
        # Siempre actualizamos la foto de perfil para refrescarla en la UI
        usuario.foto_perfil = datos.imagen_base64
        db.commit()
        db.refresh(usuario)

        token = crear_token_acceso(data={"sub": usuario.correo})
        return TokenRespuesta(access_token=token, usuario=usuario)

    # Caso 2: Búsqueda Biométrica directa (Face ID sin correo)
    else:
        # Obtener todos los usuarios que tengan rostro registrado
        usuarios_con_rostro = db.query(Usuario).filter(Usuario.face_encoding != None, Usuario.activo == True).all()
        
        if not usuarios_con_rostro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay rostros registrados en el sistema. Registra tu rostro primero ingresando tu correo. 📷"
            )

        # Deserializar todos los encodings de la base de datos
        encodings_conocidos = []
        usuarios_validos = []
        for u in usuarios_con_rostro:
            try:
                enc_lista = json.loads(u.face_encoding)
                encodings_conocidos.append(np.array(enc_lista))
                usuarios_validos.append(u)
            except Exception:
                continue

        if not encodings_conocidos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudieron cargar los datos faciales registrados"
            )

        # Calcular distancia euclidiana entre el rostro de login y los registrados
        distancias = face_recognition.face_distance(encodings_conocidos, encoding_login)
        
        if len(distancias) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Rostro no reconocido. Intenta centrar tu cara frente a la cámara o ingresa con tu correo. 📷"
            )
            
        # Encontrar el índice de la distancia mínima
        idx_minimo = np.argmin(distancias)
        distancia_minima = distancias[idx_minimo]

        # Umbral estándar de face_recognition: 0.6. Usamos 0.58 para mayor seguridad.
        if distancia_minima <= 0.58:
            usuario_autenticado = usuarios_validos[idx_minimo]
            
            # Actualizar racha y último acceso
            usuario_autenticado.ultimo_acceso = datetime.utcnow()
            db.commit()

            token = crear_token_acceso(data={"sub": usuario_autenticado.correo})
            return TokenRespuesta(access_token=token, usuario=usuario_autenticado)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Rostro no reconocido o no registrado. Por favor, ingresa tu correo para vincularlo por primera vez. 🌿"
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

