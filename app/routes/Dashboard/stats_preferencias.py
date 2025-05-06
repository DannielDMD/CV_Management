# routes/Dashboard/stats_preferencias.py

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_preferencias_service import obtener_estadisticas_preferencias
from app.schemas.dashboard.stats_preferencias_schema import EstadisticasPreferenciasResponse

router = APIRouter(
    prefix="/reportes/preferencias",
    tags=["Reportes – Preferencias"]
)

@router.get(
    "/",
    response_model=EstadisticasPreferenciasResponse,
    summary="Obtener estadísticas de preferencias y disponibilidad de los candidatos filtradas por año"
)
def estadisticas_preferencias(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas de preferencias (por ejemplo, 2025). Si no se indica, usa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Devuelve un objeto con:
    - preferencias_por_mes: total de registros por mes del año indicado
    - top_disponibilidad_inicio_anual: distribución por inicio de disponibilidad en el año
    - top_disponibilidad_inicio_por_mes: inicio de disponibilidad más frecuente por mes
    - top_rangos_salariales_anual: distribución por rangos salariales en el año
    - top_rangos_salariales_por_mes: rango salarial más frecuente por mes
    - top_motivos_salida_anual: distribución por motivos de salida en el año
    - top_motivos_salida_por_mes: motivo de salida más frecuente por mes
    - disponibilidad_viajar_anual: conteo de disponibilidad para viajar (Sí/No) en el año
    - disponibilidad_viajar_por_mes: disponibilidad para viajar más frecuente por mes
    - situacion_laboral_actual_anual: conteo de situación laboral actual (Sí/No) en el año
    - situacion_laboral_actual_por_mes: situación laboral más frecuente por mes
    """
    return obtener_estadisticas_preferencias(db, año)
