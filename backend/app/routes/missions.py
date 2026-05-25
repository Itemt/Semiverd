"""
routes/missions.py - Endpoints de misiones y progreso de Semiverd
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Mision, ProgresoUsuario, Usuario, Recompensa, RecompensaUsuario, EstadoMision
from app.schemas import (
    MisionRespuesta, MisionConProgreso,
    ActualizarProgreso, ProgresoRespuesta, MensajeRespuesta
)
from app.routes.auth import obtener_usuario_actual

router = APIRouter(prefix="/misiones", tags=["Misiones"])


# ─────────────────────────────────────────────────────────
# Funciones auxiliares
# ─────────────────────────────────────────────────────────

def calcular_nivel_arbol(puntos: int) -> int:
    """Calcula el nivel del árbol (1-10) basado en los puntos totales"""
    if puntos < 100:
        return 1
    elif puntos < 250:
        return 2
    elif puntos < 450:
        return 3
    elif puntos < 700:
        return 4
    elif puntos < 1000:
        return 5
    elif puntos < 1350:
        return 6
    elif puntos < 1750:
        return 7
    elif puntos < 2200:
        return 8
    elif puntos < 2700:
        return 9
    return 10


def calcular_nivel_usuario(puntos: int) -> str:
    """Determina el nivel/título del usuario según sus puntos"""
    if puntos < 100:
        return "Semilla"
    elif puntos < 350:
        return "Brote"
    elif puntos < 700:
        return "Árbol"
    elif puntos < 1200:
        return "Guardián"
    return "Maestro del Bosque"


def verificar_y_otorgar_recompensas(usuario: Usuario, db: Session):
    """
    Verifica si el usuario cumple condiciones para nuevas recompensas
    y las otorga automáticamente.
    """
    misiones_completadas = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario.id,
        ProgresoUsuario.estado == EstadoMision.COMPLETADA
    ).count()

    # Recompensa: primera misión
    if misiones_completadas >= 1:
        recompensa = db.query(Recompensa).filter(Recompensa.nombre == "Primera Semilla").first()
        if recompensa:
            ya_tiene = db.query(RecompensaUsuario).filter(
                RecompensaUsuario.usuario_id == usuario.id,
                RecompensaUsuario.recompensa_id == recompensa.id
            ).first()
            if not ya_tiene:
                db.add(RecompensaUsuario(usuario_id=usuario.id, recompensa_id=recompensa.id))

    # Recompensa: todas las misiones
    if misiones_completadas >= 4:
        recompensa = db.query(Recompensa).filter(Recompensa.nombre == "Semilla Verde Total").first()
        if recompensa:
            ya_tiene = db.query(RecompensaUsuario).filter(
                RecompensaUsuario.usuario_id == usuario.id,
                RecompensaUsuario.recompensa_id == recompensa.id
            ).first()
            if not ya_tiene:
                db.add(RecompensaUsuario(usuario_id=usuario.id, recompensa_id=recompensa.id))

    db.commit()


# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────

@router.get("/", response_model=List[MisionConProgreso])
def listar_misiones(
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Retorna todas las misiones activas con el progreso del usuario actual.
    La primera misión siempre está disponible; las demás se desbloquean en orden.
    """
    misiones = db.query(Mision).filter(Mision.activa == True).order_by(Mision.orden).all()
    resultado = []

    for mision in misiones:
        progreso = db.query(ProgresoUsuario).filter(
            ProgresoUsuario.usuario_id == usuario_actual.id,
            ProgresoUsuario.mision_id == mision.id
        ).first()

        # Determinar estado inicial si no existe progreso
        if progreso is None:
            # La primera misión siempre está disponible
            estado_calculado = EstadoMision.DISPONIBLE if mision.orden == 1 else EstadoMision.BLOQUEADA

            # Verificar si la misión anterior fue completada para desbloquear
            if mision.orden > 1:
                mision_anterior = db.query(Mision).filter(Mision.orden == mision.orden - 1).first()
                if mision_anterior:
                    progreso_anterior = db.query(ProgresoUsuario).filter(
                        ProgresoUsuario.usuario_id == usuario_actual.id,
                        ProgresoUsuario.mision_id == mision_anterior.id,
                        ProgresoUsuario.estado == EstadoMision.COMPLETADA
                    ).first()
                    if progreso_anterior:
                        estado_calculado = EstadoMision.DISPONIBLE

            mision_con_progreso = MisionConProgreso(
                **mision.__dict__,
                estado=estado_calculado,
                porcentaje_completado=0.0,
                puntos_ganados=0
            )
        else:
            mision_con_progreso = MisionConProgreso(
                **mision.__dict__,
                estado=progreso.estado,
                porcentaje_completado=progreso.porcentaje_completado,
                puntos_ganados=progreso.puntos_ganados
            )

        resultado.append(mision_con_progreso)

    return resultado


