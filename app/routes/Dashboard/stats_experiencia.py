"""Ruta para obtener estadísticas de experiencia laboral de los candidatos."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_experiencia_service import obtener_estadisticas_experiencia
from app.schemas.dashboard.stats_experiencia_schema import EstadisticasExperienciaResponse

router = APIRouter(
    prefix="/reportes/experiencia",
    tags=["Reportes – Experiencia Laboral"]
)

@router.get(
    "/",
    response_model=EstadisticasExperienciaResponse,
    summary="Obtener estadísticas de experiencia laboral de los candidatos filtradas por año"
)
def estadisticas_experiencia(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas de experiencia (por ejemplo, 2025). Si no se indica, usa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna estadísticas sobre la experiencia laboral registrada por los candidatos.

    Estadísticas devueltas:
    - experiencias_por_mes: cantidad de experiencias registradas por mes.
    - top_rangos_experiencia_anual: rangos de experiencia más frecuentes en el año.
    - top_rangos_por_mes: rango de experiencia más común por mes.
    - top_ultimos_cargos_anual: últimos cargos más comunes en el año.
    - top_ultimos_cargos_por_mes: cargo más frecuente por mes.
    - top_ultimas_empresas_anual: empresas más mencionadas como últimas.
    - top_ultimas_empresas_por_mes: empresa más frecuente por mes.
    - distribucion_duracion: distribución de duración de experiencia laboral (acumulado anual).

    Args:
        año (Optional[int]): Año para aplicar filtro. Si no se especifica, devuelve estadísticas globales.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EstadisticasExperienciaResponse: Datos estadísticos consolidados de experiencia laboral.
    """
    return obtener_estadisticas_experiencia(db, año)
