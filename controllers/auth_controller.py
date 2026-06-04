"""
controllers/auth_controller.py - Endpoints de autenticación de Semiverd
Incluye login tradicional y login facial real (Face ID)
"""

import base64
import io
import os
import sys
import json
from datetime import datetime, timedelta
from typing import Optional, List

import numpy as np
import face_recognition
from PIL import Image, ImageOps
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import bcrypt
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ─────────────────────────────────────────────────────────
# Funciones de utilidad
# ─────────────────────────────────────────────────────────

def verificar_password(password_plano: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password_plano.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


def hashear_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


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


def obtener_encoding_facial(imagen_base64: str, num_jitters: int = 1) -> np.ndarray:
    """
    Decodifica una imagen en base64, realiza preprocesamiento avanzado
    (auto-rotación EXIF y autocontraste) y extrae el vector 128D del rostro.
    Si falla el primer intento, realiza una detección resiliente upsampleando la imagen.
    """
    try:
        if "," in imagen_base64:
            imagen_base64 = imagen_base64.split(",")[1]

        imagen_bytes = base64.b64decode(imagen_base64)
        if len(imagen_bytes) < 100:
            raise ValueError("Imagen demasiado pequeña o inválida")
            
        # Convertir bytes a imagen RGB de PIL
        img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        
        # 1. Rotación automática basada en metadatos EXIF
        img = ImageOps.exif_transpose(img)
        
        # 2. Normalización de iluminación y contraste
        img = ImageOps.autocontrast(img, cutoff=2)
        
        img_np = np.array(img)
        
        # 3. Intentar extraer codificaciones faciales (HOG regular por defecto)
        encodings = face_recognition.face_encodings(img_np, num_jitters=num_jitters)
        
        # 4. Detección resiliente con upsampling si falla el primer intento
        if not encodings:
            face_locations = face_recognition.face_locations(img_np, number_of_times_to_upsample=2)
            if face_locations:
                encodings = face_recognition.face_encodings(img_np, known_face_locations=face_locations, num_jitters=max(2, num_jitters))
        
        if not encodings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se detectó ningún rostro en la foto. Centra tu cara frente a la cámara con buena luz e intenta de nuevo. 📷"
            )
            
        return encodings[0]
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar la imagen facial: {str(e)}"
        )


if getattr(sys, 'frozen', False):
    executable_dir = os.path.dirname(sys.executable)
    if ".app/Contents/MacOS" in executable_dir:
        # En macOS dentro del .app bundle, subir niveles para colocar la carpeta al lado de la app
        app_path = executable_dir.split(".app/Contents/MacOS")[0] + ".app"
        FACES_DIR = os.path.join(os.path.dirname(app_path), "faces_db")
    else:
        FACES_DIR = os.path.join(executable_dir, "faces_db")
else:
    FACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faces_db")

def guardar_imagen_rostro_local(user_id: int, imagen_base64: str) -> str:
    """Decodifica y guarda la imagen del rostro en el disco local"""
    try:
        # Limpiar base64
        if "," in imagen_base64:
            imagen_base64 = imagen_base64.split(",")[1]
        imagen_bytes = base64.b64decode(imagen_base64)
        
        # Crear directorio para el usuario
        user_dir = os.path.join(FACES_DIR, f"user_{user_id}")
        os.makedirs(user_dir, exist_ok=True)
        
        # Generar nombre único usando timestamp
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        filename = f"face_{timestamp}.png"
        filepath = os.path.join(user_dir, filename)
        
        # Guardar archivo
        with open(filepath, "wb") as f:
            f.write(imagen_bytes)
            
        # Mantener un límite físico de archivos en disco (máximo 5)
        archivos = sorted(
            [os.path.join(user_dir, arch) for arch in os.listdir(user_dir) if arch.startswith("face_")],
            key=os.path.getmtime
        )
        while len(archivos) > 5:
            viejo = archivos.pop(0)
            try:
                os.remove(viejo)
            except OSError:
                pass
                
        return filepath
    except Exception as e:
        print(f"Error al guardar imagen de rostro localmente: {e}")
        return ""