@router.get("/{mision_id}", response_model=MisionConProgreso)
def obtener_mision(
    mision_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Retorna el detalle de una misión con el progreso del usuario"""
    mision = db.query(Mision).filter(Mision.id == mision_id, Mision.activa == True).first()
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    progreso = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_actual.id,
        ProgresoUsuario.mision_id == mision_id
    ).first()

    return MisionConProgreso(
        **mision.__dict__,
        estado=progreso.estado if progreso else "bloqueada",
        porcentaje_completado=progreso.porcentaje_completado if progreso else 0.0,
        puntos_ganados=progreso.puntos_ganados if progreso else 0
    )


@router.post("/{mision_id}/iniciar", response_model=ProgresoRespuesta)
def iniciar_mision(
    mision_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Inicia una misión para el usuario, creando o actualizando su progreso"""
    mision = db.query(Mision).filter(Mision.id == mision_id, Mision.activa == True).first()
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    # Verificar si ya existe un progreso
    progreso = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_actual.id,
        ProgresoUsuario.mision_id == mision_id
    ).first()

    if progreso and progreso.estado == EstadoMision.COMPLETADA:
        raise HTTPException(status_code=400, detail="Esta misión ya fue completada anteriormente")

    if progreso is None:
        progreso = ProgresoUsuario(
            usuario_id=usuario_actual.id,
            mision_id=mision_id,
            estado=EstadoMision.EN_PROGRESO,
            fecha_inicio=datetime.utcnow()
        )
        db.add(progreso)
    else:
        progreso.estado = EstadoMision.EN_PROGRESO
        progreso.intentos += 1
        if not progreso.fecha_inicio:
            progreso.fecha_inicio = datetime.utcnow()

    db.commit()
    db.refresh(progreso)
    return progreso


@router.put("/{mision_id}/progreso", response_model=ProgresoRespuesta)
def actualizar_progreso(
    mision_id: int,
    datos: ActualizarProgreso,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza el porcentaje de progreso de una misión"""
    progreso = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_actual.id,
        ProgresoUsuario.mision_id == mision_id
    ).first()

    if not progreso:
        raise HTTPException(status_code=404, detail="No has iniciado esta misión")

    progreso.porcentaje_completado = datos.porcentaje_completado
    progreso.estado = datos.estado
    db.commit()
    db.refresh(progreso)
    return progreso


@router.post("/{mision_id}/completar", response_model=dict)
def completar_mision(
    mision_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Marca una misión como completada y otorga los puntos y recompensas al usuario.
    Actualiza el nivel del árbol Semiverd.
    """
    mision = db.query(Mision).filter(Mision.id == mision_id, Mision.activa == True).first()
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    progreso = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_actual.id,
        ProgresoUsuario.mision_id == mision_id
    ).first()

    if not progreso:
        raise HTTPException(status_code=400, detail="Debes iniciar la misión primero")

    if progreso.estado == EstadoMision.COMPLETADA:
        raise HTTPException(status_code=400, detail="Esta misión ya fue completada")

    # Completar la misión
    progreso.estado = EstadoMision.COMPLETADA
    progreso.porcentaje_completado = 100.0
    progreso.puntos_ganados = mision.puntos_recompensa
    progreso.monedas_ganadas = mision.monedas_recompensa
    progreso.fecha_completada = datetime.utcnow()

    # Actualizar puntos del usuario
    usuario_actual.puntos_totales += mision.puntos_recompensa
    usuario_actual.monedas_verdes += mision.monedas_recompensa
    usuario_actual.nivel = calcular_nivel_usuario(usuario_actual.puntos_totales)
    usuario_actual.nivel_arbol = calcular_nivel_arbol(usuario_actual.puntos_totales)

    db.commit()

    # Verificar y otorgar recompensas
    verificar_y_otorgar_recompensas(usuario_actual, db)
    db.refresh(usuario_actual)

    return {
        "mensaje": f"🎉 ¡Misión '{mision.titulo}' completada!",
        "puntos_ganados": mision.puntos_recompensa,
        "monedas_ganadas": mision.monedas_recompensa,
        "puntos_totales": usuario_actual.puntos_totales,
        "nivel": usuario_actual.nivel,
        "nivel_arbol": usuario_actual.nivel_arbol,
        "exito": True
    }
