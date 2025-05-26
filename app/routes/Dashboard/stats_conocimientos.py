"""Ruta para obtener estadísticas de conocimientos de los candidatos."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_conocimientos_service import obtener_estadisticas_conocimientos
from app.schemas.dashboard.stats_conocimientos_schema import EstadisticasConocimientosResponse

router = APIRouter(
    prefix="/reportes/conocimientos",
    tags=["Reportes – Conocimientos"]
)

@router.get(
    "/",
    response_model=EstadisticasConocimientosResponse,
    summary="Obtener estadísticas de conocimientos de los candidatos filtradas por año"
)
def estadisticas_conocimientos(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas de conocimientos (por ejemplo, 2025). Si no se indica, agrupa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna estadísticas de conocimientos registrados por los candidatos.

    Estadísticas devueltas:
    - conocimientos_por_mes: cantidad total de registros por mes.
    - top_habilidades_blandas_anual: Top 5 habilidades blandas más frecuentes en el año.
    - top_habilidades_blandas_por_mes: habilidad blanda más frecuente por mes.
    - top_habilidades_tecnicas_anual: Top 5 habilidades técnicas más frecuentes en el año.
    - top_habilidades_tecnicas_por_mes: habilidad técnica más frecuente por mes.
    - top_herramientas_anual: Top 5 herramientas más frecuentes en el año.
    - top_herramientas_por_mes: herramienta más frecuente por mes.

    Args:
        año (Optional[int]): Año para aplicar filtro (opcional).
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EstadisticasConocimientosResponse: Datos estadísticos consolidados.
    """
    return obtener_estadisticas_conocimientos(db, año)
