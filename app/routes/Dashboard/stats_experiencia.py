# routes/Dashboard/stats_experiencia.py

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
    Devuelve un objeto con:
    - experiencias_por_mes: total de registros de experiencia cada mes del año indicado
    - top_rangos_experiencia_anual: Top rangos de experiencia en el año
    - top_rangos_por_mes: rango más frecuente por mes
    - top_ultimos_cargos_anual: Top últimos cargos en el año
    - top_ultimos_cargos_por_mes: cargo más frecuente por mes
    - top_ultimas_empresas_anual: Top últimas empresas en el año
    - top_ultimas_empresas_por_mes: empresa más frecuente por mes
    - distribucion_duracion: distribución de duración de la experiencia (todo el año)
    """
    return obtener_estadisticas_experiencia(db, año)
