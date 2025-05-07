# routes/Dashboard/stats_proceso.py

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
    Devuelve:
    - candidatos_por_mes: total de candidatos registrados cada mes
    - top_estados_anual: conteo por estado para todo el año
    - top_estados_por_mes: estado más frecuente por mes
    """
    return obtener_estadisticas_proceso(db, año)