def sincronizar_encodings_desde_disco(usuario: Usuario, db: Session) -> List[np.ndarray]:
    """
    Escanea las imágenes locales del usuario, genera sus encodings y 
    actualiza el caché en la base de datos si es necesario (self-healing).
    """
    user_dir = os.path.join(FACES_DIR, f"user_{usuario.id}")
    if not os.path.exists(user_dir):
        return []
        
    archivos = [os.path.join(user_dir, f) for f in os.listdir(user_dir) if f.startswith("face_")]
    if not archivos:
        return []
        
    encodings = []
    for filepath in archivos:
        try:
            # Leer imagen y extraer encoding con preprocesamiento avanzado
            img = Image.open(filepath).convert("RGB")
            img = ImageOps.exif_transpose(img)
            img = ImageOps.autocontrast(img, cutoff=2)
            img_np = np.array(img)
            
            encs = face_recognition.face_encodings(img_np)
            if not encs:
                face_locations = face_recognition.face_locations(img_np, number_of_times_to_upsample=2)
                if face_locations:
                    encs = face_recognition.face_encodings(img_np, known_face_locations=face_locations)
                    
            if encs:
                encodings.append(encs[0])
        except Exception as e:
            print(f"Error cargando imagen {filepath} para encoding: {e}")
            
    if encodings:
        # Actualizar caché de la base de datos
        lista_json = [enc.tolist() for enc in encodings]
        usuario.face_encoding = json.dumps(lista_json)
        db.commit()
        
    return encodings


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

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El correo ingresado no está registrado en el sistema. Por favor, crea una cuenta primero. 🌿",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verificar_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta. Inténtalo de nuevo. 🔐",
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
    # 1. Extraer el encoding del rostro enviado (con 1 jitter para velocidad en login)
    encoding_login = obtener_encoding_facial(datos.imagen_base64)

    # Caso 1: Se provee correo → Vincular, verificar o auto-registrar
    if datos.correo:
        usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()

        # Si el usuario ya existe y ya tiene rostro vinculado (o respaldado en disco)
        if usuario:
            # Self-healing: restaurar desde disco si la base de datos se borró
            if not usuario.face_encoding:
                sincronizar_encodings_desde_disco(usuario, db)

            if usuario.face_encoding and usuario.face_encoding != "[]":
                try:
                    enc_lista = json.loads(usuario.face_encoding)
                    
                    # Soporte para formato legacy (una sola lista de floats) o formato multi-template (lista de listas)
                    if isinstance(enc_lista[0], (int, float)):
                        encodings_registrados = [np.array(enc_lista)]
                    else:
                        encodings_registrados = [np.array(enc) for enc in enc_lista]
                    
                    # Comparar rostro de login contra todos los registrados para este usuario
                    distancias = face_recognition.face_distance(encodings_registrados, encoding_login)
                    if len(distancias) == 0:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="El rostro capturado no coincide con el guardián registrado para este correo. 📷"
                        )
                    
                    distancia_minima = np.min(distancias)
                    es_valido = False
                    
                    # Validación robusta multi-template
                    if distancia_minima <= 0.50:
                        # Altamente confiable
                        es_valido = True
                    elif distancia_minima <= 0.58:
                        if len(encodings_registrados) > 1:
                            # Si tiene más de una plantilla, exigir que la media de distancias sea <= 0.55 para descartar falsos positivos
                            if np.mean(distancias) <= 0.55:
                                es_valido = True
                        else:
                            # Si es plantilla única, exigir umbral más seguro de 0.55 en lugar de 0.60
                            if distancia_minima <= 0.55:
                                es_valido = True
                                
                    if not es_valido:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="El rostro capturado no coincide con el guardián registrado para este correo. 📷"
                        )
                    
                    # Guardar la imagen localmente como respaldo físico
                    guardar_imagen_rostro_local(usuario.id, datos.imagen_base64)
                    
                    # Coincide exitosamente. Agregar la nueva plantilla para aprendizaje adaptativo (máx 5)
                    if isinstance(enc_lista[0], (int, float)):
                        enc_lista = [enc_lista]
                    
                    # Solo agregar si no es extremadamente redundante (distancia > 0.22 con las ya guardadas)
                    if np.min(distancias) > 0.22:
                        enc_lista.append(encoding_login.tolist())
                        if len(enc_lista) > 5:
                            enc_lista.pop(0) # Eliminar la más antigua
                        usuario.face_encoding = json.dumps(enc_lista)
                except HTTPException as he:
                    raise he
                except Exception:
                    # Si el JSON está corrupto, permitimos re-vincular de cero con precisión de login
                    usuario.face_encoding = json.dumps([encoding_login.tolist()])
                    guardar_imagen_rostro_local(usuario.id, datos.imagen_base64)
            else:
                # El usuario existe pero NO tiene rostro registrado (cuenta tradicional)
                # Impedimos vincularlo sin autenticación (seguridad contra usurpación de identidad)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este correo ya está registrado en Semiverd. Por favor, inicia sesión con tu contraseña tradicional primero y vincula tu rostro desde tu perfil. 🔐"
                )

        # Si no existe, auto-registrar con los datos proporcionados
        if not usuario:
            # Evitar registrar una cara que ya pertenece a otro correo
            todos_usuarios = db.query(Usuario).filter(Usuario.activo == True).all()
            for u in todos_usuarios:
                if not u.face_encoding:
                    sincronizar_encodings_desde_disco(u, db)

            usuarios_con_rostro = [u for u in todos_usuarios if u.face_encoding]

            encodings_conocidos = []
            usuarios_validos = []
            for u in usuarios_con_rostro:
                try:
                    enc_lista = json.loads(u.face_encoding)
                    if isinstance(enc_lista[0], (int, float)):
                        encodings_conocidos.append(np.array(enc_lista))
                        usuarios_validos.append(u)
                    else:
                        for enc in enc_lista:
                            encodings_conocidos.append(np.array(enc))
                            usuarios_validos.append(u)
                except Exception:
                    continue

            if encodings_conocidos:
                # Verificar duplicados usando el umbral más seguro de 0.58
                distancias = face_recognition.face_distance(encodings_conocidos, encoding_login)
                if len(distancias) > 0 and np.min(distancias) <= 0.58:
                    idx_coincidente = np.argmin(distancias)
                    usuario_duplicado = usuarios_validos[idx_coincidente]
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Este rostro ya está registrado con otra cuenta de correo ({usuario_duplicado.correo}). 📷"
                    )

            # Para el registro por primera vez, extraer encoding con alta precisión (num_jitters=3)
            encoding_registro = obtener_encoding_facial(datos.imagen_base64, num_jitters=3)

            nombre_usuario = datos.nombre or datos.correo.split("@")[0].capitalize()
            # Generar una contraseña aleatoria segura
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

            # Guardar la imagen en el disco local
            guardar_imagen_rostro_local(usuario.id, datos.imagen_base64)
            usuario.face_encoding = json.dumps([encoding_registro.tolist()])

        # Siempre actualizamos la foto de perfil para refrescarla en la UI
        usuario.foto_perfil = datos.imagen_base64
        db.commit()
        db.refresh(usuario)

        token = crear_token_acceso(data={"sub": usuario.correo})
        return TokenRespuesta(access_token=token, usuario=usuario)

    # Caso 2: Búsqueda Biométrica directa (Face ID sin correo)
    else:
        # Obtener todos los usuarios activos
        usuarios = db.query(Usuario).filter(Usuario.activo == True).all()
        
        # Self-healing dinámico
        for u in usuarios:
            if not u.face_encoding:
                sincronizar_encodings_desde_disco(u, db)
                
        # Filtrar usuarios que tienen rostros válidos cargados
        usuarios_con_rostro = [u for u in usuarios if u.face_encoding is not None]
        
        if not usuarios_con_rostro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay rostros registrados en el sistema. Registra tu rostro primero ingresando tu correo. 📷"
            )

        # Deserializar todos los encodings de todos los usuarios
        encodings_conocidos = []
        usuarios_validos = []
        for u in usuarios_con_rostro:
            try:
                enc_lista = json.loads(u.face_encoding)
                if isinstance(enc_lista[0], (int, float)):
                    encodings_conocidos.append(np.array(enc_lista))
                    usuarios_validos.append(u)
                else:
                    for enc in enc_lista:
                        encodings_conocidos.append(np.array(enc))
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

        # Umbral estricto de pre-filtración
        if distancia_minima <= 0.58:
            usuario_autenticado = usuarios_validos[idx_minimo]
            
            # Validación local robusta específica para el candidato
            try:
                enc_lista = json.loads(usuario_autenticado.face_encoding)
                if isinstance(enc_lista[0], (int, float)):
                    encodings_usuario = [np.array(enc_lista)]
                else:
                    encodings_usuario = [np.array(enc) for enc in enc_lista]
                
                distancias_locales = face_recognition.face_distance(encodings_usuario, encoding_login)
                distancia_min_local = np.min(distancias_locales)
                
                es_valido = False
                if distancia_min_local <= 0.50:
                    es_valido = True
                elif distancia_min_local <= 0.58:
                    if len(encodings_usuario) > 1:
                        if np.mean(distancias_locales) <= 0.55:
                            es_valido = True
                    else:
                        if distancia_min_local <= 0.55:
                            es_valido = True
                            
                if not es_valido:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Rostro no reconocido o no registrado. Por favor, ingresa tu correo para vincularlo por primera vez. 🌿"
                    )
            except HTTPException as he:
                raise he
            except Exception:
                # Fallback por si hay algún error inesperado en la validación local
                if distancia_minima > 0.55:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Rostro no reconocido o no registrado. Por favor, ingresa tu correo para vincularlo por primera vez. 🌿"
                    )
            
            # Guardar la imagen localmente como respaldo físico
            guardar_imagen_rostro_local(usuario_autenticado.id, datos.imagen_base64)
            
            # Aprendizaje adaptativo
            try:
                enc_lista = json.loads(usuario_autenticado.face_encoding)
                if isinstance(enc_lista[0], (int, float)):
                    enc_lista = [enc_lista]
                
                # Comprobar si es muy similar a las suyas propias para evitar redundancia
                sus_encodings = [np.array(enc) for enc in enc_lista]
                propias_distancias = face_recognition.face_distance(sus_encodings, encoding_login)
                
                if len(propias_distancias) == 0 or np.min(propias_distancias) > 0.22:
                    enc_lista.append(encoding_login.tolist())
                    if len(enc_lista) > 5:
                        enc_lista.pop(0)
                    usuario_autenticado.face_encoding = json.dumps(enc_lista)
            except Exception:
                pass
            
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

