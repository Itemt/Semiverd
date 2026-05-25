"""
controllers/users_controller.py - Endpoints de perfil de usuario
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.models import Usuario, ProgresoUsuario, RecompensaUsuario, Recompensa, EstadoMision
from models.schemas import (
    UsuarioRespuesta, UsuarioActualizar,
    EstadisticasUsuario, RecompensaRespuesta, MensajeRespuesta
)
from controllers.auth_controller import obtener_usuario_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Puntos necesarios para cada nivel
PUNTOS_POR_NIVEL = {
    "Semilla": 100,
    "Brote": 350,
    "Árbol": 700,
    "Guardián": 1200,
    "Maestro del Bosque": 9999
}


@router.get("/perfil", response_model=UsuarioRespuesta)
def obtener_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Retorna el perfil completo del usuario autenticado"""
    return usuario_actual


@router.put("/perfil", response_model=UsuarioRespuesta)
def actualizar_perfil(
    datos: UsuarioActualizar,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza el nombre, apodo o foto de perfil del usuario"""
    if datos.nombre:
        usuario_actual.nombre = datos.nombre
    if datos.apodo:
        usuario_actual.apodo = datos.apodo
    if datos.foto_perfil:
        usuario_actual.foto_perfil = datos.foto_perfil
        
        # Intentar actualizar el encoding facial (Face ID) si la nueva foto contiene un rostro legible
        try:
            from controllers.auth_controller import obtener_encoding_facial
            import json
            encoding = obtener_encoding_facial(datos.foto_perfil)
            usuario_actual.face_encoding = json.dumps(encoding.tolist())
        except Exception:
            # Si no hay rostro o falla, no se actualiza el Face ID, solo la foto de perfil en la UI
            pass

    db.commit()
    db.refresh(usuario_actual)
    return usuario_actual


@router.get("/estadisticas", response_model=EstadisticasUsuario)
def obtener_estadisticas(
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Panel completo de estadísticas del guardián"""
    misiones_completadas = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_actual.id,
        ProgresoUsuario.estado == EstadoMision.COMPLETADA
    ).count()

    misiones_en_progreso = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_actual.id,
        ProgresoUsuario.estado == EstadoMision.EN_PROGRESO
    ).count()

    # Recompensas ganadas
    recompensas_query = db.query(RecompensaUsuario, Recompensa).join(
        Recompensa, RecompensaUsuario.recompensa_id == Recompensa.id
    ).filter(RecompensaUsuario.usuario_id == usuario_actual.id).all()

    recompensas = [
        RecompensaRespuesta(
            id=r.id,
            nombre=r.nombre,
            descripcion=r.descripcion,
            icono_emoji=r.icono_emoji,
            tipo=r.tipo,
            fecha_obtenida=ru.fecha_obtenida
        )
        for ru, r in recompensas_query
    ]

    # Calcular puntos para siguiente nivel
    nivel_actual = usuario_actual.nivel
    puntos_siguiente = PUNTOS_POR_NIVEL.get(nivel_actual, 9999)
    puntos_faltantes = max(0, puntos_siguiente - usuario_actual.puntos_totales)

    return EstadisticasUsuario(
        usuario=usuario_actual,
        misiones_completadas=misiones_completadas,
        misiones_en_progreso=misiones_en_progreso,
        recompensas=recompensas,
        nivel_arbol=usuario_actual.nivel_arbol,
        puntos_para_siguiente_nivel=puntos_faltantes
    )


@router.get("/ranking", response_model=List[dict])
def obtener_ranking(db: Session = Depends(get_db), limite: int = 10):
    """Tabla de clasificación de los mejores guardianes"""
    top_usuarios = (
        db.query(Usuario)
        .filter(Usuario.activo == True)
        .order_by(Usuario.puntos_totales.desc())
        .limit(limite)
        .all()
    )

    return [
        {
            "posicion": idx + 1,
            "nombre": u.nombre,
            "apodo": u.apodo,
            "puntos_totales": u.puntos_totales,
            "nivel": u.nivel,
            "nivel_arbol": u.nivel_arbol
        }
        for idx, u in enumerate(top_usuarios)
    ]
