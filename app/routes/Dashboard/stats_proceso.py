"""Ruta para obtener estadísticas del proceso de selección de candidatos."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_proceso_service import obtener_estadisticas_proceso
from app.schemas.dashboard.stats_proceso_schema import EstadisticasProcesoResponse

router = APIRouter(
    prefix="/reportes/proceso",
    tags=["Reportes – Proceso"]
)

@router.get(
    "/",
    response_model=EstadisticasProcesoResponse,
    summary="Obtener estadísticas del proceso de selección"
)
def estadisticas_proceso(
    año: Optional[int] = Query(None, title="Año", description="Filtrar estadísticas por año"),
    db: Session = Depends(get_db)
):
    """
    Retorna estadísticas del avance de los candidatos en el proceso de selección.

    Estadísticas devueltas:
    - candidatos_por_mes: total de candidatos registrados por mes.
    - top_estados_anual: cantidad total por estado (EN_PROCESO, ADMITIDO, DESCARTADO) en el año.
    - top_estados_por_mes: estado más común por mes.

    Args:
        año (Optional[int]): Año para aplicar el filtro. Si no se indica, se toman todos los años.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EstadisticasProcesoResponse: Estadísticas del proceso de selección.
    """
    return obtener_estadisticas_proceso(db, año)
