"""Ruta para obtener estadísticas educativas de los candidatos."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_educacion_service import obtener_estadisticas_educacion
from app.schemas.dashboard.stats_educacion_schema import EstadisticasEducacionResponse

router = APIRouter(
    prefix="/reportes/educacion",
    tags=["Reportes – Educación"]
)

@router.get(
    "/",
    response_model=EstadisticasEducacionResponse,
    summary="Obtener estadísticas de educación de los candidatos filtradas por año"
)
def estadisticas_educacion(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas de educación (por ejemplo, 2025). Si no se indica, usa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna estadísticas de los registros educativos de los candidatos.

    Estadísticas devueltas:
    - educaciones_por_mes: cantidad de registros de educación por mes.
    - top_niveles_educacion_anual: Top 5 niveles educativos más frecuentes en el año.
    - top_niveles_por_mes: nivel educativo más frecuente por mes.
    - top_titulos_obtenidos_anual: Top 5 títulos obtenidos en el año.
    - top_titulos_por_mes: título más frecuente por mes.
    - top_instituciones_academicas_anual: Top 5 instituciones académicas en el año.
    - top_instituciones_por_mes: institución más frecuente por mes.
    - distribucion_nivel_ingles_anual: distribución de niveles de inglés durante el año.
    - distribucion_nivel_ingles_por_mes: nivel de inglés más común por mes.
    - distribucion_anio_graduacion: conteo de candidatos por año de graduación (sin filtro anual).

    Args:
        año (Optional[int]): Año para aplicar filtro. Si no se envía, devuelve estadísticas generales.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EstadisticasEducacionResponse: Datos estadísticos consolidados de educación.
    """
    return obtener_estadisticas_educacion(db, año)
