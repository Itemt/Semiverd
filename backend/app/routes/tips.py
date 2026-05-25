"""
routes/tips.py - Endpoints para tips y consejos de la Academia de Guardianes
"""

import random
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tip
from app.schemas import TipRespuesta

router = APIRouter(prefix="/tips", tags=["Academia de Guardianes"])


@router.get("/", response_model=List[TipRespuesta])
def listar_tips(
    categoria: Optional[str] = Query(None, description="Filtrar por: jardinería, agua, energia, reciclaje"),
    limite: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Lista todos los tips activos, opcionalmente filtrados por categoría"""
    query = db.query(Tip).filter(Tip.activo == True)

    if categoria:
        query = query.filter(Tip.categoria == categoria)

    return query.limit(limite).all()


@router.get("/diario", response_model=TipRespuesta)
def tip_del_dia(db: Session = Depends(get_db)):
    """
    Retorna un tip aleatorio del día.
    En producción se podría almacenar el tip del día en cache (Redis).
    """
    tips_activos = db.query(Tip).filter(Tip.activo == True).all()

    if not tips_activos:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No hay tips disponibles aún")

    # Selección basada en el día actual para que sea consistente durante el día
    from datetime import date
    dia_del_anio = date.today().timetuple().tm_yday
    tip_index = dia_del_anio % len(tips_activos)
    return tips_activos[tip_index]


@router.get("/aleatorio", response_model=TipRespuesta)
def tip_aleatorio(db: Session = Depends(get_db)):
    """Retorna un tip completamente aleatorio"""
    tips_activos = db.query(Tip).filter(Tip.activo == True).all()
    if not tips_activos:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No hay tips disponibles")
    return random.choice(tips_activos)


@router.get("/categorias", response_model=List[str])
def listar_categorias(db: Session = Depends(get_db)):
    """Lista las categorías únicas de tips disponibles"""
    categorias = db.query(Tip.categoria).filter(
        Tip.activo == True,
        Tip.categoria != None
    ).distinct().all()
    return [c[0] for c in categorias]
